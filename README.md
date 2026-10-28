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

| # | Název trasy | Odkud → Kam | Rok / Stav | Mapy.cz | Zdroj existence a ověření |
| :-: | :--- | :--- | :-: | :-: | :--- |
| **1** | Polní cesta P9 | Štolmíř → Kounická (Mexiko) | 2020–2021 | ✅ Ano | SPÚ Kolín – KoPÚ k.ú. Štolmíř (cesta P9) & Odbor rozvoje města Český Brod |
| **2** | Hlavní polní cesta HPC 4 | Štolmíř → směr Břežany II | 2020–2021 | ✅ Ano | SPÚ Kolín – KoPÚ Štolmíř (hlavní polní cesta HPC 4, kolaudace 2021, Středočeská ovocná stezka) |
| **3** | Polní cesta P3 + mokřad Na Útulně | Český Brod (V Lukách) → Štolmíř | 2024 | ✅ Ano | Město Český Brod – profil zadavatele E-ZAK (zakázka „Polní cesta P3 a biocentrum Na Útulně“, OPŽP) |
| **4** | Přírodní cesta a alej Topolovka | Topolová / Pod Hájem → Štolmíř | 2024 | ⚠️ Částečně | Město Český Brod – Broďáci Brodu & spolek Sázíme stromy (výsadby a obnova cesty 2021–2025) |
| **5** | Biokoridor LBK 14 Štolmířský potok | Trať u Štolmíře → podél potoka | 2022–2023 | ⚠️ Částečně | SPÚ Kolín – realizace plánu společných zařízení (biokoridor LBK 14 Štolmířský potok, 1,2 mil. Kč) |
| **6** | Polní cesta P6 | Rostoklaty → směr Břežany II | 2022–2023 | ✅ Ano | SPÚ Kolín – KoPÚ k.ú. Rostoklaty (polní cesta P6 s doprovodnou zelení, ÚP Rostoklaty) |
| **7** | Mlýnská cesta C6 | Tuklaty / Tlustovousy → Břežany II | 2022–2023 | ✅ Ano | SPÚ Kolín – KoPÚ Tuklaty a Břežany II (polní cesta C6 „Mlýnská“, 1,3 km asfalt + alej, 2022) |
| **8** | Stezka Břetislava Jedličky-Brodského | Kouřimská brána → sv. Gothard → Liblice | 2024 | ✅ Ano | Město Český Brod – Odbor rozvoje & TS Český Brod (obnova nábřežní stezky Šembery 2021–2024) |
| **9** | Cyklostezka podél pravého břehu Šembery | Havlíčkova → Pod Malechovem | 2026 | ⚠️ Částečně | Město Český Brod – Schválený rozpočet 2025/2026 (výkupy parcel 118/1 a 118/7 u PRO-DOMA, E-ZAK) |
| **10** | Nová lipová alej u hřbitova | Ul. Klučovská → podél hřbitova | 2026 | ⚠️ Částečně | Spolek Sázíme stromy & Město Český Brod (komunitní výsadba 20 vzrostlých lip u hřbitova, březen 2026) |
| **11** | Obnovená cesta a Alej do Klučova | Za Drahou → Klučov | 2022–2023 | ⚠️ Částečně | Obec Klučov & spolek NeKluč z.s. ve spolupráci s městem Český Brod (obnova polní cesty a aleje) |
| **12** | Kudrnáčova stezka | Klučov → hradiště → Poříčany | 2022–2023 | ✅ Ano | Klub českých turistů (KČT), Obec Klučov & MAS Zálabí (obnova historické stezky a alejí 2022–2026) |
| **13** | Alej „Žherák“ | Klučov → Žhery | 2024 | ✅ Ano | Obec Klučov & spolek Sázíme stromy (výsadba 34 stromů podél cesty do Žher 2022–2024) |
| **14** | Polní cesta Skramníky – Tatce | Východní okraj Skramníků → Tatce | 2024 | ⚠️ Částečně | Obec Klučov (Skramníky) a Obec Tatce ve spolupráci se spolkem Sázíme stromy (březen 2024) |
| **15** | Cesta C4 a Kočárová cesta KZ 7 | Chrášťany → Chotouň | 2025 | ⚠️ Částečně | SPÚ Kolín – KoPÚ Chrášťany u Českého Brodu (polní cesta C4 a kočárová cesta KZ 7, dokončeno 2025) |
| **16** | Cyklostezka Nad Malechovem – Přistoupim | Nad Malechovem → Přistoupim | Plán 2026+ | 🚧 V přípravě | Město Český Brod a Obec Přistoupim – Smlouva o spolupráci a profil E-ZAK (příprava cyklostezky III/1131) |
| **17** | Stezka Č. Brod – Štolmíř (podél II/245) | Žitomířská → Českobrodská | Plán 2026+ | 🚧 V přípravě | Město Český Brod – profil zadavatele E-ZAK (vysoutěžená PD na páteřní cyklostezku podél II/245) |
| **18** | Stezka Na Kutilce k Podviňáku | Sportovní areál → rybník Podviňák | 2024 | ✅ Ano | Město Český Brod – Fond komunikací & participativní rozpočet Broďáci Brodu (areál Na Kutilce) |
| **19** | Šemberské stezky (singletraily) | Les za Tuchorazí (5 km MTB trailů) | 2020–2021 | ✅ Ano | Spolek Šemberské stezky z.s. & Obec Tuchoraz (oficiální 5km lesní MTB singletraily od r. 2020) |
| **20** | Zastavení u Šembery + Lávka u Skautské louky | Na Šamtalech → Skautská louka → Na Zámkách | 2024 | ✅ Ano | Městské lesy Český Brod s.r.o. (lávka u Skautské louky, 3 odpočívadla a rekonstrukce Cesty lásky 2025) |
| **21** | Hravá NS Ekocentrum Vrátkov | Tuchoraz → hájovna Vrátkov | 2022–2023 | ⚠️ Částečně | Ekocentrum Vrátkov z.s. & Obec Tuchoraz s podporou Fondu hejtmanky Středočeského kraje (2021–2023) |
| **22** | Mrzecká cesta a alej | Limuzy → Mrzky | 2026 | ✅ Ano | Obec Tismice – Program rozvoje obce, obnova aleje na parc. 688 k.ú. Limuzy (Ovocná stezka) |
| **23** | Obnovená Naučná stezka Klepec | Skřivany → vrch Klepec (358 m) | 2026 | ✅ Ano | Obec Přišimasy – Program obnovy venkova Středočeského kraje (rekonstrukce NS Klepec, říjen 2026) |
| **24** | Nové chodníky 2024–2026 | Štolmířská, Žižkova, Komenského | 2026 | ✅ Ano | Město Český Brod – profil E-ZAK, Fond komunikací města a TS Český Brod (veřejné zakázky chodníků) |
| **25** | Opravené chodníky 2020–2023 | Palackého, Bezručova, Krále Jiřího | 2020–2021 | ✅ Ano | Město Český Brod – Státní fond dopravní infrastruktury (SFDI) a IROP (dotační programy bezpečnosti) |

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