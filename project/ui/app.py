# ui/app.py

import gradio as gr
import requests

BACKEND_URL = "http://backend:5001"


def process_input_ui(user_input, model, zip_code):
    response = requests.post(
        f"{BACKEND_URL}/process",
        json={"user_input": user_input, "model": model, "zip_code": zip_code},
    )
    return response.json().get("response", "Error processing input.")

def submit_feedback(model, user_input, output):
    requests.post(
        f"{BACKEND_URL}/feedback",
        json={"model": model, "user_input": user_input, "output": output},
    )
    return "Feedback submitted."

def retrieve_feedback():
    response = requests.get(f"{BACKEND_URL}/feedback")
    feedback = response.json()
    return [[row["id"], row["model"], row["user_input"], row["output"]] for row in feedback]

def delete_feedback():
    requests.delete(f"{BACKEND_URL}/delete")
    return "History deleted."


# Apply the custom theme to your app
with gr.Blocks() as app:
    gr.Markdown("## The Medical Plan Advisor")
    models = ["llama3.1:latest", "granite3-dense:8b", "mistral:7b", "gpt-4o"]
    locations = ["80001", "30002", "90001", "60005"]

    with gr.Row():
        model_choice = gr.Radio(models, label="Select a Model", scale=1)
        location_choice = gr.Dropdown(choices=locations, label="Select your location")
        
    user_input = gr.Textbox(lines=2, label="Ask your question")
    
    submit_button = gr.Button("Submit")
    output = gr.Markdown(label="Response")

    submit_button.click(
        process_input_ui, inputs=[user_input, model_choice, location_choice], outputs=output
    )
    thumbs_up = gr.Button("👍", elem_classes="feedback-btn thumbs-up",scale=2)
    feedback_button = gr.Button("Retrieve Feedback",scale=1)
    feedback_table = gr.DataFrame(
        headers=["ID", "Model Name", "User prompt", "LLM response"],
        value=[],scale=4
    )

    feedback_button.click(retrieve_feedback, outputs=feedback_table)

# Store feedback on thumbs-up click
    thumbs_up.click(
        submit_feedback, inputs=[model_choice, user_input, output], outputs=[]
    )

    delete_button = gr.Button("Delete History",scale=1)

    delete_button.click(delete_feedback)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
