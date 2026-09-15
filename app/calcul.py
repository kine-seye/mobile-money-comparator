


def trouver_tranche(cur, operateur_id, type_operation_id, montant):
    cur.execute("""
        SELECT frais_fixe, frais_pourcentage
        FROM grille_tarifaire
        WHERE operateur_id = %s
          AND type_operation_id = %s
          AND montant_min <= %s
          AND (montant_max IS NULL OR montant_max >= %s)
    """, (operateur_id, type_operation_id, montant, montant))
    return cur.fetchone()


def calculer_frais_operateur(frais_fixe, frais_pourcentage, montant):
    return float(frais_fixe) + (float(montant) * float(frais_pourcentage))


TAUX_TTA = 0.005
PLAFOND_TTA = 2000

def calculer_tta(montant, operateur_nom, type_operation_nom):
    # La TTA (Loi 2025-17) s'applique légalement aux transferts, paiements et retraits — PAS au dépôt.
    # Seul Orange Money a confirmé officiellement la collecter.
    # Wave : aucune TTA constatée en usage réel, sur aucune opération.
    # Yas : la TTA est déjà incluse dans le taux de retrait affiché (1%).
    if type_operation_nom == "depot":
        return 0
    if operateur_nom == "Orange Money":
        return min(float(montant) * TAUX_TTA, PLAFOND_TTA)
    return 0
def calculer_frais_total(cur, operateur_id, operateur_nom, type_operation_id, type_operation_nom, montant):
    tranche = trouver_tranche(cur, operateur_id, type_operation_id, montant)
    if tranche is None:
        return None  # aucune tranche ne couvre ce montant pour cet opérateur/opération

    frais_fixe, frais_pourcentage = tranche
    frais_operateur = calculer_frais_operateur(frais_fixe, frais_pourcentage, montant)
    tta = calculer_tta(montant, operateur_nom, type_operation_nom)

    return {
        "frais_operateur": round(frais_operateur, 2),
        "tta": round(tta, 2),
        "frais_total": round(frais_operateur + tta, 2)
    }


def comparer_operateurs(cur, type_operation_nom, montant):
    cur.execute("SELECT id, nom FROM operateurs ORDER BY nom")
    operateurs = cur.fetchall()

    cur.execute("SELECT id FROM types_operation WHERE nom = %s", (type_operation_nom,))
    type_operation_id = cur.fetchone()[0]

    resultats = []
    for operateur_id, operateur_nom in operateurs:
        detail = calculer_frais_total(
            cur, operateur_id, operateur_nom,
            type_operation_id, type_operation_nom, montant
        )
        if detail is not None:
            resultats.append({"operateur": operateur_nom, **detail})

    resultats.sort(key=lambda r: r["frais_total"])
    return resultats


if __name__ == "__main__":
    import os
    import psycopg2
    from dotenv import load_dotenv

    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"), dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    resultats = comparer_operateurs(cur, "transfert", 10000)
    for r in resultats:
        print(r)

    cur.close()
    conn.close()

   