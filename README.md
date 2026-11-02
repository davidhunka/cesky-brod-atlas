# Českobrodsko — atlas cest a městských financí

Interaktivní přehled 25 evidovaných cest a stezek, doplněný o výletní trasy do širšího okolí Českého Brodu a veřejné finance města.

**[Otevřít atlas](https://davidhunka.github.io/cesky-brod-atlas/)**

> Geometrie tras je orientační, ne geodetické zaměření ani navigační pokyn. Označení OSM samo o sobě nepotvrzuje realizaci. Finanční část odděluje hlavní rozpočet od VHČ; nejde o konsolidované účetní výkazy.

## Podrobnější přehled

- [Trasy, zdroje a metodika zákresu](docs/routes.md)
- [Rozpočty a hospodářská činnost](docs/finances.md)
- [Metodika, technické poznámky a licence](docs/methodology.md)
- [GeoJSON tras](data/trasy_ceskobrodsko.geojson)
- [Statická mapa Českobrodska](assets/maps/mapa_stezky_podle_roku.svg)

## Spuštění a generování

Požadavky: Python 3 a Node.js / npm. Statická stránka zůstává v kořeni repozitáře pro GitHub Pages.

```powershell
npm ci
npm run build
py -3 -m http.server 8000
python scripts/generate_maps.py
python scripts/generate_budget_sankey.py
```

Otevři `http://localhost:8000`. `scripts/generate_maps.py` bere zdrojové trasy z `ROUTES` v `index.html`; generované GeoJSON patří do `data/`, mapové exporty do `assets/maps/` a finanční diagramy do `assets/finance/`. Mapové podklady v `data/cache/` jsou pracovní vstupy generátoru.
