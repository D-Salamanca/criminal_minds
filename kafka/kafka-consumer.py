import json
import logging
import socket
import sys
from datetime import datetime
import streamlit as st
from confluent_kafka import Consumer, KafkaException
import pandas as pd
import matplotlib.pyplot as plt
import time
import plotly.express as px


logger = logging.getLogger("KAFKA CONSUMER LOGGER")

def grafica_genero(df):
    if 'Vict Sex' in df.columns:
        conteo_genero = df['Vict Sex'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(conteo_genero, labels=conteo_genero.index, autopct='%1.1f%%')
        ax.set_title('Distribución por Género')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.write("No hay datos disponibles para 'genero'.")

def grafica_razas(df):
    if 'Vict Descent' in df.columns:
        conteo_razas = df['Vict Descent'].value_counts()
        st.bar_chart(conteo_razas)
    else:
        st.write("No hay datos disponibles para 'Vict Descent'.")

def grafica_tipo_delito(df):
    if 'Crm Cd Desc' in df.columns:
        conteo_delitos = df['Crm Cd Desc'].value_counts().head(10)
        fig, ax = plt.subplots()
        ax.pie(conteo_delitos, labels=conteo_delitos.index, autopct='%1.1f%%')
        ax.set_title('Distribución por Tipo de Delito')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.write("No hay datos disponibles para 'Crm Cd Desc'.")

def grafica_tipo_arma(df):
    if 'Weapon Desc' in df.columns:
        conteo_armas = df['Weapon Desc'].value_counts()
        st.bar_chart(conteo_armas)
    else:
        st.write("No hay datos disponibles para 'Weapon Desc'.")

connection_conf = {
    "bootstrap.servers": "localhost:9092",
    "client.id": socket.gethostname(),
    'group.id': 'mi_grupo_consumidor',
    'auto.offset.reset': 'latest'
}

topic = "criminaltopic"

consumer = None
try:
    logger.info("Start Consumer connection")
    consumer = Consumer(connection_conf)
    consumer.subscribe([topic])

    placeholder_genero = st.empty()
    placeholder_razas = st.empty()
    placeholder_delito = st.empty()
    placeholder_arma = st.empty()

    data_list = []

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue

        data = json.loads(msg.value().decode('utf-8'))
        logger.info(f"Received message as dict: {data}")
        data_list.append(data)
        df = pd.DataFrame(data_list)

        with placeholder_genero.container():
            grafica_genero(df)
        with placeholder_razas.container():
            grafica_razas(df)
        with placeholder_delito.container():
            grafica_tipo_delito(df)
        with placeholder_arma.container():
            grafica_tipo_arma(df)

        

        time.sleep(1)
        consumer.commit(msg)

except Exception as e:
    logger.error(f"[{datetime.now()}] The consumer could not connect to the topic {topic}")
    logger.error(e)

finally:
    if consumer is not None:
        consumer.close()
