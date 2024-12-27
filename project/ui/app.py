# ui/app.py

import gradio as gr
import requests

BACKEND_URL = "http://localhost:5000"

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

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("## The Medical Plan Advisor")
    models = ["llama3:latest", "granite3-dense:8b", "gpt-4o"]
    locations = ["80001", "30002", "90001", "60005"]

    with gr.Row():
        model_choice = gr.Radio(models, label="Select a Model", scale=1)
        location_choice = gr.Dropdown(choices=locations, label="Select your location")
        user_input = gr.Textbox(lines=2, label="Ask your question")
    output = gr.Markdown(label="Response")
    submit_button = gr.Button("Submit")

    submit_button.click(
        process_input_ui, inputs=[user_input, model_choice, location_choice], outputs=output
    )

    feedback_button = gr.Button("Retrieve Feedback")
    feedback_table = gr.DataFrame(
        headers=["ID", "Model Name", "User prompt", "LLM response"],
        value=[],
    )

    feedback_button.click(retrieve_feedback, outputs=feedback_table)

if __name__ == "__main__":
    app.launch()
