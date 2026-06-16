import folium
from folium import TileLayer  # Note: Capitalized class name
from folium.plugins import Draw, Fullscreen, MeasureControl
from streamlit_folium import st_folium


def render_map():
    m = folium.Map(location=[22.5, 72.5], zoom_start=7)

    draw_plugin = Draw(
        draw_options={
            "polyline": False,
            "rectangle": True,
            "circle": False,
            "circlemarker": False,
            "marker": False,
            "polygon": True,
        },
        edit_options={"edit": True},
    )
    draw_plugin.add_to(m)

    TileLayer(tiles="openstreetmap", name="street map").add_to(m)
    TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="google",
        name="satellite",
        overlay=False,
        control=True,
    ).add_to(m)
    TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attr="google",
        name="terrain",
        overlay=False,
        control=True,
    ).add_to(m)

    Fullscreen().add_to(m)
    MeasureControl().add_to(m)
    folium.LayerControl().add_to(m)

    map_data = st_folium(
        m, width=900, height=600, returned_objects=["all_drawings"]
    )

    # FIX: Safety check for None values
    if map_data is None:
        return None

    drawings = map_data.get("all_drawings", [])

    if not drawings:  # Pythonic check for empty lists
        return None

    return drawings[0]
