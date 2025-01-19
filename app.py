from fpdf import FPDF
import tempfile
import gradio as gr
from src.prep_for_meeting.crew import PrepForMeetingCrew


def run_crew(participants, company, context, objective, prior_interactions):
    try:
        inputs = {
            "participants": participants,
            "company": company,
            "context": context,
            "objective": objective,
            "prior_interactions": prior_interactions,
        }
        crew = PrepForMeetingCrew().crew()
        results = crew.kickoff(inputs=inputs)

        # Create a temporary PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Crew Output for Meeting Preparation\n\n{results}")

        # Save the PDF to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_file_path = temp_file.name
        pdf.output(pdf_file_path)

        return results, pdf_file_path  # Return text output and PDF path
    except Exception as e:
        return f"An error occurred: {e}", None


# Define Gradio interface
with gr.Blocks() as app:
    gr.Markdown("## CrewAI Meeting Preparation App")
    gr.Markdown("Provide the details for the meeting preparation below. Click 'Run' to execute the crew.")

    participants = gr.Textbox(label="Participants", placeholder="Enter participants (e.g., 'John Doe <johndoe@example.com>, Jane Doe <janedoe@example.com>')")
    company = gr.Textbox(label="Company", placeholder="Enter company name")
    context = gr.Textbox(label="Context", placeholder="Enter context (e.g., 'Human Rights')")
    objective = gr.Textbox(label="Objective", placeholder="Enter objective (e.g., 'Empower Human Rights worldwide')")
    prior_interactions = gr.Textbox(label="Prior Interactions", placeholder="Enter prior interactions (e.g., 'Save the date')")

    output = gr.Textbox(label="Output", lines=10, placeholder="Task results will appear here...")
    download_button = gr.File(label="Download PDF")

    run_button = gr.Button("Run")
    run_button.click(
        run_crew,
        inputs=[participants, company, context, objective, prior_interactions],
        outputs=[output, download_button]  # Output the text and downloadable PDF
    )

# Launch the Gradio app
if __name__ == "__main__":
    app.launch(share=True)
