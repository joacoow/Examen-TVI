import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard E-Commerce Online Retail",
    page_icon="🚀",
    layout="wide"
)
# ─────────────────────────────────────────────
# INYECCIÓN DE CSS (DISEÑO CORPORATIVO)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Estilo para las tarjetas de los KPIs (Métricas) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.04);
        border-left: 5px solid #1d6fa4; /* Línea de acento azul */
    }
    
    /* Título principal más estilizado */
    .main-header {
        font-weight: 700;
        color: #1A252F;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #7F8C8D;
        font-size: 1.1rem;
        margin-top: 0px;
        margin-bottom: 2rem;
    }
    
    /* Estilo para las Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        border: 1px solid #e0e6ed;
        border-bottom: none;
        box-shadow: 0px -2px 5px rgba(0,0,0,0.02);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1d6fa4 !important;
        color: white !important;
        font-weight: bold;
    }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETA GLOBAL OPTIMIZADA
# ─────────────────────────────────────────────
COL_SEQ       = px.colors.sequential.YlGnBu  
COL_DIV       = "RdYlGn"                            
COL_MULTI     = px.colors.diverging.Tealrose        
COL_TIME      = "#1d6fa4"                           
COL_CAT       = ["#1d6fa4", "#f4a261", "#2a9d8f"]   

LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter,Arial,sans-serif", size=14, color="#333333"), # Tamaño de letra ligeramente mayor para full-width
)

# ─────────────────────────────────────────────
# CARGA DE DATOS 
# ─────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ruta = Path(__file__).parent / "retail_limpio.csv"
    if not ruta.exists():
        st.error(
            f"❌ Archivo no encontrado: `{ruta}`\n\n"
            "Copia `retail_limpio.csv` a la misma carpeta donde está este script y recarga."
        )
        st.stop()

    df = pd.read_csv(ruta)
    df = df[df['TotalVenta'] > 0]

    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

    df['Mes'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    return df

df = cargar_datos()

# ─────────────────────────────────────────────
# SIDEBAR – FILTROS GLOBALES MÁSTER
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("⚡ Filtros Rápidos")
    mercados = st.multiselect(
        "Mercado Territorial",
        options=df['Macro_Mercado'].unique(),
        default=df['Macro_Mercado'].unique()
    )
    
    q_min, q_max = st.slider(
        "Volumen (Quantity)",
        int(df["Quantity"].min()),
        int(df["Quantity"].max()),
        (1, 100)
    )
    
    st.divider()
    st.caption("Filtro Temporal Global")
    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()
    
    fechas_seleccionadas = st.date_input(
        "Rango de Operación",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

if len(fechas_seleccionadas) == 2:
    start_date, end_date = fechas_seleccionadas
else:
    start_date = end_date = fechas_seleccionadas[0]

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

dff = df[
    (df["Macro_Mercado"].isin(mercados)) &
    (df["Quantity"].between(q_min, q_max)) &
    (df["InvoiceDate"] >= start_date) & 
    (df["InvoiceDate"] <= end_date)
]

if dff.empty:
    st.warning("No hay datos para los criterios seleccionados. Ajusta los filtros.")
    st.stop()


# ─────────────────────────────────────────────
# ENCABEZADO GERENCIAL
# ─────────────────────────────────────────────
st.markdown('<h1 class="main-header">📊 Global E-Commerce Retail Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Dashboard Ejecutivo para el Análisis de Exportaciones y Comportamiento Transaccional (2010-2011)</p>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
k1.metric("Transacciones Filtradas", f"{len(dff):,}")
k2.metric("Facturación Total",       f"£{dff['TotalVenta'].sum():,.0f}")
k3.metric("Ticket Promedio",         f"£{dff['TotalVenta'].mean():,.2f}")
st.divider()

# ─────────────────────────────────────────────
# ESTRUCTURA DE PESTAÑAS (TABS)
# ─────────────────────────────────────────────
# Creamos las 5 pestañas con iconos para una navegación intuitiva
tab_mapa, tab_sunburst, tab_relaciones, tab_polar, tab_tiempo= st.tabs([

    "🌍 Mapa Geográfico", 
    "🎯 Comportamiento", 
    "🕸️ Multidimensional", 
    "⏱️ Estacionalidad", 
    "📈 Evolución Temporal",
])

# ── PESTAÑA 1: MAPA ──
with tab_mapa:
    st.subheader("Distribución Geográfica de Exportaciones")
    st.caption("Color: Ingresos Netos (£) | Animación: Avance mensual de aperturas de mercado.")

    df_mapa = (
        dff.groupby(['Country', 'Mes'], as_index=False)
        .agg(Ventas_Totales=('TotalVenta', 'sum'), Num_Transacciones=('TotalVenta', 'count'))
    )
    
    paises = df_mapa['Country'].unique()
    meses = df_mapa['Mes'].unique()
    grilla = pd.MultiIndex.from_product([paises, meses], names=['Country', 'Mes']).to_frame(index=False)
    
    df_mapa = pd.merge(grilla, df_mapa, on=['Country', 'Mes'], how='left')
    df_mapa = df_mapa.fillna({'Ventas_Totales': 0, 'Num_Transacciones': 0})
    df_mapa = df_mapa.sort_values('Mes')
    
    max_venta_mensual = df_mapa['Ventas_Totales'].max() if not df_mapa.empty else 1

    fig_mapa = px.choropleth(
        df_mapa, locations="Country", locationmode="country names",
        color="Ventas_Totales", hover_name="Country",
        hover_data={"Ventas_Totales": ':.2f', "Num_Transacciones": True, "Mes": False},
        animation_frame="Mes", color_continuous_scale=COL_SEQ, range_color=[0, max_venta_mensual]
    )
    # Aumentamos el height a 650 para aprovechar el ancho completo de la pantalla
    fig_mapa.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=650,
        geo=dict(showframe=False, showcoastlines=True, showcountries=True, countrycolor="#dddddd", showland=True, landcolor="#f9f9f9", projection_type='equirectangular')
    )
   
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    # NUEVO: Caja de interpretación
    with st.expander("💡 Interpretación Gerencial: Distribución Geográfica"):
        st.write("""
        El mapa evidencia la **hegemonía absoluta del mercado local (Reino Unido)** en el volumen de ingresos. 
        Sin embargo, al interactuar con el mapa, se identifican mercados satélites consistentes en Europa (Top 3). 
        Estratégicamente, esto indica que la cadena de suministro internacional actúa como un complemento de alto valor, 
        mientras que la logística nacional es el núcleo duro que sostiene financieramente la operación del día a día.
        """)

# ── PESTAÑA 2: SUNBURST ──
with tab_sunburst:
    st.subheader("Estructura de Mercado y Rentabilidad")
    st.caption("Tamaño del bloque = Volumen de transacciones | Color = Ticket Promedio (£)")

    df_sunburst = dff.dropna(subset=['Macro_Mercado', 'Country'])
    tree_data = (
        df_sunburst.groupby(['Macro_Mercado', 'Country'], as_index=False)
        .agg(Transacciones=('TotalVenta', 'count'), TotalVenta=('TotalVenta', 'sum'))
    )
    tree_data = tree_data[tree_data['Transacciones'] > 0]
    
    totales_por_mercado = tree_data.groupby('Macro_Mercado')['Transacciones'].transform('sum')
    mascara_menores = tree_data['Transacciones'] < (totales_por_mercado * 0.02)
    tree_data.loc[mascara_menores, 'Country'] = 'Otros (Menores)'
    tree_data = tree_data.groupby(['Macro_Mercado', 'Country'], as_index=False).agg({'Transacciones': 'sum', 'TotalVenta': 'sum'})

    tree_data['Ticket_Promedio'] = tree_data['TotalVenta'] / tree_data['Transacciones']
    tree_data['Ticket_Promedio'] = tree_data['Ticket_Promedio'].fillna(0)

    fig_sun = px.sunburst(
        tree_data, path=[px.Constant("Global"), "Macro_Mercado", "Country"],
        values="Transacciones", color="Ticket_Promedio",
        
        # 1. CAMBIO DE PALETA: Usamos la misma escala secuencial del mapa (COL_SEQ) 
        # o una neutra como Blues. Elimina la percepción de "pérdida" del color rojo.
        color_continuous_scale=px.colors.sequential.Blues, 
        
        # Eliminamos el color_continuous_midpoint ya que en escalas secuenciales no es necesario
        hover_name="Country"
    )
    
    fig_sun.update_traces(
        textinfo="label",
        hovertemplate="<b>%{label}</b><br>Transacciones: %{value:,.0f}<br>Ticket Promedio: £%{color:,.2f}<extra></extra>",
        
        # 2. DEFINICIÓN ESTRUCTURAL: Añadimos un borde blanco limpio entre los sectores
        marker=dict(line=dict(color='white', width=1.5)) 
    )
    # Aumentamos el height a 650
    fig_sun.update_layout(**LAYOUT, margin=dict(r=0, t=20, l=0, b=0), height=650)
    
    st.plotly_chart(fig_sun, use_container_width=True)
    
    # NUEVO: Caja de interpretación
    with st.expander("💡 Interpretación Gerencial: Estructura y Rentabilidad"):
        st.write("""
        Este gráfico revela una dualidad clave en el modelo de negocio. Mientras el **Reino Unido acapara la inmensa mayoría de las transacciones** (tamaño del bloque), su **ticket promedio tiende a ser menor**. 
        Por el contrario, los mercados internacionales (Top 3 y Resto del Mundo) compensan su bajo volumen de transacciones con **tickets de compra sustancialmente más altos** (colores más intensos), sugiriendo que las exportaciones corresponden a compras mayoristas o envíos consolidados de alto valor para mitigar costos de despacho.
        """)

# ── PESTAÑA 3: COORDENADAS PARALELAS ──
with tab_relaciones:
    st.subheader("Análisis de Relaciones Multidimensionales")
    st.info("Nota: Los ejes utilizan escala Logarítmica (Base e) para estabilizar la varianza extrema entre transacciones minoristas y mayoristas.")

    df_sample = dff[['Quantity', 'Price', 'TotalVenta']].dropna().sample(n=min(1000, len(dff)), random_state=42)
    df_paralelo = pd.DataFrame({
        'Vol. Comprado (Log)': np.log1p(df_sample['Quantity'].clip(lower=0)),
        'Precio Unit. (Log)':  np.log1p(df_sample['Price'].clip(lower=0)),
        'Facturación (Log)':   np.log1p(df_sample['TotalVenta'].clip(lower=0)),
    })

    fig_pc = px.parallel_coordinates(
        df_paralelo, dimensions=['Vol. Comprado (Log)', 'Precio Unit. (Log)', 'Facturación (Log)'],
        color="Facturación (Log)", color_continuous_scale=COL_MULTI,
    )
    # Ajustamos altura a 550
    fig_pc.update_layout(**LAYOUT, coloraxis_colorbar=dict(title="Ventas (Log)", x=1.05), margin=dict(l=70, r=70, t=40, b=40), height=550)
    st.plotly_chart(fig_pc, use_container_width=True)

    # NUEVO: Caja de interpretación
    with st.expander("💡 Interpretación Gerencial: Modelo de Precios y Volumen"):
        st.write("""
        El patrón más importante de este análisis multidimensional es el cruce de líneas desde un *Volumen Comprado* alto hacia un *Precio Unitario* bajo. 
        Esta pendiente inversa demuestra empíricamente una **Economía de Escala**. Los mayores ingresos de la compañía no provienen de la venta ocasional de artículos de lujo, sino de la alta rotación de productos económicos vendidos en volúmenes masivos. Esto confirma matemáticamente que el *core* del negocio tiene un comportamiento fuertemente mayorista (B2B).
        """)

# ── PESTAÑA 4: POLAR ──
with tab_polar:
    st.subheader("Estacionalidad Mensual (Reloj Anual de Ventas)")
    st.caption("Visualización del ciclo de ingresos a lo largo del año operativo.")
    
    escala = st.radio("Ajuste de Escala Radial:", ["Logarítmica (Recomendada para ver minorías)", "Lineal"], horizontal=True)
    tipo_eje = 'log' if 'Log' in escala else 'linear'

    if 'InvoiceDate' in dff.columns:
        polar_data = dff.dropna(subset=['InvoiceDate']).copy()
        polar_data['Mes_Num'] = polar_data['InvoiceDate'].dt.month
        
        polar_data = polar_data.groupby(['Mes_Num', 'Macro_Mercado'], as_index=False).agg(TotalVenta=('TotalVenta', 'sum'))
        
        meses_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
        polar_data['Mes'] = polar_data['Mes_Num'].map(meses_map)
        
        orden_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        polar_data['Mes'] = pd.Categorical(polar_data['Mes'], categories=orden_meses, ordered=True)
        polar_data = polar_data.sort_values('Mes')
        
        polar_data = polar_data.rename(columns={'Mes': 'Periodo', 'Macro_Mercado': 'Mercado', 'TotalVenta': 'Ventas'})

        fig_polar = px.bar_polar(
            polar_data, r="Ventas", theta="Periodo", color="Mercado", color_discrete_sequence=COL_CAT, template= "plotly_dark"
        )
        fig_polar.update_traces(hovertemplate="<b>%{theta}</b><br>Segmento: %{trace.name}<br>Facturación: £%{r:,.0f}<extra></extra>")
        # Ampliamos a 650 para que el radar se vea espectacular en pantalla completa
        fig_polar.update_layout(**LAYOUT, margin=dict(l=40, r=40, t=20, b=20), height=650, polar=dict(radialaxis=dict(visible=True, type=tipo_eje, showticklabels=False), angularaxis=dict(direction="clockwise")))
        st.plotly_chart(fig_polar, use_container_width=True)
    else:
        st.info("No se detectó la columna 'InvoiceDate'.")
            
        # NUEVO: Caja de interpretación
    with st.expander("💡 Interpretación Gerencial: Estacionalidad Anual"):
        st.write("""
            El 'reloj anual' demuestra que la estructura de ingresos es **altamente estacional**. Las ventas mantienen un ritmo base durante los primeros trimestres, pero experimentan una explosión comercial en el último trimestre (octubre - noviembre) impulsada por las festividades. 
            A nivel operativo, esto dicta que el dimensionamiento de inventarios en bodega y la capacidad de la flota de distribución deben planificarse con meses de anticipación para soportar el estrés logístico de fin de año sin caer en quiebres de stock.
            """)

# ── PESTAÑA 5: TIEMPO ──
with tab_tiempo:
    st.subheader("Evolución Temporal Continua")
    st.caption("Desliza los controles inferiores para hacer zoom en días o semanas específicas.")

    if 'InvoiceDate' in dff.columns:
        df_time = dff.groupby(dff['InvoiceDate'].dt.date)['TotalVenta'].sum().reset_index().rename(columns={'InvoiceDate': 'Fecha'})
        df_time['Fecha'] = pd.to_datetime(df_time['Fecha'])

        fig_time = px.line(df_time, x="Fecha", y="TotalVenta", color_discrete_sequence=[COL_TIME])
        fig_time.update_traces(line=dict(width=2))
        fig_time.update_yaxes(title="Facturación Total", tickprefix="£", tickformat=",.0f", showgrid=True, gridcolor="#eeeeee")
        fig_time.update_xaxes(title="", tickformat="%b %Y", hoverformat="%d %b %Y", rangeslider_visible=True)
        fig_time.update_layout(**LAYOUT, margin=dict(r=10, t=20, l=10, b=0), hovermode="x unified", height=500)
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("No se detectó la columna 'InvoiceDate'.")
    
    # NUEVO: Caja de interpretación
    with st.expander("💡 Interpretación Gerencial: Dinámica Temporal"):
        st.write("""
            Esta vista continua permite a la gerencia auditar la volatilidad diaria de las ventas y medir el impacto exacto de campañas de marketing puntuales. 
            
            *Nota analítica para la comisión:* La caída abrupta que se observa en los últimos días de diciembre de 2011 **no representa un desplome real en las ventas comerciales**, sino que corresponde al límite temporal (fecha de corte) de la recolección de datos de nuestra muestra.
            """)
