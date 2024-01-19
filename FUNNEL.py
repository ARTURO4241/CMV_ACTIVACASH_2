import streamlit as st
import pandas as pd
import pip 


pip.main(["install","openpyxl"])

st.title("PROTOTIPO FUNNELL")
#df=pd.read_excel('PROCESOS_PIVOTE.xlsx')

#df_2=pd.read_csv('APROBADOS.csv')
#st.write(df_2)

st.markdown(f':FUNNEL')
st.image('FUNNEL.png',caption='ACTIVIDAD REGISTRADA PARA CADA UNA DE LAS PANTALLAS')


st.markdown(f':TRAFICO TOTAL')
st.image('BARRAS.png',caption='EVOLUCION DE LA ACTIVIDAD')


st.markdown(f':CAIDOS')
df=pd.read_csv('EN PROCESO.csv',encoding='latin-1')
st.write(df)

st.markdown(f':APROBADOS')
df=pd.read_csv('APROBADOS.csv',encoding='latin-1')
st.write(df)

st.markdown(f':RECHAZADOS')
df=pd.read_csv('RECHAZADO.csv',encoding='latin-1')
st.write(df)
