"""
map_builder.py – Folium interactive map module for CityLens (Micro-Zone Edition)
Renders one folium.Circle per micro-zone, colour-coded by heat_score,
with a folium.Marker at each zone centre showing the intervention popup.
"""

import folium


def _zone_color(heat_score: int) -> str:
    """Return hex fill colour based on heat_score threshold."""
    if heat_score >= 8:
        return "#FF4B4B"   # Red   – critical
    elif heat_score >= 5:
        return "#FFA500"   # Orange – moderate
    else:
        return "#00FF00"   # Green  – low risk


def _marker_icon_color(heat_score: int) -> str:
    """Map heat score to a Folium icon colour name."""
    if heat_score >= 8:
        return "red"
    elif heat_score >= 5:
        return "orange"
    else:
        return "green"


def build_map(
    lat: float,
    lon: float,
    micro_zones: list[dict],
    city_name: str = "",
) -> folium.Map:
    """
    Build an interactive Folium map with one circle + marker per micro-zone.

    Args:
        lat:         Latitude of the searched city centre
        lon:         Longitude of the searched city centre
        micro_zones: List of zone dicts, each with zone_name, lat, lon,
                     heat_score, intervention
        city_name:   Display name for the centre pin

    Returns:
        A configured folium.Map instance
    """
    # Base map — CARTO dark tiles for Industrial Tech vibe
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="CartoDB dark_matter",
        attr=(
            '&copy; <a href="https://carto.com/attributions">CARTO</a> | '
            'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        ),
    )

    # ── City centre anchor pin ────────────────────────────────────────────────
    folium.Marker(
        location=[lat, lon],
        tooltip=f"📍 {city_name or 'Search Location'} — Audit Centre",
        popup=folium.Popup(
            f"""
            <div style="font-family:monospace;min-width:170px;">
              <b style="color:#ff7700;">🏙️ {city_name or 'Search Location'}</b><br>
              <small>Lat {lat:.4f}, Lon {lon:.4f}</small><br>
              <small style="color:#aaa;">{len(micro_zones)} micro-zones analysed</small>
            </div>
            """,
            max_width=240,
        ),
        icon=folium.Icon(color="darkblue", icon="crosshairs", prefix="fa"),
    ).add_to(m)

    # ── Micro-zone circles + markers ─────────────────────────────────────────
    for zone in micro_zones:
        z_lat   = float(zone["lat"])
        z_lon   = float(zone["lon"])
        score   = int(zone["heat_score"])
        name    = zone["zone_name"]
        action  = zone["intervention"]
        color   = _zone_color(score)
        mk_clr  = _marker_icon_color(score)

        # Filled circle representing the zone's heat footprint
        folium.Circle(
            location=[z_lat, z_lon],
            radius=600,                  # 600 m radius as specified
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.30,
            weight=2,
            tooltip=f"🌡 {name}  |  Heat Score: {score}/10",
        ).add_to(m)

        # Intervention marker at the zone centre
        popup_html = f"""
        <div style="font-family:monospace;min-width:200px;max-width:260px;">
          <b style="color:{'#FF4B4B' if score >= 8 else ('#FFA500' if score >= 5 else '#00CC00')};">
            {'🔴' if score >= 8 else ('🟠' if score >= 5 else '🟢')} {name}
          </b><br>
          <span style="font-size:0.85em;color:#ccc;">Heat Score: <b>{score}/10</b></span><br>
          <hr style="border-color:#444;margin:6px 0;">
          <b style="color:#39ff14;">🌿 Recommended Intervention:</b><br>
          <span style="font-size:0.82em;color:#ddd;">{action}</span>
        </div>
        """

        folium.Marker(
            location=[z_lat, z_lon],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{'🔴' if score >= 8 else ('🟠' if score >= 5 else '🟢')} {name} — click for intervention",
            icon=folium.Icon(
                color=mk_clr,
                icon="map-marker",
                prefix="fa",
            ),
        ).add_to(m)

    return m
