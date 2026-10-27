#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generátor Sankey diagramů rozpočtu města Český Brod (IČO 00235334)
ve stylu "App Economy Insights" (How They Make & Spend Money):
1. Skutečnost FY 2025 (Závěrečný účet & Monitor Státní pokladny MF ČR — 404,1 mil. Kč)
2. Schválený rozpočet FY 2026 (č. j. 3558/2026 — 478,7 mil. Kč, rekordní investice)
"""

import os

OUT_DIR = "/Users/david.hunka/.gemini/antigravity/scratch/cesky-brod-atlas"
ARTIFACT_DIR = "/Users/david.hunka/.gemini/antigravity/brain/fb04040c-a126-472b-977a-b11f7bcc8927"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def sankey_ribbon(x0, y0_top, y0_bot, x1, y1_top, y1_bot, color, opacity=0.42):
    """Vykreslí hladkou kubickou Bézierovu stuhu (Sankey link) mezi dvěma svislými úsečkami."""
    cx0 = x0 + (x1 - x0) * 0.48
    cx1 = x0 + (x1 - x0) * 0.52
    d = (
        f"M {x0:.1f},{y0_top:.1f} "
        f"C {cx0:.1f},{y0_top:.1f} {cx1:.1f},{y1_top:.1f} {x1:.1f},{y1_top:.1f} "
        f"L {x1:.1f},{y1_bot:.1f} "
        f"C {cx1:.1f},{y1_bot:.1f} {cx0:.1f},{y0_bot:.1f} {x0:.1f},{y0_bot:.1f} Z"
    )
    return f'  <path d="{d}" fill="{color}" opacity="{opacity}"/>'


def build_app_economy_sankey(
    filename_base,
    title_main,
    title_sub,
    period_badge,
    total_label,
    total_val,
    total_sub,
    left_sources,       # list of dicts: {name, val, sub, color, group}
    mid_left_groups,    # list of dicts: {id, name, val, pct, sub, color}
    mid_right_groups,   # list of dicts: {id, name, val, pct, sub, color}
    right_targets,      # list of dicts: {name, val, sub, color, parent_id}
    kpi_cards           # list of 4 tuples: (label, val, sub, accent_color)
):
    W, H = 1920, 1220
    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="bgCanvas" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="nodeShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Pozadí ve stylu App Economy Insights -->
  <rect width="{W}" height="{H}" fill="url(#bgCanvas)"/>

  <!-- Horní barevná linka -->
  <rect x="0" y="0" width="{W}" height="8" fill="#0f172a"/>

  <!-- HLAVIČKA INFOGRAFIKY (APP ECONOMY INSIGHTS STYL) -->
  <!-- Městský znak / ikona hradby Českého Brodu -->
  <g transform="translate(48, 28)" filter="url(#nodeShadow)">
    <rect x="0" y="0" width="64" height="64" rx="16" fill="#0f172a"/>
    <!-- Stylizovaná gotická brána s věží -->
    <path d="M 16,50 L 16,24 L 22,24 L 22,29 L 27,29 L 27,16 L 32,10 L 37,16 L 37,29 L 42,29 L 42,24 L 48,24 L 48,50 Z" fill="#38bdf8"/>
    <path d="M 27,50 L 27,37 A 5,5 0 0 1 37,37 L 37,50 Z" fill="#0f172a"/>
  </g>

  <text x="128" y="56" fill="#0f172a" font-size="30" font-weight="900" letter-spacing="-0.4">{title_main}</text>
  <text x="128" y="82" fill="#475569" font-size="15" font-weight="600">{title_sub}</text>

  <!-- Pravý horní odznak období -->
  <g transform="translate({W-340}, 30)" filter="url(#cardShadow)">
    <rect x="0" y="0" width="292" height="58" rx="14" fill="#0f172a"/>
    <text x="146" y="25" fill="#38bdf8" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">IČO 00235334 • MĚSTO ČESKÝ BROD</text>
    <text x="146" y="45" fill="#ffffff" font-size="15" font-weight="800" text-anchor="middle">{period_badge}</text>
  </g>

  <!-- Nadpisy sloupců Sankey diagramu -->
  <g transform="translate(0, 118)">
    <text x="368" y="0" fill="#64748b" font-size="12" font-weight="800" text-anchor="end" letter-spacing="0.8">1. DETAILNÍ ZDROJE PŘÍJMŮ</text>
    <text x="660" y="0" fill="#64748b" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">2. KATEGORIE PŘÍJMŮ</text>
    <text x="945" y="0" fill="#0f172a" font-size="12.5" font-weight="900" text-anchor="middle" letter-spacing="0.8">3. CELKOVÝ ROZPOČET</text>
    <text x="1225" y="0" fill="#64748b" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="0.8">4. PROVOZ VS. INVESTICE</text>
    <text x="1505" y="0" fill="#64748b" font-size="12" font-weight="800" text-anchor="start" letter-spacing="0.8">5. NA CO PENÍZE JDOU (ÚČEL A AKCE)</text>
    <line x1="48" y1="10" x2="{W-48}" y2="10" stroke="#e2e8f0" stroke-width="1.5"/>
  </g>
''')

    NODE_W = 22
    X1 = 380
    X2 = 650
    X3 = 930
    X4 = 1210
    X5 = 1480

    TOP_Y = 152
    USABLE_H = 850

    # Měřítko výšky: celková výška všech položek v daném sloupci = total_val
    # Necháme prostor na mezery mezi uzly
    SCALE = 600.0 / total_val

    # --------------------------------------------------------------------------
    # Výpočet pozic Col 3 (Centrální uzel)
    # --------------------------------------------------------------------------
    c3_h = total_val * SCALE
    c3_y = TOP_Y + (USABLE_H - c3_h) / 2.0 - 15

    # --------------------------------------------------------------------------
    # Výpočet pozic Col 2 (Skupiny příjmů)
    # --------------------------------------------------------------------------
    gap2 = 34.0
    total_h2 = sum(g["val"] * SCALE for g in mid_left_groups) + gap2 * (len(mid_left_groups) - 1)
    cur_y2 = TOP_Y + (USABLE_H - total_h2) / 2.0 - 15
    c2_pos = {}
    for g in mid_left_groups:
        h = max(8.0, g["val"] * SCALE)
        c2_pos[g["id"]] = {"top": cur_y2, "bot": cur_y2 + h, "cur_in": cur_y2, "data": g}
        cur_y2 += h + gap2

    # --------------------------------------------------------------------------
    # Výpočet pozic Col 1 (Detailní položky příjmů vlevo)
    # --------------------------------------------------------------------------
    gap1 = 18.0
    total_h1 = sum(max(6.0, s["val"] * SCALE) for s in left_sources) + gap1 * (len(left_sources) - 1)
    cur_y1 = TOP_Y + (USABLE_H - total_h1) / 2.0 - 15
    c1_pos = []
    for s in left_sources:
        h = max(6.0, s["val"] * SCALE)
        c1_pos.append({"top": cur_y1, "bot": cur_y1 + h, "data": s})
        cur_y1 += h + gap1

    # --------------------------------------------------------------------------
    # Výpočet pozic Col 4 (Provoz vs. Investice)
    # --------------------------------------------------------------------------
    gap4 = 70.0
    total_h4 = sum(g["val"] * SCALE for g in mid_right_groups) + gap4 * (len(mid_right_groups) - 1)
    cur_y4 = TOP_Y + (USABLE_H - total_h4) / 2.0 - 15
    c4_pos = {}
    for g in mid_right_groups:
        h = max(10.0, g["val"] * SCALE)
        c4_pos[g["id"]] = {"top": cur_y4, "bot": cur_y4 + h, "cur_out": cur_y4, "data": g}
        cur_y4 += h + gap4

    # --------------------------------------------------------------------------
    # Výpočet pozic Col 5 (Cílové výdajové kapitoly a investice vpravo)
    # --------------------------------------------------------------------------
    gap5 = 16.0
    total_h5 = sum(max(6.0, t["val"] * SCALE) for t in right_targets) + gap5 * (len(right_targets) - 1)
    cur_y5 = TOP_Y + (USABLE_H - total_h5) / 2.0 - 15
    c5_pos = []
    for t in right_targets:
        h = max(6.0, t["val"] * SCALE)
        c5_pos.append({"top": cur_y5, "bot": cur_y5 + h, "data": t})
        cur_y5 += h + gap5

    # ==========================================================================
    # VYKRESLENÍ SANKEY STUH (LINKS)
    # ==========================================================================

    # 1. Links Col 1 -> Col 2
    for item in c1_pos:
        s = item["data"]
        gid = s["group"]
        gbox = c2_pos[gid]
        h_link = s["val"] * SCALE
        y0_t = item["top"]
        y0_b = item["bot"]
        y1_t = gbox["cur_in"]
        y1_b = y1_t + h_link
        gbox["cur_in"] = y1_b
        svg.append(sankey_ribbon(X1 + NODE_W, y0_t, y0_b, X2, y1_t, y1_b, s["color"], opacity=0.38))

    # 2. Links Col 2 -> Col 3 (Centrální uzel)
    cur_c3_in = c3_y
    for g in mid_left_groups:
        gbox = c2_pos[g["id"]]
        h_link = g["val"] * SCALE
        svg.append(sankey_ribbon(X2 + NODE_W, gbox["top"], gbox["bot"], X3, cur_c3_in, cur_c3_in + h_link, g["color"], opacity=0.44))
        cur_c3_in += h_link

    # 3. Links Col 3 -> Col 4 (Provoz vs. Investice)
    cur_c3_out = c3_y
    for g in mid_right_groups:
        gbox = c4_pos[g["id"]]
        h_link = g["val"] * SCALE
        svg.append(sankey_ribbon(X3 + NODE_W, cur_c3_out, cur_c3_out + h_link, X4, gbox["top"], gbox["bot"], g["color"], opacity=0.44))
        cur_c3_out += h_link

    # 4. Links Col 4 -> Col 5 (Konkrétní účely výdajů)
    for item in c5_pos:
        t = item["data"]
        pid = t["parent_id"]
        pbox = c4_pos[pid]
        h_link = t["val"] * SCALE
        y0_t = pbox["cur_out"]
        y0_b = y0_t + h_link
        pbox["cur_out"] = y0_b
        svg.append(sankey_ribbon(X4 + NODE_W, y0_t, y0_b, X5, item["top"], item["bot"], t["color"], opacity=0.38))

    # ==========================================================================
    # VYKRESLENÍ UZLŮ (NODES) A POPISKŮ VE STYLU APP ECONOMY INSIGHTS
    # ==========================================================================

    # Col 1 uzly + popisky vlevo
    for item in c1_pos:
        s = item["data"]
        top, bot = item["top"], item["bot"]
        mid = (top + bot) / 2.0
        svg.append(f'  <rect x="{X1}" y="{top:.1f}" width="{NODE_W}" height="{bot-top:.1f}" rx="4" fill="{s["color"]}" filter="url(#nodeShadow)"/>')
        svg.append(f'  <text x="{X1-12}" y="{mid-2:.1f}" fill="#0f172a" font-size="12.5" font-weight="800" text-anchor="end">{s["name"]}: <tspan fill="{s["color"]}">{s["val"]:.1f} mil. Kč</tspan></text>')
        svg.append(f'  <text x="{X1-12}" y="{mid+13:.1f}" fill="#64748b" font-size="10.5" font-weight="600" text-anchor="end">{s["sub"]}</text>')

    # Col 2 uzly + štítky kategorií příjmů
    for g in mid_left_groups:
        gbox = c2_pos[g["id"]]
        top, bot = gbox["top"], gbox["bot"]
        mid = (top + bot) / 2.0
        svg.append(f'  <rect x="{X2}" y="{top:.1f}" width="{NODE_W}" height="{bot-top:.1f}" rx="5" fill="{g["color"]}" filter="url(#nodeShadow)"/>')
        # Kartička nad/u uzlu
        card_w, card_h = 222, 48
        cx = X2 + NODE_W / 2.0 - card_w / 2.0
        cy = mid - card_h / 2.0
        svg.append(f'  <rect x="{cx:.1f}" y="{cy:.1f}" width="{card_w}" height="{card_h}" rx="9" fill="#ffffff" stroke="{g["color"]}" stroke-width="2" filter="url(#nodeShadow)"/>')
        svg.append(f'  <text x="{X2+NODE_W/2:.1f}" y="{cy+18:.1f}" fill="#0f172a" font-size="11.5" font-weight="800" text-anchor="middle">{g["name"]}</text>')
        svg.append(f'  <text x="{X2+NODE_W/2:.1f}" y="{cy+35:.1f}" fill="{g["color"]}" font-size="13" font-weight="900" text-anchor="middle">{g["val"]:.1f} mil. Kč <tspan fill="#64748b" font-size="11" font-weight="700">({g["pct"]})</tspan></text>')

    # Col 3 Centrální uzel (CELKOVÝ ROZPOČET)
    c3_mid = c3_y + c3_h / 2.0
    svg.append(f'  <rect x="{X3}" y="{c3_y:.1f}" width="{NODE_W+6}" height="{c3_h:.1f}" rx="6" fill="#0f172a" filter="url(#nodeShadow)"/>')
    svg.append(f'''
  <g transform="translate({X3 + (NODE_W+6)/2}, {c3_mid})" filter="url(#cardShadow)">
    <rect x="-118" y="-44" width="236" height="88" rx="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="0" y="-18" fill="#38bdf8" font-size="11.5" font-weight="800" text-anchor="middle" letter-spacing="0.6">{total_label}</text>
    <text x="0" y="10" fill="#ffffff" font-size="24" font-weight="900" text-anchor="middle">{total_val:.1f} mil. Kč</text>
    <text x="0" y="30" fill="#94a3b8" font-size="11" font-weight="600" text-anchor="middle">{total_sub}</text>
  </g>
''')

    # Col 4 uzly (Provoz vs. Investice)
    for g in mid_right_groups:
        gbox = c4_pos[g["id"]]
        top, bot = gbox["top"], gbox["bot"]
        mid = (top + bot) / 2.0
        svg.append(f'  <rect x="{X4}" y="{top:.1f}" width="{NODE_W}" height="{bot-top:.1f}" rx="5" fill="{g["color"]}" filter="url(#nodeShadow)"/>')
        card_w, card_h = 236, 54
        cx = X4 + NODE_W / 2.0 - card_w / 2.0
        cy = mid - card_h / 2.0
        svg.append(f'  <rect x="{cx:.1f}" y="{cy:.1f}" width="{card_w}" height="{card_h}" rx="10" fill="#ffffff" stroke="{g["color"]}" stroke-width="2.2" filter="url(#nodeShadow)"/>')
        svg.append(f'  <text x="{X4+NODE_W/2:.1f}" y="{cy+19:.1f}" fill="#0f172a" font-size="12" font-weight="800" text-anchor="middle">{g["name"]}</text>')
        svg.append(f'  <text x="{X4+NODE_W/2:.1f}" y="{cy+37:.1f}" fill="{g["color"]}" font-size="14" font-weight="900" text-anchor="middle">{g["val"]:.1f} mil. Kč <tspan fill="#64748b" font-size="11" font-weight="700">({g["pct"]})</tspan></text>')
        svg.append(f'  <text x="{X4+NODE_W/2:.1f}" y="{cy+49:.1f}" fill="#64748b" font-size="9.5" font-weight="600" text-anchor="middle">{g["sub"]}</text>')

    # Col 5 uzly + popisky vpravo (Na co peníze jdou)
    for item in c5_pos:
        t = item["data"]
        top, bot = item["top"], item["bot"]
        mid = (top + bot) / 2.0
        svg.append(f'  <rect x="{X5}" y="{top:.1f}" width="{NODE_W}" height="{bot-top:.1f}" rx="4" fill="{t["color"]}" filter="url(#nodeShadow)"/>')
        svg.append(f'  <text x="{X5+NODE_W+12}" y="{mid-2:.1f}" fill="#0f172a" font-size="12.5" font-weight="800" text-anchor="start">{t["name"]}: <tspan fill="{t["color"]}">{t["val"]:.1f} mil. Kč</tspan></text>')
        svg.append(f'  <text x="{X5+NODE_W+12}" y="{mid+13:.1f}" fill="#64748b" font-size="10.5" font-weight="600" text-anchor="start">{t["sub"]}</text>')

    # ==========================================================================
    # SPODNÍ PÁS: 4 KARTY FINANČNÍHO ZDRAVÍ A HOSPODÁŘSKÉ ČINNOSTI
    # ==========================================================================
    BY = 1075
    svg.append(f'  <line x1="48" y1="{BY-14}" x2="{W-48}" y2="{BY-14}" stroke="#cbd5e1" stroke-width="1.5"/>')

    card_w = (W - 96 - 3 * 20) / 4.0
    for idx, (k_label, k_val, k_sub, k_col) in enumerate(kpi_cards):
        kx = 48 + idx * (card_w + 20)
        svg.append(f'''
  <g transform="translate({kx:.1f}, {BY})" filter="url(#cardShadow)">
    <rect x="0" y="0" width="{card_w:.1f}" height="106" rx="14" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
    <rect x="0" y="0" width="8" height="106" rx="4" fill="{k_col}"/>
    <text x="24" y="28" fill="#64748b" font-size="11.5" font-weight="800" letter-spacing="0.5">{k_label}</text>
    <text x="24" y="60" fill="#0f172a" font-size="24" font-weight="900">{k_val}</text>
    <text x="24" y="84" fill="#475569" font-size="11.5" font-weight="600">{k_sub}</text>
  </g>''')

    svg.append(f'''
  <text x="{W/2}" y="{H-12}" fill="#94a3b8" font-size="11" font-weight="600" text-anchor="middle">Zdroj dat: Monitor Státní pokladny MF ČR (výkaz FIN 2-12 M, IČO 00235334), Závěrečné účty a Schválené rozpočty města Český Brod (cesbrod.cz) • Vizualizace ve stylu App Economy Insights</text>
</svg>''')

    svg_str = "\n".join(svg)
    for d in [OUT_DIR, ARTIFACT_DIR]:
        with open(os.path.join(d, f"{filename_base}.svg"), "w", encoding="utf-8") as f:
            f.write(svg_str)
    print(f"Generated {filename_base}.svg")


def generate_2025_actual():
    """Skutečné plnění rozpočtu města Český Brod za rok 2025 (Závěrečný účet 2025: příjmy 396,1M, výdaje 404,1M)."""
    left_sources = [
        {"name": "Daň z přidané hodnoty (DPH)", "val": 85.5, "sub": "Sdílená daň od státu (RUD) • hlavní příjmový pilíř", "color": "#059669", "group": "tax"},
        {"name": "Daň z příjmů firem (DPPO)", "val": 48.0, "sub": "Sdílená DPPO ze zisků firem + vlastní daň obce", "color": "#059669", "group": "tax"},
        {"name": "Daň z příjmů fyzických osob (DPFO)", "val": 39.0, "sub": "Ze závislé činnosti (zaměstnanci), OSVČ a srážková", "color": "#10b981", "group": "tax"},
        {"name": "Daň z nemovitých věcí", "val": 24.2, "sub": "100 % příjmem města (koef. 2,5) → Fond komunikací", "color": "#10b981", "group": "tax"},
        {"name": "Místní, správní poplatky a hazard", "val": 21.6, "sub": "Odpady (8,0M), správní popl. (7,5M), hazard (6,0M)", "color": "#34d399", "group": "tax"},

        {"name": "Státní rozpočet – výkon státní správy", "val": 27.5, "sub": "Souhrnný dotační vztah SR (24,0M) + SPOD (3,5M)", "color": "#2563eb", "group": "grants"},
        {"name": "Dotace MPSV – Domov Anna a soc. práce", "val": 16.9, "sub": "Státní dotace na Domov pro seniory a pečovatelky", "color": "#3b82f6", "group": "grants"},
        {"name": "Investiční dotace EU / IROP / SFŽP", "val": 73.8, "sub": "ZŠ Žitomířská (IROP 32M+), dětská skupina (20M)", "color": "#60a5fa", "group": "grants"},

        {"name": "Nedaňové příjmy (radary, úroky, služby)", "val": 26.9, "sub": "Pokuty z měření I/12 a Rostoklaty, úroky, převody HČ", "color": "#0d9488", "group": "other"},
        {"name": "Kapitálové příjmy (prodej majetku)", "val": 32.7, "sub": "Prodej pozemků a příspěvky investorů na sítě", "color": "#14b8a6", "group": "other"},

        {"name": "Zapojení rezerv a fondů města (Saldo)", "val": 8.0, "sub": "Krytí investičního schodku z fondů minulých let", "color": "#64748b", "group": "fin"},
    ]

    mid_left_groups = [
        {"id": "tax", "name": "DAŇOVÉ PŘÍJMY (Tř. 1)", "val": 218.3, "pct": "54 %", "sub": "RUD + místní daně a poplatky", "color": "#059669"},
        {"id": "grants", "name": "DOTACE OD STÁTU A EU (Tř. 4)", "val": 118.2, "pct": "29 %", "sub": "Státní správa, MPSV, fondy EU", "color": "#2563eb"},
        {"id": "other", "name": "NEDAŇOVÉ A KAPITÁLOVÉ (Tř. 2+3)", "val": 59.6, "pct": "15 %", "sub": "Pokuty, úroky, prodej majetku", "color": "#0d9488"},
        {"id": "fin", "name": "ZAPOJENÍ ÚSPOR (Tř. 8)", "val": 8.0, "pct": "2 %", "sub": "Fondy města", "color": "#64748b"},
    ]

    mid_right_groups = [
        {"id": "opex", "name": "BĚŽNÉ PROVOZNÍ VÝDAJE", "val": 257.2, "pct": "63,6 %", "sub": "Třída 5: Chod města, škol, služeb a úřadu", "color": "#334155"},
        {"id": "capex", "name": "KAPITÁLOVÉ INVESTICE", "val": 146.9, "pct": "36,4 %", "sub": "Třída 6: Nová výstavba, rekonstrukce a rozvoj", "color": "#dc2626"},
    ]

    right_targets = [
        # Provozní výdaje (součet = 257,2 mil. Kč)
        {"name": "Veřejná správa, radnice a IT", "val": 78.5, "sub": "Chod MěÚ (platy a státní správa ORP), IT a kamery (6,8M)", "color": "#475569", "parent_id": "opex"},
        {"name": "Školství – provoz 7 škol a jídelny", "val": 46.8, "sub": "ZŠ Tyršova, ZŠ Žitomířská, 3× MŠ, SŠ Liblice a ŠJ", "color": "#2563eb", "parent_id": "opex"},
        {"name": "Komunální služby, odpady a zeleň", "val": 44.2, "sub": "Technické služby ČB (33,5M – odpady, čištění, VO) + OŽP", "color": "#16a34a", "parent_id": "opex"},
        {"name": "Sociální služby a Domov Anna", "val": 26.8, "sub": "Domov pro seniory, pečovatelky, stacionář (22M) + SPOD", "color": "#0d9488", "parent_id": "opex"},
        {"name": "Kultura, knihovna, KD Svět a sport", "val": 25.4, "sub": "CVIK (12,5M), Fond kultury a sportu (granty klubům)", "color": "#7c3aed", "parent_id": "opex"},
        {"name": "Doprava, údržba komunikací a PID", "val": 19.8, "sub": "Běžné opravy ulic a chodníků, autobusy PID", "color": "#d97706", "parent_id": "opex"},
        {"name": "Městská policie, bezpečnost a hasiči", "val": 15.7, "sub": "Městská policie ČB, úsekové měření, hasiči JSDH/HZS", "color": "#475569", "parent_id": "opex"},

        # Kapitálové investice (součet = 146,9 mil. Kč)
        {"name": "Přístavba a rekonstrukce ZŠ Žitomířská", "val": 64.5, "sub": "Odborné učebny, hlavní budova a poradenské pracoviště", "color": "#dc2626", "parent_id": "capex"},
        {"name": "Příprava MŠ Kollárova + splátka SŠ", "val": 26.4, "sub": "Dočasná MŠ, příprava MŠ Letadýlko + splátka SŠ (8,4M)", "color": "#e11d48", "parent_id": "capex"},
        {"name": "Rekonstrukce komunikací a stezek", "val": 24.2, "sub": "Opravy ulic a chodníků z Fondu komunikací, cyklostezky", "color": "#ea580c", "parent_id": "capex"},
        {"name": "Kultura, Stará radnice čp. 1 a parky", "val": 16.0, "sub": "Dokončení úprav čp. 1 (Podkroví), veřejný prostor, participace", "color": "#db2777", "parent_id": "capex"},
        {"name": "Domov Anna (kotelna) a ekologie", "val": 15.8, "sub": "Nová kotelna Domov Anna (7,8M), polopodzemní kontejnery", "color": "#be123c", "parent_id": "capex"},
    ]

    kpi_cards = [
        ("CELKOVÉ PŘÍJMY 2025 (SKUTEČNOST)", "396,1 mil. Kč", "53 849 Kč na obyvatele (+19,7 % oproti r. 2024)", "#059669"),
        ("PODÍL INVESTIC NA VÝDAJÍCH", "36,4 % (146,9M)", "Mimořádně vysoká míra investic (průměr obcí ČR je ~22 %)", "#dc2626"),
        ("HOTOVOST NA ÚČTECH A V REZERVÁCH", "108,6 mil. Kč", "Dluh města jen 19,0 mil. Kč (5,6 % příjmů vs. limit 60 %)", "#2563eb"),
        ("VLASTNÍ HOSPODÁŘSKÁ ČINNOST (MIMO ROZP.)", "+40,5 mil. Kč zisk", "Byty a nemocnice (+25,3M), Voda (+13,6M), Městské lesy (+1,6M)", "#0d9488"),
    ]

    build_app_economy_sankey(
        filename_base="rozpocet_sankey_2025",
        title_main="ČESKÝ BROD — JAK MĚSTO HOSPODAŘÍ (FY 2025)",
        title_sub="Skutečné plnění rozpočtu za rok 2025: Odkud plynou peníze od státu a občanů a na co přesně jdou",
        period_badge="SKUTEČNOST ROKU 2025 (ZÚ)",
        total_label="CELKOVÝ ROZPOČET 2025",
        total_val=404.1,
        total_sub="Příjmy 396,1M + Fondy 8,0M",
        left_sources=left_sources,
        mid_left_groups=mid_left_groups,
        mid_right_groups=mid_right_groups,
        right_targets=right_targets,
        kpi_cards=kpi_cards
    )


def generate_2026_budget():
    """Schválený rozpočet města Český Brod na rok 2026 (č. j. 3558/2026: příjmy 377,5M, výdaje 478,7M)."""
    left_sources = [
        {"name": "Daň z přidané hodnoty (DPH)", "val": 101.5, "sub": "Sdílená daň od státu (RUD) • nejvyšší příjmová položka", "color": "#059669", "group": "tax"},
        {"name": "Daň z příjmů firem (DPPO + vlastní)", "val": 61.9, "sub": "Sdílená DPPO (53,5M) + vlastní daň placená obcí (8,4M)", "color": "#059669", "group": "tax"},
        {"name": "Daň z příjmů fyzických osob (DPFO)", "val": 49.5, "sub": "Ze závislé činnosti (40,0M), srážková (6,5M) a OSVČ (3,0M)", "color": "#10b981", "group": "tax"},
        {"name": "Daň z nemovitých věcí", "val": 25.0, "sub": "100 % příjmem města (koef. 2,5) → plní Fond komunikací", "color": "#10b981", "group": "tax"},
        {"name": "Poplatky (odpady, správní) a hazard", "val": 20.7, "sub": "Správní popl. (9,0M), odpady 1 140 Kč/os (7,9M), hazard (3M)", "color": "#34d399", "group": "tax"},

        {"name": "Státní rozpočet – výkon státní správy", "val": 28.0, "sub": "Příspěvek státu na státní správu ORP (24,3M) + SPOD (3,7M)", "color": "#2563eb", "group": "grants"},
        {"name": "Dotace MPSV – Domov Anna a soc. práce", "val": 15.4, "sub": "Státní dotace na provoz Domova Anna (15,0M) a soc. práci", "color": "#3b82f6", "group": "grants"},
        {"name": "Investiční dotace EU / IROP / OPŽP", "val": 50.2, "sub": "Školské dotace, kyberbezpečnost (8,2M), kontejnery (6,5M)", "color": "#60a5fa", "group": "grants"},

        {"name": "Nedaňové příjmy a převody z HČ", "val": 25.4, "sub": "Pokuty z radarů (14,5M), vratka CVIK (7,7M), převody HČ (3M)", "color": "#0d9488", "group": "other"},

        {"name": "Fondy města + investiční úvěr na MŠ", "val": 101.2, "sub": "Fond komunikací (19M), Fond infrastr. a úvěr KB na MŠ (50M)", "color": "#64748b", "group": "fin"},
    ]

    mid_left_groups = [
        {"id": "tax", "name": "DAŇOVÉ PŘÍJMY (Tř. 1)", "val": 258.6, "pct": "54 %", "sub": "RUD + místní daně a poplatky", "color": "#059669"},
        {"id": "grants", "name": "DOTACE A TRANSFERY (Tř. 4)", "val": 93.6, "pct": "20 %", "sub": "Státní správa, MPSV, fondy EU", "color": "#2563eb"},
        {"id": "other", "name": "NEDAŇOVÉ PŘÍJMY (Tř. 2)", "val": 25.4, "pct": "5 %", "sub": "Pokuty, úroky, služby", "color": "#0d9488"},
        {"id": "fin", "name": "FONDY A ÚVĚR NA INVESTICE", "val": 101.2, "pct": "21 %", "sub": "Krytí výstavby škol a ulic", "color": "#64748b"},
    ]

    mid_right_groups = [
        {"id": "opex", "name": "PROVOZNÍ VÝDAJE (BĚŽNÉ)", "val": 287.5, "pct": "60,1 %", "sub": "Chod města, škol, organizací a příděly fondům", "color": "#334155"},
        {"id": "capex", "name": "INVESTIČNÍ VÝDAJE (KAPITÁLOVÉ)", "val": 191.2, "pct": "39,9 %", "sub": "25 investičních akcí (+ 19M Fond komunikací)", "color": "#dc2626"},
    ]

    right_targets = [
        # Provozní výdaje (součet = 287,5 mil. Kč)
        {"name": "Radnice, zaměstnanci MěÚ, IT a správa", "val": 97.6, "sub": "Osobní náklady MěÚ (70,5M), zastupitelé (5,0M), IT (6,7M)", "color": "#475569", "parent_id": "opex"},
        {"name": "Školství – provoz 7 škol a jídelny", "val": 60.2, "sub": "ZŠ Žitomířská (15,2M), ŠJ (12,8M), ZŠ Tyršova (12,6M), MŠ, SŠ", "color": "#2563eb", "parent_id": "opex"},
        {"name": "Technické služby, odpady, zeleň a VO", "val": 36.1, "sub": "TS Český Brod (33,3M – odpady, zeleň, čištění, VO) + OŽP", "color": "#16a34a", "parent_id": "opex"},
        {"name": "Fond komunikací a doprava PID", "val": 24.4, "sub": "Příděl do Fondu komunikací (20,9M), autobusy PID (2,8M)", "color": "#d97706", "parent_id": "opex"},
        {"name": "Domov Anna a sociální služby", "val": 22.8, "sub": "Domov Anna (15,0M MPSV + 5,8M město) + soc. granty (2,1M)", "color": "#0d9488", "parent_id": "opex"},
        {"name": "Kultura (CVIK, KD Svět) a sport", "val": 28.9, "sub": "CVIK a knihovna (13,3M), Fond kultury a sportu (4,2M), památky", "color": "#7c3aed", "parent_id": "opex"},
        {"name": "Městská policie, bezpečnost a hasiči", "val": 17.5, "sub": "Městská policie ČB (16,2M – strážníci, radary) + HZS (1,2M)", "color": "#475569", "parent_id": "opex"},

        # Kapitálové investice (součet = 191,2 mil. Kč)
        {"name": "Nová MŠ Kollárova + dočasná MŠ", "val": 61.0, "sub": "Novostavba MŠ Kollárova (50,0M) + úprava dočasné MŠ (11,0M)", "color": "#dc2626", "parent_id": "capex"},
        {"name": "Přístavba a rozšíření ZŠ Žitomířská", "val": 59.0, "sub": "Pokračování hlavní školské investice (nové učebny a zázemí)", "color": "#e11d48", "parent_id": "capex"},
        {"name": "Svazková škola (DSO) + splátka SŠ", "val": 18.4, "sub": "Příspěvek DSO na svazkovou školu (10,0M) + splátka SŠ (8,4M)", "color": "#f43f5e", "parent_id": "capex"},
        {"name": "Náměstí, Jiráskovy sady a chodníky", "val": 20.7, "sub": "PD dvojnáměstí (10,8M), PD Jiráskovy sady (2,2M), Gothardka", "color": "#ea580c", "parent_id": "capex"},
        {"name": "Kyberbezpečnost, IT, radary a radnice", "val": 16.5, "sub": "Kyberbezpečnost (9,6M), úpravy čp. 70 (2,5M), radary RAMER", "color": "#db2777", "parent_id": "capex"},
        {"name": "Sportoviště, pozemky a Broďáci Brodu", "val": 15.6, "sub": "Pozemky (5,0M), hřiště Sportovní (4,0M), TS (2,5M), participace", "color": "#be123c", "parent_id": "capex"},
    ]

    kpi_cards = [
        ("SCHVÁLENÉ PŘÍJMY 2026", "377,5 mil. Kč", "Daňové příjmy rostou na 258,6 mil. Kč (+27 % oproti r. 2024)", "#059669"),
        ("REKORDNÍ INVESTICE 2026", "210,2 mil. Kč", "191,2M v hlavním rozpočtu + 19,0M z Fondu komunikací na ulice", "#dc2626"),
        ("INVESTICE DO ŠKOLSTVÍ 2026", "138,4 mil. Kč", "MŠ Kollárova (61M), ZŠ Žitomířská (59M), Svazková škola (10M), SŠ (8,4M)", "#2563eb"),
        ("OPRAVY ULIC, PARKŮ A STEZEK", "39,7 mil. Kč", "Fond komunikací (19M), PD dvojnáměstí (10,8M), Jiráskovy sady a Gothardka", "#ea580c"),
    ]

    build_app_economy_sankey(
        filename_base="rozpocet_sankey_2026",
        title_main="ČESKÝ BROD — SCHVÁLENÝ ROZPOČET (FY 2026)",
        title_sub="Plán hospodaření na rok 2026 (č. j. 3558/2026): Rekordní investice do škol, náměstí, parků a komunikací",
        period_badge="ROZPOČET 2026 (SCHVÁLENÝ)",
        total_label="CELKOVÉ VÝDAJE 2026",
        total_val=478.7,
        total_sub="Příjmy 377,5M + Fondy/Úvěr 101,2M",
        left_sources=left_sources,
        mid_left_groups=mid_left_groups,
        mid_right_groups=mid_right_groups,
        right_targets=right_targets,
        kpi_cards=kpi_cards
    )


def generate_vhc_sankey():
    """Vlastní hospodářská činnost města Český Brod (Bytové hospodářství & Nemocnice, Vodohospodářský fond, Městské lesy)."""
    left_sources = [
        {"name": "Nájemné z městských bytů a domů", "val": 16.8, "sub": "Čistý výnos z pronájmu bytového fondu města", "color": "#059669", "group": "bh"},
        {"name": "Nebytové prostory a areál Nemocnice", "val": 8.5, "sub": "Pronájem ordinací polikliniky/nemocnice a komerčních prostor", "color": "#10b981", "group": "bh"},

        {"name": "Vodohospodářský majetek (pacht a vodné)", "val": 10.2, "sub": "Výnosy z vodovodní a kanalizační sítě města", "color": "#2563eb", "group": "ohc"},
        {"name": "Ostatní hospodářská činnost (OHČ)", "val": 3.4, "sub": "Komerční pronájmy pozemků a hospodářské služby města", "color": "#3b82f6", "group": "ohc"},
        {"name": "Rezervní fond vodohospodářský (akumulace)", "val": 12.8, "sub": "Zapojení naakumulovaných zdrojů fondu na velké rekonstrukce sítí", "color": "#60a5fa", "group": "ohc"},

        {"name": "Městské lesy – prodej dřeva a hospodaření", "val": 4.2, "sub": "Vlastní tržby z těžby dřeva a lesního hospodářství (zisk +1,56M)", "color": "#0d9488", "group": "lesy"},
        {"name": "Dotace na projekty Městských lesů", "val": 26.8, "sub": "Dotace na dětskou skupinu (20M), Cestu lásky (80 %), altán a tůně", "color": "#14b8a6", "group": "lesy"},
        {"name": "Fondy města a předfinancování lesních akcí", "val": 19.7, "sub": "Kofinancování výstavby dětské skupiny a lesní infrastruktury", "color": "#64748b", "group": "lesy"},
    ]

    mid_left_groups = [
        {"id": "bh", "name": "BYTY A NEMOCNICE (BH)", "val": 25.3, "pct": "25 %", "sub": "Zisk před zdaněním +25,31 mil. Kč", "color": "#059669"},
        {"id": "ohc", "name": "VODA A OSTATNÍ HČ", "val": 26.4, "pct": "26 %", "sub": "Zisk +13,58M + Vodohosp. fond", "color": "#2563eb"},
        {"id": "lesy", "name": "MĚSTSKÉ LESY A DOTACE", "val": 50.7, "pct": "49 %", "sub": "Zisk +1,56M + investiční dotace", "color": "#0d9488"},
    ]

    mid_right_groups = [
        {"id": "inv_vhc", "name": "INVESTICE STŘEDISEK HČ", "val": 78.9, "pct": "77,1 %", "sub": "Vodovody, lesní cesty, dětská skupina, nemocnice", "color": "#dc2626"},
        {"id": "rezervy", "name": "ODVOD MĚSTU A REZERVY", "val": 23.5, "pct": "22,9 %", "sub": "Převod městu (3M) + Fond bytového hospodářství", "color": "#334155"},
    ]

    right_targets = [
        # Investice středisek HČ (78,9 mil. Kč)
        {"name": "Vybudování nové dětské skupiny", "val": 38.0, "sub": "Stěžejní investice v rámci Městských lesů / města (dotace 20,0M)", "color": "#dc2626", "parent_id": "inv_vhc"},
        {"name": "Rekonstrukce vodovodu a kanalizace Tuchorazská", "val": 16.0, "sub": "Hlavní vodohospodářská stavba + příprava intenzifikace ČOV", "color": "#2563eb", "parent_id": "inv_vhc"},
        {"name": "PD vodovodů a obnova sítí (7 ulic + vodoměry)", "val": 9.4, "sub": "PD Klučovská, Za Drahou, Žižkova, Ruská, Sokolovská, 28. října, vodoměry", "color": "#3b82f6", "parent_id": "inv_vhc"},
        {"name": "Lesní cesta „Cesta lásky“ (2. část)", "val": 6.8, "sub": "Kompletní rekonstrukce lesní cesty Městských lesů (dotace 80 %)", "color": "#0d9488", "parent_id": "inv_vhc"},
        {"name": "Bytový fond a kotelna v Nemocnici", "val": 4.8, "sub": "Technologie kotelny v nemocnici (1,2M), PD čp. 202 (1,3M), čp. 620, spisovna", "color": "#059669", "parent_id": "inv_vhc"},
        {"name": "Lesní technika, altán Skautská louka a tůně", "val": 3.9, "sub": "Lesnický traktor (2,6M), altán a lesní workout (1,2M), tůně v lese (0,25M)", "color": "#16a34a", "parent_id": "inv_vhc"},

        # Odvod městu a tvorba rezerv (23,5 mil. Kč)
        {"name": "Tvorba Fondu bytového hospodářství a nemocnice", "val": 20.5, "sub": "Akumulace čistého zisku z nájmů na budoucí výstavbu a opravy domů", "color": "#475569", "parent_id": "rezervy"},
        {"name": "Převod zisku do hlavního rozpočtu města", "val": 3.0, "sub": "Příspěvek z OHČ, Městských lesů a BH přímo do rozpočtu města", "color": "#0f172a", "parent_id": "rezervy"},
    ]

    kpi_cards = [
        ("ZISK HOSPODÁŘSKÉ ČINNOSTI", "+40,45 mil. Kč", "Čistý zisk před zdaněním mimo hlavní rozpočet města (ZÚ 2024)", "#059669"),
        ("BYTY A FOND NEMOCNICE", "+25,31 mil. Kč", "Nejziskovější pilíř: městské byty, nebytové prostory a poliklinika", "#2563eb"),
        ("VODOHOSPODÁŘSKÝ FOND A OHČ", "+13,58 mil. Kč", "Financuje opravy vodovodů, kanalizací a přípravu rozšíření ČOV", "#0d9488"),
        ("INVESTICE MĚSTSKÝCH LESŮ", "49,65 mil. Kč", "Dětská skupina (38M), Cesta lásky (6,8M), altán Skautská louka, tůně", "#dc2626"),
    ]

    build_app_economy_sankey(
        filename_base="rozpocet_sankey_vhc",
        title_main="ČESKÝ BROD — VLASTNÍ HOSPODÁŘSKÁ ČINNOST (MIMO ROZPOČET)",
        title_sub="Druhý finanční pilíř města: Bytové hospodářství a nemocnice, Vodohospodářský fond a Městské lesy (2024–2025)",
        period_badge="HOSPODÁŘSKÁ ČINNOST MĚSTA",
        total_label="ZDROJE A INVESTICE HČ",
        total_val=102.4,
        total_sub="Zisk +40,5M • Dotace a fondy 61,9M",
        left_sources=left_sources,
        mid_left_groups=mid_left_groups,
        mid_right_groups=mid_right_groups,
        right_targets=right_targets,
        kpi_cards=kpi_cards
    )


if __name__ == "__main__":
    generate_2025_actual()
    generate_2026_budget()
    generate_vhc_sankey()
