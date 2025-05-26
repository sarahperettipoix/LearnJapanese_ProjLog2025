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

### Architecture du projet
L'application adopte une architecture client-serveur, 
comprenant une interface utilisateur développée en HTML 5 
et un back-end développé avec FastAPI. MongoDB sert de base de 
données principale pour le stockage des informations sur 
les caractères et les utilisateurs.

```
ProjetLogiciel2025/
├── backend/
│   ├── main.py
│   ├── db
│   │   ├── kanji.js
│   │   ├── user.js
│   │   ├── katakana.js
│   │   └── hiragana.js
│   ├── db copie
│   └── requirements.txt
├── frontend/
│   ├── static
│   │   └── images
│   ├── auth.html
│   ├── index.html
│   ├── browse.html
│   ├── flashcard.html
│   ├── profile.html
│   ├── learn.html
│   └── about.html
├── dbInsertion.SQL
├── dbTable.SQL
├── old/
├── INSTRUCTIONSMONGODB.txt
└── README.md
```
---

### Description du dataset

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


### Backend Setup

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
* utiliser le dbInsertion.SQL et dbTable.SQL scripts pour initialiser 
et remplir le database.

#### Phases du projet

**Le projet doit contenir une base de données, un backend, un frontend**

1. **Brainstorming** :
   - Le projet est né d'une volonté de créer un logiciel d'apprentissage pour
le japonais moins austère que les options actuels.
   - Un choix de fonctionnalités a été effectué selon des considerations de difficulté
et d'aptitudes.
     - Ces fonctionnalités ont dû s'adapter aux exigences du professeur et 
aux capacités de chaque contributeur.
   - Un code couleur uniforme et paisible

2. **Base de données** :
   - les bases de données ont été trouvés sur anki et modifier afin de
correspondre aus attentes du projet.
   - initialement il était prévu de garder uniquement des json pour ce projet.
Suite aus requêtes du professeur la framework mongoDB a été ajoutée.

3. **Backend** :
   - le backend a été réalisé avec fastAPI.

4. **Frontend** :
   - le frontend a été réalisé avec html 5, css, et js.
     
### Bugs potentiels
   
1. **fonctionnalité de favoris**
   - en l'état actuel, les favoris peuvent être ajouté plusieurs fois, 
cependant ils peuvent être retiré


### Contributeurs
Sarah Peretti-Poix
Virgile Albasini
Sophie Ward
Orsowen Chétioui
