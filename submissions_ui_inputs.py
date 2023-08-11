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
        ui.h2("Assessment Interaction"),
        ui.tags.hr(),
        ui.input_text("name_input", "Enter your name", placeholder="Your Name"),
        ui.input_select(
            id="SUBMISSION_SELECT",
            label="Choose an assessment",
            choices=["Vertical Jump", "Broad Jump", "40-Yard Dash"],
            selected="Vertical Jump",
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
