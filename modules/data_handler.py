import pandas as pd

class DataHandler:
    def load_data(self, file_path):
        """Charge des données GPS depuis un fichier JSON."""
        return pd.read_json(file_path)