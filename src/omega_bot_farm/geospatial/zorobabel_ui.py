#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - Interactive Web UI
-----------------------------------
Provides an interactive web interface for exploring the Zorobabel
geospatial visualization system with sacred locations and divine overlays.

🌀 MODULE: Web Visualization Interface
🧭 CONSCIOUSNESS LEVEL: 6 - Empathy
"""

import os
import base64
import io
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Local imports (assuming they are in the same directory)
from . import dem_util
from . import zorobabel_k1l1


# Initialize the Dash app with Bootstrap styling
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],  # Dark theme for cosmic vibes
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

# Set app title
app.title = "ZOROBABEL K1L1 - Sacred Geospatial System"

# Layout with cosmic styling
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1(
                            "🌀 ZOROBABEL K1L1 🌀", 
                            className="text-center mb-2",
                            style={"color": "gold", "font-family": "Copperplate, Fantasy"}
                        ),
                        html.H4(
                            "5D Sacred Geospatial System", 
                            className="text-center mb-4",
                            style={"color": "#B19CD9"}
                        ),
                    ]
                ),
                width=12,
            )
        ),
        
        # Main content
        dbc.Row(
            [
                # Left sidebar with controls
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("🧭 Divine Controls", className="card-title"),
                                    html.Hr(style={"borderColor": "#555"}),
                                    
                                    # Region selector
                                    html.P("Select Sacred Region:", style={"color": "#B19CD9"}),
                                    dcc.Dropdown(
                                        id="region-dropdown",
                                        options=[
                                            {"label": "🌋 Ngorongoro", "value": "ngorongoro"},
                                            {"label": "🧬 Olduvai Gorge", "value": "olduvai"},
                                            {"label": "🏔️ Kilimanjaro", "value": "kilimanjaro"},
                                        ],
                                        value="ngorongoro",
                                        style={"backgroundColor": "#2A2A2A", "color": "#FFF"}
                                    ),
                                    html.Br(),
                                    
                                    # Visualization options
                                    html.P("Cosmic Overlays:", style={"color": "#B19CD9"}),
                                    dbc.Checklist(
                                        id="overlay-checklist",
                                        options=[
                                            {"label": " 🌀 Zorobabel Spiral", "value": "spiral"},
                                            {"label": " ✨ Resonance Nodes", "value": "nodes"},
                                            {"label": " 🔱 Trinity Paths", "value": "paths"},
                                        ],
                                        value=["spiral", "nodes", "paths"],
                                        style={"color": "#DDD"}
                                    ),
                                    html.Br(),
                                    
                                    # Spiral options
                                    html.P("Spiral Parameters:", style={"color": "#B19CD9"}),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Revolutions:", style={"color": "#DDD"}),
                                            dcc.Slider(
                                                id="revolutions-slider",
                                                min=1, max=7, step=1, value=4,
                                                marks={i: str(i) for i in range(1, 8)},
                                                tooltip={"placement": "bottom", "always_visible": True}
                                            ),
                                        ]),
                                    ]),
                                    html.Br(),
                                    
                                    # Node count options
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Node Count:", style={"color": "#DDD"}),
                                            dcc.Slider(
                                                id="nodes-slider",
                                                min=3, max=12, step=1, value=7,
                                                marks={i: str(i) for i in range(3, 13, 3)},
                                                tooltip={"placement": "bottom", "always_visible": True}
                                            ),
                                        ]),
                                    ]),
                                    html.Br(),
                                    
                                    # Generate button
                                    dbc.Button(
                                        "🔮 Generate Sacred Map",
                                        id="generate-button",
                                        color="warning",
                                        className="w-100 mb-3",
                                        style={"backgroundColor": "#8A2BE2", "borderColor": "gold"}
                                    ),
                                    
                                    # Cosmic explanation
                                    html.Div(
                                        id="cosmic-explanation",
                                        style={
                                            "backgroundColor": "#111", 
                                            "padding": "10px", 
                                            "borderRadius": "5px",
                                            "color": "#AAA",
                                            "fontSize": "0.9em"
                                        }
                                    ),
                                ]
                            ),
                            className="mb-4",
                            style={"backgroundColor": "#222", "borderColor": "#444"}
                        ),
                    ],
                    width=3,
                ),
                
                # Main visualization area
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Visualization header
                                    html.H4(
                                        id="viz-title", 
                                        className="card-title text-center",
                                        style={"color": "#B19CD9"}
                                    ),
                                    
                                    # Visualization image
                                    html.Div(
                                        id="loading-div",
                                        children=[
                                            dbc.Spinner(
                                                html.Img(
                                                    id="visualization-img",
                                                    style={
                                                        "width": "100%", 
                                                        "borderRadius": "10px",
                                                        "border": "1px solid #444"
                                                    }
                                                ),
                                                color="primary",
                                                type="grow",
                                            ),
                                        ],
                                    ),
                                    
                                    # Info below visualization
                                    html.Div(
                                        id="location-info",
                                        className="text-center mt-3",
                                        style={"color": "#DDD"}
                                    ),
                                    
                                    # Download button
                                    html.Div(
                                        dbc.Button(
                                            "💾 Download Sacred Map",
                                            id="download-button",
                                            color="success",
                                            className="mt-3",
                                            style={"backgroundColor": "#1E7B1E", "borderColor": "#DDD"}
                                        ),
                                        className="text-center"
                                    ),
                                    dcc.Download(id="download-image"),
                                ]
                            ),
                            style={"backgroundColor": "#222", "borderColor": "#444"}
                        ),
                    ],
                    width=9,
                ),
            ]
        ),
        
        # Footer
        dbc.Row(
            dbc.Col(
                html.Footer(
                    [
                        html.Hr(style={"borderColor": "#444"}),
                        html.P(
                            "🌸 WE BLOOM NOW AS ONE 🌸", 
                            className="text-center",
                            style={"color": "#B19CD9", "fontStyle": "italic"}
                        ),
                        html.P(
                            "GBU2™ LICENSE - Genesis-Bloom-Unfoldment 2.0",
                            className="text-center small",
                            style={"color": "#888"}
                        ),
                    ]
                ),
                width=12,
            )
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#111", "color": "#DDD", "minHeight": "100vh", "padding": "20px"}
)


# Cosmic explanations for each region
COSMIC_EXPLANATIONS = {
    "ngorongoro": """
        💫 The Ngorongoro Crater is more than a geological marvel — it's a divine resonance point, 
        a volcanic womb, and a symbolic return spiral. The crater floor creates a natural 
        meditation chamber, amplifying Earth's subtle vibrations.
        
        🔱 Zorobabel's spiral here represents the divine builder's return pattern, 
        connecting to Olduvai Gorge, the birthplace of humanity.
    """,
    "olduvai": """
        💫 Olduvai Gorge — where humanity's first steps were taken — contains layers 
        of cosmic memory in its sedimentary walls. This sacred site holds the 
        origin codes of human consciousness.
        
        🔱 The Zorobabel spiral represents humanity's evolution from 
        primal awareness to cosmic consciousness.
    """,
    "kilimanjaro": """
        💫 Mount Kilimanjaro, Africa's highest peak, serves as a sacred antenna 
        connecting Earth to cosmic consciousness. Its three volcanic cones — 
        Kibo, Mawenzi, and Shira — form a trinity of ascension.
        
        🔱 The Zorobabel spiral here maps the path of spiritual evolution 
        from base consciousness to divine enlightenment.
    """,
}


@app.callback(
    [
        Output("cosmic-explanation", "children"),
        Output("viz-title", "children"),
    ],
    [
        Input("region-dropdown", "value"),
    ]
)
def update_region_info(region):
    """Update the cosmic explanation and visualization title based on selected region."""
    # Get the explanation for the selected region
    explanation = COSMIC_EXPLANATIONS.get(region, "")
    
    # Create a formatted explanation with proper spacing
    formatted_explanation = html.Div([
        html.P(paragraph.strip()) for paragraph in explanation.split('\n\n') if paragraph.strip()
    ])
    
    # Set the title based on the region
    if region == "ngorongoro":
        title = "🌋 Ngorongoro Crater - Cosmic Center"
    elif region == "olduvai":
        title = "🧬 Olduvai Gorge - Birth of Consciousness"
    elif region == "kilimanjaro":
        title = "🏔️ Mount Kilimanjaro - Sacred Peak"
    else:
        title = "Sacred Visualization"
    
    return formatted_explanation, title


@app.callback(
    [
        Output("visualization-img", "src"),
        Output("location-info", "children"),
    ],
    [
        Input("generate-button", "n_clicks"),
    ],
    [
        State("region-dropdown", "value"),
        State("overlay-checklist", "value"),
        State("revolutions-slider", "value"),
        State("nodes-slider", "value"),
    ],
    prevent_initial_call=True
)
def generate_visualization(n_clicks, region, overlays, revolutions, node_count):
    """Generate the sacred visualization based on user selections."""
    if n_clicks is None:
        return dash.no_update, dash.no_update
    
    try:
        # Ensure DEM data is available
        dem_path = dem_util.ensure_dem_available("tanzania")
        
        # Create the Zorobabel mapper
        mapper = zorobabel_k1l1.ZorobabelMapper(dem_path)
        mapper.load_dem()
        
        # Create visualization
        mapper.create_visualization(title=f"ZOROBABEL K1L1 - {region.capitalize()} Visualization")
        
        # Add sacred locations
        location_coords = mapper.add_all_sacred_locations()
        
        # Apply requested overlays
        if "spiral" in overlays:
            spiral_x, spiral_y = mapper.add_zorobabel_spiral(
                center_key=region, 
                revolutions=revolutions
            )
            
            if "nodes" in overlays:
                mapper.add_resonance_nodes(spiral_x, spiral_y, num_nodes=node_count)
                
        if "paths" in overlays:
            mapper.add_cosmic_paths(location_coords)
        
        # Save the visualization to a BytesIO object
        img_io = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_io, format='png', dpi=150, bbox_inches='tight')
        img_io.seek(0)
        
        # Convert the image to base64 for display
        encoded_img = base64.b64encode(img_io.getvalue()).decode('ascii')
        img_src = f'data:image/png;base64,{encoded_img}'
        
        # Get information about the selected location
        if region in mapper.sacred_locations:
            location = mapper.sacred_locations[region]
            lon, lat = location["coords"]
            location_info = html.Div([
                html.P([
                    html.Span("Location: ", style={"fontWeight": "bold"}),
                    f"{location['name']} {location['symbol']}"
                ]),
                html.P([
                    html.Span("Coordinates: ", style={"fontWeight": "bold"}),
                    f"Latitude: {lat}°, Longitude: {lon}°"
                ]),
                html.P([
                    html.Span("Sacred Significance: ", style={"fontWeight": "bold"}),
                    f"{location['description']}"
                ]),
            ])
        else:
            location_info = "No location information available."
        
        return img_src, location_info
        
    except Exception as e:
        error_msg = f"Error generating visualization: {str(e)}"
        return dash.no_update, error_msg


@app.callback(
    Output("download-image", "data"),
    Input("download-button", "n_clicks"),
    [
        State("visualization-img", "src"),
        State("region-dropdown", "value"),
    ],
    prevent_initial_call=True
)
def download_image(n_clicks, img_src, region):
    """Download the visualization image."""
    if not img_src:
        return dash.no_update
    
    # Extract the base64 data
    content_type, content_string = img_src.split(',')
    decoded = base64.b64decode(content_string)
    
    # Prepare the file for download
    filename = f"zorobabel_k1l1_{region}_{int(np.datetime64('now').astype('int'))}.png"
    
    return dict(content=decoded, filename=filename, type="image/png")


# Main function to run the app
def main():
    """Run the Dash app."""
    app.run_server(debug=True, port=8050)


if __name__ == "__main__":
    main() 