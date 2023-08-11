"""
Purpose: Provide user interaction options for MT Cars dataset.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

"""
from shiny import ui

# Define the UI inputs and include our new selection options

def get_tests_inputs():
    return ui.panel_sidebar(
        ui.h2("Assessment Submission"),
        ui.tags.hr(),
        ui.input_text("NAME_INPUT", "Enter your name", placeholder="Your Name"),
        ui.input_select(
            id="SUBMISSION_SELECT",
            label="Which assessment is being performed?",
            choices=["Vertical Jump", "Broad Jump", "40-Yard Dash"],
            selected="Vertical Jump",
        ),
        ui.input_date("SUBMISSION_DATE", "Date:"),
        ui.input_numeric("SUBMISSION_SCORE", "Score:", 0),
        ui.input_action_button("SUBMIT", "Submit"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Assessment Results Display"),
            ui.input_select(
            id="TEST_DISPLAY_SELECT",
            label="Choose an assessment to show results for",
            choices=["Vertical Jump", "Broad Jump", "40-Yard Dash"],
            selected="Vertical Jump",
            ),
        ),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Assessments Table"),
            ui.tags.p("Description of each field in the table:"),
            ui.tags.ul(
                ui.tags.li("name: Person performing the test"),
                ui.tags.li("date: The date the test was performed"),
                ui.tags.li("test: The test being performed"),
                ui.tags.li("score: The result of the test (units may vary)"),
            ),
            ui.output_table("tests_table"),
        ),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
