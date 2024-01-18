import streamlit as st
import pandas as pd
import numpy as np
import pip
pip.main(["install","openpyxl"])

#pip.install plotly_express

#import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly.express as px
from datetime import datetime, timedelta

#"""#METODOS"""

def nombres(a,b,c):
  return str(a)+' '+str(b)+' '+str(c)

def maximizador_pantalla(DF):
  TEMPORAL=DF.groupby('numero_socio').max()
  TEMPORAL['numero_socio']=TEMPORAL.index
  TEMPORAL=TEMPORAL.reset_index(drop=True)
  TEMPORAL=TEMPORAL[['numero_socio','paso']]
  TEMPORAL=TEMPORAL.rename(columns={'paso':'PASO_MAXIMO'})
  return TEMPORAL

def maximizador_fecha(DF):
  TEMPORAL=DF.groupby('numero_socio').max()
  TEMPORAL['numero_socio']=TEMPORAL.index
  TEMPORAL=TEMPORAL.reset_index(drop=True)
  TEMPORAL=TEMPORAL[['numero_socio','FECHA']]
  TEMPORAL=TEMPORAL.rename(columns={'FECHA':'FECHA_MAXIMA'})
  return TEMPORAL

def ULTIMA_PANTALLA(v):
  if v==0:
    return 'PANTALLA HOME'
  elif v==1:
    return 'DATOS PERSONALES'
  elif v==2:
    return 'DATOS ADICIONALES'
  elif v==3:
    return 'VERIFICACION CELULAR Y ACEPTACION BURO'
  elif v==4:
    return 'VERIFICACION INE'
  elif v==5:
    return 'COMPROBANTE DE DOMICILIO'
  elif v==6:
    return 'VALIDACION DE SELFI'
  elif v==7:
    return 'VIDEO_SELFIE'
  elif v==8:
    return 'PENDIENTE'
  elif v==9:
    return 'BENEFICIOS DE SER SOCIO, PARAMETRIZAR Y CONFIRMAR OFERTA'
  elif v==10:
    return 'NO ENCONTRADO'
  elif v==11:
    return 'MESA DE CONTROL'

#"""#ARCHIVO"""


#DF=pd.read_excel('ONBOARDING ACTIVA 2 AL 19 ENERO.xlsx',sheet_name='Hoja1',usecols=['nombre_s','apellido_paterno','apellido_materno','numero_socio','celular','evaluado','aprobado','mensaje_rechazo','paso_proceso','Icc','BcScore','EstimadorIngresos','fecha_created_at'])
#
DF=pd.read_csv('ONBOARDING ACTIVA 2 AL 19 ENERO.csv',encoding='latin-1',usecols=['nombre_s','apellido_paterno','apellido_materno','numero_socio','celular','evaluado','aprobado','mensaje_rechazo','paso_proceso','Icc','BcScore','EstimadorIngresos','fecha_created_at'])

DF=DF.rename(columns={'paso_proceso':'paso','fecha_created_at':'FECHA'})

#"""LIMPIEZA"""

DF=DF.merge(maximizador_pantalla(DF),on='numero_socio',how='left')
DF=DF.drop('paso',axis=1)
DF=DF.merge(maximizador_fecha(DF),on='numero_socio',how='left')
DF=DF.drop('FECHA',axis=1)
DF=DF.rename(columns={'PASO_MAXIMO':'paso'})
DF=DF.rename(columns={'FECHA_MAXIMA':'FECHA'})
DF['NOMBRE']=list(map(nombres,DF['nombre_s'],DF['apellido_paterno'],DF['apellido_materno']))
DF['ultima_pantalla']=list(map(ULTIMA_PANTALLA,DF['paso']))
DF=DF.drop_duplicates()
DF=DF[['NOMBRE','numero_socio','celular','evaluado','aprobado','mensaje_rechazo','ultima_pantalla','paso','Icc','BcScore','EstimadorIngresos','FECHA']]

DF=DF.fillna('VACIO')

#"""#CODIGO"""

st.title("FUNNEL PROTOTIPE")

#"""##FUNNEL"""

st.markdown(f': sad: FUNELL')

LISTA_PASOS=[]
LISTA_VALORES=[]

for i in range(0,12):
  LISTA_PASOS.append(i)
  LISTA_VALORES.append(len(DF[DF['paso']>=i]))

LISTA_PASOS=list(map(ULTIMA_PANTALLA,LISTA_PASOS))

data = dict(
    number=LISTA_VALORES,
    stage=LISTA_PASOS)
#fig = px.funnel(data, x='number', y='stage')
#fig.show()
#st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit") # de esta forma se va a mostrar el dataframe en Streamlit

#"""##BARRAS DE ACTIVIDAD"""

st.markdown(f':cry: GRAFICA DE ACTIVIDAD')

fecha_minima=DF['FECHA'].min()
fecha_maxima=DF['FECHA'].max()
fechas=[]
dias_a_sumar = 1
fechita=fecha_minima

timedelta(days=dias_a_sumar)


while fechita<=fecha_maxima:
  fechas.append(fechita)
  fechita = fechita + timedelta(days=dias_a_sumar)

ACTIVIDAD=[]
for i in range(0,len(fechas)-1):
  ACTIVIDAD.append(len(DF[(DF['FECHA']>=fechas[i])&(DF['FECHA']<=fechas[i+1])]))

# Datos de muestra
df = pd.DataFrame(list(zip(x,y)),columns=['FECHA','FRECUENCIA'])
#fig = px.bar(df, x = 'FECHA', y = 'FRECUENCIA')
#fig.show()
#st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit", **kwargs) # de esta forma se va a mostrar el dataframe en Streamlit

# Datos
#x = fechas[0:len(ACTIVIDAD)]
#y = ACTIVIDAD

# Gráfico de barras
#fig, ax = plt.subplots(figsize=(20,10))
#ax.bar(x=x, height=y)

# Mostrar el gráfico
#plt.show()

#"""##EN PROCESO"""

st.markdown(f':cry: ESTOS SOCIOS NO TERMINARON EL PROCESO')

TEMPORAL=DF[(DF['aprobado']==1)&(DF['evaluado']==1)&(DF['mensaje_rechazo']=='VACIO')]
TEMPORAL=TEMPORAL[['NOMBRE','numero_socio','celular','ultima_pantalla','paso','FECHA']]
TEMPORAL=TEMPORAL.sort_values(by='paso')
TEMPORAL=TEMPORAL.reset_index(drop=True)
TEMPORAL=TEMPORAL.rename(columns={'numero_socio':'NUMERO_SOCIO','celular':'CELULAR','ultima_pantalla':'ULTIMA_PANTALLA','paso':'PASO'})
#TEMPORAL.to_excel('EN PROCESO.xlsx')
st.write(TEMPORAL)

PROCESOS=TEMPORAL.pivot_table( ['FECHA'], ['PASO','NOMBRE','NUMERO_SOCIO','CELULAR'])
#PROCESOS=PROCESOS.sort_values(by='FECHA',ascending=False)
#PROCESOS.to_excel('PROCESOS_PIVOTE.xlsx')
PROCESOS

#"""##APROBADOS"""

st.markdown(f':cry: LOS SIGUIENTES SOCIOS TERMINARON EL PROCESO')

TEMPORAL=DF[(DF['aprobado']==1)&(DF['evaluado']==1)&(DF['mensaje_rechazo']=='N')&(DF['paso']==11)]
TEMPORAL=TEMPORAL[['NOMBRE','numero_socio','celular','ultima_pantalla','paso','FECHA']]
TEMPORAL=TEMPORAL.sort_values(by='paso')
TEMPORAL=TEMPORAL.reset_index(drop=True)
TEMPORAL=TEMPORAL.rename(columns={'numero_socio':'NUMERO_SOCIO','celular':'CELULAR','ultima_pantalla':'ULTIMA_PANTALLA','paso':'PASO'})
#TEMPORAL.to_excel('APROBADOS.xlsx')
st.write(TEMPORAL)


#"""##RECHAZADO"""

st.markdown(f':cry: LOS SIGUIENTES SOCIOS FUERON RECHAZADOS EN EL PROCESO')

TEMPORAL=DF[(DF['aprobado']==0)&(DF['evaluado']==1)]
TEMPORAL=TEMPORAL[['NOMBRE','numero_socio','celular','mensaje_rechazo','Icc','BcScore','EstimadorIngresos','paso','FECHA']]
TEMPORAL=TEMPORAL.sort_values(by='mensaje_rechazo')
TEMPORAL=TEMPORAL.reset_index(drop=True)
TEMPORAL=TEMPORAL.rename(columns={'numero_socio':'NUMERO_SOCIO','celular':'CELULAR','mensaje_rechazo':'MENSAJE_RECHAZO','Icc':'ICC','BcScore':'BCSCORE','EstimadorIngresos':'ESTIMADOR_INGRESOS','paso':'PASO'})
#TEMPORAL.to_excel('RECHAZADO.xlsx')
st.write(TEMPORAL)


RECHAZOS=TEMPORAL.pivot_table(['ICC','BCSCORE','ESTIMADOR_INGRESOS','FECHA'],['PASO','MENSAJE_RECHAZO','NOMBRE','NUMERO_SOCIO','CELULAR'])
RECHAZOS=RECHAZOS.sort_values(by='FECHA',ascending=False)
#RECHAZOS.to_excel('RECHAZOS_PIVOTE.xlsx')
RECHAZOS

#"""##INDEFINIDO"""

TEMPORAL=DF[(DF['aprobado']==0)&(DF['evaluado']==0)]
TEMPORAL=TEMPORAL[['NOMBRE','numero_socio','celular','mensaje_rechazo','paso','FECHA']]
TEMPORAL=TEMPORAL.sort_values(by='mensaje_rechazo')
TEMPORAL=TEMPORAL.reset_index(drop=True)
TEMPORAL=TEMPORAL.rename(columns={'numero_socio':'NUMERO_SOCIO','celular':'CELULAR','mensaje_rechazo':'MENSAJE_RECHAZO','paso':'PASO'})
#TEMPORAL.to_excel('INDEFINIDO.xlsx')
st.write(TEMPORAL)

