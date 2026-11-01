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

| # | Název trasy | Odkud → Kam | Rok / Stav | Mapy.cz | Zdroj existence a ověření (přímý odkaz) |
| :-: | :--- | :--- | :-: | :-: | :--- |
| **1** | Polní cesta P9 | Štolmíř → Kounická (Mexiko) | 2020–2021 | ✅ Ano | [SPÚ & MZe – Zakázka „Výstavba polní cesty P 9 v k.ú. Štolmíř“ (PDF)](https://zakazky.eagri.cz/document_audit_12838/c03811b5be611464e043821411aca521-pdf) |
| **2** | Hlavní polní cesta HPC 4 | Štolmíř → směr Břežany II | 2020–2021 | ✅ Ano | [SPÚ Kolín – KoPÚ Štolmíř: Hlavní polní cesta HPC 4 (591 m)](https://spu.gov.cz/pozemkove-upravy/program-rozvoje-venkova/projekty/projekty-zrealizovane) |
| **3** | Polní cesta P3 + mokřad Na Útulně | Český Brod (V Lukách) → Štolmíř | 2024 | ✅ Ano | [Město Český Brod – Koncepční studie a úpravy lokality Na Útulně u cesty P3](https://www.ns.cesbrod.cz/item/verejne-setkani-na-utulne) |
| **4** | Přírodní cesta a alej Topolovka | Topolová / Pod Hájem → Štolmíř | 2024 | ⚠️ Částečně | [Broďáci Brodu – Zútulnění pěších tras z Brodu na Štolmíř (Topolovka)](https://www.participativni-rozpocet.cz/ceskybrod/navrhy/zutulneni-pesich-tras-z-brodu-na-stolmir/) |
| **5** | Biokoridor LBK 14 Štolmířský potok | Trať u Štolmíře → podél potoka | 2022–2023 | ⚠️ Částečně | [SPÚ Kolín – Projektový list „Výsadba biokoridoru LBK 14 v k.ú. Štolmíř“ (PDF)](https://spu.gov.cz/frontend/webroot/uploads/files/2018/01/vysadba_biokoridoru_lbk_14_v_k7383.u7383._stolmir7383.pdf) |
| **6** | Polní cesta P6 | Rostoklaty → směr Břežany II | 2022–2023 | ✅ Ano | [SPÚ Kolín – Projektový list KoPÚ v k.ú. Rostoklaty a Nová Ves II (PDF)](https://spu.gov.cz/frontend/webroot/uploads/files/2020/05/realizace_lokalnich_biocenter_bc_4_a_bc_6_v_k10370.u10370._nova_ves_ii10370._a_bc_2a_v_k10370.u10370._rostoklaty10370.pdf) |
| **7** | Mlýnská cesta C6 | Tuklaty / Tlustovousy → Břežany II | 2022–2023 | ✅ Ano | [SPÚ Kolín – Projektový list „Polní cesta C 6 v k.ú. Tuklaty a Břežany II“ (PDF)](https://spu.gov.cz/frontend/webroot/uploads/files/2018/01/polni_cesta_c_6_v_k7388.u7388._tuklaty7388.pdf) |
| **8** | Stezka Břetislava Jedličky-Brodského | Kouřimská brána → sv. Gothard → Liblice | 2024 | ✅ Ano | [IC CVIK ČB – Stezka B. Jedličky-Brodského](https://ic.cvik.info/stezka-bretislava-jedlicky-brodskeho) & [Registr smluv č. 33545964 (V Podskalí)](https://smlouvy.gov.cz/smlouva/33545964) |
| **9** | Cyklostezka podél pravého břehu Šembery | Havlíčkova → Pod Malechovem | 2026 | ⚠️ Částečně | [Usnesení ČB příloha 7381 (p.č. 118/1 a 118/7)](https://usneseni.cesbrod.cz/usneseni/usneseni/priloha/7381) & [Situace DSP (PDF)](https://lotus.cesbrod.cz/MUCB%5Carz.nsf/0/E69C91EF472CB0EEC125878F00318694/%24file/z199_SITUACE_DSP_PRACOVNI_211117_PREDAVANE.pdf) |
| **10** | Nová lipová alej u hřbitova | Ul. Hřbitovní → podél hřbitova | 2026 | ⚠️ Částečně | [Sázíme stromy č. 1622 (1. etapa)](https://sazimestromy.cz/sazeni/1622) & [č. 1715 (2. etapa u hřbitova)](https://sazimestromy.cz/sazeni/1715) |
| **11** | Obnovená cesta a Alej do Klučova | Za Drahou → Klučov | 2022–2023 | ⚠️ Částečně | [Českobrodský zpravodaj – zakázka „Alej Klučov – Český Brod“ (PDF)](https://cesbrod.cz/files/ceskybrod/gallery/12171/66ac980452048_CeskobrodskyZpravodaj-2020-rijen.pdf) |
| **12** | Kudrnáčova stezka | Klučov → hradiště → Poříčany | 2022–2023 | ✅ Ano | [Naučné-stezky.cz – Kudrnáčova stezka](https://www.naucne-stezky.cz/kudrnacova-stezka/) & [Sázíme stromy č. 1314](https://sazimestromy.cz/sazeni/1314) |
| **13** | Alej „Žherák“ | Klučov → Žhery | 2024 | ✅ Ano | [Sázíme stromy č. 950 – „Z Klučova na Žhery krásným stromořadím“](https://sazimestromy.cz/sazeni/950) |
| **14** | Polní cesta Skramníky – Tatce | Východní okraj Skramníků → Tatce | 2024 | ⚠️ Částečně | [Sázíme stromy č. 1143 – Obnova a výsadba na polní cestě Skramníky – Tatce](https://sazimestromy.cz/sazeni/1143) |
| **15** | Cesta C4 a Kočárová cesta KZ 7 | Chrášťany → Chotouň | 2025 | ⚠️ Částečně | [SPÚ Kolín – Projektový list „Polní cesta C4 a KZ7 v k.ú. Chrášťany u ČB“ (PDF)](https://spu.gov.cz/frontend/webroot/uploads/files/2025/01/polni_cesta_c4_v_k24503.u24503._chrastany_u_cb_s_doprovodnou_zeleni_a_vysadbou_zelene_v_doprovodnem_prvku_kz7_224503.pdf) |
| **16** | Cyklostezka Nad Malechovem – Přistoupim | Nad Malechovem → Přistoupim | Plán 2026+ | 🚧 V přípravě | [Článek místostarosty T. Klineckého – Cyklostezka ČB – Přistoupim (600 m)](https://www.top09.cz/regiony/stredocesky-kraj/top-09-v-mediich/klinecky-nova-cyklostezka-spoji-cesky-brod-se-sousedni-obci-30834.html) |
| **17** | Stezka Č. Brod – Štolmíř (podél II/245) | Žitomířská → Českobrodská | Plán 2026+ | 🚧 V přípravě | [Generel cyklodopravy města Český Brod – stezka podél II/245 (PDF)](https://cesbrod.cz/files/ceskybrod/gallery/12024/668e6669c9eac_Generel-cyklodopravy-text.pdf) |
| **18** | Stezka Na Kutilce k Podviňáku | Sportovní areál → rybník Podviňák | 2024 | ✅ Ano | [Zastupitelstvo ČB (Tisk 44): Urbanistická studie areálu Kutilka (PDF)](https://lotus.cesbrod.cz/__C1257E4D002B7D3A.nsf/0/61248EEEB1D71D30C125855F0049BC1E/%24File/Tisk_44_Jakub%20Nekoln%C3%BD_Zpracov%C3%A1n%C3%AD%20urbanistick%C3%A9%20studie%20are%C3%A1lu%20Kutilka.pdf?OpenElement) |
| **19** | Šemberské stezky (singletraily) | Les za Tuchorazí (5 km MTB trailů) | 2020–2021 | ✅ Ano | [Spolek Šemberské stezky z.s. – Oficiální mapa a popis singletrailů](https://www.semberskestezky.cz/) |
| **20** | Zastavení u Šembery + Lávka u Skautské louky | Na Šamtalech → Skautská louka → Na Zámkách | 2024 | ✅ Ano | [Město ČB – Zastavení u Šembery a lávka](https://cesbrod.cz/default/default/24199_nadace-cez) & [E-ZAK VZ00000164 (Altán)](https://ezak.cesbrod.cz/vz00000164) |
| **21** | Hravá NS Ekocentrum Vrátkov | Tuchoraz → hájovna Vrátkov | 2022–2023 | ⚠️ Částečně | [Město ČB – Projekt Ekocentrum Vrátkov](https://cesbrod.cz/default/default/18045_ekocentrum-vratkov) & [ekocentrumvratkov.cz](https://www.ekocentrumvratkov.cz/) |
| **22** | Mrzecká cesta a alej | Limuzy → Mrzky | 2026 | ✅ Ano | [Obec Tismice – Obnova aleje na Mrzecké cestě (parc. 688 k.ú. Limuzy)](https://www.tismice.cz/obec/aktuality/do-jasanove-aleje-na-mrzecke-ceste-vstup-jen-na-vlastni-nebezpeci-443cs.html) |
| **23** | Obnovená Naučná stezka Klepec | Skřivany → vrch Klepec (358 m) | 2026 | ✅ Ano | [Obec Přišimasy – „Klepec má novou naučnou stezku“ (obnova 2025)](https://www.prisimasy.cz/zivot-v-obci/aktuality/klepec-ma-novou-naucnou-stezku-1623cs.html) |
| **24** | Nové chodníky 2024–2026 | Štolmířská, Sportovní, Želivského | 2026 | ✅ Ano | [E-ZAK ČB dok. č. 3425 (Štolmířská)](https://ezak.cesbrod.cz/document_download_3425.html) & [zakázka č. 222 (Sportovní)](https://ezak.cesbrod.cz/contract_display_222.html) |
| **25** | Opravené chodníky 2020–2023 | Palackého, Zborovská, Krále Jiřího | 2020–2021 | ✅ Ano | [E-ZAK ČB zakázka č. 225 – Chodníky Zborovská, Jana Kouly a Krále Jiřího](https://ezak.cesbrod.cz/contract_display_225.html) |

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
