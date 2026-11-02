#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor kartografických map a synchronizace dat pro Českobrodsko
"""

import os
import sys
import json
import math
import subprocess
import re
import shutil
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO_ROOT, "data", "cache")
MAP_DIR = os.path.join(REPO_ROOT, "assets", "maps")

CATEGORY_COLORS = {
    "stezka": "#1d4ed8",
    "alej": "#15803d",
    "polni": "#b45309",
    "chodnik": "#334155",
}
CATEGORY_LABELS = {
    "stezka": "Cyklostezky / naučné stezky",
    "alej": "Aleje / přírodní pěší trasy",
    "polni": "Polní cesty / biokoridory",
    "chodnik": "Městské chodníky",
}

def latlon_to_tile_float(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xt = (lon + 180.0) / 360.0 * n
    yt = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return xt, yt

def project_to_grid(lat, lon, grid_meta, offset_x=0.0, offset_y=0.0, scale=1.0):
    xt, yt = latlon_to_tile_float(lat, lon, grid_meta["zoom"])
    px = (xt - grid_meta["x0"]) * 256.0 * scale + offset_x
    py = (yt - grid_meta["y0"]) * 256.0 * scale + offset_y
    return round(px, 1), round(py, 1)

def load_regional_grid():
    with open(os.path.join(CACHE_DIR, "grid_overview_region.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_geojson():
    with open(os.path.join(REPO_ROOT, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()
    match = re.search(r"const ROUTES = (\[.*?\]);", html, flags=re.DOTALL)
    if not match:
        raise ValueError("Cannot find the canonical ROUTES array in index.html")
    routes = json.loads(match.group(1))
    ids = [route.get("id") for route in routes]
    if len(ids) != len(set(ids)) or not all(isinstance(route.get("coords"), list) and route["coords"] for route in routes):
        raise ValueError("Routes must have unique IDs and non-empty coordinates")
    features = []
    for route in routes:
        coords = route["coords"]
        if coords and isinstance(coords[0][0], list):
            points = [point for line in coords for point in line]
            geometry = {"type": "MultiLineString", "coordinates": [
                [[lon, lat] for lat, lon in line] for line in coords
            ]}
        else:
            points = coords
            geometry = {"type": "LineString", "coordinates": [[lon, lat] for lat, lon in coords]}
        if not all(
            isinstance(point, list) and len(point) == 2 and
            -90 <= point[0] <= 90 and -180 <= point[1] <= 180
            for point in points
        ):
            raise ValueError(f"Route {route.get('id')} has invalid latitude/longitude coordinates")
        features.append({
            "type": "Feature",
            "properties": {
                "id": route["id"],
                "name": f'#{route["id"]} {route["name"]}',
                "rok_obnovy": route.get("yearCat", ""),
                "category": route.get("category", ""),
                "mapy_cz_stav": route.get("mapyStatus", ""),
                "stroke": CATEGORY_COLORS.get(route.get("category"), "#2563eb"),
                "presnost": "orientacni" if route.get("dashed") else "OSM",
                "stroke-dasharray": "8,6" if route.get("dashed") else None,
                "delka_povrch": route.get("lengthSurface", ""),
                "odkud_A": route.get("fromLabel", ""),
                "kam_B": route.get("toLabel", ""),
                "zdroj": route.get("source", ""),
                "zdroj_url": route.get("sourceUrl", ""),
                "zdroj_dokument": route.get("sourceDoc", ""),
                "zdroj_citace": route.get("sourceQuote", ""),
                "zdroj_url2": route.get("sourceUrl2", ""),
                "osm_url": route.get("osmUrl", ""),
                "stav_zakresu": "orientacni_nebo_plan" if route.get("dashed") else "oznaceno_osm",
                "naklady": route.get("costAmount", ""),
                "poznamka_k_nakladum": route.get("costScopeNote", ""),
            },
            "geometry": geometry,
        })
    return {"type": "FeatureCollection", "features": features}


def write_geojson():
    path = os.path.join(REPO_ROOT, "data", "trasy_ceskobrodsko.geojson")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(load_geojson(), f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Generated {os.path.basename(path)}")

def render_svg_to_png(svg_path, width=1920, height=1280):
    png_path = svg_path.replace(".svg", ".png")
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
    browser = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome") or shutil.which("google-chrome-stable") or next((b for b in chrome_candidates if os.path.exists(b)), None)
    if not browser:
        print("Warning: No headless browser found for PNG rendering.")
        return
    file_url = Path(svg_path).resolve().as_uri()
    try:
        subprocess.run([
            browser,
            "--headless",
            "--disable-gpu",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={png_path}",
            file_url
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Warning: SVG and GeoJSON were generated, but PNG rendering failed in this environment.")
        return
    print(f"Rendered {os.path.basename(png_path)} ({os.path.getsize(png_path) // 1024} KB)")

def generate_regional_map():
    grid = load_regional_grid()
    gj = load_geojson()

    W, H = 1920, 1280
    MAP_X, MAP_Y = 24, 102
    MAP_W, MAP_H = 1260, 1040

    SCALE = 1.05
    TILE_OFF_X = MAP_X - 25
    TILE_OFF_Y = MAP_Y - 15

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="hdrReg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <clipPath id="regClip">
      <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" rx="14"/>
    </clipPath>
    <filter id="regShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.22"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="#f1f5f9"/>

  <!-- Hlavička -->
  <rect x="24" y="16" width="{W-48}" height="74" rx="14" fill="url(#hdrReg)" filter="url(#regShadow)"/>
  <text x="48" y="48" fill="#ffffff" font-size="23" font-weight="900">MAPA OBNOVENÝCH STEZEK A POLNÍCH CEST NA CELÉM ČESKOBRODSKU (2020–2026+)</text>
  <text x="48" y="72" fill="#94a3b8" font-size="13.5" font-weight="600">Podklad OpenStreetMap (Zoom 13) • Plná čára: označení OSM • Čárkovaná: orientační / plán</text>

  <g clip-path="url(#regClip)">
''')

    for t in grid["tiles"]:
        tx = TILE_OFF_X + t["px"] * SCALE
        ty = TILE_OFF_Y + t["py"] * SCALE
        tw = 256.0 * SCALE + 0.5
        svg.append(f'    <image x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{tw:.1f}" xlink:href="data:image/png;base64,{t["b64"]}"/>')

    svg.append(f'    <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" fill="#ffffff" opacity="0.10"/>')

    # Trasy
    badge_positions = {}
    for f in gj["features"]:
        p = f["properties"]
        rid = p["id"]
        geom = f["geometry"]
        is_osm = p.get("presnost") == "OSM"
        col = p.get("stroke") or CATEGORY_COLORS.get(p.get("category"), "#2563eb")
        dash = "" if is_osm else 'stroke-dasharray="9,6"'
        sw = 5.2 if is_osm else 4.4

        lines = geom["coordinates"] if geom["type"] == "MultiLineString" else [geom["coordinates"]]
        all_screen_pts = []

        for l in lines:
            pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lon, lat in l]
            all_screen_pts.extend(pts)
            d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
            svg.append(f'    <path d="{d}" fill="none" stroke="#ffffff" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>')
            svg.append(f'    <path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" {dash} stroke-linecap="round" stroke-linejoin="round"/>')

        if all_screen_pts:
            mid = all_screen_pts[len(all_screen_pts) // 2]
            badge_positions[rid] = mid

    # Vyladění posunů odznaků proti kolizím
    offsets = {
        1: (0, -14),
        2: (12, -12),
        3: (-12, 12),
        4: (14, -12),
        5: (-14, 0),
        6: (-15, -12),
        7: (0, -14),
        8: (14, -12),
        9: (-14, 14),
        10: (12, -10),
        11: (14, 10),
        12: (-14, -12),
        13: (14, 12),
        14: (12, -12),
        15: (0, -14),
        16: (18, 0),
        17: (-18, 0),
        18: (-16, 14),
        19: (20, -10),
        20: (-18, 14),
        21: (-16, -14),
        22: (-18, 14),
        23: (16, -12),
        24: (-16, -12),
        25: (16, 12),
    }

    # Popisky klíčových oblastí
    reg_callouts = []

    # Vodící linky ke kartičkám
    for rid, ox, oy, l1, l2 in reg_callouts:
        if rid in badge_positions:
            px, py = badge_positions[rid]
            cw, ch = 224, 38
            bx = max(MAP_X + cw/2 + 10, min(MAP_X + MAP_W - cw/2 - 10, px + ox))
            by = max(MAP_Y + ch/2 + 10, min(MAP_Y + MAP_H - ch/2 - 10, py + oy))
            svg.append(f'    <line x1="{px}" y1="{py}" x2="{bx}" y2="{by}" stroke="#0f172a" stroke-width="1.8" stroke-dasharray="3,3"/>')

    # Číselné odznaky
    for f in gj["features"]:
        rid = f["properties"]["id"]
        col = f["properties"].get("stroke") or CATEGORY_COLORS.get(f["properties"].get("category"), "#2563eb")
        if rid in badge_positions:
            mx, my = badge_positions[rid]
            ox, oy = offsets.get(rid, (0, 0))
            bx, by = mx + ox, my + oy
            svg.append(f'    <circle cx="{bx}" cy="{by}" r="11" fill="{col}" stroke="#ffffff" stroke-width="2.2" filter="url(#regShadow)"/>')
            svg.append(f'    <text x="{bx}" y="{by+3.8}" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">{rid}</text>')

    # Kartičky popisků
    for rid, ox, oy, l1, l2 in reg_callouts:
        if rid in badge_positions:
            f = next(x for x in gj["features"] if x["properties"]["id"] == rid)
            col = f["properties"].get("stroke") or CATEGORY_COLORS.get(f["properties"].get("category"), "#2563eb")
            px, py = badge_positions[rid]
            cw, ch = 224, 38
            bx = max(MAP_X + cw/2 + 10, min(MAP_X + MAP_W - cw/2 - 10, px + ox))
            by = max(MAP_Y + ch/2 + 10, min(MAP_Y + MAP_H - ch/2 - 10, py + oy))
            svg.append(f'    <g transform="translate({bx-cw/2:.1f}, {by-ch/2:.1f})" filter="url(#regShadow)">')
            svg.append(f'      <rect x="0" y="0" width="{cw}" height="{ch}" rx="7" fill="#ffffff" stroke="{col}" stroke-width="2" opacity="0.96"/>')
            svg.append(f'      <text x="{cw/2}" y="15" fill="#0f172a" font-size="10.5" font-weight="800" text-anchor="middle">#{rid} {l1}</text>')
            svg.append(f'      <text x="{cw/2}" y="29" fill="#334155" font-size="9.5" font-weight="700" text-anchor="middle">{l2}</text>')
            svg.append(f'    </g>')

    svg.append('  </g>')
    svg.append(f'  <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" rx="14" fill="none" stroke="#0f172a" stroke-width="2.5"/>')

    # Pravý panel se seznamem všech 25 tras
    PX = MAP_X + MAP_W + 18
    PW = W - PX - 24
    svg.append(f'''
  <rect x="{PX}" y="{MAP_Y}" width="{PW}" height="{MAP_H}" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#regShadow)"/>
  <text x="{PX+18}" y="{MAP_Y+30}" fill="#0f172a" font-size="16" font-weight="900">SEZNAM TRAS (ODKUD → KAM &amp; ZÁKRES)</text>
  <text x="{PX+18}" y="{MAP_Y+48}" fill="#64748b" font-size="11" font-weight="600">Číslo odpovídá značce v mapě • Stav ověřte v citovaných zdrojích</text>
  <line x1="{PX+14}" y1="{MAP_Y+58}" x2="{PX+PW-14}" y2="{MAP_Y+58}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    # Legenda kategorií
    ly = MAP_Y + 76
    lx = PX + 16
    for category, ylabel in CATEGORY_LABELS.items():
        ycol = CATEGORY_COLORS[category]
        svg.append(f'  <rect x="{lx}" y="{ly-11}" width="12" height="12" rx="3" fill="{ycol}"/>')
        svg.append(f'  <text x="{lx+16}" y="{ly-1}" fill="#1e293b" font-size="10.5" font-weight="700">{ylabel}</text>')
        ly += 18

    # Legenda stylu čáry
    ly2 = MAP_Y + 150
    svg.append(f'''
  <line x1="{PX+16}" y1="{ly2-5}" x2="{PX+46}" y2="{ly2-5}" stroke="#0f172a" stroke-width="4"/>
  <text x="{PX+52}" y="{ly2-1}" fill="#0f172a" font-size="10.5" font-weight="800">Plná čára = označeno jako OSM</text>
  <line x1="{PX+220}" y1="{ly2-5}" x2="{PX+250}" y2="{ly2-5}" stroke="#0f172a" stroke-width="3" stroke-dasharray="6,4"/>
  <text x="{PX+256}" y="{ly2-1}" fill="#64748b" font-size="10.5" font-weight="700">Čárkovaná = orientační / plán</text>
  <line x1="{PX+14}" y1="{MAP_Y+164}" x2="{PX+PW-14}" y2="{MAP_Y+164}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    row_y = MAP_Y + 180
    for f in gj["features"]:
        p = f["properties"]
        rid = p["id"]
        col = p.get("stroke") or CATEGORY_COLORS.get(p.get("category"), "#2563eb")
        is_osm = p.get("presnost") == "OSM"
        badge_bg = "#dcfce7" if is_osm else "#fef3c7"
        badge_fg = "#166534" if is_osm else "#92400e"
        badge_txt = "OSM v datech" if is_osm else "Orientační / plán"

        svg.append(f'  <circle cx="{PX+26}" cy="{row_y-2}" r="10" fill="{col}"/>')
        svg.append(f'  <text x="{PX+26}" y="{row_y+2}" fill="#ffffff" font-size="9.5" font-weight="800" text-anchor="middle">{rid}</text>')
        clean_name = p["name"].replace(f"#{rid} ", "")
        if len(clean_name) > 36:
            clean_name = clean_name[:34] + "…"
        from_to = f"{p['odkud_A']} → {p['kam_B']}"
        if len(from_to) > 42:
            from_to = from_to[:40] + "…"

        svg.append(f'  <text x="{PX+44}" y="{row_y-4}" fill="#0f172a" font-size="10.2" font-weight="800">{clean_name}</text>')
        svg.append(f'  <text x="{PX+44}" y="{row_y+8}" fill="#475569" font-size="9.2" font-weight="600">{from_to}</text>')

        svg.append(f'  <rect x="{PX+PW-106}" y="{row_y-13}" width="92" height="18" rx="5" fill="{badge_bg}"/>')
        svg.append(f'  <text x="{PX+PW-60}" y="{row_y-1}" fill="{badge_fg}" font-size="9.2" font-weight="800" text-anchor="middle">{badge_txt}</text>')
        row_y += 34

    BY = MAP_Y + MAP_H + 16
    svg.append(f'''
  <rect x="24" y="{BY}" width="{W-48}" height="102" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#regShadow)"/>
  <text x="48" y="{BY+28}" fill="#0f172a" font-size="14" font-weight="800">METODICKÁ POZNÁMKA:</text>
  <text x="48" y="{BY+50}" fill="#334155" font-size="12.5" font-weight="600">Styl čáry přebírá označení z dat aplikace; není potvrzením dokončení ani veřejné přístupnosti projektu.</text>
  <text x="48" y="{BY+71}" fill="#334155" font-size="12.5" font-weight="600">Geometrie slouží k orientační lokalizaci. Před navigací ověřte trasu v terénu a v primárním zdroji.</text>
  <text x="48" y="{BY+90}" fill="#64748b" font-size="11" font-weight="600">Podklad: © OpenStreetMap contributors • https://www.openstreetmap.org/copyright</text>
</svg>''')

    svg_path = os.path.join(MAP_DIR, "mapa_stezky_podle_roku.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated {os.path.basename(svg_path)}")
    render_svg_to_png(svg_path, W, H)

if __name__ == "__main__":
    write_geojson()
    generate_regional_map()
