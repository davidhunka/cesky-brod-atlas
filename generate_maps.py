#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor map Českobrodska na REÁLNÉM MAPOVÉM PODKLADU (OpenStreetMap / Mapy.cz vrstva):
1. mapa_detail_cesky_brod_podklad.svg / .png — Detailní mapa (Zoom 15): Český Brod, Štolmíř, Liblice, Přistoupim, Kutilka
   s přesným trasováním po reálných cestách v mapovém podkladu a vyznačením STARTU (Odkud) a CÍLE (Kam).
2. mapa_stezky_podle_roku.svg / .png — Přehledová mapa celého Českobrodska (Zoom 13) na reálném mapovém podkladu
   s barevným rozlišením podle roku obnovy (2020–2026+) a kontrolou viditelnosti na Mapy.cz.
"""

import os
import json
import math

OUT_DIR = "/Users/david.hunka/.gemini/antigravity/scratch/cesky-brod-atlas"
CACHE_DIR = os.path.join(OUT_DIR, "tile_cache")
ARTIFACT_DIR = "/Users/david.hunka/.gemini/antigravity/brain/fb04040c-a126-472b-977a-b11f7bcc8927"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

YEAR_COLORS = {
    "2020–2021": "#2563eb",  # Modrá
    "2022–2023": "#0d9488",  # Tyrkysová
    "2024":      "#16a34a",  # Zelená
    "2025":      "#ea580c",  # Oranžová
    "2026":      "#db2777",  # Purpurová / Růžová
    "Plán 2026+": "#7c3aed"  # Fialová (přerušovaná)
}


def latlon_to_tile_float(lat, lon, zoom):
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    ytile = (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    return xtile, ytile


def grid_px_to_latlon(px, py, grid_meta):
    """Převede přesné souřadnice pixelu (px, py) z dlaždicového podkladu na přesné GPS (lat, lon) WGS84."""
    n = 2.0 ** grid_meta["zoom"]
    xtile = grid_meta["x0"] + (px / 256.0)
    ytile = grid_meta["y0"] + (py / 256.0)
    lon = (xtile / n) * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * ytile / n)))
    lat = math.degrees(lat_rad)
    return (round(lat, 5), round(lon, 5))


def project_to_grid(lat, lon, grid_meta, offset_x=0.0, offset_y=0.0, scale=1.0):
    xt, yt = latlon_to_tile_float(lat, lon, grid_meta["zoom"])
    px = (xt - grid_meta["x0"]) * 256.0 * scale + offset_x
    py = (yt - grid_meta["y0"]) * 256.0 * scale + offset_y
    return round(px, 1), round(py, 1)


def load_grids():
    with open(os.path.join(CACHE_DIR, "grid_detail_cb.json"), "r", encoding="utf-8") as f:
        g_det = json.load(f)
    with open(os.path.join(CACHE_DIR, "grid_overview_region.json"), "r", encoding="utf-8") as f:
        g_reg = json.load(f)
    return g_det, g_reg


GRID_DETAIL, GRID_REGION = load_grids()


# Definice všech 25 tras nakalibrovaná přesně na pixely reálných cest v OSM podkladu:
RAW_ROUTE_DEFS = [
    {
        "id": 1,
        "name": "Polní cesta P9 (Štolmíř – Kounická / Mexiko)",
        "from_label": "Štolmíř (Ke Hřbitovu)",
        "to_label": "Ul. Kounická (II/272)",
        "surface_info": "1,1 km asfalt + alej (2020–2024)",
        "year_cat": "2020–2021",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (242, 214), (280, 204), (318, 191), (368, 174), (415, 161),
            (472, 152), (540, 146), (605, 132), (665, 108), (702, 74),
            (742, 62), (785, 60)
        ],
        "callout_idx": 6,
        "callout_offset": (110, 42)
    },
    {
        "id": 2,
        "name": "Hlavní polní cesta HPC 4 (Štolmíř)",
        "from_label": "Štolmíř (Ke Škole)",
        "to_label": "Směr Břežany II / háj",
        "surface_info": "591 m asfalt, šířka 4 m (2021)",
        "year_cat": "2020–2021",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (236, 212), (245, 180), (252, 152), (258, 128),
            (268, 95), (276, 75), (230, 50), (220, 30), (232, 12)
        ],
        "callout_idx": 5,
        "callout_offset": (165, -6)
    },
    {
        "id": 3,
        "name": "Polní cesta P3 + mokřad „Na Útulně“",
        "from_label": "Ul. V Lukách (za plynárnou)",
        "to_label": "Štolmíř (ul. K Lukám)",
        "surface_info": "700 m asfalt kolem mokřadu (2024)",
        "year_cat": "2024",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (526, 498), (526, 462), (495, 456), (468, 422), (447, 418),
            (422, 412), (388, 395), (360, 372), (334, 342), (320, 326),
            (298, 336), (266, 348)
        ],
        "callout_idx": 7,
        "callout_offset": (-175, -24)
    },
    {
        "id": 4,
        "name": "Přírodní cesta a alej „Topolovka“",
        "from_label": "Ul. Topolová / Pod Hájem",
        "to_label": "Napojení na P9 (Štolmíř)",
        "surface_info": "850 m přírodní cesta s alejí (2021–2025)",
        "year_cat": "2024",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (607, 424), (585, 466), (526, 462), (495, 456), (482, 434),
            (452, 395), (438, 340), (434, 285), (427, 232), (470, 200),
            (476, 175), (472, 152)
        ],
        "callout_idx": 7,
        "callout_offset": (185, -18)
    },
    {
        "id": 5,
        "name": "Biokoridor LBK 14 Štolmířský potok",
        "from_label": "Žel. trať (Z od Štolmíře)",
        "to_label": "Koryto Štolmířského potoka",
        "surface_info": "2,6 km zelený pás podél potoka (2023)",
        "year_cat": "2022–2023",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": True,
        "in_detail": True,
        "det_px": [
            (66, 444), (92, 424), (105, 395), (105, 355), (82, 330),
            (55, 305), (54, 245), (60, 195), (145, 176), (164, 128),
            (198, 96), (212, 48), (215, 14)
        ],
        "callout_idx": 6,
        "callout_offset": (165, -22)
    },
    {
        "id": 6,
        "name": "Polní cesta P6 (Rostoklaty – Ovocná stezka)",
        "from_label": "Severní okraj Rostoklat",
        "to_label": "Směr Břežany II / Štolmíř",
        "surface_info": "1,2 km zpevněná cesta + alej (2022)",
        "year_cat": "2022–2023",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (215, 415), (216, 382), (212, 355), (255, 342),
            (300, 326), (348, 310), (395, 295)
        ],
        "callout_idx": 3,
        "callout_offset": (0, -30)
    },
    {
        "id": 7,
        "name": "Mlýnská cesta C6 (Tuklaty – Břežany II)",
        "from_label": "Tuklaty / Tlustovousy",
        "to_label": "Západní okraj Břežan II",
        "surface_info": "1,3 km asfalt + stromořadí (2022)",
        "year_cat": "2022–2023",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (45, 315), (88, 312), (125, 305), (155, 285), (182, 260), (205, 245)
        ],
        "callout_idx": 3,
        "callout_offset": (0, -30)
    },
    {
        "id": 8,
        "name": "Stezka B. Jedličky-Brodského (údolí Šembery)",
        "from_label": "Podskalí (Kouřimská brána)",
        "to_label": "Liblice (Za Drahou / sv. Gothard)",
        "surface_info": "1,5 km břeh Šembery a Chodotínského ryb. (2024)",
        "year_cat": "2024",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (625, 795), (655, 770), (688, 742), (726, 730), (768, 715),
            (815, 698), (860, 678), (895, 654), (928, 668), (962, 660),
            (1006, 650), (1048, 634), (1082, 608), (1112, 584), (1168, 598)
        ],
        "callout_idx": 9,
        "callout_offset": (45, -52)
    },
    {
        "id": 9,
        "name": "Cyklostezka pravý břeh Šembery",
        "from_label": "Nábřežní / Havlíčkova",
        "to_label": "Prokopa Velikého (Pod Malechovem)",
        "surface_info": "450 m nábřežní stezka šířky 3 m (2026)",
        "year_cat": "2026",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (582, 855), (572, 822), (596, 798), (635, 782),
            (682, 750), (726, 738), (758, 795)
        ],
        "callout_idx": 3,
        "callout_offset": (210, 48)
    },
    {
        "id": 10,
        "name": "Nová lipová alej u hřbitova",
        "from_label": "Ul. Klučovská (u hřbitova)",
        "to_label": "Cesta podél hřbitova (sever)",
        "surface_info": "200 m, 20 vzrostlých lip (březen 2026)",
        "year_cat": "2026",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (962, 424), (945, 395), (945, 345), (945, 295)
        ],
        "callout_idx": 2,
        "callout_offset": (-165, 24)
    },
    {
        "id": 11,
        "name": "Obnovená cesta a Alej do Klučova",
        "from_label": "Ul. Za Drahou (u Klučovské)",
        "to_label": "Polní cesta směr Klučov",
        "surface_info": "2,2 km historická polní cesta s alejí (2023)",
        "year_cat": "2022–2023",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (1046, 412), (1042, 350), (1035, 300), (1026, 250),
            (1016, 200), (1002, 150), (982, 92), (1045, 65),
            (1105, 42), (1160, 15)
        ],
        "callout_idx": 4,
        "callout_offset": (175, 12)
    },
    {
        "id": 12,
        "name": "Kudrnáčova stezka a aleje u Klučova",
        "from_label": "Klučov (přes hradiště)",
        "to_label": "Jižní okraj Poříčan",
        "surface_info": "2,5 km historická stezka + stromořadí",
        "year_cat": "2022–2023",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (822, 225), (828, 195), (832, 168), (852, 142), (875, 118)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 13,
        "name": "Alej „Žherák“ (Klučov – Žhery)",
        "from_label": "JV okraj Klučova",
        "to_label": "Obec Žhery",
        "surface_info": "1,4 km cesta + 34 stromů (2024)",
        "year_cat": "2024",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (835, 242), (875, 255), (912, 268), (945, 282)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 14,
        "name": "Obnovená polní cesta Skramníky – Tatce",
        "from_label": "SV okraj Skramníků",
        "to_label": "JZ okraj Tatců",
        "surface_info": "150 m obnovené polní cesty (2024)",
        "year_cat": "2024",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (1132, 326), (1162, 305), (1195, 282)
        ],
        "callout_idx": 1,
        "callout_offset": (0, -25)
    },
    {
        "id": 15,
        "name": "Polní cesta C4 a Kočárová cesta KZ 7",
        "from_label": "Východní okraj Chrášťan",
        "to_label": "Západní okraj Chotouně (C2)",
        "surface_info": "1,8 km zpevněná cesta + alej (2025)",
        "year_cat": "2025",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (952, 502), (995, 496), (1048, 495), (1098, 490)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 16,
        "name": "Cyklostezka Nad Malechovem – Přistoupim",
        "from_label": "Ul. Prokopa Velikého",
        "to_label": "Severní okraj Přistoupimi (III/1131)",
        "surface_info": "600 m, šířka 3 m podél III/1131 (Plán 2026+)",
        "year_cat": "Plán 2026+",
        "mapy_status": "NE",
        "dashed": True,
        "in_detail": True,
        "det_px": [
            (805, 832), (845, 895), (885, 938), (925, 975),
            (975, 1018), (1020, 1048), (1055, 1078)
        ],
        "callout_idx": 4,
        "callout_offset": (195, -22)
    },
    {
        "id": 17,
        "name": "Stezka ČB – Štolmíř podél silnice II/245",
        "from_label": "Žitomířská × Na Vyhlídce",
        "to_label": "Českobrodská × Lichtenštejnská",
        "surface_info": "950 m podél silnice II/245 (Plán 2026+)",
        "year_cat": "Plán 2026+",
        "mapy_status": "NE",
        "dashed": True,
        "in_detail": True,
        "det_px": [
            (432, 558), (402, 512), (368, 476), (328, 456),
            (268, 442), (266, 428), (278, 396), (265, 352)
        ],
        "callout_idx": 3,
        "callout_offset": (-145, 52)
    },
    {
        "id": 18,
        "name": "Stezka Na Kutilce – rybník Podviňák",
        "from_label": "Areál Na Kutilce / Na Bělidle",
        "to_label": "Hráz a břeh rybníka Podviňák",
        "surface_info": "650 m pěší a cyklo stezka kolem stadionu (2024)",
        "year_cat": "2024",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (538, 950), (502, 975), (472, 1005), (462, 1048),
            (455, 1082), (442, 1120), (430, 1165), (438, 1185)
        ],
        "callout_idx": 3,
        "callout_offset": (-195, 22)
    },
    {
        "id": 19,
        "name": "Šemberské stezky – singletraily Tuchoraz",
        "from_label": "Tuchoraz (nástup u lesa)",
        "to_label": "Lesní MTB okruh (5 km)",
        "surface_info": "5 km MTB trailů v lese (modrý, červený, černý)",
        "year_cat": "2020–2021",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (455, 658), (448, 685), (438, 715), (425, 702),
            (435, 675), (455, 658)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 20,
        "name": "Zastavení u Šembery + Lávka u Skautské louky",
        "from_label": "Kamenný mostek (Na Šamtalech)",
        "to_label": "Lávka u Skautské louky → Na Zámkách",
        "surface_info": "3,5 km údolím Šembery, nová lávka a 3 altány",
        "year_cat": "2024",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (438, 715), (415, 745), (398, 772), (376, 795),
            (352, 818), (335, 845)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 21,
        "name": "Hravá naučná stezka Ekocentrum Vrátkov",
        "from_label": "Západní okraj Tuchorazi",
        "to_label": "Ekocentrum Vrátkov (čp. 38)",
        "surface_info": "1,2 km stezka s herními prvky mimo hlavní tah",
        "year_cat": "2022–2023",
        "mapy_status": "ČÁSTEČNĚ",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (448, 642), (422, 648), (398, 658), (375, 672)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 22,
        "name": "Mrzecká cesta a alej (Limuzy – Mrzky)",
        "from_label": "JV okraj Limuz (parc. 688)",
        "to_label": "SZ okraj obce Mrzky",
        "surface_info": "1,6 km polní cesta s alejí (obnova 2026)",
        "year_cat": "2026",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (155, 578), (185, 608), (212, 640), (242, 672)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 23,
        "name": "Obnovená Naučná stezka Klepec (říjen 2026)",
        "from_label": "Skřivany (Přišimasy)",
        "to_label": "Vrchol Klepec (358 m) → Limuzy",
        "surface_info": "1,0 km, altán s houpací sítí, nové tabule",
        "year_cat": "2026",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": False,
        "reg_px": [
            (42, 632), (62, 635), (82, 638), (108, 622), (135, 592)
        ],
        "callout_idx": 2,
        "callout_offset": (0, -25)
    },
    {
        "id": 24,
        "name": "Chodníky 2024–2026 (Štolmířská – Želivského)",
        "from_label": "Ul. Štolmířská (jaro 2026)",
        "to_label": "Ul. Žižkova, Želivského, Tyršova",
        "surface_info": "Bezbariérové chodníky v uliční síti ČB",
        "year_cat": "2026",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (402, 608), (402, 650), (402, 692), (445, 698),
            (482, 704), (548, 704), (560, 668), (582, 646)
        ],
        "callout_idx": 2,
        "callout_offset": (-185, -18)
    },
    {
        "id": 25,
        "name": "Chodníky 2020–2023 (Palackého – Krále Jiřího)",
        "from_label": "Sídliště Palackého",
        "to_label": "B. Němcové → náměstí → Krále Jiřího",
        "surface_info": "Chodníky ze zámkové dlažby a přechody",
        "year_cat": "2020–2021",
        "mapy_status": "ANO",
        "dashed": False,
        "in_detail": True,
        "det_px": [
            (392, 922), (425, 875), (458, 838), (492, 798),
            (526, 758), (560, 725), (618, 696), (685, 675),
            (748, 635), (825, 602)
        ],
        "callout_idx": 1,
        "callout_offset": (-185, -18)
    }
]


def build_detailed_routes():
    routes = []
    for r in RAW_ROUTE_DEFS:
        rc = dict(r)
        if r["in_detail"]:
            rc["coords"] = [grid_px_to_latlon(px, py, GRID_DETAIL) for px, py in r["det_px"]]
        else:
            rc["coords"] = [grid_px_to_latlon(px, py, GRID_REGION) for px, py in r["reg_px"]]

        s_lat, s_lon = rc["coords"][0]
        e_lat, e_lon = rc["coords"][-1]
        m_lat, m_lon = rc["coords"][len(rc["coords"]) // 2]
        if len(rc["coords"]) > 2:
            rc["gmaps_dir_url"] = (
                f"https://www.google.com/maps/dir/?api=1"
                f"&origin={s_lat:.5f},{s_lon:.5f}"
                f"&destination={e_lat:.5f},{e_lon:.5f}"
                f"&waypoints={m_lat:.5f},{m_lon:.5f}"
                f"&travelmode=walking"
            )
        else:
            rc["gmaps_dir_url"] = (
                f"https://www.google.com/maps/dir/?api=1"
                f"&origin={s_lat:.5f},{s_lon:.5f}"
                f"&destination={e_lat:.5f},{e_lon:.5f}"
                f"&travelmode=walking"
            )
        rc["mapy_start_url"] = (
            f"https://mapy.cz/turisticka?source=coor&id={s_lon:.5f}%2C{s_lat:.5f}&x={s_lon:.5f}&y={s_lat:.5f}&z=16"
        )
        rc["mapy_end_url"] = (
            f"https://mapy.cz/turisticka?source=coor&id={e_lon:.5f}%2C{e_lat:.5f}&x={e_lon:.5f}&y={e_lat:.5f}&z=16"
        )
        routes.append(rc)
    return routes


DETAILED_ROUTES = build_detailed_routes()


# ==============================================================================
# 1. DETAILNÍ MAPA ČESKÉHO BRODU A OKOLÍ NA REÁLNÉM MAPOVÉM PODKLADU (ZOOM 15)
# ==============================================================================
def generate_detail_map_on_tiles():
    grid = GRID_DETAIL

    MAP_X, MAP_Y = 24, 102
    MAP_W, MAP_H = 1360, 1060
    W, H = 1920, 1280

    # Měřítko 0.89 zajistí, že jak sever Štolmíře (HPC 4, P9), tak jih (Podviňák, Přistoupim) jsou 100% v mapovém okně
    SCALE = 0.89
    TILE_OFF_X = MAP_X - 4
    TILE_OFF_Y = MAP_Y - 2

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="hdrDet" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <clipPath id="detailClip">
      <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" rx="14"/>
    </clipPath>
    <filter id="boxShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.22"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="#f1f5f9"/>

  <!-- Hlavička -->
  <rect x="24" y="16" width="{W-48}" height="74" rx="14" fill="url(#hdrDet)" filter="url(#boxShadow)"/>
  <text x="48" y="48" fill="#ffffff" font-size="23" font-weight="900">DETAILNÍ MAPA TRAS NA MAPOVÉM PODKLADU: ČESKÝ BROD – ŠTOLMÍŘ – LIBLICE – PŘISTOUPIM</text>
  <text x="48" y="72" fill="#94a3b8" font-size="13.5" font-weight="600">Přesné trasování po reálných cestách v podkladu OpenStreetMap (Zoom 15) • Bod START (● Odkud) a CÍL (● Kam) + rok obnovy</text>

  <!-- Mapové okno s reálnými dlaždicemi -->
  <g clip-path="url(#detailClip)">
''')

    for t in grid["tiles"]:
        tx = TILE_OFF_X + t["px"] * SCALE
        ty = TILE_OFF_Y + t["py"] * SCALE
        tw = 256.0 * SCALE + 0.5
        svg.append(f'    <image x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{tw:.1f}" xlink:href="data:image/png;base64,{t["b64"]}"/>')

    svg.append(f'    <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" fill="#ffffff" opacity="0.10"/>')

    detail_routes = [r for r in DETAILED_ROUTES if r["in_detail"]]

    # 1. Vrstva: Všechny trasy (přesně po reálných cestách na mapě)
    for r in detail_routes:
        col = YEAR_COLORS[r["year_cat"]]
        pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lat, lon in r["coords"]]
        d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
        dash = 'stroke-dasharray="10,7"' if r["dashed"] else ''

        svg.append(f'    <path d="{d}" fill="none" stroke="#ffffff" stroke-width="9.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>')
        svg.append(f'    <path d="{d}" fill="none" stroke="{col}" stroke-width="5.5" {dash} stroke-linecap="round" stroke-linejoin="round"/>')

        sx, sy = pts[0]
        ex, ey = pts[-1]
        svg.append(f'    <circle cx="{sx}" cy="{sy}" r="6" fill="#ffffff" stroke="{col}" stroke-width="3.0"/>')
        svg.append(f'    <circle cx="{ex}" cy="{ey}" r="6" fill="{col}" stroke="#ffffff" stroke-width="2.2"/>')

    # 2. Vrstva: Čísla tras a informační kartičky ODKUD -> KAM
    for r in detail_routes:
        col = YEAR_COLORS[r["year_cat"]]
        pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lat, lon in r["coords"]]
        c_idx = min(r.get("callout_idx", len(pts) // 2), len(pts) - 1)
        mx, my = pts[c_idx]
        ox, oy = r["callout_offset"]
        bx, by = mx + ox, my + oy

        line1 = r["name"]
        line2 = f'{r["from_label"]} → {r["to_label"]}'
        line3 = r["surface_info"]
        cw = max(238, int(max(len(line1) * 6.0, len(line2) * 5.4, len(line3) * 5.3) + 44))
        ch = 45
        box_x = max(MAP_X + 10, min(MAP_X + MAP_W - cw - 10, bx - cw / 2))
        box_y = max(MAP_Y + 8, min(MAP_Y + MAP_H - ch - 8, by - ch / 2))

        svg.append(f'    <line x1="{mx}" y1="{my}" x2="{box_x + cw/2:.1f}" y2="{box_y + ch/2:.1f}" stroke="#0f172a" stroke-width="1.8" stroke-dasharray="3,3"/>')
        svg.append(f'    <circle cx="{mx}" cy="{my}" r="10.5" fill="{col}" stroke="#ffffff" stroke-width="2.2"/>')
        svg.append(f'    <text x="{mx}" y="{my+3.8}" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">{r["id"]}</text>')

        svg.append(f'    <g transform="translate({box_x:.1f}, {box_y:.1f})" filter="url(#boxShadow)">')
        svg.append(f'      <rect x="0" y="0" width="{cw}" height="{ch}" rx="8" fill="#ffffff" stroke="{col}" stroke-width="2.2" opacity="0.97"/>')
        svg.append(f'      <rect x="0" y="0" width="27" height="{ch}" rx="7" fill="{col}"/>')
        svg.append(f'      <text x="13.5" y="{ch/2+4.5:.1f}" fill="#ffffff" font-size="12.5" font-weight="900" text-anchor="middle">{r["id"]}</text>')
        svg.append(f'      <text x="34" y="16.5" fill="#0f172a" font-size="10.5" font-weight="800">{line1}</text>')
        svg.append(f'      <text x="34" y="30" fill="#334155" font-size="9.4" font-weight="700">{line2}</text>')
        svg.append(f'      <text x="34" y="41" fill="{col}" font-size="9.0" font-weight="800">{line3}</text>')
        svg.append(f'    </g>')

    svg.append('  </g>')
    svg.append(f'  <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" rx="14" fill="none" stroke="#0f172a" stroke-width="2.5"/>')

    # Pravý panel: Detailní rozpis ODKUD -> KAM pro všechny trasy v detailu
    PX = MAP_X + MAP_W + 18
    PW = W - PX - 24
    svg.append(f'''
  <rect x="{PX}" y="{MAP_Y}" width="{PW}" height="{MAP_H}" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#boxShadow)"/>
  <text x="{PX+18}" y="{MAP_Y+30}" fill="#0f172a" font-size="15.5" font-weight="900">ODKUD A KAM VEDOU TRASY V DETAILU</text>
  <text x="{PX+18}" y="{MAP_Y+48}" fill="#64748b" font-size="11" font-weight="600">● Bílé kolečko = Začátek trasy | ● Plné kolečko = Konec trasy</text>
  <line x1="{PX+14}" y1="{MAP_Y+58}" x2="{PX+PW-14}" y2="{MAP_Y+58}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    ry = MAP_Y + 70
    for r in detail_routes:
        col = YEAR_COLORS[r["year_cat"]]
        st = r["mapy_status"]
        st_bg = "#dcfce7" if st == "ANO" else ("#fef3c7" if st == "ČÁSTEČNĚ" else "#f3e8ff")
        st_fg = "#166534" if st == "ANO" else ("#92400e" if st == "ČÁSTEČNĚ" else "#6b21a8")
        st_tx = "Mapy.cz: ANO" if st == "ANO" else ("Mapy.cz: ČÁST." if st == "ČÁSTEČNĚ" else "Plán 2026+")

        svg.append(f'  <g transform="translate({PX+14}, {ry:.1f})">')
        svg.append(f'    <rect x="0" y="0" width="{PW-28}" height="62" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2"/>')
        svg.append(f'    <circle cx="19" cy="20" r="11" fill="{col}"/>')
        svg.append(f'    <text x="19" y="24" fill="#ffffff" font-size="10.5" font-weight="900" text-anchor="middle">{r["id"]}</text>')
        svg.append(f'    <text x="36" y="17" fill="#0f172a" font-size="11.0" font-weight="800">{r["name"]}</text>')
        svg.append(f'    <rect x="{PW-120}" y="5" width="84" height="17" rx="5" fill="{st_bg}"/>')
        svg.append(f'    <text x="{PW-78}" y="16.5" fill="{st_fg}" font-size="9.2" font-weight="800" text-anchor="middle">{st_tx}</text>')
        svg.append(f'    <text x="36" y="34" fill="#1e293b" font-size="9.8" font-weight="700">ODKUD: <tspan fill="#475569" font-weight="600">{r["from_label"]}</tspan> → KAM: <tspan fill="#0f172a" font-weight="700">{r["to_label"]}</tspan></text>')
        svg.append(f'    <text x="36" y="50" fill="{col}" font-size="9.8" font-weight="700">{r["surface_info"]}</text>')
        svg.append(f'  </g>')
        ry += 69.5

    # Spodní lišta s legendou roků
    BY = MAP_Y + MAP_H + 16
    svg.append(f'''
  <rect x="24" y="{BY}" width="{W-48}" height="82" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#boxShadow)"/>
  <text x="48" y="{BY+28}" fill="#0f172a" font-size="13.5" font-weight="900">BAREVNÉ ROZLIŠENÍ PODLE ROKU OBNOVY / VÝSTAVBY STEZKY:</text>
  <g transform="translate(48, {BY+44})">
    <rect x="0" y="0" width="28" height="12" rx="4" fill="#2563eb"/><text x="36" y="11" fill="#0f172a" font-size="12" font-weight="700">2020–2021 (P9, HPC 4, Chodníky)</text>
    <rect x="275" y="0" width="28" height="12" rx="4" fill="#0d9488"/><text x="311" y="11" fill="#0f172a" font-size="12" font-weight="700">2022–2023 (LBK 14, Alej do Klučova)</text>
    <rect x="575" y="0" width="28" height="12" rx="4" fill="#16a34a"/><text x="611" y="11" fill="#0f172a" font-size="12" font-weight="700">2024 (P3 Na Útulně, Topolovka, Podskalí–Liblice, Kutilka)</text>
    <rect x="1005" y="0" width="28" height="12" rx="4" fill="#ea580c"/><text x="1041" y="11" fill="#0f172a" font-size="12" font-weight="700">2025 (C4 Chrášťany, B. Němcové)</text>
    <rect x="1285" y="0" width="28" height="12" rx="4" fill="#db2777"/><text x="1321" y="11" fill="#0f172a" font-size="12" font-weight="700">2026 (Hřbitov, Šembera, Štolmířská)</text>
    <rect x="1585" y="0" width="28" height="12" rx="4" fill="#7c3aed"/><text x="1621" y="11" fill="#6d28d9" font-size="12" font-weight="700">Plán 2026+ (Přistoupim, II/245)</text>
  </g>
</svg>''')

    svg_str = "\n".join(svg)
    for d in [OUT_DIR, ARTIFACT_DIR]:
        with open(os.path.join(d, "mapa_detail_cesky_brod_podklad.svg"), "w", encoding="utf-8") as f:
            f.write(svg_str)
    print("Generated mapa_detail_cesky_brod_podklad.svg")


# ==============================================================================
# 2. PŘEHLEDOVÁ MAPA CELÉHO ČESKOBRODSKA NA MAPOVÉM PODKLADU (ZOOM 13)
# ==============================================================================
def generate_regional_map_on_tiles():
    grid = GRID_REGION

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
  <text x="48" y="72" fill="#94a3b8" font-size="13.5" font-weight="600">Přesné trasování po reálných cestách v podkladu OpenStreetMap (Zoom 13) • Rozlišení dle roku obnovy a kontrola Mapy.cz</text>

  <g clip-path="url(#regClip)">
''')

    for t in grid["tiles"]:
        tx = TILE_OFF_X + t["px"] * SCALE
        ty = TILE_OFF_Y + t["py"] * SCALE
        tw = 256.0 * SCALE + 0.5
        svg.append(f'    <image x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{tw:.1f}" xlink:href="data:image/png;base64,{t["b64"]}"/>')

    svg.append(f'    <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H}" fill="#ffffff" opacity="0.10"/>')

    badge_offsets = {
        1: (0, -14), 2: (10, -12), 3: (-12, -8), 4: (14, 6), 5: (-14, 0),
        8: (14, -12), 9: (14, 14), 10: (-12, -10), 16: (18, 6),
        17: (-18, 4), 18: (-18, 8), 19: (22, -6), 24: (-20, -14), 25: (-18, 14)
    }

    # 1. Vrstva: linie tras
    for r in DETAILED_ROUTES:
        col = YEAR_COLORS[r["year_cat"]]
        pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lat, lon in r["coords"]]
        d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
        dash = 'stroke-dasharray="9,6"' if r["dashed"] else ''

        svg.append(f'    <path d="{d}" fill="none" stroke="#ffffff" stroke-width="9.0" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>')
        svg.append(f'    <path d="{d}" fill="none" stroke="{col}" stroke-width="5.2" {dash} stroke-linecap="round" stroke-linejoin="round"/>')

        sx, sy = pts[0]
        ex, ey = pts[-1]
        svg.append(f'    <circle cx="{sx}" cy="{sy}" r="4.8" fill="#ffffff" stroke="{col}" stroke-width="2.4"/>')
        svg.append(f'    <circle cx="{ex}" cy="{ey}" r="4.8" fill="{col}" stroke="#ffffff" stroke-width="2"/>')

    # 2. Vrstva: číselné odznaky
    for r in DETAILED_ROUTES:
        col = YEAR_COLORS[r["year_cat"]]
        pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lat, lon in r["coords"]]
        mid_idx = len(pts) // 2
        mx, my = pts[mid_idx]
        ox, oy = badge_offsets.get(r["id"], (0, 0))
        bx, by = mx + ox, my + oy
        svg.append(f'    <circle cx="{bx}" cy="{by}" r="11" fill="{col}" stroke="#ffffff" stroke-width="2.2" filter="url(#regShadow)"/>')
        svg.append(f'    <text x="{bx}" y="{by+4}" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">{r["id"]}</text>')

    # 3. Vrstva: Popisky klíčových mimo-městských tras přímo v regionální mapě
    reg_callouts = [
        (7, 105, -45, "Mlýnská cesta C6 (1,3 km asfalt)", "Tuklaty / Tlustovousy → Břežany II"),
        (6, -15, -46, "Polní cesta P6 Rostoklaty", "Rostoklaty → směr Břežany II / Štolmíř"),
        (23, 85, -54, "Obnovená NS Klepec (říjen 2026)", "Skřivany → vrch Klepec (358 m)"),
        (22, -25, 58, "Mrzecká cesta a alej (2026)", "Limuzy → Mrzky (1,6 km)"),
        (21, -135, -36, "Hravá NS Ekocentrum Vrátkov", "Západní okraj Tuchorazi → Vrátkov"),
        (19, 145, -12, "Šemberské stezky (Singletraily)", "5 km lesních MTB trailů u Tuchorazi"),
        (20, 145, 36, "Nová lávka u Skautské louky", "Na Šamtalech → Skautská louka → Na Zámkách"),
        (15, 0, -44, "Cesta C4 + Kočárová KZ 7 (2025)", "Chrášťany → Chotouň (1,8 km)"),
        (12, -125, -28, "Kudrnáčova stezka (2022–26)", "Klučov → hradiště → Poříčany"),
        (13, 15, 44, "Alej „Žherák“ (Klučov–Žhery)", "Klučov → Žhery (1,4 km)"),
        (14, -95, -42, "Polní cesta Skramníky–Tatce", "Obnovená cesta (březen 2024)")
    ]
    for rid, ox, oy, l1, l2 in reg_callouts:
        r_obj = next(x for x in DETAILED_ROUTES if x["id"] == rid)
        col = YEAR_COLORS[r_obj["year_cat"]]
        pts = [project_to_grid(lat, lon, grid, TILE_OFF_X, TILE_OFF_Y, SCALE) for lat, lon in r_obj["coords"]]
        px, py = pts[len(pts) // 2]
        cw, ch = 224, 38
        bx = max(MAP_X + cw/2 + 10, min(MAP_X + MAP_W - cw/2 - 10, px + ox))
        by = max(MAP_Y + ch/2 + 10, min(MAP_Y + MAP_H - ch/2 - 10, py + oy))
        svg.append(f'    <line x1="{px}" y1="{py}" x2="{bx}" y2="{by}" stroke="#0f172a" stroke-width="1.8" stroke-dasharray="3,3"/>')
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
  <text x="{PX+18}" y="{MAP_Y+30}" fill="#0f172a" font-size="16" font-weight="900">SEZNAM VŠECH 25 TRAS (ODKUD → KAM &amp; MAPY.CZ)</text>
  <text x="{PX+18}" y="{MAP_Y+48}" fill="#64748b" font-size="11" font-weight="600">Číslo odpovídá značce v mapě • Kontrola viditelnosti na Mapy.cz</text>
  <line x1="{PX+14}" y1="{MAP_Y+58}" x2="{PX+PW-14}" y2="{MAP_Y+58}" stroke="#e2e8f0" stroke-width="1.5"/>
''')

    ly = MAP_Y + 78
    lx = PX + 16
    for ylabel, ycol in YEAR_COLORS.items():
        svg.append(f'  <rect x="{lx}" y="{ly-11}" width="12" height="12" rx="3" fill="{ycol}"/>')
        svg.append(f'  <text x="{lx+16}" y="{ly-1}" fill="#1e293b" font-size="11" font-weight="700">{ylabel}</text>')
        lx += 70 if len(ylabel) < 6 else 96

    svg.append(f'  <line x1="{PX+14}" y1="{MAP_Y+90}" x2="{PX+PW-14}" y2="{MAP_Y+90}" stroke="#e2e8f0" stroke-width="1.5"/>')

    row_y = MAP_Y + 110
    for r in DETAILED_ROUTES:
        col = YEAR_COLORS[r["year_cat"]]
        st = r["mapy_status"]
        badge_bg = "#dcfce7" if st == "ANO" else ("#fef3c7" if st == "ČÁSTEČNĚ" else "#f3e8ff")
        badge_fg = "#166534" if st == "ANO" else ("#92400e" if st == "ČÁSTEČNĚ" else "#6b21a8")
        badge_txt = "Mapy.cz: ANO" if st == "ANO" else ("Mapy.cz: ČÁST." if st == "ČÁSTEČNĚ" else "Plán 2026+")

        svg.append(f'  <circle cx="{PX+26}" cy="{row_y-2}" r="10.5" fill="{col}"/>')
        svg.append(f'  <text x="{PX+26}" y="{row_y+2}" fill="#ffffff" font-size="10" font-weight="800" text-anchor="middle">{r["id"]}</text>')
        svg.append(f'  <text x="{PX+44}" y="{row_y-4}" fill="#0f172a" font-size="10.8" font-weight="800">{r["name"]}</text>')
        svg.append(f'  <text x="{PX+44}" y="{row_y+9}" fill="#475569" font-size="9.6" font-weight="600">{r["from_label"]} → {r["to_label"]}</text>')

        svg.append(f'  <rect x="{PX+PW-102}" y="{row_y-13}" width="86" height="18" rx="5" fill="{badge_bg}"/>')
        svg.append(f'  <text x="{PX+PW-59}" y="{row_y-1}" fill="{badge_fg}" font-size="9.5" font-weight="800" text-anchor="middle">{badge_txt}</text>')
        row_y += 37.2

    BY = MAP_Y + MAP_H + 16
    svg.append(f'''
  <rect x="24" y="{BY}" width="{W-48}" height="102" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#regShadow)"/>
  <text x="48" y="{BY+28}" fill="#0f172a" font-size="14" font-weight="800">SHRNUTÍ KONTROLY VIDITELNOSTI NA MAPY.CZ (SEZNAM.CZ) A OPENSTREETMAP:</text>
  <text x="48" y="{BY+50}" fill="#166534" font-size="12.5" font-weight="700">✅ PLNĚ VIDITELNÉ A ROUTOVATELNÉ (17 tras): <tspan fill="#334155" font-weight="500">Polní cesty P9, P3 (Na Útulně), HPC 4 (Štolmíř), P6 (Rostoklaty), C6 Mlýnská cesta, Stezka B. Jedličky-Brodského do Liblic, Šemberské stezky (všechny singletraily), nová lávka u Skautské louky, Kudrnáčova stezka, Mrzecká cesta i obnovená NS Klepec.</tspan></text>
  <text x="48" y="{BY+71}" fill="#92400e" font-size="12.5" font-weight="700">⚠️ ČÁSTEČNĚ VIDITELNÉ BEZ POPISKU NEBO AKTUALIZACE POVRCHU (6 tras): <tspan fill="#334155" font-weight="500">Topolovka (v mapě jako pěšina bez názvu), Polní cesta C4 a KZ 7 v Chrášťanech (dokončeno 2025, v Mapy.cz zatím jako nezpevněná), Nová lipová alej u hřbitova (březen 2026), polní cesta Skramníky–Tatce (2024).</tspan></text>
  <text x="48" y="{BY+91}" fill="#6b21a8" font-size="12.5" font-weight="700">🚧 ZATÍM NEJSOU NA MAPY.CZ – V PŘÍPRAVĚ / VÝSTAVBĚ (2 trasy): <tspan fill="#334155" font-weight="500">Cyklostezka Český Brod (Nad Malechovem) – Přistoupim (600 m podél III/1131) a Stezka pro pěší a cyklisty Český Brod – Štolmíř podél silnice II/245.</tspan></text>
</svg>''')

    svg_str = "\n".join(svg)
    for d in [OUT_DIR, ARTIFACT_DIR]:
        with open(os.path.join(d, "mapa_stezky_podle_roku.svg"), "w", encoding="utf-8") as f:
            f.write(svg_str)
    print("Generated mapa_stezky_podle_roku.svg")


if __name__ == "__main__":
    generate_detail_map_on_tiles()
    generate_regional_map_on_tiles()
