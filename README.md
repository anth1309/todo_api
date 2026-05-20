# 📝 ToDo List API - FastAPI

## 🚀 Présentation

API REST de gestion de tâches développée avec FastAPI.

Ce projet a été réalisé dans un objectif d’apprentissage backend afin de comprendre :

- l’architecture d’une API REST
- la gestion de données en JSON
- la structuration en couches (service / models)
- les filtres dynamiques
- les opérations CRUD

---

## ⚙️ Stack technique

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## 🧠 Fonctionnalités

- CRUD complet des tâches
- Ajout / suppression / modification de tâches
- Recherche par mot-clé
- Filtrage (done / priority)
- Tri automatique des tâches
- Stockage local en JSON

---

## 🏗️ Architecture du projet

- `main.py` → routes FastAPI (API)
- `service.py` → logique métier
- `models.py` → structure des données (Task)
- `storage.py` → lecture / écriture JSON

---

## ▶️ Installation

```bash
git clone https://github.com/TON_USER/todo-api.git
cd todo-api
pip install -r requirements.txt
```

▶️ Lancement du serveur

python -m uvicorn main:app --reload
