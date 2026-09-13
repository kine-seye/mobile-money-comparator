# Comparateur de frais Mobile Money — Sénégal

API qui compare en temps réel les frais de transfert, retrait et dépôt entre **Wave**, **Orange Money** et **Yas (Mixx by Yas)** au Sénégal, taxe TTA incluse.

🔗 **API en ligne :** https://mobile-money-comparator-api.onrender.com/docs

## Pourquoi ce projet

Les 3 principaux opérateurs mobile money du Sénégal ont des grilles tarifaires publiées séparément, dans des formats différents (pourcentage simple, pourcentage plafonné, taxe incluse ou non). Ce projet centralise ces données dans un modèle unique et calcule le coût réel d'une opération, taxe d'État comprise.

## Stack technique

- **Base de données :** PostgreSQL (modélisation par tranches de montant)
- **Backend :** Python, FastAPI
- **Déploiement :** Render (base + API)

## Modèle de données

Le cœur du projet est la table `grille_tarifaire`, qui représente chaque tarif comme une **tranche de montant** (`montant_min` → `montant_max`) avec un frais fixe et/ou un pourcentage. Ce choix permet de représenter fidèlement des règles réelles comme *"1%, plafonné à 5000 FCFA"* en la décomposant en deux tranches (une avec pourcentage, une avec frais fixe au-delà du plafond).

## Choix méthodologiques et limites connues

- **Scope volontairement limité à 3 opérations** (retrait, transfert, dépôt). Le paiement marchand a été exclu : sa tarification réelle repose sur un cumul journalier par commerçant, une logique incompatible avec un modèle par tranche de montant unitaire — une évolution possible en V2.
- **Taxe TTA (0,5%, plafonnée à 2000 FCFA)** appliquée séparément du frais opérateur pour Wave et Orange Money, sauf pour Yas où elle est déjà incluse dans le taux affiché — cas géré explicitement dans le code de calcul.
- **Toutes les données sont sourcées** (site officiel de chaque opérateur, MomoCalc, ou expérience personnelle documentée comme telle) avec date de vérification — voir `data/grille_tarifaire_template.csv`.

## Utilisation de l'API

Retourne les 3 opérateurs classés du moins cher au plus cher, avec le détail frais opérateur / TTA / total.

## Installation en local

\`\`\`bash
pip install -r requirements.txt
# configurer .env (voir .env.example)
psql -d ta_base -f db/schema.sql
psql -d ta_base -f db/seed_reference_data.sql
python scripts/import_tarifs.py
cd app && uvicorn main:app --reload
\`\`\`