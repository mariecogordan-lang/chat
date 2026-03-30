
import csv

COMMUNES_METROPOLE = {
    "Ambarès-et-Lagrave", "Ambès", "Artigues-près-Bordeaux", "Bassens", "Bègles",
    "Blanquefort", "Bordeaux", "Bouliac", "Le Bouscat", "Bruges", "Carbon-Blanc",
    "Cenon", "Eysines", "Floirac", "Gradignan", "Le Haillan", "Lormont",
    "Martignas-sur-Jalle", "Mérignac", "Parempuyre", "Pessac", "Saint-Aubin-de-Médoc",
    "Saint-Louis-de-Montferrand", "Saint-Médard-en-Jalles", "Saint-Vincent-de-Paul",
    "Le Taillan-Médoc", "Talence", "Villenave-d'Ornon"
}

# Bounding box approximative pour Bordeaux Métropole
LAT_MIN, LAT_MAX = 44.75, 45.00
LONG_MIN, LONG_MAX = -0.80, -0.40

file_path = "RAW_met_lieux_inclusion_numerique - RAW_met_lieux_inclusion_numerique.csv"

outliers = []
stats = {"total": 0, "hors_metropole_commune": 0, "hors_metropole_gps": 0, "gps_invalide": 0}

with open(file_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stats["total"] += 1
        nom = row.get("nom")
        commune = row.get("adresse_commune", "").strip()
        lat_str = row.get("latitude")
        lon_str = row.get("longitude")

        is_outlier = False
        reasons = []

        # Vérification Commune
        if commune not in COMMUNES_METROPOLE:
            stats["hors_metropole_commune"] += 1
            is_outlier = True
            reasons.append(f"Commune inconnue: {commune}")

        # Vérification GPS
        try:
            if lat_str and lon_str:
                lat = float(lat_str)
                lon = float(lon_str)
                
                if not (LAT_MIN <= lat <= LAT_MAX) or not (LONG_MIN <= lon <= LONG_MAX):
                    stats["hors_metropole_gps"] += 1
                    is_outlier = True
                    reasons.append(f"GPS hors limites: ({lat}, {lon})")
            else:
                stats["gps_invalide"] += 1
                is_outlier = True
                reasons.append("Coordonnées GPS absentes")
        except ValueError:
            stats["gps_invalide"] += 1
            is_outlier = True
            reasons.append(f"GPS invalide: ({lat_str}, {lon_str})")

        if is_outlier:
            outliers.append({
                "id": row.get("id"),
                "nom": nom,
                "commune": commune,
                "reasons": reasons
            })

print(f"--- Statistiques ---")
print(f"Total de lignes : {stats['total']}")
print(f"Lieux hors communes Métropole : {stats['hors_metropole_commune']}")
print(f"Lieux avec GPS hors limites : {stats['hors_metropole_gps']}")
print(f"Lieux avec GPS invalide/absent : {stats['gps_invalide']}")
print(f"\n--- Détails des anomalies ({len(outliers)}) ---")
for o in outliers:
    print(f"ID {o['id']} - {o['nom']} ({o['commune']}) : {', '.join(o['reasons'])}")
