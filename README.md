# Learn Japanese: Projet Logiciel 2025

## Objectif du projet
L'objectif principal de ce projet est de créer un logiciel
d'apprentissage des caractères japonais en utilisant des flashcards.

### Implications et applications potentielles
Le projet permettra aux étudiants de japonais d'apprendre les caractères
par niveau de difficulté, les mettre en favoris et de les reviser avec des flashcards.
L'interface visuelle accueillante aux couleurs matcha encourage un environment 
de travail calme et évoque un jardin zen.

## Modules

* main.py : Ce module implémente :
    - Les routes FastAPI pour le frontend
    - La gestion des utilisateurs (login/signup)
    - L'accès aux données des kanas (hiragana, katakana) et kanjis
    - Le système de favoris


## Architecture du projet

```
ProjetLogiciel2025/
├── backend/
│   ├── main.py
│   ├── db
│   │   ├── kanji.json
│   │   ├── user.json
│   │   ├── katakana.json
│   │   └── hiragana.json
│   └── requirements.txt
├── frontend/
│   ├── static
│   │   ├── images
│   │   │   ├──background.png
│   │   │   ├── home.png
│   │   │   └── pastel_background.png
│   │   ├── about.css
│   │   ├── browse.css
│   │   ├── browse.js
│   │   ├── flashcard.css
│   │   ├── flashcard.js
│   │   ├── kanji.css
│   │   ├── learn.css
│   │   ├── login.css
│   │   ├── login.js
│   │   ├── profile.css
│   │   ├── profile.js
│   │   └── style.css
│   ├── about.html
│   ├── auth.html
│   ├── browse.html
│   ├── flashcard.html
│   ├── index.html
│   ├── learn.html
│   └── profile.html
├── INSTRUCTIONSMONGODB.txt
└── README.md
```
---

## Description du dataset

* _kanji.json_

   contient des informations sur chaque caractère de type kanji:
  
  * id
  * kanji
  * onyomi: prononciations chinoises
  * kunyomi: prononciations japonaises
  * meaning: signification du kanji
  * JLPT: niveau de difficulté

* _katakana.json_

   contient des informations sur chaque caractère de type katakana:
  
  * id
  * katakana
  * romaji: prononciation latine

* _hiragana.json_

   contient des informations sur chaque caractère de type hiragana:
  
  * id
  * hiragana
  * romaji: prononciation latine

## Installation
### Backend Setup

Cloner le dépôt :

    git clone https://github.com/sarahperettipoix/LearnJapanese_ProjLog2025.git

Créer et activer un environnement virtuel:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Aller au dossier backend/ :

    cd backend

Installer les Python packages requis:

    pip install -r requirements.txt


### Database Initialisation

* S'assurer que MongoDB est installé et en marche.
* Suivre les instructions de INSTRUCTIONSMONGODB.txt pour mettre 
en place le database.

## Fonctions détaillées

### main.py

#### class NarrativeNode (abstract)

- `extract_content()`

  - Description : Extrait le contenu textuel du nœud.  
  - Arguments : Aucun.  
  - Retour : `str` – contenu textuel.  
  - Exemple :
    ```python
    node = ParagraphNode(1, "paragraph", "Un paragraphe.")
    print(node.extract_content())  # "Un paragraphe."

## Phases du projet

**Le projet doit contenir une base de données, un backend, un frontend**

1. **Brainstorming** :
   - Le projet est né d'une volonté de créer un logiciel d'apprentissage pour
le japonais moins austère que les options actuelles.
   - Un choix de fonctionnalités a été effectué selon des considerations de difficulté
et d'aptitudes.
     - Ces fonctionnalités ont dû s'adapter aux exigences du professeur et 
aux capacités de chaque contributeur.
   - Un code couleur uniforme et paisible

2. **Base de données** :
   - Les bases de données ont été trouvés sur Anki et modifiées avec des regex afin de
correspondre aux attentes du projet. Au format json.
   - Initialement il était prévu de garder uniquement des json pour ce projet.
Suite aux requêtes du professeur le framework mongoDB a été ajouté, les json ont été
importé dans mongodb.

3. **Backend** :
   - Le backend a été réalisé en python avec fastAPI.

4. **Frontend** :
   - Le frontend a été réalisé avec HTML5, CSS, JavaScript et Figma.


## Contributeurs
Sarah Peretti-Poix
Virgile Albasini
Sophie Ward
Orsowen Chétioui
