import numpy as np
from PIL import Image
import streamlit as st
import pandas as pd
pip install plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

title_image = Image.open("AppTitle.png")
st.set_page_config(page_title="Stock Clientes AFP Capital", 
                   page_icon=title_image, 
                   layout='wide')

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------
col1, col2, col3 = st.columns(3)
with col1:
	st.markdown("")
with col2:
	st.image(title_image,use_column_width='auto',width = 800)
with col3:
	st.markdown("")


st.markdown("##### Bienvenidos al Panel de Stock clientes AFP Capital, Aqui encontrarás la información necesaria para su gestión")

#importar datos
base = pd.read_csv('Base.csv',sep = ";")


#Filtro de segmento
sorted_segmento = base.groupby('Segmento')['Cantidad'].sum()\
    .sort_values(ascending=True).index

st.markdown("###### **Segmento:**")
Select_Segmento = []

Select_Segmento.append(st.selectbox('', sorted_segmento))


#Fitlro de Periodo
sorted_periodo = base.groupby('Periodo_Cartera')['Cantidad'].sum().index.sort_values(ascending=False)

st.markdown("###### **Periodo:**")
select_Periodo = []

select_Periodo.append(st.selectbox('', sorted_periodo))



#Filtro basado en seleccion de segmento 
select_df = base[base['Segmento'].isin(Select_Segmento) & base['Periodo_Cartera'].isin(select_Periodo)]
df_Segmento = base[base['Segmento'].isin(Select_Segmento)]

abue2H = Image.open("abue2H.png")
abueM1 = Image.open("abueM1.png")
personas = Image.open("personas.jpg")
no_cotizantes = Image.open("no_cotizantes.jpg")

st.markdown(f"**Cantidad de Clientes:** {select_df['Cantidad'].sum()}")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Cotizantes:** {select_df[select_df['Tipo_Cotizante']=='Afiliado no Pensionado']['Cantidad'].sum()}")
    st.image([personas],width = 90)


with col2:
    st.markdown(f"**Pensionados:** {select_df[select_df['Tipo_Cotizante']=='Pensionado']['Cantidad'].sum()}")
    st.image([abue2H,abueM1],width = 40)


with col3:
    st.markdown(f"**No Cotizantes:** {select_df[select_df['Tipo_Cotizante']=='No Cotizante']['Cantidad'].sum()}")
    st.image([no_cotizantes],width = 90)

#EVOLUTIVO DE CLIENTES 
df_scarter = df_Segmento.groupby('Periodo_Cartera')['Cantidad'].sum()

trace0 = go.Scatter(
                x= df_scarter.index.astype(str),
                y= df_scarter.values,
                mode = 'lines+markers',
                marker_color = '#191970',
                legendgroup = 'grp1',
                showlegend=False
                )

layout = go.Layout(title = dict(text =  'Evolucion del Stock de Clientes',x=0.5,y=0.95),
	xaxis=dict(
	showgrid=False, # Hide Gridlines
	showline=False, # Hide X-Axis
	),
	yaxis=dict(
	categoryorder = "category ascending",
	showgrid=False, 
	showline=False
	),
	paper_bgcolor='LightSteelBlue',height=400, width=800
	)

fig2 = go.Figure(data=trace0,layout=layout)



st.plotly_chart(fig2,use_container_width=True)

fig = make_subplots(
	rows= 2, cols=2, 
        column_widths=[0.4, 0.6],
        specs=[[{"type": "pie"}, {"type": "bar"}],
              [ None, None]],
            subplot_titles=('Distribucion de clientes por Sexo','Distribucion Grupo de Productos'),vertical_spacing=0.01,horizontal_spacing= 0.05)

#PIE
#data for pie
pie_data = select_df.groupby('SEXO')['Cantidad'].sum()
colors = ['#87CEFA','#4682B4']

fig.add_trace(go.Pie(labels = pie_data.index,
                            values = pie_data.values,
                            hole = 0.4,
                            legendgroup = 'grp1',
                            showlegend=True),
                	    row = 1, col = 1)

fig.update_traces(hoverinfo = 'label+percent',
                        textinfo = 'value+percent',
                        textfont_color = 'white',
			marker=dict(colors=colors,line=dict(color='white', width=1)),
			row = 1, col = 1)

#STACKED BAR
grupo_df = select_df.groupby(['Grupo_Producto'])['Cantidad'].sum().sort_values(ascending=False)


fig.add_trace(go.Bar(y = grupo_df.values, 
			x = grupo_df.index,
                        marker_color = '#191970',
                        legendgroup = 'grp2',
                        showlegend=False),
                        row = 1, col = 2)


fig.update_yaxes(linecolor = 'grey', mirror = False, 
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False,automargin=False,
                        row = 1, col = 2)



fig.update_layout(height=800, width=800, paper_bgcolor="LightSteelBlue")


st.plotly_chart(fig,use_container_width=True)


with st.expander("Definiciones"):
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Segmento")
        st.markdown("La Segmentación Estratégica de Clientes permite monitorear el desempeño de los negocios, clasificando a los clientes en 5 segmentos, Alto Patrimonio, Prime, Alto Valor, Rentas Medias y Rentas Masivas, de acuerdo a ciertas características que tiene el cliente")
    
    with col2:
        st.subheader("Tipo de Cliente")
        st.markdown("**Cotizante:** Cliente que cotiza en el sistema de AFP")
        st.markdown("**Pensionado:** Cliente que recibe pensión o algun otro beneficio estatal")
        st.markdown("**No Cotizantes:** Cliente con saldo mayor a 0 que no cotiza en el sistema de AFP")

    with col3:  
        st.subheader("Grupo Productos")        
        st.markdown("**AFP**: Incluye los productos **APO** (Ahorro Previsional Obligatorio), **APV** (Ahorro Previsional Voluntario) y **CTA2** (Ahorro Voluntario).")
        st.markdown("**CB** Corredora de Bolsa:  Incluye productos de Fondos Mutuos **FFMM**, Acciones **ACC**, Caja, Administración de Cartera **ADC**, Exchange-Traded Fund **ETF**, Fondos de Inversión, Fondo Inmoviliario **FI**, Pershing **PERSH**")
        st.markdown("**VIDA** Seguros de vida: Incluye la familia de productos Dotales y Flexibles (Ahorro e Inversión, No APV), Planificador, (Seguro de Vida con Ahorro e Inversión, No APV), Previsor (APV), Tradicionales (Protección, Prima Equivalente, No Ahorro) y Salud (Protección, Prima Equivalente, No Ahorro).")



