# Atlas obnovených cest Českobrodska (2020–2026+) & Rozpočet města Český Brod

Tento repozitář obsahuje dva ucelené výstupy pro město Český Brod a region Českobrodska:
1. **Atlas 25 obnovených cest, alejí a stezek** (kartografická mapa a interaktivní aplikace).
2. **Finanční toky rozpočtu města Český Brod** ve stylu App Economy Insights (Sankey diagramy pro roky 2023–2026 a vlastní hospodářskou činnost).

---

## 🚀 Hlavní výstupy projektu

| Výstup | Popis | Odkaz |
| :--- | :--- | :--- |
| **🌐 Interaktivní aplikace** | Webová aplikace s mapou na podkladu OpenStreetMap (filtr roku/typu) a přepínatelnými Sankey diagramy rozpočtu | [Otevřít na GitHub Pages](https://davidhunka.github.io/cesky-brod-atlas/) |
| **🗺️ Mapa stezek Českobrodska** | Přehledová kartografická mapa celého regionu (25 tras na reálném mapovém podkladu) | [mapa_stezky_podle_roku.png](./mapa_stezky_podle_roku.png) |
| **📊 Rozpočet města (Sankey)** | Vizuální diagramy příjmů a výdajů: skutečnost 2025 (404 mil. Kč) a schválený rozpočet 2026 (479 mil. Kč) | [2025](./rozpocet_sankey_2025.png) / [2026](./rozpocet_sankey_2026.png) |
| **📁 Otevřená data (GeoJSON)** | Všech 25 tras se souřadnicemi WGS-84, metadaty, odkazy na Mapy.cz a Google Maps | [trasy_ceskobrodsko.geojson](./trasy_ceskobrodsko.geojson) |

---

## 1. Mapa obnovených cest a stezek Českobrodska

![Mapa obnovených stezek Českobrodska 2020–2026+](./mapa_stezky_podle_roku.png)

### Způsob zobrazení tras v mapě
- **Plná čára (13 tras):** Trasy zmapované a ověřené v datech OpenStreetMap / Mapy.cz (např. polní cesta P3 Na Útulně, HPC 4, Topolovka, Stezka B. Jedličky-Brodského, Šemberské singletraily, Kudrnáčova stezka, Mrzecká cesta, NS Klepec a městské chodníky).
- **Čárkovaná čára (12 tras):** Plánované úseky, biokoridory či orientační spojnice v přípravě (např. cyklostezka Nad Malechovem – Přistoupim, stezka podél II/245 do Štolmíře, nábřežní cyklostezka pod Malechovem).

### Přehled všech 25 tras

| # | Název trasy | Odkud → Kam | Rok / Stav | Mapy.cz |
| :-: | :--- | :--- | :-: | :-: |
| **1** | Polní cesta P9 | Štolmíř → Kounická (Mexiko) | 2020–2021 | ✅ Ano |
| **2** | Hlavní polní cesta HPC 4 | Štolmíř → směr Břežany II | 2020–2021 | ✅ Ano |
| **3** | Polní cesta P3 + mokřad Na Útulně | Český Brod (V Lukách) → Štolmíř | 2024 | ✅ Ano |
| **4** | Přírodní cesta a alej Topolovka | Topolová / Pod Hájem → Štolmíř | 2024 | ⚠️ Částečně |
| **5** | Biokoridor LBK 14 Štolmířský potok | Trať u Štolmíře → podél potoka | 2022–2023 | ⚠️ Částečně |
| **6** | Polní cesta P6 | Rostoklaty → směr Břežany II | 2022–2023 | ✅ Ano |
| **7** | Mlýnská cesta C6 | Tuklaty / Tlustovousy → Břežany II | 2022–2023 | ✅ Ano |
| **8** | Stezka Břetislava Jedličky-Brodského | Kouřimská brána → sv. Gothard → Liblice | 2024 | ✅ Ano |
| **9** | Cyklostezka podél pravého břehu Šembery | Havlíčkova → Pod Malechovem | 2026 | ⚠️ Částečně |
| **10** | Nová lipová alej u hřbitova | Ul. Klučovská → podél hřbitova | 2026 | ⚠️ Částečně |
| **11** | Obnovená cesta a Alej do Klučova | Za Drahou → Klučov | 2022–2023 | ⚠️ Částečně |
| **12** | Kudrnáčova stezka | Klučov → hradiště → Poříčany | 2022–2023 | ✅ Ano |
| **13** | Alej „Žherák“ | Klučov → Žhery | 2024 | ✅ Ano |
| **14** | Polní cesta Skramníky – Tatce | Východní okraj Skramníků → Tatce | 2024 | ⚠️ Částečně |
| **15** | Cesta C4 a Kočárová cesta KZ 7 | Chrášťany → Chotouň | 2025 | ⚠️ Částečně |
| **16** | Cyklostezka Nad Malechovem – Přistoupim | Nad Malechovem → Přistoupim | Plán 2026+ | 🚧 V přípravě |
| **17** | Stezka Č. Brod – Štolmíř (podél II/245) | Žitomířská → Českobrodská | Plán 2026+ | 🚧 V přípravě |
| **18** | Stezka Na Kutilce k Podviňáku | Sportovní areál → rybník Podviňák | 2024 | ✅ Ano |
| **19** | Šemberské stezky (singletraily) | Les za Tuchorazí (5 km MTB trailů) | 2020–2021 | ✅ Ano |
| **20** | Zastavení u Šembery + Lávka u Skautské louky | Na Šamtalech → Skautská louka → Na Zámkách | 2024 | ✅ Ano |
| **21** | Hravá NS Ekocentrum Vrátkov | Tuchoraz → hájovna Vrátkov | 2022–2023 | ⚠️ Částečně |
| **22** | Mrzecká cesta a alej | Limuzy → Mrzky | 2026 | ✅ Ano |
| **23** | Obnovená Naučná stezka Klepec | Skřivany → vrch Klepec (358 m) | 2026 | ✅ Ano |
| **24** | Nové chodníky 2024–2026 | Štolmířská, Žižkova, Komenského | 2026 | ✅ Ano |
| **25** | Opravené chodníky 2020–2023 | Palackého, Bezručova, Krále Jiřího | 2020–2021 | ✅ Ano |

---

## 2. Rozpočet města Český Brod (App Economy Insights)

Infografika zachycuje toky peněz od daňových příjmů a dotací přes provozní výdaje až po jmenovité investiční akce:

### Skutečnost roku 2025 (404,1 mil. Kč)
![Rozpočet Český Brod 2025 — Sankey diagram](./rozpocet_sankey_2025.png)

- **Příjmy:** 396,1 mil. Kč (daně RUD 218,3 mil. Kč, dotace 118,2 mil. Kč, nedaňové a kapitálové 59,6 mil. Kč).
- **Výdaje:** 404,1 mil. Kč (provoz 257,2 mil. Kč / 63,6 %, investice 146,9 mil. Kč / 36,4 %).
- **Hlavní investice:** Přístavba ZŠ Žitomířská (64,5 mil. Kč), MŠ Kollárova (26,4 mil. Kč), rekonstrukce ulic a stezek z Fondu komunikací (24,2 mil. Kč).

### Schválený rozpočet roku 2026 (478,7 mil. Kč)
![Rozpočet Český Brod 2026 — Sankey diagram](./rozpocet_sankey_2026.png)

- **Výdaje:** 478,7 mil. Kč (provoz 287,5 mil. Kč / 60,1 %, investice 191,2 mil. Kč / 39,9 %).
- **Klíčové investice:** Novostavba MŠ Kollárova (61,0 mil. Kč), dokončení ZŠ Žitomířská (59,0 mil. Kč), projektová dokumentace nového náměstí (10,8 mil. Kč) a Fond komunikací (19,0 mil. Kč).

---

## 💻 Spuštění lokálně

1. Webovou aplikaci můžete otevřít v libovolném prohlížeči otevřením souboru [`index.html`](./index.html).
2. Přegenerování map a synchronizace dat:
   ```bash
   python generate_maps.py
   ```
