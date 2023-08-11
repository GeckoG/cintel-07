""" 
Purpose: Provide continuous and reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

------------------------------------
Important Concept - Variable Scope
------------------------------------
In Python, the scope of a variable refers to where in the code that variable 
can be accessed and used. 

Variables defined outside of functions or blocks have global scope 
and can be used anywhere in the file. 

Variables defined inside a function or block have local scope 
and can only be used within that specific function or block.

------------------------------------
Important Concept - Reactivity
------------------------------
Reactive Effects only have "side effects" (they set reactive values, but don't return anything directly).
Reactive Calcs return a value (they can also set reactive values).
If a reactive.Effect depends on inputs, you must add them using the
reactive.event decorator (otherwise, the function won't be triggered).
"""

# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget
import csv

# Local Imports
from tests_get_basics import get_assessments_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
csv_assessments = Path(__file__).parent.joinpath("data").joinpath("assessments.csv")


def get_tests_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    # First, declare shared reactive values (used between functions) up front
    # Initialize the values on startup
    
    """Save for later updates
    reactive_submission = reactive.Value("Vertical Jump")
    """
    
    reactive_test = reactive.Value("Vertical Jump")

    # Then, define our server functions

    @reactive.Effect
    @reactive.event(input.SUBMIT)
    def _():
        name = input.NAME_INPUT()
        date = input.SUBMISSION_DATE()
        test = input.SUBMISSION_SELECT()
        score = input.SUBMISSION_SCORE()
        new_record = [name, date, test, score]

        with open(csv_assessments, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_record)

    @reactive.Effect
    @reactive.event(input.TEST_DISPLAY_SELECT)
    def _():
        """Set two reactive values (the location and temps df) when user changes location"""
        reactive_test.set(input.TEST_DISPLAY_SELECT())
        df = get_tests_temp_df()
        logger.info(f"init reactive_temp_df len: {len(df)}")

    @reactive.file_reader(str(csv_assessments))
    def get_tests_temp_df():
        """Return pandas Dataframe."""
        logger.info(f"READING df from {csv_assessments}")
        df = pd.read_csv(csv_assessments, quoting=csv.QUOTE_NONE)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def assessment_string():
        """Return a string based on selected location."""
        logger.info("tests_string starting")
        selected = reactive_test.get()
        line1 = f"Showing test results for {selected}."
        line2 = "Each person has their own color."
        line3 = "Units may vary."
        message = f"{line1}\n{line2}\n{line3}"
        logger.info(f"{message}")
        return message

    @output
    @render.table
    def assessment_table():
        df = get_tests_temp_df()
        # Filter the data based on the selected location
        df_assessment = df[df["test"] == reactive_test.get()]
        logger.info(f"Rendering TEMP table with {len(df_assessment)} rows")
        return df_assessment

    @output
    @render_widget
    def assessment_chart():
        df = get_tests_temp_df()
        # Filter the data based on the selected location
        df_assessment = df[df["test"] == reactive_test.get()]
        logger.info(f"Rendering TEMP chart with {len(df_assessment)} points")
        plotly_express_plot = px.line(
            df_assessment, x="date", y="score", color="name", markers=True
        )
        plotly_express_plot.update_layout(title="Test Results")
        return plotly_express_plot

    # return a list of function names for use in reactive outputs
    # Includes our 2 new selection strings and 2 new output widgets

    return [
        assessment_string,
        assessment_table,
        assessment_chart,
    ]