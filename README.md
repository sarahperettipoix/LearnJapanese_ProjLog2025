# Learn Japanese: Projet Logiciel 2025
## Logiciel d'apprentissage des caractères japonais

#### Objectif du projet
L'objectif principal de ce projet est de créer un logiciel
d'apprentissage des caractères japonais en utilisant des flashcards.

#### Implications et applications potentielles
Le projet permettra aux étudiants de japonais, d'apprendre les caractères
par niveau de difficulté, les mettre en favoris et de les reviser avec des flashcards.
l'interface visuelle accueillante aux couleurs matcha encourage un environment 
de travail calme et évoque un jardin zen.

### Description du dataset TODO

**Contenu**
Dans tous les fichiers, 

* _movie_titles_metadata.txt_

   contient des informations sur chaque titre de film
   champs :
  
      * movieID,
      * titre du film,
      * année du film,
      * cote IMDB,
      * non. votes IMDB,
      * genres au format ['genre1', 'genre2',É, 'genreN']


### Backend Setup

Aller au dossier backend/ :

    cd backend

Créer et activer un environnement virtuel:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Installer les Python packages requis:

    pip install -r requirements.txt

Démarrer le server backend:

    bash runBackend.bash  

Sur Windows: 

    runBackend_windows.bash

### Database Initialisation

* S'assurer que MongoDB est installé et en marche.
* Suivre les instructions de INSTRUCTIONSMONGODB.txt pour mettre 
en place le database.
* utiliser le dbInsertion.SQL et dbTable.SQL scripts pour initialiser 
et remplir le database.

#### Phases du projet

**Le projet doit être entièrement construit selon une architecture de programmation orientée objet.**

1. **Sélection des films et collecte des dialogues** :
   - Pour la sélection des données et la préparation du projet EMODIA ("ÉMotions et DIalogues Analyse"), 


### Analyses Statistiques et Visualisations

1. **Distribution des Genres de Films**
         - Créer un histogramme ou un diagramme circulaire pour visualiser la distribution des genres de films dans le dataset.
         - Examiner les genres de films les plus communs et ceux moins représentés pour déterminer des tendances ou des biais potentiels dans la sélection des films.
      
     
### Visualisations des Données Textuelles
   
1. **Cartographie des Dialogues**
         - Créer des graphes de réseau pour visualiser les interactions entre personnages dans les films, en illustrant la fréquence et la profondeur des dialogues.
         - Utiliser des cartes de chaleur pour montrer la densité des échanges entre différents personnages principaux.

   
### Contributeurs

Sarah Peretti-Poix

Virgile Albasini

Sophie Ward

Orsowen Chétioui
