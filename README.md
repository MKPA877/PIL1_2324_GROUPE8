@readme
#PIL_2324_[8]

## Projet d'application d'une application de rencontre:
Il s'agit d'un service de rencontres en ligne sous la forme d'une application web. Cette application dispose d'une interface graphique web communiquant avec la base de données suivant le modèle server-client.

## Membres:

- ADANLIENCLOUNO Précieux
- ADONON Jiovany
- AKAKPO Godwin
- AKOTO Yves
- AMOUO Othiniel
- GLELE Freddy
- GUEZODJE Ferréol
- HOUSSOU Prodige
- MONGADJI Jihad
- KOUMAGNON Carmel

### Requirements  
- Langage de programmation: Python avec framework Django
- Anaconda
- Daphne
- Channels
- Channels redis
- Dj-database-url
- psycopg2-binary
- Base de donnée: PostgreSQL
- Système d'exploitation: Compatible avec les distributions Linux et Windows


### Captures des pages développées

- Accueil
  ![Home capture 1](page_d'accueil.jpg)

- Login & Inscription
  ![Login](page_connexion.jpg)
  ![Signup](page_inscription.jpg)
  ![Modificationprofil](Page_modif_profil.jpg)

- Chat & notifications
  ![Messagerie](Page_chat.jpg)
  ![Notification](Page_notif.jpg)
  ![Page de suggestions](page_sug.jpg)

#### Exécution en local de l'application:
Pour le déploiement en local, veuillez suivre les étapes suivantes:
 1.Installer les dépendances :
   - Assurez vous d'avoir Python et PostgreSQL installés sur votre machine.
   - Installez les dépendances Python requises pour votre projet (vous pouvez utiliser pip install -r requirements.txt).

2. Configurer la base de données :
   - Créez une base de données PostgreSQL localement.
   - Mettez à jour les paramètres de connexion à la base de données dans votre fichier settings.py.

3. Exécutez les migrations :
   - Utilisez la commande python manage.py migrate pour créer les tables dans la base de données.

4. Lancez le serveur de développement :
   - Exécutez python manage.py runserver pour démarrer le serveur de développement.
   - Accédez à l'application dans votre navigateur en utilisant l'URL http://127.0.0.1:8000/.

5. Créez un superutilisateur :
   - Utilisez python manage.py createsuperuser pour créer un compte administrateur.
   - Vous pourrez vous connecter à l'interface d'administration Django à l'URL http://127.0.0.1:8000/admin/.
