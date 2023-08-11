"""
Purpose: Use Python to create a continuous intelligence and 
interactive analytics dashboard using Shiny for Python with 
interactive charts from Plotly Express.

Each Shiny app has two parts: 

- a user interface app_ui object (similar to the HTML in a web page) 
- a server function that provides the logic for the app (similar to JS in a web page).

"""
# First, import from the Python Standard Library (no installation required).
import asyncio

# Then, outside imports (these must be installed into your active Python environment).
from shiny import App, ui   # pip install shiny
import shinyswatch          # pip install shinyswatch

# Finally, import what we need from other local code files.
from tests_server import get_tests_server_functions
from tests_ui_inputs import get_tests_inputs
from tests_ui_outputs import get_tests_outputs
from util_logger import setup_logger

# Set up a logger for this file (see the logs folder to help with debugging).
logger, logname = setup_logger(__file__)


# Define a function that will run continuously to update our data.
# We update to a local file, but we could also update to a database.
# Or a cloud service. Or a data lake. Or a data warehouse.
#async def update_csv_files():
#    while True:
#        logger.info("Calling continuous updates ...")
#        task1 = asyncio.create_task(update_csv_location())
#        task2 = asyncio.create_task(update_csv_stock())
#        await asyncio.gather(task1, task2)
#        await asyncio.sleep(60)  # wait for 60 seconds

app_ui = ui.page_navbar(
    shinyswatch.theme.lumen(),
    ui.nav(
        "Test Results",
        ui.layout_sidebar(
            get_tests_inputs(),
            get_tests_outputs(),
        ),
    ),
    #ui.nav(
    #    "Test Submissions",
    #   ui.layout_sidebar(
    #       get_submissions_inputs(),
    #       get_submissions_outputs(),
    #   ),
    #),
    ui.nav(ui.a("About", href="https://github.com/geckog")),
    ui.nav(ui.a("GitHub", href="https://github.com/geckog/cintel-07")),
    ui.nav(ui.a("App", href="https://mattgoeckel.shinyapps.io/cintel-07/")),
    ui.nav(ui.a("Plotly Express", href="https://plotly.com/python/line-and-scatter/")),
    ui.nav(ui.a("File_Reader", href="https://shiny.rstudio.com/py/api/reactive.file_reader.html")),
    title=ui.h1("Matt's Dashboard"),
)






def server(input, output, session):
    """Define functions to create UI outputs."""
    logger.info("Starting server ...")

    # Kick off continuous updates when the app starts
    #asyncio.create_task(update_csv_files())
    #update_csv_assessments()
    logger.info("Starting continuous updates ...")

    get_tests_server_functions(input, output, session)


app = App(app_ui, server, debug=True)
