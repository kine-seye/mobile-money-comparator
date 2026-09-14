import os
from fastapi import FastAPI, HTTPException
import psycopg2
from dotenv import load_dotenv
from calcul import comparer_operateurs

load_dotenv()
app = FastAPI(title="Comparateur Mobile Money Sénégal")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

@app.get("/comparer")
def comparer(type_operation: str, montant: float):
    if montant <= 0:
        raise HTTPException(status_code=400, detail="Le montant doit être positif")

    conn = get_connexion()
    cur = conn.cursor()

    try:
        resultats = comparer_operateurs(cur, type_operation, montant)
    finally:
        cur.close()
        conn.close()

    if not resultats:
        raise HTTPException(status_code=404, detail="Aucune donnée pour ce type d'opération")

    return {
        "type_operation": type_operation,
        "montant": montant,
        "resultats": resultats
    }