# Volatility Smile Analyzer

Une application pour récupérer les prix des options via API, analyser le volatility smile et visualiser les données en 2D et 3D.

## Description

Ce projet permet de :
- Récupérer les prix courants des options via une API
- Calculer et analyser le volatility smile
- Visualiser le volatility smile en 2D et 3D
- Interagir avec l'application via une interface Streamlit avec des curseurs pour ajuster les paramètres

## Prérequis

- Python 3.8+
- pip

## Installation

1. Cloner le repository
```bash
git clone https://github.com/yourusername/volatility_smile.git
cd volatility_smile
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API
```

## Utilisation

Lancer l'application Streamlit :
```bash
streamlit run app/streamlit_app.py
```

## Structure du projet

```
volatility_smile/
├── src/                 # Code source principal
│   ├── api/            # Module pour récupérer les données via API
│   ├── analysis/       # Analyse du volatility smile
│   └── visualization/  # Visualisation 2D/3D
├── app/                # Application Streamlit
├── config/             # Configuration et settings
├── tests/              # Tests unitaires
├── data/               # Données locales
├── requirements.txt    # Dépendances
├── .env.example        # Exemple de fichier .env
├── .gitignore         # Fichiers à ignorer dans Git
└── README.md          # Documentation
```

## Configuration

Voir le fichier `.env.example` pour la configuration requise (clé API, etc.)

## API Support

Ce projet supporte les APIs pour les options (à spécifier selon votre choix):
- Exemple : Alpha Vantage, IEX Cloud, etc.

## Contribution

Les contributions sont les bienvenues ! Veuillez créer une branche pour vos modifications.

## License

Voir le fichier [LICENSE](LICENSE)

## Contact

Pour des questions, veuillez ouvrir une issue sur GitHub.
