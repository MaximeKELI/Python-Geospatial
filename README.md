# Python-Geospatial


Real-Time Geospatial Map Visualization Project
Overview

This project is a real-time geospatial map visualization tool built using Python. It allows users to interactively display and update map data, such as GPS coordinates, in real time. The application is designed to be user-friendly and modular, making it easy to extend with additional features.

The core functionality includes:

    Displaying an interactive map centered on a specific location.

    Adding and updating markers on the map in real time.

    Loading and visualizing GPS data from a JSON file.

    Providing a simple user interface for adding custom markers.

The project leverages popular Python libraries such as Folium for map rendering, Streamlit for the web interface, and Pandas for data handling.
Key Features

    Interactive Map Display:

        The map is centered on an initial location (e.g., Paris) and supports zooming and panning.

        Markers are added to the map to represent specific GPS coordinates.

    Real-Time Data Integration:

        GPS data is loaded from a JSON file (gps_data.json) and displayed on the map.

        The application can be extended to support real-time data streams (e.g., live GPS tracking).

    User Interface:

        A sidebar allows users to add custom markers by specifying latitude, longitude, and a description.

        The map updates dynamically as new markers are added.

    Modular Design:

        The project is organized into modules (map_manager.py, data_handler.py) for better code maintainability.

        Each module handles a specific task (e.g., map rendering, data loading).

    Extensibility:

        The project can be extended with additional features, such as:

            Integration with APIs (e.g., OpenStreetMap, Google Maps).

            Drawing shapes (lines, polygons) on the map.

            Exporting the map as an image or PDF.

Technologies Used

    Python: The core programming language.

    Folium: A library for creating interactive maps.

    Streamlit: A framework for building web applications with Python.

    Pandas: A library for data manipulation and analysis.

    JSON: Used for storing and loading GPS data.

Project Structure
Copy

/geospatial_python
│
├── /projet_carte_temps_reel
│   ├── main.py                 # Main application script
│   ├── config.py               # Configuration file (API keys, settings)
│   ├── requirements.txt        # List of dependencies
│
├── /modules
│   ├── __init__.py             # Makes the folder a Python module
│   ├── map_manager.py          # Handles map creation and marker management
│   ├── data_handler.py         # Handles data loading and processing
│   ├── ui_manager.py           # Manages the user interface (future use)
│   └── utils.py                # Utility functions (future use)
│
├── /data
│   └── gps_data.json           # Sample GPS data in JSON format
│
└── /output
    └── map_export.html         # Exported map file (future use)

How It Works

    Data Loading:

        GPS data is loaded from gps_data.json using the DataHandler module.

        The data includes latitude, longitude, and a description for each location.

    Map Rendering:

        The MapManager module creates an interactive map using Folium.

        Markers are added to the map based on the loaded GPS data.

    User Interaction:

        Users can add custom markers via the Streamlit sidebar.

        The map updates in real time as new markers are added.

    Real-Time Updates:

        The application can be extended to support real-time updates (e.g., live GPS tracking).

Future Enhancements

    API Integration:

        Integrate with geospatial APIs (e.g., OpenStreetMap, Google Maps) for additional features like route planning or traffic data.

    Advanced User Interface:

        Add more interactive elements, such as dropdown menus, sliders, and buttons.

    Data Export:

        Allow users to export the map as an image (PNG) or PDF.

    Real-Time Tracking:

        Implement live GPS tracking to display moving objects on the map.

    Shape Drawing:

        Enable users to draw shapes (lines, polygons) on the map and calculate distances or areas.

How to Run the Project

    Clone the repository or set up the project structure as described above.

    Install the required dependencies:
    bash
    Copy

    pip install -r requirements.txt

    Run the Streamlit application:
    bash
    Copy

    streamlit run projet_carte_temps_reel/main.py

    Open the application in your web browser and interact with the map.

Conclusion

This project is a powerful and flexible tool for visualizing geospatial data in real time. Its modular design and use of popular Python libraries make it easy to extend and customize for various use cases, such as GPS tracking, location-based services, or geospatial analysis.
