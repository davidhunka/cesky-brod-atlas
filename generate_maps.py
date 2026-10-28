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

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(OUT_DIR, "tile_cache")

YEAR_COLORS = {
    "2020–2021": "#2563eb",
    "2022–2023": "#0d9488",
    "2024":      "#16a34a",
    "2025":      "#ea580c",
    "2026":      "#db2777",
    "Plán 2026+": "#7c3aed"
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
    with open(os.path.join(OUT_DIR, "trasy_ceskobrodsko.geojson"), "r", encoding="utf-8") as f:
        return json.load(f)

def render_svg_to_png(svg_path, width=1920, height=1280):
    png_path = svg_path.replace(".svg", ".png")
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
    browser = next((b for b in chrome_candidates if os.path.exists(b)), None)
    if not browser:
        print("Warning: No headless browser found for PNG rendering.")
        return
    file_url = "file:///" + os.path.abspath(svg_path).replace("\\", "/")
    subprocess.run([
        browser,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        file_url
    ], check=True)
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
  <text x="48" y="72" fill="#94a3b8" font-size="13.5" font-weight="600">Reálný mapový podklad OpenStreetMap (Zoom 13) • 13 tras ověřeno v OSM (plná čára) • 12 tras orientačních/v přípravě (čárkovaná čára)</text>

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
        col = p.get("stroke") or YEAR_COLORS.get(p.get("rok_obnovy"), "#2563eb")
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
    reg_callouts = [
        (7, 105, -45, "Mlýnská cesta C6 (1,3 km asfalt)", "Tuklaty / Tlustovousy → Břežany II"),
        (6, -15, -46, "Polní cesta P6 Rostoklaty", "Rostoklaty → směr Břežany II / Štolmíř"),
        (23, 85, -56, "Obnovená NS Klepec (říjen 2026)", "Skřivany → vrch Klepec (358 m)"),
        (22, -35, 62, "Mrzecká cesta a alej (2026)", "Limuzy → Mrzky (1,6 km)"),
        (21, -40, -64, "Hravá NS Ekocentrum Vrátkov", "Západní okraj Tuchorazi → Vrátkov"),
        (19, 155, -10, "Šemberské stezky (Singletraily)", "5 km lesních MTB trailů u Tuchorazi"),
        (20, 155, 36, "Nová lávka u Skautské louky", "Na Šamtalech → Skautská louka → Na Zámkách"),
        (15, 0, -46, "Cesta C4 + Kočárová KZ 7 (2025)", "Chrášťany → Chotouň (1,8 km)"),
        (12, -125, -28, "Kudrnáčova stezka (2022–26)", "Klučov → hradiště → Poříčany"),
        (13, 15, 44, "Alej „Žherák“ (Klučov–Žhery)", "Klučov → Žhery (1,4 km)"),
        (14, -105, -44, "Polní cesta Skramníky–Tatce", "Obnovený úsek cesty (březen 2024)")
    ]

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
        col = f["properties"].get("stroke") or YEAR_COLORS.get(f["properties"].get("rok_obnovy"), "#2563eb")
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
            col = f["properties"].get("stroke") or YEAR_COLORS.get(f["properties"].get("rok_obnovy"), "#2563eb")
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
  <text x="{PX+18}" y="{MAP_Y+30}" fill="#0f172a" font-size="16" font-weight="900">SEZNAM VŠECH 25 TRAS (ODKUD → KAM &amp; STAV)</text>
  <text x="{PX+18}" y="{MAP_Y+48}" fill="#64748b" font-size="11" font-weight="600">Číslo odpovídá značce v mapě • Rozlišení ověřených a orientačních tras</text>
  <line x1="{PX+14}" y1="{MAP_Y+58}" x2="{PX+PW-14}" y2="{MAP_Y+58}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    # Legenda roků
    ly = MAP_Y + 76
    lx = PX + 16
    for ylabel, ycol in YEAR_COLORS.items():
        svg.append(f'  <rect x="{lx}" y="{ly-11}" width="12" height="12" rx="3" fill="{ycol}"/>')
        svg.append(f'  <text x="{lx+16}" y="{ly-1}" fill="#1e293b" font-size="10.5" font-weight="700">{ylabel}</text>')
        lx += 70 if len(ylabel) < 6 else 96

    # Legenda stylu čáry
    ly2 = MAP_Y + 98
    svg.append(f'''
  <line x1="{PX+16}" y1="{ly2-5}" x2="{PX+46}" y2="{ly2-5}" stroke="#0f172a" stroke-width="4"/>
  <text x="{PX+52}" y="{ly2-1}" fill="#0f172a" font-size="10.5" font-weight="800">Plná čára = Ověřeno v OSM (13)</text>
  <line x1="{PX+220}" y1="{ly2-5}" x2="{PX+250}" y2="{ly2-5}" stroke="#0f172a" stroke-width="3" stroke-dasharray="6,4"/>
  <text x="{PX+256}" y="{ly2-1}" fill="#64748b" font-size="10.5" font-weight="700">Čárkovaná = Orientační / plán (12)</text>
  <line x1="{PX+14}" y1="{MAP_Y+108}" x2="{PX+PW-14}" y2="{MAP_Y+108}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    row_y = MAP_Y + 128
    for f in gj["features"]:
        p = f["properties"]
        rid = p["id"]
        col = p.get("stroke") or YEAR_COLORS.get(p.get("rok_obnovy"), "#2563eb")
        is_osm = p.get("presnost") == "OSM"
        badge_bg = "#dcfce7" if is_osm else "#fef3c7"
        badge_fg = "#166534" if is_osm else "#92400e"
        badge_txt = "✅ OSM ověřeno" if is_osm else "⚠️ Orientační"

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
        row_y += 36.4

    BY = MAP_Y + MAP_H + 16
    svg.append(f'''
  <rect x="24" y="{BY}" width="{W-48}" height="102" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#regShadow)"/>
  <text x="48" y="{BY+28}" fill="#0f172a" font-size="14" font-weight="800">SHRNUTÍ METADAT A PŘESNOSTI TRAS:</text>
  <text x="48" y="{BY+50}" fill="#166534" font-size="12.5" font-weight="700">✅ 13 TRAS OVĚŘENO V SÍTI OPENSTREETMAP (plná čára): <tspan fill="#334155" font-weight="500">P3 Na Útulně, HPC 4, Topolovka, Stezka B. Jedličky-Brodského, Alej do Klučova, Kudrnáčova stezka, Šemberské singletraily, Lávka u Skautské louky, Mrzecká cesta, NS Klepec a opravené chodníky.</tspan></text>
  <text x="48" y="{BY+71}" fill="#92400e" font-size="12.5" font-weight="700">⚠️ 12 TRAS ORIENTAČNÍCH / V PŘÍPRAVĚ (čárkovaná čára): <tspan fill="#334155" font-weight="500">P9 Mexiko, LBK 14 Štolmířský potok, P6 Rostoklaty, C6 Mlýnská cesta, alej u hřbitova, Skramníky–Tatce, C4 Chrášťany, Ekocentrum Vrátkov, cyklostezky do Přistoupimi a Štolmíře.</tspan></text>
  <text x="48" y="{BY+90}" fill="#64748b" font-size="11" font-weight="600">Interaktivní verze s možností libovolného zoomu a přepínání vrstev: https://davidhunka.github.io/cesky-brod-atlas/</text>
</svg>''')

    svg_path = os.path.join(OUT_DIR, "mapa_stezky_podle_roku.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated {os.path.basename(svg_path)}")
    render_svg_to_png(svg_path, W, H)

def sync_html():
    gj = load_geojson()
    html_path = os.path.join(OUT_DIR, "index.html")
    if not os.path.exists(html_path):
        return

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Build updated JS ROUTES array
    routes_js_items = []
    for f in gj["features"]:
        p = f["properties"]
        rid = p["id"]
        geom = f["geometry"]
        is_osm = p.get("presnost") == "OSM"
        
        # Coords for leaflet: [lat, lon]
        if geom["type"] == "MultiLineString":
            coords = [[[round(lat, 5), round(lon, 5)] for lon, lat in seg] for seg in geom["coordinates"]]
            mid_seg = coords[len(coords) // 2]
            center = mid_seg[len(mid_seg) // 2]
        else:
            coords = [[round(lat, 5), round(lon, 5)] for lon, lat in geom["coordinates"]]
            center = coords[len(coords) // 2]

        item = {
            "id": rid,
            "name": p["name"].replace(f"#{rid} ", ""),
            "yearCat": p.get("rok_obnovy", "2024"),
            "yearExact": p.get("rok_obnovy", "2024"),
            "category": "stezka",
            "fromTo": f"{p['odkud_A']} → {p['kam_B']}",
            "lengthSurface": p.get("delka_povrch", ""),
            "suitableFor": "Pěší, rodiny s dětmi, kolo",
            "mapyStatus": p.get("mapy_cz_stav", "ANO"),
            "mapyNote": "Ověřeno v OpenStreetMap" if is_osm else "Orientační průběh / v přípravě",
            "coords": coords,
            "center": center,
            "fromLabel": p.get("odkud_A", ""),
            "toLabel": p.get("kam_B", ""),
            "gmapsDirUrl": p.get("google_maps_trasa_A_B", ""),
            "mapyStartUrl": p.get("mapy_cz_start_A", ""),
            "mapyEndUrl": p.get("mapy_cz_cil_B", ""),
            "dashed": not is_osm
        }
        routes_js_items.append(item)

    routes_json = json.dumps(routes_js_items, ensure_ascii=False, indent=2)

    # Replace const ROUTES = [...] in index.html
    pattern = r"const ROUTES = \[.*?\];\n\n    // Sídla"
    replacement = f"const ROUTES = {routes_json};\n\n    // Sídla"
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html with real route geometries")

if __name__ == "__main__":
    generate_regional_map()
    sync_html()
