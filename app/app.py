# Import required libraries
import seaborn as sns  # For data visualization (scatterplot)
from faicons import icon_svg  # For displaying icons in the UI
from shiny import reactive  # For reactive programming (used for updating UI based on inputs)
from shiny.express import input, render, ui  # For creating UI components and rendering outputs in Shiny for Python
import palmerpenguins  # For loading the penguins dataset
import shinyswatch  # For using different themes in Shiny apps

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Set up the page options (title, fillable layout, and theme)
ui.page_opts(
    title="Penguins dashboard",  # Page title
    fillable=True,  # Allows the layout to fill the entire screen
    theme=shinyswatch.theme.flatly()  # Using the 'flatly' theme from shinyswatch
)

# Sidebar layout for filter controls
with ui.sidebar():
    ui.h4("Filter controls")  # Header for the filter controls section
    ui.hr(style="border-top: 4px solid #2c0735; margin-top: 2px;")  # A horizontal rule (line separator)
    
    # Slider input to filter by penguin mass (range: 2000 to 6000 g, default: 6000 g)
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    
    # Checkbox group to filter by species (Adelie, Gentoo, Chinstrap, default: all selected)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    
    ui.hr(style="border-top: 4px solid #2c0735;")  # Another horizontal rule
    ui.h6("Links")  # Links section header
    
    # Several clickable links to GitHub resources, PyShiny documentation, and templates
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main content area (displaying values and charts)
with ui.layout_column_wrap(fill=False):
    
    # Value box showing the number of penguins in the filtered dataset
    with ui.value_box(
        showcase=icon_svg("earlybirds"),  # Icon for this value box
        theme="bg-gradient-blue-purple"  # Custom theme for the value box
    ):
        "Number of penguins"

        # Reactive function to return the number of rows in the filtered dataset
        @render.text
        def count():
            return filtered_df().shape[0]  # Count the number of penguins after filtering

    # Value box showing the average bill length of the filtered penguins
    with ui.value_box(
        showcase=icon_svg("ruler-horizontal"),  # Icon for this value box
        theme="bg-gradient-blue-purple"  # Custom theme for the value box
    ):
        "Average bill length"

        # Reactive function to calculate the average bill length (in mm)
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box showing the average bill depth of the filtered penguins
    with ui.value_box(
        showcase=icon_svg("ruler-vertical"),  # Icon for this value box
        theme="bg-gradient-blue-purple"  # Custom theme for the value box
    ):
        "Average bill depth"

        # Reactive function to calculate the average bill depth (in mm)
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Two cards displaying visualizations and data
with ui.layout_columns():
    
    # Card displaying a scatter plot of bill length vs. bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        # Reactive function to render the scatter plot
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),  # Use the filtered dataset
                x="bill_length_mm",  # X-axis: bill length
                y="bill_depth_mm",  # Y-axis: bill depth
                hue="species",  # Color points by species
                palette={"Adelie": "#858ae3", "Gentoo": "#83c5be", "Chinstrap": "#023e8a"}  # Custom colors for species
            )

    # Card displaying the summary statistics of the filtered dataset
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        # Reactive function to render a data grid with selected columns
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",  # Species of penguins
                "island",  # Island where the penguins were found
                "bill_length_mm",  # Bill length in mm
                "bill_depth_mm",  # Bill depth in mm
                "body_mass_g",  # Body mass in grams
            ]
            # Display the selected columns in a data grid with filter options
            return render.DataGrid(filtered_df()[cols], filters=True)

# Uncomment the line below to include external CSS (if available)
# ui.include_css(app_dir / "styles.css")

# Reactive function to filter the dataset based on user inputs (species and mass)
@reactive.calc
def filtered_df():
    # Filter data by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Filter data by selected maximum body mass
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    # Return the filtered dataset
    return filt_df
