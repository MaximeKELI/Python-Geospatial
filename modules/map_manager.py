import folium

class MapManager:
    def create_map(self, lat, lon, zoom_start=13):
        """Crée une carte centrée sur les coordonnées spécifiées."""
        return folium.Map(location=[lat, lon], zoom_start=zoom_start)

    def add_marker(self, map_obj, lat, lon, popup_text):
        """Ajoute un marqueur à la carte."""
        folium.Marker([lat, lon], popup=popup_text).add_to(map_obj)