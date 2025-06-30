# Analyseur_cv - version personnalisée
## Description du Projet
Ce projet est basé sur un dépôt existant (https://github.com/Mudassiruddin7/Resume-Parser-with-SpaCy-NLP-Streamlit.git), adapté pour mieux traiter l'extraction des données de CV en format PDF, en français à l'aide de SpaCy et des pipelines sur mesure.

## Modifications apportées
- suppression de la bibliothèque pyresparser, problématique
- Meilleure prise en charge des fichiers PDF en français
- Retrait du logo initial, jugé non pertinent pour le bon fonctionnement de l’application.
- Ajout des compétences détectées dans le CV, intégrées à la liste skills_list.
- Installation du modèle linguistique français fr_core_news_sm de spaCy, ainsi que de la bibliothèque spaCy elle-même, afin de permettre une analyse linguistique adaptée à la langue française.
- Suppression de la fonctionnalité de génération de vidéos et du fichier Courses.py, considérée comme non essentielle au projet.
- Traduction intégrale des commentaires dans le code et des éléments de l’interface utilisateur, initialement en anglais, vers le français.
- Mise en place de la collecte et de l’enregistrement du nom réel du candidat dans la base de données, remplaçant l’affichage générique « Candidat inconnu » issu du code d’origine.
- Ajout d’un pipeline de parsing plus robuste pour l’extraction de données

## Pour démarrer
Instructions simplifiées pour utiliser ma version (en local ou via une API, si c’est le cas) :

git clone https://github.com/Mudassiruddin7/Resume-Parser-with-SpaCy-NLP-Streamlit.git
pip install -r requirements.txt


## Fonctionnalités
L'application permet à l'utilisateur de:

- Faire l'extraction intelligente d’informations (nom, email et compétences)
- Nettoyage et normalisation des données
- Stockage structuré dans une base PostgreSQL / SQLite

## Technologies Utilisées
- [Python](https://www.python.org/) – Langage principal du projet  
- [Streamlit](https://streamlit.io/) – Framework pour créer des interfaces web interactives  
- [spaCy](https://spacy.io/) – Traitement du langage naturel, notamment pour le français  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – Extraction de texte depuis des fichiers PDF  
- [pdfminer3](https://pypi.org/project/pdfminer3/) – Analyse fine de la structure des PDF  
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) – Base de données légère embarquée  
- [re (regex)](https://docs.python.org/3/library/re.html) – Expressions régulières pour le nettoyage de texte  
- [base64](https://docs.python.org/3/library/base64.html) – Encodage/décodage de données binaires (ex. images)  
- [random](https://docs.python.org/3/library/random.html) – Génération de valeurs aléatoires  
- [datetime](https://docs.python.org/3/library/datetime.html) – Gestion des dates et heures  
- [time](https://docs.python.org/3/library/time.html) – Mesure du temps et temporisation  
- [io](https://docs.python.org/3/library/io.html) – Manipulation de flux en mémoire (utile avec pdfminer3)

## Remerciements

Basé sur le dépot de Mudassiruddin7, thanks for the inspiration!

## Auteur
ANGOR RACHILDE Nora

## Déploiement
Streamlit-Pycharm
