import streamlit as st
import pandas as pd
import pickle




# Load the model from the disk:
model_filename = "palladium_model_catboost.pkl"
loaded_model = pickle.load(open(model_filename, "rb"))

# Predictive Def
def predecir_cancelacion(top_6_names_hotels, llegada_mes_anyo, salida_mes_anyo, lead_time_group, paises_agrupados):
    datos = {
        'TOP_6_NAMES_HOTELS': [top_6_names_hotels],
        'LLEGADA_MES_ANYO': [llegada_mes_anyo],
        'SALIDA_MES_ANYO': [salida_mes_anyo],
        'LEAD_TIME_GROUP': [lead_time_group],
        'PAISES_AGRUPADOS': [paises_agrupados],
    }

    df = pd.DataFrame(datos)
    probabilidad_cancelacion = loaded_model.predict_proba(df)[0, 1]
    return probabilidad_cancelacion

# Streamlit app imputs
st.title("Cancelación Hotelera")
st.write("Modelo de predicción de cancelaciones de la cadena hotelera Palladium")

top_6_names_hotels = st.selectbox("Hotel", options=["C.Riviera_Maya", "C.Punta_Cana", "C.Costa_Mujeres", "G.P._Jamaica", "G.P._Imb._R&SPA", "P.Vallarta", "Otros"])
llegada_mes_anyo = st.selectbox("Mes de llegada", options=["January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021"])
salida_mes_anyo = st.selectbox("Mes de salida", options=["January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "November 2021", "October 2021", "December 2021", "January 2022"])
lead_time_group = st.selectbox("Anticipo cancelación", options=["1_dia", "2_a_7_dias","8_a_15_dias", "16_a_30_dias", "31_a_60_dias", "61_a_90_dias", "91_a_120_dias", "121_a_180_dias", "181_a_360_dias", "+360_dias"])
paises_agrupados = st.selectbox("Pais Origen", options=["ESTADOS UNIDOS", "MEXICO", "REPUBLICA DOMINICANA", "BRASIL", "ESPANA", "CANADA", "OTROS", "SIN PAIS"])



# Output
if st.sidebar.button('Predecir'):
    probabilidad = predecir_cancelacion(top_6_names_hotels, llegada_mes_anyo, salida_mes_anyo, lead_time_group, paises_agrupados)
    st.sidebar.success(f'Probabilidad de cancelación: {probabilidad:.2%}')

