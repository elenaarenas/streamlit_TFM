import streamlit as st
import pandas as pd
import pickle

# Load the model from the disk
with open('palladium_model_catboost.pkl', 'rb') as archivo:
    loaded_model = pickle.load(archivo)

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

# Feature definition as a list for calling Def generador_respuestas
paises_agrupados = ["ESTADOS UNIDOS", "MEXICO", "REPUBLICA DOMINICANA", "BRASIL", "ESPANA", "CANADA", "OTROS", "SIN PAIS"]

# Marketing actions answers Def
def generador_respuestas(probabilidad):
    if probabilidad is None:
        return ''
    if probabilidad >= 0.34:
        if 'SIN PAIS' in paises_agrupados:
            respuesta = ("**Acción comercial:**   Descuento del 7% a todas las reservas realizadas a través de canal directo y cuya tarifa sea no reembolsable. Descuento disponible a través de nuestra APP y programa de fidelización.")
        else:
            respuesta = ("**Acción comercial:**   Posibilidad de modificaciones ya sea, fechas de estancia o nº noches. Cualquier modificación de la reserva será cobrada en el momento y con una tarifa no reembolsable.")
    elif probabilidad <= 0.10:
        if 'SIN PAIS' in paises_agrupados:
            respuesta = ("**Acción comercial:**   Canal Intermediario - Descuento 10% en  el momento del check in")
        else:
            respuesta = ("**Acción comercial:**   Canal directo - Contratación servicios premium ofertados a través de nuestra app con un 30% de descuento de su precio original.")
    else:
        respuesta = ("**Acción comercial:**   Posibilidad de mejora de estancias con un upgrade de habitación + obsequio sorpresa.")

    return respuesta


# Setting layout page
st.set_page_config(layout='wide')

# Logo upload
logo = 'palladium_logo_2.png'

# Streamlit App setting and inputs
with st.container():
    column_1, column_2 = st.columns([0.8,1])
    with column_1:
        st.image(logo, width=520)
    with column_2:
        st.title('Cancelación de reservas hoteleras')
        st.write("Modelo de predicción de cancelaciones de la cadena hotelera Palladium")
        top_6_names_hotels = st.selectbox("Hoteles", options=['', "C.Riviera_Maya", "C.Punta_Cana", "C.Costa_Mujeres", "G.P._Jamaica", "G.P._Imb._R&SPA", "P.Vallarta", "Otros"])
        llegada_mes_anyo = st.selectbox("Mes de llegada", options=['', "January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021"])
        salida_mes_anyo = st.selectbox("Mes de salida", options=['', "January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021", 'January 2022'])
        lead_time_group = st.selectbox("Anticipo cancelación", options=['', "1_dia", "2_a_7_dias", "8_a_15_dias", "16_a_30_dias", "31_a_60_dias", "61_a_90_dias", "91_a_120_dias", "121_a_180_dias", "181_a_360_dias", "+360_dias"])
        paises_agrupados = st.selectbox("Paises agrupados", options=['', "ESTADOS UNIDOS", "MEXICO", "REPUBLICA DOMINICANA", "BRASIL", "ESPANA", "CANADA", "OTROS", "SIN PAIS"])
# Output
        if st.button('Predecir'):
            if not top_6_names_hotels or not llegada_mes_anyo or not salida_mes_anyo or not lead_time_group or not paises_agrupados:
                st.warning('Primero debes seleccionar los inputs para predecir la probabilidad de cancelación.', icon='⚠️')
            else:
                probabilidad = predecir_cancelacion(top_6_names_hotels, llegada_mes_anyo, salida_mes_anyo, lead_time_group, paises_agrupados)
                st.write(f'Esta reserva tiene una probabilidad del **{probabilidad:.2%}** de ser cancelada.')
                respuesta = generador_respuestas(probabilidad)
                st.write(f'{respuesta}')





# >34% > 120 días Lead Time, mayor probabilidad de cancelación. Acción comercial:
 # Mail brindando posibilidad de modificaciones ya sea, fechas de estancia o nº noches."
 #"Cualquier modificación de la reserva será cobrada en el momento y con una tarifa no reembolsable."

# > 34%  + Clientes SIN PAIS = ventas externas (TTOO). Acción Comercial:
 # Descuento del 7% a todas las reservas realizadas a través de canal directo y cuya tarifa sea no reembolsable. Dto a través de nuestra APP y programa de fidelización

# Cancelación entre el 10% y 34%
 # Posibilidad de mejora de estancias con un upgrade de habitación + obsequio sorpresa

# Cancelación razonable < 10%
 # Canal directo - Contratación servicios premium ofertados a través de su app con un 30% de descuento de su precio original.
 # Canal Intermediario - Descuento 10% en  el momento del check in.


