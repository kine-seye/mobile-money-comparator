import os
import csv
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

def get_id(table, colonne_nom, valeur):
    cur.execute(f"SELECT id FROM {table} WHERE {colonne_nom} = %s", (valeur,))
    resultat = cur.fetchone()
    if resultat is None:
        raise ValueError(f"'{valeur}' introuvable dans la table {table}")
    return resultat[0]

with open("data/grille_tarifaire_template.csv", newline="", encoding="utf-8") as fichier_csv:
    lecteur = csv.DictReader(fichier_csv)
    for ligne in lecteur:
        operateur_id = get_id("operateurs", "nom", ligne["operateur"])
        type_operation_id = get_id("types_operation", "nom", ligne["type_operation"])

        cur.execute("""
            INSERT INTO grille_tarifaire
                (operateur_id, type_operation_id, montant_min, montant_max,
                 frais_fixe, frais_pourcentage, date_maj, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            operateur_id,
            type_operation_id,
            ligne["montant_min"],
            ligne["montant_max"] if ligne["montant_max"] else None,
            ligne["frais_fixe"],
            ligne["frais_pourcentage"],
            ligne["date_maj"],
            ligne["source"]
        ))

conn.commit()
cur.close()
conn.close()
print("Import terminé avec succès.")



