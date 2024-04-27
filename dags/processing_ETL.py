import json
import pathlib
import airflow 
import requests 
import requests.exceptions as requests_exceptions
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd

# Initialisation de DAG
dag= DAG(
    dag_id="Crypto_ETL", # Le nom de mon DAG
    start_date=airflow.utils.dates.days_ago(14),  # La date à laquelle le DAG commence à s'exécuter pour la première fois
    schedule_interval="@daily",  # La fréquence à laquelle le DAG devraits'exécuter# 
)

# Appliquer Bash pour telecharger l'URL response with CURL
download_launches= BashOperator(
    task_id="Telechagement_API_Binance", # le nom de tache
    bash_command="curl -o /tmp/download.json -L 'https://api.sampleapis.com/bitcoin/historical_prices'",
    dag=dag
)

def _get_data():
    try:
        # Essayez d'ouvrir le fichier
        with open("/tmp/download.json") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            return df
    except FileNotFoundError:
        # Si le fichier n'existe pas, affichage de message d'erreur
        print("Le fichier '/tmp/download.json' n'existe pas.")
        return None
    except json.JSONDecodeError:
        # Si le fichier JSON est mal formé, affichage de message d'erreur
        print("Le fichier JSON est mal formé.")
        return None

# Stockage de df nettoyé dans un fichier csv
def binance_to_csv(df):
    if df is not None:
        df.to_csv("/opt/airflow/dags/binance_dataset.csv", index=False)
        print("Data sauvegardé dans binance_dataset.csv")
    else:
        print("Problème survenu.")

# Implémentation de la fonction
def _fetch_and_save_data():
    binance_data = _get_data()
    if binance_data is not None:
        binance_to_csv(binance_data)

# Appel de fonction python dans DAG avec PythonOperator
get_data= PythonOperator(
    task_id="fetch_and_save_data",
    python_callable=_fetch_and_save_data,
    dag=dag,
)

# Convertir les colonnes vers le bon type
def convert_to_float(price_str, char):
    return float(price_str.replace(char, ''))
# Nettoyage de données
def _cleanBinance_File_Dataset():
    df=pd.read_csv('/opt/airflow/dags/BitcoinHistorical_Data.csv')
    df['Price'] = df['Price'].apply(convert_to_float,char=',')
    df['Open'] = df['Open'].apply(convert_to_float,char=',')
    df['High'] = df['High'].apply(convert_to_float,char=',')
    df['Low'] = df['Low'].apply(convert_to_float,char=',')
    df = df.rename(columns={'Vol.': 'Volume'})
    df['Change %']= df['Change %'].apply(convert_to_float,char='%')
    df = df.rename(columns={'Change %': 'ChangePercentFromLastMonth'})
    return df	

# L'operateur qui permet d'Executer la tache de nottoyage
cleanBinance_File_data= PythonOperator(
    task_id="cleanBinance_File_Dataset",
    python_callable=_cleanBinance_File_Dataset,
    dag=dag,
)

# Recuperation de dataframe nettoyé en vue de l'utilisation
def _clean_Binance_Dataset():
    df1=pd.read_csv('/opt/airflow/dags/binance_dataset.csv')
    df1['Date']=pd.to_datetime(df1['Date'])
    return df1

# Concatiner les deux datasets
def _concat_datasets():
    df=_cleanBinance_File_Dataset()
    df1=_clean_Binance_Dataset()
    df_final=pd.concat([df,df1])
    df_final.to_csv('/opt/airflow/dags/final_dataset.csv')
    

concat_data= PythonOperator(
    task_id="concat_datasets",
    python_callable=_concat_datasets,
    dag=dag,
)

# Fonction qui permet de prédire un le prix 
def _Predict_Price():
    df_final=pd.read_csv('/opt/airflow/dags/final_dataset.csv')
    # Entrainenement de modèle
    df_final.set_index('Date', inplace=True)
    print('Cette phase consiste de entrainer le modèle')

# Operateur qui permet d'Executer le modele d'entrainement fictif
predict_price=PythonOperator(
    task_id="predict_price",
    python_callable=_Predict_Price,
    dag=dag,
)

# Tache qui permet de notifier à la fin d'entraienement
notifier= BashOperator(
task_id="notify",
bash_command='echo "Ceci est la fin de l entrainement !"',
dag=dag,
)



[download_launches >> get_data , cleanBinance_File_data] >> concat_data >> predict_price  >> notifier