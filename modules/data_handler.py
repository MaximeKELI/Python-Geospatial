import pandas as pd
import geopandas as gpd


class DataHandler:
    def load_data(self, file_path):
        """Charge des données GPS depuis un fichier JSON."""
        return pd.read_json(file_path)

    def load_geospatial_data(self, file_path):
        """Charge des données géospatiales (Shapefile, GeoJSON, etc.) à l'aide
        de geopandas. Gère les formats supportés par geopandas.read_file().
        """
        try:
            gdf = gpd.read_file(file_path)
            return gdf
        except Exception as e:
            error_message = (f"Erreur lors du chargement du fichier "
                             f"géospatial {file_path}: {e}")
            print(error_message)
            return None