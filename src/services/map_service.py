import folium

class MapService:
    @staticmethod
    def generate_map(lat, lon, output_file="user_location_map.html"):
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], tooltip="User Location").add_to(m)
        m.save(output_file)
        return output_file