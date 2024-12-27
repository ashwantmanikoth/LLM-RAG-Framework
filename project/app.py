
import gradio as gr
from services.ollama_service import process_input
from database.feedback_service import FeedbackService
from database.factory import get_repository

# setup_database()
repository = get_repository()
feedback_service = FeedbackService(repository)


def format_feedback_for_table() -> list[list]:
    """
    Convert the list of dicts from retrieve_feedback() into
    a list of lists suitable for displaying in gr.DataFrame.
    """
    data = feedback_service.get_feedback()

    # The first sub-list is used as the header row if we pass headers="first_row" to gr.DataFrame
    # table_data = [["id","Model Name", "User prompt", "LLM Response"]]
    table_data = []
    for row in data:
        table_data.append([
            row["id"],
            row["model"],
            row["user_input"],
            row["output"],
        ])
    return table_data

def submit_feedback(model, user_input, output):
    return print(feedback_service.add_feedback(model, user_input, output))


# Gradio App
with gr.Blocks() as app:
    gr.Markdown("## The Medical Plan Advisor")

    models = ["llama3:latest", "granite3-dense:8b", "gpt-4o"]
    locations = ["80001", "30002","90001","60005"]
    with gr.Row():
        model_choice = gr.Radio(models, label="Select a Model", scale=1)
        location_choice = gr.Dropdown(
            choices=locations, label="Select your location", interactive=True
        )

    with gr.Row():
        # location_choice = gr.Radio(locations, label="Select Location")
        user_input = gr.Textbox(lines=2, interactive=True, label="Ask your question")
    output = gr.Markdown(label="Response")
    submit_button = gr.Button("Submit")

    submit_button.click(
        process_input,
        inputs=[user_input, model_choice, location_choice],
        outputs=output,
    )

    with gr.Row():
        thumbs_up_button = gr.Button("👍", elem_classes="feedback-btn thumbs-up")
        retrieve_button = gr.Button("Retrieve History", elem_classes="feedback-btn")

    # Store feedback on thumbs-up click
    thumbs_up_button.click(
        submit_feedback, inputs=[model_choice, user_input, output], outputs=[]
    )

    feedback_table = gr.DataFrame(
        headers=["ID", "Model Name", "User prompt", "LLM response"],
        label="History",
        datatype=["number", "str", "str", "str"],
        column_widths=[10, 10, 20, 100],
        interactive=False,
        wrap=True,
        line_breaks=True,
        value=[],
    )

    retrieve_button.click(
        fn=format_feedback_for_table, inputs=[], outputs=feedback_table
    )
    delete_button = gr.Button("Delete History")

    delete_button.click(feedback_service.delete_feedback)

if __name__ == "__main__":
    app.launch()
