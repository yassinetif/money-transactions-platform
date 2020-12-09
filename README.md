# money-transactions-platform

Money transactions platform : Cash to Cash transactions, cash to Wallet, Payment API integrations ...

## Installation environnement de test :  Ubuntu 18.04
   
## Etape 1 : Véfifier la version de python et installation de pip

### Mise à jour de l'environnement
-   ```
    apt-get update
    apt -y upgrade
    ```
Vérifier la version de python sur le serveur
-   ```
    python3 -V
    ```

### Installer pip

-   ```
    apt install -y python3-pip
    ```

#### Autres Prérequis

-   ```
    apt install build-essential libssl-dev libffi-dev python3-dev
    apt install libsasl2-dev libldap2-dev
    ```

## Etape 2 : Setup d'un virtual env

-   ```
    apt install -y python3-venv
    ```

### Création du dossier qui va contenir les environnements virtuels
-   ```
    mkdir environments
    cd environments
    ```
### Création de l'environnement virutel
-   ```
    python3.6 -m venv env_monnamon_backend
    ```

## Etape 3 :  Récupérer du code source depuis le repository git
### S'assurer d'être dans le bon repertoire
-   ```
    apt install git
    mkdir src && cd src
    git clone https://github.com/williamsko/money-transactions-platform.git
    ```


## Etape 4 : Installation des requirements du backend
-   ```
    source ~/environments/env_monnamon_backend/bin/activate
    cd money-transactions-platform
    pip3 install -r requirements.txt
    pip3 install pyOpenSSL
    ```

## Etape 5 : Lancement du backend
-   ```
    pyhton manage.py migrate
    pyhton manage.py createsuperuser
    pyhton manage.py collectstatic
    pyhton manage.py runserver 0.0.0.0:8000
    ```

## Etape 6 : Lancement du gestionnaire de file d'attente
-   ```
    pyhton manage.py qcluster
    ```

TEST - PR
