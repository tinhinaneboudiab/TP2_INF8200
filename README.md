# Travail pratique 2: Céation d'un pipeline avec Airflow
Disponible à l'Adresse: [https://github.com/tinhinaneboudiab/TP1_INF8200.git](https://github.com/tinhinaneboudiab/TP1_INF8200.git).

## Auteur

* [BOUDIAB Tinhinane](<a href="mailto:boudiab.tinhinane@courrier.uqam.ca">**`BOUT79360000`**</a>)

## Objectif

* Le but de Tp est d'utiliser le workflow manager **Airflow** afin de recuillir les données sur Bitcoin à partir de plusieurs sources (ETL), appliquer quelques prétraitement, et entrainer modèle de prédiction de prix. 

## Environnement de travail

Le tp est realisé sur Windows 11, en utilisant `Airflow` avec `Docker-compose`.


## Taches à réaliser

1. Installation et lancement de `Airflow` avec `Docker-compose` sur `Window 11`.
2. Description de données.
3. Description de pipeline.
4. Vérification de fonctionnement de pipeline.
5. Discussion.
6. Commentaires.

## Tache 1

Cette tache vise à citer les étapes à suivre afin d'assurer l'installation de `Airflow` avec `Docker-compose`.

1. Première étape consiste à verifier l'installation de docker-compose sur la machine.

    ```Docker
    # Verification des intallations
    docker --version
    docker-compose --version
    ```

2. Ensuite, pour le deploiement de airflow, nous devrons récuperer le fichier `docker-compose.yml`. Pour y parvenir:

    2.1. Nous devons d'abord créer un répèrtoire nommé dans mon cas `airflow-docker`:  
    ```bash
    # Récupération du fichier docker-compose.yml
    mkdir airflow-docker
    ```
    2.2. Ensuite, nous devons accéder à ce répertoire et ouvrir le terminal afin de récuper le fichier docker-compose:

    ```bash
    # Récupération du fichier docker-compose.yml
    cd airflow-docker
    # Dans le terminal de VsCode
    curl 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml' -o 'docker-compose.yaml'
    ```
    2.3. Puis, nous procédons à la création des répétoires `dags`, `logs`, `plugins` à l'aide de la commande suivante:
     ```bash
    # Création des répertoires
    mkdir dags
    mkdir logs
    mkdir plugins
    ```
3. Nous lançons après ça airflow  grace à la commande suivante:
    ```docker
        # Initialisation de airflow (cette commande peut prendre plusieurs minutes)
        docker compose up airflow-init
        # Lancement de airflow
        docker compose up 
    ```
4. Lancement de serveur airflow sur l'adresse suivante:
    ```docker
        http://localhost:8080/
    ```
## Tache 2

Dans cette étape, nous décrivons les données que nous avons utilisé. <br>

1. La premiere source de données est une API (disponible sur le site: https://sampleapis.com/api-list/bitcoin) qu'est sous forme de fichier json contenant les informations historiques sur le bitcoin de 2010 jusqu'au 2022. Ces données sont dans leur état brute, Ceci dit, que nous aurons besoin de faire du nettoyage.<br>

    La figure suivante illustre les cinq premières lignes de dataset
    ```text
    | Date       | Price    | Open     | High     | Low      | Vol.  | Change % |
    |------------|----------|----------|----------|----------|-------|----------|
    | 12/19/2023 | 42,259.3 | 42,659.7 | 43,473.3 | 41,842.7 | 55.29K| -0.94%   |
    | 12/18/2023 | 42,659.7 | 41,369.1 | 42,728.0 | 40,554.0 | 61.58K| 3.12%    |
    | 12/17/2023 | 41,368.7 | 42,271.7 | 42,413.2 | 41,276.9 | 35.46K| -2.14%   |
    | 12/16/2023 | 42,271.7 | 41,929.0 | 42,690.3 | 41,698.2 | 30.11K| 0.82%    |
    | 12/15/2023 | 41,929.0 | 43,025.2 | 43,080.7 | 41,697.9 | 45.28K| -2.55%   |
    ```
2. La deuxieme source de données est une données plus récente contenant les information sur le bitcoin de 2021 au 2023.

    ```text
    | Date       | Price   | Open    | High    | Low     | Volume | ChangePercentFromLastMonth|
    |------------|---------|---------|---------|---------|--------|---------------------------|
    | 2023-12-19 | 42259.3 | 42659.7 | 43473.3 | 41842.7 | 55.29K | -0.94                     |
    | 2023-12-18 | 42659.7 | 41369.1 | 42728.0 | 40554.0 | 61.58K | 3.12                      |
    | 2023-12-17 | 41368.7 | 42271.7 | 42413.2 | 41276.9 | 35.46K | -2.14                     |
    | 2023-12-16 | 42271.7 | 41929.0 | 42690.3 | 41698.2 | 30.11K | 0.82                      |
    | 2023-12-15 | 41929.0 | 43025.2 | 43080.7 | 41697.9 | 45.28K | -2.55                     |
    ```

## Tache 3
Nous passons maintenant à la description de notre pipeline.<br>
Notre pipeline se divise en plusieurs taches.<br>
1. La premiere tache nommée `Telechargement_API_Binance` qui vise à télécharger les données de bitcoin à partir de l'API. 
2. La deuxieme tache nommée  `fetch_and_save_data` consiste à nettoyer les données brutes récupéré par l'API et les stocker dans un fichier csv. 
3. La troisieme tache nommée `cleanBinance_File_Dataset` est une tache indépendante des deux premières taches, qui consiste à lire un fichier csv trouvée dans le site suivant:  https://www.kaggle.com/datasets/armanzhalgasbayev/bitcoin-historical-data-2021-2023. 
4. La Quatrième tache nommèe `concat_datasets` est une tache qui permet de concaténer les deux sources de données hétérogènes afin de construire un historique de 2012 au 2023, en vue de l'utiliser pour prédire le comportement futur de Bitcoin.
5. La Cinquième tache nommée  `predict_price` consiste en un modèle fictif qui permettre de predire le comportement futur de prix de Bitcoin.
6. La derniere tache nommée `notify` permet de notifier lors l'entrainement de modèle est fini.

La figure suivante illustre le graphe de dependance du pipeline:
![img](images/graphe_Dependance.png)

## Tache 4
Nous sommes arrivé à l'étape de vérification de fonctionnement de pipeline. Pour y parvenir.
1. S'assurer que l'interface UI de airflow est accessible sur `http://localhost:8080/` à l'aide de la commande sur le terminal `Docker compose up`. Les figures suivantes représentent le lancement de mon workflow manager.
![img](images/lanc.png)
![img](images/lancement_airflow.png)
La figure suivante illustre l'interface UI d'Airflow. mon username est `airflow` et le mot de passe est: `airflow` 
![img](images/interf.png)
Pour créer un nouveau utilisateur, nous utiliserons la commande suivante:
nous lançons après ça airflow  grace à la commande suivante:
    ```bash
    # Creation de nouvel utilisateur
    airflow db init 
    airflow users create --username admin --password admin --firstname
    Tina --lastname Admin --role Admin --email tinboud@gmail.com  
    ```
    ![img](images/interfaceUI.png)
2. Le DAG est nommé: `Crypto_ETL`. La figure suivante illustre la fenetre contenant les détails de mon DAG. Y compris: Le status de mon DAG, Le scheduler de mon DAG est quotidien, les informations sur la durée d'execution qu'est 11 secondes. 
![img](images/details.png)
3. Le status success de mon graphe de dependances suivant indiquent que toutes les taches sont executées avec succès.
![img](images/execution.png)
4. Le digramme de Gant suivant represente l'ordre d'éxecution des taches.
![img](images/GANT.png)
5. Le fichier logs indique le moment d'éxecution de chaque tache et son état succès ou echec. La figure suivante l'illustre:
![img](images/logs.png)

## Tache 5 : Discussion 
1. Parmi les aspects aspects de airflow que j'ai pas pu implementer sont: 
    1. J'ai essayé d'ajouter une tache permettant d'afficher le graphe globale de dataset concaténé mais la bibliothèque `Plotly.express` n'a pas été accepté par Airflow, et pourtant, je fais l'installation et le redémarrage à plusieurs reprise de mon DAG.
2. Dans le cas d'utilisation d'une base de données il faudra installer la bibliothèque de SGBD. Car, Airflow utilise par défaut **SQLITE3**.
Exemple d'installation de SGBD **PostgreSQL**:
 ```Python
    # 1.Installation de bibliothèque 
    pip install psycopg2
    # 2.Installation de provider
    pip install apache-airflow-providers-postgres
    # 3.Dans Admin-> Connexion dans l'interface UI, on doit remplir tous les parametres de notre Base de données.
    # 4.Ensuite dans le fichier airflow.cfg on change les parametre de la variable sql_alchmey vers PostgreSQl
    sql_alchemy_conn = postgresql+psycopg2://postgres:1234@localhost:5432/test
    # 5.On change l'executeur d'Airflow
    executor = LocalExecutor
```
## Tache 6 : Commentaires
1. Pour déclencher le DAG sur l'interface UI de Airflow, il suffit de cliquer sur le bouton suivant:
![img](images/trigger.png)

2. La connexion au UI est déja cité dans les sections précédentes.












