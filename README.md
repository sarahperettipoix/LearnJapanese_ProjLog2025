Learn Japanese: Projet Logiciel 2025
---
## Objectif du projet
L'objectif principal de ce projet est de créer un logiciel
d'apprentissage des caractères japonais en utilisant des flashcards.

### Implications et applications potentielles
Le projet permettra aux étudiants de japonais d'apprendre les caractères
par niveau de difficulté, les mettre en favoris et de les reviser avec des flashcards.
L'interface visuelle accueillante aux couleurs matcha encourage un environment 
de travail calme et évoque un jardin zen.

---
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
---

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

---
## Modules

* main.py : Ce module implémente :
    - Les routes FastAPI pour le frontend
    - La gestion des utilisateurs (login/signup)
    - Le système de favoris
* character.py : Ce module implémente :
    - les classes des kanas (hiragana, katakana) et kanjis
    - la classe de l'utilisateur

---
## Fonctions détaillées

### main.py

- `test_db()`
  - Description : Teste la connexion à la base de données MongoDB.
  - Arguments : Aucun.
  - Retour : `dict` – Message confirmant la connexion et 
  le nombre de documents dans la collection kanji.
---
- `home(request: Request)`
  - Description : Route racine qui retourne la page d'accueil.
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `index.html`.
---
- `read_hiragana(request: Request)`
  - Description : Retourne tous les hiraganas depuis la base de données.
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : TemplateResponse` – Page `flashcard.html` avec la liste des hiraganas.
---
- `read_katakana(request: Request)`
  - Description : Retourne tous les katakanas depuis la base de données.
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `flashcard.html` avec la liste des katakanas.
---
- `read_kanji(request: Request)`
  - Description : Retourne la page des kanjis (sans données dynamiques).
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `kanji.html`.
---
- `read_kanji_by_level(request: Request, level: str)`
  - Description : Retourne les kanjis filtrés par niveau JLPT.
  - Arguments : 
    - `request` (`Request`) – Objet requête FastAPI.
    - `level` (`str`) – Niveau JLPT (N1 à N5)
  - Retour : `TemplateResponse` – Page `flashcard.html` avec les kanjis du niveau.
  - Exemple :
- ```python
    await read_kanji_by_level(request, "N3")  # retourne la page avec les kanjis N3
    ```
---
- `browse_everything(request: Request)`
  - Description : Retourne toutes les données (hiragana, katakana, kanji) pour la page de navigation.
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `browse.html` avec toutes les données.
---
- `learn_everything(request: Request)`
  - Description : Retourne la page d’apprentissage (`learn.html`).
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `learn.html`.
---
- `about(request: Request)`
  - Description : Retourne la page “À propos” (`about.html`).
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `about.html`.
---
- `get_login_form(request: Request)`
  - Description : Affiche le formulaire de connexion.
  - Arguments : `request` (`Request`) – Objet requête FastAPI.
  - Retour : `TemplateResponse` – Page `auth.html` en mode login.
---
- `post_login(request: Request, username: str, password: str)`
  - Description : Traite la soumission du formulaire de connexion.
  - Arguments : 
      - `request` (`Request`) – Objet requête FastAPI.
      - `username` (`str`) – Nom d’utilisateur 
      - `password` (`str`) – Mot de passe
  - Retour : 
    - `TemplateResponse` – Page `auth.html` avec erreur si échec
    - `RedirectResponse` – Redirection vers l’accueil si succès
  - Exemple :
    ```python
    await post_login(request, "user123", "secret")  # redirige ou affiche une erreur
    ```
---
- `post_signup(request: Request, username: str, password: str)`
   - Description : Traite la soumission du formulaire d’inscription.
   - Arguments : 
      - `request` (`Request`) – Objet requête FastAPI.
      - `username` (`str`) – Nom d’utilisateur souhaité
      - `password` (`str`) – Mot de passe
  - Retour : `TemplateResponse` – Page `auth.html` avec message de succès ou erreur.
  - Exemple :     
  ```python
  await post_signup(request, "new_user", "pass123")  # crée un compte ou affiche une erreur
    ```
---
- `profile(request: Request, user: str)`
  - Description : Affiche le profil utilisateur avec ses favoris.
  - Arguments : 
      - `request` (`Request`) – Objet requête FastAPI.
      - `user` (`str`) – Nom d’utilisateur depuis les cookies
  - Retour : 
    - `TemplateResponse` – Page `profile.html` avec données
    - `RedirectResponse` – Redirection vers login si non connecté
---
- `logout()`
  - Description : Déconnecte l’utilisateur et supprime le cookie.
  - Arguments : Aucun.
  - Retour : `RedirectResponse` – Redirection vers la page de login.
---
- `add_favourite(request: Request)`
  - Description : Ajoute un élément aux favoris de l’utilisateur.
  - Arguments : `request` (`Request`) – Objet requête contenant les données JSON
  - Retour : `JSONResponse` – Message de confirmation ou d’erreur.
---
- `remove_favourite(request: Request, data: dict)`
  - Description : ASupprime un élément des favoris de l’utilisateur.
  - Arguments : 
    - `request` (`Request`) – Objet requête contenant les données JSON
    - `data` (`dict`) – Corps de la requête JSON contenant l'identifiant de l’élément
  - Retour : `JSONResponse` – Message d’erreur si ID manquant ou succès si favori supprimé.
  - Exemple:
    ```python
    await remove_favourite(request, {"id": "kanji123"})  # {"message": "Favori supprimé"}
    ```

---
## Contributeurs
Sarah Peretti-Poix
Virgile Albasini
Sophie Ward
Orsowen Chétioui
