pip.main(['install', 'plotly'])
pip.main(['install', 'plotly_express'])
pip.main(["install","openpyxl"])
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st

import streamlit as st
import pandas as pd
import plotly.express as px
import pip 

def reemplazos(v):
  v=str(v)
  v=v.replace(',','')
  return v


pip.main(["install","openpyxl"])

st.title("PROTOTIPO FUNNELL")
st.text('La presente página permite visualizar el comportamiento generalizado de los socios en la aplicacion.')
#df=pd.read_excel('PROCESOS_PIVOTE.xlsx')

#df_2=pd.read_csv('APROBADOS.csv')
#st.write(df_2)

st.markdown(f' FUNNEL')
df=pd.read_csv('FUNEL.csv',encoding='latin-1')
LISTA_VALORES=df['VALOR']
LISTA_PASOS=df['PASO']
data = dict(
    number=LISTA_VALORES,
    stage=LISTA_PASOS)
fig = px.funnel(data, x='number', y='stage')
st.ploty_chart(fig)
#fig.show()
#st.image('FUNNEL.png',caption='ACTIVIDAD REGISTRADA PARA CADA UNA DE LAS PANTALLAS')


st.markdown(f' AFLUENCIA DIARIA EN EL UNBORDING 2.0')
st.image('BARRAS.png',caption='EVOLUCION DE LA ACTIVIDAD')

st.markdown(f' RESUMEN')
df=pd.read_csv('RESUMEN.csv',encoding='latin-1')
df=df.drop('Unnamed: 0',axis=1)
st.text('Con la finalidad de presentar de manera rápida los resultados reelevantes acerca del uso de la app, se muestra a continuación una tabla de concentración.')
st.write(df)

st.markdown(f' CAIDOS')
df=pd.read_csv('EN PROCESO.csv',encoding='latin-1')
df=df.drop('Unnamed: 0',axis=1)
df['NUMERO_SOCIO']=list(map(reemplazos,df['NUMERO_SOCIO']))
df['CELULAR']=list(map(reemplazos,df['CELULAR']))
st.write(df)

st.markdown(f' APROBADOS')
df=pd.read_csv('APROBADOS.csv',encoding='latin-1')
df=df.drop('Unnamed: 0',axis=1)
df=df.drop('PASO',axis=1)
df['NUMERO_SOCIO']=list(map(reemplazos,df['NUMERO_SOCIO']))
df['CELULAR']=list(map(reemplazos,df['CELULAR']))
st.write(df)

st.markdown(f' RECHAZADOS')
df=pd.read_csv('RECHAZADO.csv',encoding='latin-1')
df=df.drop('Unnamed: 0',axis=1)
df['NUMERO_SOCIO']=list(map(reemplazos,df['NUMERO_SOCIO']))
df['CELULAR']=list(map(reemplazos,df['CELULAR']))
st.write(df)
