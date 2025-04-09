# ---------  ALLER DANS LE DOSSIER backend ET ENSUITE DANS LE TERMINAL DE VSCODE, TAPER CECI : ---------

cd .\backend\
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload



#ouvrir le browser taper localhost:8080/ (suivi du path que vous voulez voir)
#terminer le programme sur le terminal avec ctrl c


################# POUR MONGO DB ##############
#dans un terminal
mongod --dbpath C:\0_TRAVAIL\1_UNI\3eme\z_creation_logiciel\ProjetLogiciel2025\backend\db

# pour le tuer 
net stop MongoDB

# pour le lancer
net start MongoDB

# pour vérifier son état
netstat -ano | findstr 27017