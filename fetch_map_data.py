#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stáhne mapové dlaždice (OpenStreetMap podklad) pro:
1. Detailní mapu Českého Brodu a okolí (Štolmíř, Liblice, Přistoupim, Kutilka, Podviňák) – Zoom 15
2. Přehledovou mapu celého Českobrodska (Tuklaty, Klepec, Tuchoraz/Šembera, Klučov, Chrášťany) – Zoom 13
A zároveň stáhne přesné geometrie tras po cestách z OSRM (OpenStreetMap routing), aby zakreslené stezky
na 100 % kopírovaly reálné cesty v mapovém podkladu.
"""

import os
import json
import math
import time
import base64
import urllib.request

CACHE_DIR = "/Users/david.hunka/.gemini/antigravity/scratch/cesky-brod-atlas/tile_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "CeskyBrodAtlasApp/1.0 (local educational cartography project)"
}


def latlon_to_tile_float(lat, lon, zoom):
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    ytile = (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    return xtile, ytile


def fetch_tile_b64(z, x, y):
    path = os.path.join(CACHE_DIR, f"tile_{z}_{x}_{y}.png")
    if os.path.exists(path) and os.path.getsize(path) > 100:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")

    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    with open(path, "wb") as f:
        f.write(data)
    time.sleep(0.08)
    return base64.b64encode(data).decode("ascii")


def download_grid(name, zoom, lat_min, lat_max, lon_min, lon_max):
    x_min_f, y_max_f = latlon_to_tile_float(lat_min, lon_min, zoom)
    x_max_f, y_min_f = latlon_to_tile_float(lat_max, lon_max, zoom)

    x0, x1 = int(math.floor(x_min_f)), int(math.floor(x_max_f))
    y0, y1 = int(math.floor(y_min_f)), int(math.floor(y_max_f))

    tiles = []
    print(f"[{name}] Zoom {zoom}: tiles X={x0}..{x1} ({x1-x0+1}), Y={y0}..{y1} ({y1-y0+1})")
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            b64 = fetch_tile_b64(zoom, tx, ty)
            tiles.append({
                "tx": tx,
                "ty": ty,
                "px": (tx - x0) * 256,
                "py": (ty - y0) * 256,
                "b64": b64
            })

    meta = {
        "name": name,
        "zoom": zoom,
        "x0": x0,
        "y0": y0,
        "cols": x1 - x0 + 1,
        "rows": y1 - y0 + 1,
        "width": (x1 - x0 + 1) * 256,
        "height": (y1 - y0 + 1) * 256,
        "tiles": tiles
    }
    out_json = os.path.join(CACHE_DIR, f"grid_{name}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(meta, f)
    print(f"Saved {out_json} ({meta['width']}x{meta['height']} px)")


# Definice klíčových bodů (Start -> průjezdní body -> Cíl) pro 25 tras
RAW_ROUTES = [
    (1, "Polní cesta P9 (Štolmíř – ČB Mexiko)", [(50.0836, 14.8442), (50.0837, 14.8525), (50.0815, 14.8618)], True),
    (2, "Hlavní polní cesta HPC 4 (Štolmíř – směr Břežany II)", [(50.0838, 14.8398), (50.0865, 14.8385), (50.0888, 14.8350)], True),
    (3, "Polní cesta P3 + mokřad Na Útulně (V Lukách – Štolmíř)", [(50.0792, 14.8538), (50.0804, 14.8490), (50.0816, 14.8442)], True),
    (4, "Přírodní cesta a alej Topolovka (ČB – Štolmíř)", [(50.0782, 14.8512), (50.0802, 14.8465), (50.0821, 14.8422)], True),
    (5, "Biokoridor LBK 14 Štolmířský potok", [(50.0772, 14.8350), (50.0815, 14.8400), (50.0860, 14.8485), (50.0910, 14.8580)], False),
    (6, "Polní cesta P6 (Rostoklaty – Ovocná stezka)", [(50.0762, 14.8135), (50.0785, 14.8225), (50.0808, 14.8315)], True),
    (7, "Mlýnská cesta C6 (Tlustovousy / Tuklaty – Břežany II)", [(50.0955, 14.7735), (50.0942, 14.7820), (50.0928, 14.7925)], True),
    (8, "Stezka B. Jedličky-Brodského (Podskalí – sv. Gothard – Liblice)", [(50.0713, 14.8632), (50.0722, 14.8715), (50.0745, 14.8812)], True),
    (9, "Cyklostezka pravý břeh Šembery (Havlíčkova – Pod Malechovem)", [(50.0701, 14.8595), (50.0705, 14.8618), (50.0709, 14.8638)], False),
    (10, "Nová lipová alej u hřbitova (Klučovská / Kounická)", [(50.0781, 14.8662), (50.0799, 14.8690)], True),
    (11, "Obnovená polní cesta a Alej do Klučova", [(50.0815, 14.8720), (50.0875, 14.8850), (50.0938, 14.8985)], True),
    (12, "Kudrnáčova stezka a aleje Klučov – Poříčany", [(50.0940, 14.8990), (50.0972, 14.8965), (50.1002, 14.9105)], True),
    (13, "Alej „Žherák“ (Klučov – Žhery)", [(50.0922, 14.9020), (50.0870, 14.9120), (50.0838, 14.9205)], True),
    (14, "Obnovená polní cesta Skramníky – Tatce", [(50.0820, 14.9495), (50.0820, 14.9585)], False),
    (15, "Polní cesta C4 a Kočárová cesta KZ 7 (Chrášťany – Chotouň)", [(50.0585, 14.9250), (50.0555, 14.9365), (50.0525, 14.9480)], True),
    (16, "Stezka pro pěší a cyklisty ČB (Nad Malechovem) – Přistoupim", [(50.0648, 14.8698), (50.0620, 14.8728), (50.0595, 14.8755)], False),
    (17, "Stezka pro pěší a cyklisty ČB – Štolmíř (podél silnice II/245)", [(50.0758, 14.8475), (50.0785, 14.8435), (50.0808, 14.8398)], False),
    (18, "Stezka kolem areálu Na Kutilce k rybníku Podviňák", [(50.0675, 14.8568), (50.0658, 14.8560), (50.0642, 14.8552)], True),
    (19, "Šemberské stezky – lesní singletraily u Tuchorazi", [(50.0445, 14.8590), (50.0410, 14.8530), (50.0385, 14.8485), (50.0425, 14.8475), (50.0445, 14.8590)], False),
    (20, "Údolí Šembery: Na Šamtalech – Nová lávka u Skautské louky – Na Zámkách", [(50.0445, 14.8535), (50.0365, 14.8460), (50.0255, 14.8325)], True),
    (21, "Hravá naučná stezka do Ekocentra Vrátkov", [(50.0480, 14.8480), (50.0465, 14.8430), (50.0450, 14.8385)], True),
    (22, "Mrzecká cesta a alej (Limuzy – Mrzky)", [(50.0595, 14.8125), (50.0578, 14.8225), (50.0560, 14.8325)], True),
    (23, "Kompletně obnovená Naučná stezka Klepec (Skřivany – vrch Klepec)", [(50.0520, 14.7745), (50.0558, 14.7795), (50.0575, 14.7860)], True),
    (24, "Opravené chodníky 2024–2026 (Štolmířská – B. Němcové – Masarykova)", [(50.0757, 14.8478), (50.0748, 14.8548), (50.0736, 14.8615)], True),
    (25, "Opravené chodníky 2020–2023 (Palackého – Jugoslávská – Krále Jiřího)", [(50.0715, 14.8540), (50.0688, 14.8590), (50.0702, 14.8642)], True),
]


def fetch_routed_geometries():
    out_file = os.path.join(CACHE_DIR, "routed_paths.json")
    routed = {}
    for rid, name, pts, use_osrm in RAW_ROUTES:
        if use_osrm:
            coord_str = ";".join(f"{lon:.5f},{lat:.5f}" for lat, lon in pts)
            url = f"https://router.project-osrm.org/route/v1/foot/{coord_str}?overview=full&geometries=geojson"
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if data.get("code") == "Ok" and data.get("routes"):
                    coords_lonlat = data["routes"][0]["geometry"]["coordinates"]
                    routed[str(rid)] = [[round(lat, 5), round(lon, 5)] for lon, lat in coords_lonlat]
                    print(f"Route #{rid}: OSRM geometry ({len(routed[str(rid)])} pts)")
                    time.sleep(0.1)
                    continue
            except Exception as e:
                print(f"Route #{rid} OSRM fallback: {e}")
        routed[str(rid)] = [[lat, lon] for lat, lon in pts]

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(routed, f)
    print(f"Saved routed geometries to {out_file}")


if __name__ == "__main__":
    # 1. Detailní výřez: Český Brod, Štolmíř, Liblice, Přistoupim, Na Kutilce (Zoom 15)
    download_grid("detail_cb", 15, 50.058, 50.088, 14.834, 14.892)
    # 2. Přehledový výřez celého Českobrodska (Zoom 13)
    download_grid("overview_region", 13, 50.024, 50.100, 14.770, 14.958)
    # 3. Přesné geometrie tras z OSM
    fetch_routed_geometries()
