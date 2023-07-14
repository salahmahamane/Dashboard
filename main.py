import streamlit as st
import matplotlib
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

achats=pd.read_excel('achats.xlsx')
clics=pd.read_excel('clics.xlsx')
impressions=pd.read_excel('impressions.xlsx')

base1=pd.merge(impressions,clics, on='cookie_id', how='left')
base=pd.merge(base1,achats, on='cookie_id', how='left')

#Configuration de la taille de la page et du nom de la page
st.set_page_config(
    page_title="Salah",
    layout='wide'
)

#Transformation des variables de temps
base['timestamp']=pd.to_datetime(base['timestamp'],unit="s")
base['timestamp_x']=pd.to_datetime(base['timestamp_x'],unit="s")
base['timestamp_y']=pd.to_datetime(base['timestamp_y'],unit="s")

#titre du dashboard
st.title('Dashboard de Salah Diallo')

#Afficher la base
st.dataframe(base)

#Quelques petites phrases
st.write("### Ce présent tableau de bord permettra d'avoir une meilleure vue sur les données")
st.write("##### Nous présenterons des chiffres et des graphiques pour faciliter la prise de décision")

st.write("----------------------------------------------------------------")

#séparer la partie qui suit en 3 colonnes pour représenter les chiffres sur la même ligne
part1, part2, part3=st.columns(3)

#1ère colonne de données qui est le chiffre d'affaire
part1.metric(
    label="Chiffre d'affaires",
    value=f"{base['price'].sum()} € "
)

# Date du dernier achat
datemin=base['timestamp'].min().date()

part2.metric(
    label="Date du dernier achat",
    value=f"{datemin}"
)

part3.metric(
    label="Nombre de ventes",
    value=base["timestamp"].count()
)


graph1, graph2=st.columns(2)


with graph1:
    st.markdown("##### Age en fonction du produit")
    fig=px.box(data_frame=base, x='product_id', y='age')
    st.write(fig)

    # Entonnoir
nimp = base['timestamp_x'].count()
nach = base['timestamp'].count()
nclics = base['timestamp_y'].count()

st.write(nclics)

with graph2:
    fig2 = go.Figure(
        go.Funnel(
            y=['Impressions','Achats'],
            x=[nimp, nach]
        )
    )

    st.plotly_chart(fig2)