
import csv
import json

file_path = "RAW_met_lieux_inclusion_numerique - RAW_met_lieux_inclusion_numerique.csv"
data = []

# Extraction des données
with open(file_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            # On ne garde que ceux avec des coordonnées GPS valides
            if row.get('latitude') and row.get('longitude'):
                data.append({
                    'nom': row.get('nom', 'Sans nom'),
                    'commune': row.get('adresse_commune', 'Inconnue'),
                    'type': row.get('type_lieu', ''),
                    'lat': float(row.get('latitude')),
                    'lon': float(row.get('longitude'))
                })
        except (ValueError, TypeError):
            continue

# Construction du HTML Leaflet
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Carte Inclusion Numérique - Bordeaux Métropole</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        body { margin: 0; padding: 0; font-family: sans-serif; }
        #map { height: 100vh; width: 100%; }
        .leaflet-popup-content b { color: #2c3e50; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Initialisation de la carte sur Bordeaux
        const map = L.map('map').setView([44.837789, -0.57918], 12);

        // Fond de carte OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // Données injectées
        const places = """ + json.dumps(data) + """;

        // Ajout des marqueurs
        places.forEach(place => {
            const popupContent = `
                <b>${place.nom}</b><br>
                ${place.commune}<br>
                <small>${place.type}</small>
            `;
            L.marker([place.lat, place.lon])
                .addTo(map)
                .bindPopup(popupContent);
        });
    </script>
</body>
</html>
"""

with open('carte.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"La carte a été générée avec succès : {len(data)} points affichés.")
