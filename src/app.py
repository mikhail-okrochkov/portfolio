from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.colors as pc
import geopandas as gpd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Preprocessed GeoJSON data
gdf = gpd.read_file("../data/census_dataset.geojson")
geojson_data = gdf.__geo_interface__

column_mapping = {
    "Median_Household": "Median Household Income",
    "Median_Family": "Median Family Income",
    "Median_Married": "Median Married Income",
    "Median_Non_Family": "Median Non-Family Income",
    "Household_200k": "Percent of households that earn over 200k",
    "Household_100k": "Percent of households that earn over 100k",
    "Family_200k": "Percent of families that earn over 200k",
    "Family_100k": "Percent of families that earn over 100k",
    "Married_200k": "Percent of married households that earn over 200k",
    "Married_100k": "Percent of married households that earn over 100k",
    "Non_Family_200k": "Percent of non-family households that earn over 200k",
    "Non_Family_100k": "Percent of non-family households that earn over 100k",
    "Median_Rent": "Median Rent",
    "Median_1BR_Rent": "Median 1 Bedroom Rent",
    "Fraction_Rent_Salary": "Fraction of Salary Spent on Rent"
}

app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="map-dropdown",
                    options=[{"label": "Median Household Income", "value": "Median_Household"}, 
                             {"label": "Median Family Income", "value": "Median_Family"},
                             {"label": "Median Married Income", "value": "Median_Married"},
                             {"label": "Median Non-Family Income", "value": "Median_Non_Family"},
                             {"label": "Percent of households that earn over 200k", "value": "Household_200k"},
                             {"label": "Percent of households that earn over 100k", "value": "Household_100k"},
                             {"label": "Percent of families that earn over 200k", "value": "Family_200k"},
                             {"label": "Percent of families that earn over 100k", "value": "Family_100k"},
                             {"label": "Percent of married households that earn over 200k", "value": "Married_200k"},
                             {"label": "Percent of married households that earn over 100k", "value": "Married_100k"},
                             {"label": "Percent of non-family households that earn over 200k", "value": "Non_Family_200k"},
                             {"label": "Percent of non-family households that earn over 100k", "value": "Non_Family_100k"},
                             {"label": "Median Rent", "value": "Median_Rent"},
                             {"label": "Median 1 Bedroom Rent", "value": "Median_1BR_Rent"},
                             {"label": "Fraction of Salary Spent on Rent", "value": "Fraction_Rent_Salary"},],
                    value="Median_Household",
                    clearable=False,
                    maxHeight=500,
                ), 
            ),className="g-0 col-4 offset-4", style={"margin-top": "50px"}
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading",
                    children=[dcc.Graph(id="map-container")],
                    #type="circle"
                ), 
            ),className="g-0 col-8 offset-2"
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    id="top-5-container",
                    className="mt-4 text-center"  # Custom class for styling
                ),
                className="g-0 col-3 offset-2",  # Centered and responsive
            ),
            dbc.Col(
                html.Div(
                    id="bot-5-container",
                    className="mt-4 text-center"  # Custom class for styling
                ),
                className="g-0 col-3 offset-2",  # Centered and responsive
            )
        ])
    ],
)

app.index_string += """
<style>
    /* Center the map container and limit its width */
    .map-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;  /* Makes the map take 70% of viewport height */
    }

    /* Adjust the size and aspect ratio of the map */
    #map-container {
        width: 100%;
        aspect-ratio: 2/1;  /* 16:12 aspect ratio */
    }
</style>
"""

@app.callback(
    Output("map-container", "figure"),
    Output("top-5-container", "children"),
    Output("bot-5-container", "children"),
    Input("map-dropdown", "value")
)
def update_map(selected_map):
    # Example: Generate different maps based on the dropdown
    column_name = column_mapping[selected_map]

    top_5 = gdf[['NAME', selected_map]].sort_values(by=selected_map, ascending=False).head(5)
    bot_5 = gdf[['NAME', selected_map]].sort_values(by=selected_map, ascending=True).head(5)

    fig = px.choropleth(
        gdf,
        geojson=geojson_data,
        locations=gdf.index,
        color=selected_map,
        scope="usa",
        color_continuous_scale='Viridis',
        hover_data={
            "NAME": True,  # Include county name
            selected_map: True,  # Include the selected column's value
        },
        labels={column_name: selected_map},
    )
    if selected_map == 'Fraction_Rent_Salary':  
        fig.update_layout(
            coloraxis=dict(
                cmin=0,  # Minimum value for the color axis
                cmax=0.35  # Maximum value for the color axis
            )
        )

    # Generate rows and columns for the top 5 display
    top_5_rows = []
    for _, row in top_5.iterrows():
        top_5_rows.append(
            dbc.Row([
                dbc.Col(html.Div(row['NAME']), width=6),
                dbc.Col(html.Div(f"{row[selected_map]:,}"), width=6)
            ], className="mb-2")
        )
    
    # Wrap the rows in a container
    top_5_container = html.Div(
        children=[
            html.H5(f"Top 5 Counties by {column_name}", className="mb-3"),
            *top_5_rows
        ]
    )

    bot_5_rows = []
    for _, row in bot_5.iterrows():
        bot_5_rows.append(
            dbc.Row([
                dbc.Col(html.Div(row['NAME']), width=6),
                dbc.Col(html.Div(f"{row[selected_map]:,}"), width=6)
            ], className="mb-2")
        )
    
    # Wrap the rows in a container
    bot_5_container = html.Div(
        children=[
            html.H5(f"Bottom 5 Counties by {column_name}", className="mb-3"),
            *bot_5_rows
        ]
    )

    return fig, top_5_container, bot_5_container

if __name__ == "__main__":
    app.run_server(debug=True)
