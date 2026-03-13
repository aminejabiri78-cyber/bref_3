# 📊 Superstore Sales Dashboard

Un tableau de bord interactif développé avec **Streamlit** et **Plotly** pour analyser les ventes, profits et tendances du dataset Superstore, connecté à une base de données **PostgreSQL**.

---

## 🚀 Fonctionnalités

- **KPIs globaux** : Total des ventes, profit total, marge moyenne, nombre de commandes
- **Statistiques descriptives** : Moyenne, médiane, min, max, écart-type sur les ventes et profits
- **Filtres dynamiques** : Filtrage par région, catégorie et année via la sidebar
- **Visualisations interactives** :
  - 📊 Ventes par région (bar chart)
  - 📈 Évolution des ventes dans le temps (line chart)
  - 🏆 Top 10 produits par chiffre d'affaires
  - 👥 Top 10 clients par chiffre d'affaires
  - 🗺️ Heatmap Région × Catégorie

---

## 🗂️ Structure de la base de données

Le dashboard repose sur 5 tables PostgreSQL reliées entre elles :

| Table | Clé principale | Description |
|---|---|---|
| `orders` | `order_id` | En-têtes de commandes |
| `order_details` | `order_id`, `product_id` | Lignes de commande (sales, cost) |
| `customer` | `customer_id` | Informations clients |
| `product` | `product_id` | Catalogue produits (nom, catégorie) |
| `location` | `postal_code` | Données géographiques (région, état) |

**Schéma des jointures :**
```
orders
  └── order_details (order_id)
        └── product (product_id)
  └── customer (customer_id)
  └── location (postal_code)
```

---

## ⚙️ Installation

### Prérequis

- Python 3.8+
- PostgreSQL 13+
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/your-username/superstore-dashboard.git
cd superstore-dashboard
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit
pandas
plotly
sqlalchemy
psycopg2-binary
```

### 3. Configurer la base de données

Créer la base de données PostgreSQL et importer les tables :

```bash
psql -U postgres -c "CREATE DATABASE superstore_db;"
psql -U postgres -d superstore_db -f schema.sql
```

### 4. Configurer la connexion

Dans `app.py`, modifier l'URL de connexion si nécessaire :

```python
db_url = "postgresql://postgres:admin@localhost:5432/superstore_db"
```

> ⚠️ En production, utiliser des variables d'environnement plutôt que des credentials en dur.

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'application sera disponible sur `http://localhost:8501`.

---

## 📁 Structure du projet

```
superstore-dashboard/
│
├── app.py                  # Application principale Streamlit
├── requirements.txt        # Dépendances Python
├── schema.sql              # Script de création des tables (optionnel)
└── README.md               # Documentation
```

---

## 🧮 Calculs métier

| Métrique | Formule |
|---|---|
| Profit | `sales - cost` |
| Marge | `profit / sales` |
| KPI Sales | `sum(sales)` sur la sélection filtrée |
| KPI Profit | `sum(profit)` sur la sélection filtrée |

---

## 🔒 Bonnes pratiques recommandées

- Stocker les credentials DB dans des **variables d'environnement** (`.env` + `python-dotenv`)
- Ajouter un fichier `.gitignore` pour exclure les fichiers sensibles
- Utiliser `@st.cache_data` (déjà en place) pour optimiser les performances de chargement

---

## 🛠️ Technologies utilisées

| Outil | Rôle |
|---|---|
| [Streamlit](https://streamlit.io/) | Framework web interactif |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Visualisations interactives |
| [Pandas](https://pandas.pydata.org/) | Manipulation des données |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM & connexion base de données |
| [PostgreSQL](https://www.postgresql.org/) | Base de données relationnelle |

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
