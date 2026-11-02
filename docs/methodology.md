# Technická dokumentace a metodika

## Spuštění a generování

Web v [index.html](../index.html) je statický a nepoužívá vlastní backend. Tailwind CSS se sestavuje lokálně; Leaflet, písma a mapové dlaždice OpenStreetMap se načítají z externích služeb.

```powershell
npm ci
npm run build
py -3 -m http.server 8000
py -3 scripts/generate_maps.py
py -3 scripts/generate_budget_sankey.py
```

Otevři `http://localhost:8000`. `npm run build` obnoví `assets/css/atlas.css`. `scripts/generate_maps.py` bere trasová data z pole `ROUTES` v `index.html` a zapisuje GeoJSON do `data/` a mapové výstupy do `assets/maps/`. Mapový PNG vyžaduje Chromium/Chrome/Edge. Rozpočtová data jsou stále duplicitní v aplikaci a generátoru SVG; před publikováním finančních změn je porovnej s primárními dokumenty.

Aktualizace mapového podkladu nebo pěší geometrie (vyžaduje připojení k internetu):

```powershell
py -3 scripts/fetch_map_data.py
```

## Metodika, aktuálnost a licence

- V repozitáři nejsou u všech položek zaznamenána data posledního ověření; finanční částky a stavy tras zde nejsou nezávislým auditem.
- © OpenStreetMap contributors. Mapová data OSM jsou dostupná pod licencí ODbL; viz [copyright a licenční informace OSM](https://www.openstreetmap.org/copyright). Při dalším použití odvozených dat dodrž podmínky ODbL.
- Repozitář neobsahuje samostatný soubor licence pro zdrojový kód ani původní obsah; práva k převzatým dokumentům a podkladům zůstávají jejich autorům.

## Datové zdroje

- **Cesty a pozemkové úpravy:** Státní pozemkový úřad (Pobočka Kolín), Profil zadavatele města Český Brod (`ezak.cesbrod.cz`), Registr smluv ČR (`smlouvy.gov.cz`), Usnesení Rady a Zastupitelstva města Český Brod (`usneseni.cesbrod.cz`), Generel cyklodopravy města Český Brod, Sázíme stromy z.ú., Spolek NeKluč!, OpenStreetMap.
- **Veřejné finance:** Informační portál Ministerstva financí ČR Monitor (`monitor.statnipokladna.cz`, IČO `00235334`), Závěrečné účty města Český Brod za roky 2023, 2024 a 2025, Schválený rozpočet města Český Brod na rok 2026 (`č. j. 3558/2026`).
