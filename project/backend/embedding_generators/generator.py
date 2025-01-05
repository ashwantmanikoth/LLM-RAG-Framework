import uuid
import json
from utils.config import Config
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Set your OpenAI API key and initialize Qdrant client
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

qdrant_client = QdrantClient(
    "http://localhost:6333"
)  # Assuming Qdrant is running locally
COLLECTION_NAME = "New_medical_plan_embeddings_no_name_v4_adding_plan_name_to_full_text"


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None


def create_qdrant_collection(
    client, collection_name, vector_size=1536, distance_metric=Distance.COSINE
):
    """
    Create a Qdrant collection if it doesn't exist.
    """
    if not client.collection_exists(collection_name):
        print(f"Creating collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance_metric),
        )
    else:
        print(f"Collection '{collection_name}' already exists.")


def chunk_text(text, max_length=500):
    """
    Chunk a string into fixed-size pieces for embedding, splitting on the | character when found.
    """
    chunks = []
    for part in text.split("|"):
        chunks.extend(
            [part[i : i + max_length] for i in range(0, len(part), max_length)]
        )
    return [chunk for chunk in chunks if chunk.strip()]


def generate_batch_embeddings(texts):
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002", input=texts
        )
        return [r.embedding for r in response.data]
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return [None] * len(texts)


def process_and_store_embeddings(json_data, client, collection_name):
    texts_to_embed = []
    metadata_list = []

    def process_field_chunks(
        field_name, text, plan_name, plan_id, company, plan_zip, max_length=500
    ):
        

        chunks = chunk_text(f"{field_name}: {text}", max_length=max_length)
        for chunk in chunks:
            if chunk.strip():
                texts_to_embed.append(chunk)
                metadata_list.append(
                    {
                        "ID": plan_id,
                        "Plan_Name": plan_name,
                        "Company": company,
                        "Zip_code": plan_zip,
                        "Field": field_name,
                        "Full Text": f"Plan: {plan_name} : " + chunk,
                    }
                )

    if "Medical Plans" not in json_data:
        print("Error: Invalid JSON structure. Missing 'Medical Plans' key.")
        return

    plans = json_data["Medical Plans"]
    print(f"Processing {len(plans)} plans...")

    for plan in plans:
        plan_id = plan.get("PlanID", "")
        plan_zip = plan.get("Zip_code", "")
        company = plan.get("Company", "")
        plan_name = plan.get("Name", "")

        print(f"Processing Plan ID: {plan_id}")

        # ---- 1. Build a list of all text chunks for this plan ----
        texts_to_embed = []
        metadata_list = []

        # # # (a) Plan Name
        # if "Name" in plan:
        #     chunk = f"Plan name: {plan_name}"
        #     texts_to_embed.append(chunk)
        #     metadata_list.append(
        #         {
        #             "ID": plan_id,
        #             "Plan_Name": plan_name,
        #             "Company": company,
        #             "Zip_code": plan_zip,
        #             "Field": "Plan Name",
        #             "Full Text": chunk,
        #         }
        #     )

        if "Benefits" in plan:
            process_field_chunks(
                "Benefits",
                plan["Benefits"],
                plan_name,
                plan_id,
                company,
                plan_zip,
                max_length=500,
            )

        # (c) Extra details: chunk if needed
        extra_details = plan.get("Extra_details", {})
        for category, details in extra_details.items():
            # We'll build one or more text chunks from the details list
            detail_buffer = ""
            detail_chunks = []
            for detail in details:
                line = (
                    detail.get("Detail Name", "Unknown")
                    + ": "
                    + detail.get("Type of Cost", "Unknown")
                    + ", "
                )
                # If adding this line to detail_buffer exceeds max_length, split it
                if len(detail_buffer) + len(line) > 500:
                    detail_chunks.append(detail_buffer.strip())
                    detail_buffer = line
                else:
                    detail_buffer += line

            # Add the remaining text in the buffer
            if detail_buffer:
                detail_chunks.append(detail_buffer.strip())

            # Add these chunks to the texts_to_embed
            for chunk in detail_chunks:
                texts_to_embed.append(chunk)
                metadata_list.append(
                    {
                        "ID": plan_id,
                        "Plan_Name": plan_name,
                        "Company": company,
                        "Zip_code": plan_zip,
                        "Field": category,
                        "Full Text": plan_name + chunk,
                    }
                )

        # Remove empty chunks
        texts_to_embed = [
            f"Plan: {plan_name} : " + text for text in texts_to_embed if text.strip()
        ]
        metadata_list = [
            meta for meta, text in zip(metadata_list, texts_to_embed) if text.strip()
        ]
        # ---- 2. Generate embeddings in one batch ----
        embeddings = generate_batch_embeddings(texts_to_embed)

        # ---- 3. Create PointStruct objects for this plan ----
        points_to_insert = []
        for emb, meta in zip(embeddings, metadata_list):
            if emb:
                points_to_insert.append(
                    PointStruct(
                        id=str(uuid.uuid4()),  # Generate a unique ID
                        vector=emb,  # Embedding data
                        payload=meta,  # Metadata
                    )
                )
            else:
                print(
                    f"Failed to generate embedding for text: {meta.get('Full Text','')[:50]}..."
                )

        # ---- 4. Upsert all points in Qdrant for this plan ----
        if points_to_insert:
            client.upsert(collection_name=collection_name, points=points_to_insert)
            print(f"Inserted {len(points_to_insert)} embeddings for plan ID: {plan_id}")
        else:
            print(f"No embeddings generated for plan ID: {plan_id}")

    print("Processing completed.")


# Main entry point
if __name__ == "__main__":
    json_file_paths = [
        "cigna_plans_1.json",
        "united_healthcare_plans.json",
        "aetna_plans.json",
    ]

    for json_file_path in json_file_paths:
        json_data = load_json(json_file_path)
        if not json_data:
            print(f"Error loading JSON file '{json_file_path}'. Skipping...")
            continue

        # Create Qdrant collection if it doesn't exist
        create_qdrant_collection(qdrant_client, COLLECTION_NAME)

        # Process plans and store embeddings in Qdrant (batched for efficiency)
        process_and_store_embeddings(json_data, qdrant_client, COLLECTION_NAME)

        print(f"Embedding generation and insertion completed for: {json_file_path}")

    print("All files processed. Exiting...")
