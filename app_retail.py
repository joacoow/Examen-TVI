import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
# INYECCIÓN DE CSS (DISEÑO CORPORATIVO DASH)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* 1. Limitar ancho máximo y centrar */
    [data-testid="block-container"] {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
 
    /* 2. Fondo global de la aplicación */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f6fa;
        font-family: 'Inter', Arial, sans-serif;
    }
 
    /* 3. Estilo del Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f4f6fa 100%);
        border-right: 1px solid #e0e6ed;
        width: 340px !important;
    }
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stDateInput label {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #1d6fa4 !important;
    }
    
    /* 4. Tarjetas de los KPIs */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        border-radius: 12px;
        padding: 20px 24px; /* Ajuste para que no sean tan altas */
        box-shadow: 0px 4px 6px rgba(0,0,0,0.03);
        border-left: 5px solid #1d6fa4;
        transition: all 0.3s ease-in-out; /* Animación suave */
    }
    /* Efecto al pasar el cursor: La tarjeta se eleva y proyecta más sombra */
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 15px rgba(29,111,164,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #7f8c8d !important; /* Gris elegante (Muteado) */
        font-weight: 700 !important;
        font-size: 0.85rem !important; /* Letra más pequeña */
        text-transform: uppercase; /* Todo en mayúsculas estilo corporativo */
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #1a252f !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 5px;
    }
    /* Reducimos el espacio en blanco superior general de Streamlit */
    [data-testid="block-container"] {
        padding-top: 2rem !important; 
    }
 
    /* 5. Encabezados Principales */
    .main-header {
        font-weight: 800;
        color: #1d6fa4;
        margin-bottom: 5px;
        font-size: 2.5rem;
        text-align: center;
    }
    .sub-header {
        color: #7f8c8d;
        font-size: 1.15rem;
        margin-top: 0px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
 
    /* 6. Estilo para las Pestañas (Tabs tipo "pill" flotante) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        border-radius: 14px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.03);
        gap: 6px;
        padding: 6px;
        width: 100%;
        display: flex;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        justify-content: center;
        background-color: transparent;
        border: none;
        color: #7f8c8d;
        padding: 12px 0px;
        font-family: 'Inter', Arial, sans-serif; /* 🚨 Forzamos la tipografía del Dashboard */
        font-size: 1.05rem !important;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.25s ease-in-out;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(29,111,164,0.08);
        color: #1d6fa4;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1d6fa4 0%, #164f79 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 6px 14px rgba(29,111,164,0.28);
    }
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
 
    /* 7. Contenedores de Gráficos (Corrección del desbordamiento) */
    [data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e0e6ed;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.04);
        /* 🚨 Eliminamos el padding CSS que empujaba el gráfico hacia afuera */
    }
 
    /* 8. Cajas de Interpretación */
    [data-testid="stExpander"] {
        background-color: rgba(29,111,164,0.05);
        border: none;
        border-left: 4px solid #1d6fa4;
        border-radius: 8px;
        margin-top: 15px;
    }
    [data-testid="stExpander"] summary p {
        color: #1d6fa4 !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
    }
    [data-testid="stExpander"] div[data-testid="stText"] p, 
    [data-testid="stExpander"] .stMarkdown p {
        color: #4a5568;
        line-height: 1.8;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# PALETA GLOBAL Y LAYOUT PLOTLY (HOMOLOGADO)
# ─────────────────────────────────────────────
COL_SEQ       = px.colors.sequential.YlGnBu  
COL_DIV       = "RdYlGn"                            
COL_MULTI     = px.colors.diverging.Tealrose        
COL_TIME      = "#1d6fa4"                           
COL_CAT       = ["#1d6fa4", "#f4a261", "#2a9d8f"]   
TXT_COLOR     = "#4a5568"
 
LAYOUT = dict(
    paper_bgcolor="#ffffff", # 🚨 Fondo blanco nativo para sellar la caja por dentro
    plot_bgcolor="#ffffff",
    font=dict(family="Inter, Arial, sans-serif", size=13, color=TXT_COLOR),
    margin=dict(t=55, l=20, r=20, b=25), # 🚨 Usamos este margen como nuestro nuevo "padding"
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TXT_COLOR)),
)
 
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'scrollZoom': False
}
 
# ─────────────────────────────────────────────
# CARGA DE DATOS 
# ─────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ruta = Path(__file__).parent / "retail_limpio.csv"
    if not ruta.exists():
        st.error(f"❌ Archivo no encontrado: `{ruta}`\n\nCopia `retail_limpio.csv` a la misma carpeta donde está este script y recarga.")
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
    # Título reducido y balanceado (H4 en lugar de H3, fuente a 1.25rem)
    st.markdown("""
    <div style='text-align: center; padding-bottom: 5px;'>
        <span style='font-size: 2rem;'>🛒</span>
        <h4 style='color: #1a252f; font-weight: 800; margin-top: 5px; margin-bottom: 0; font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em;'>Filtros de Tienda</h4>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
 
    st.markdown("<p style='color: #1d6fa4; font-size: 0.8rem; font-weight: 600; margin-bottom: 5px;'>🌍 Mercado Territorial</p>", unsafe_allow_html=True)
    mercados = st.multiselect(
        "Mercado Territorial",
        options=df['Macro_Mercado'].unique(),
        default=df['Macro_Mercado'].unique(),
        label_visibility="collapsed"
    )
    
    st.markdown("<p style='color: #1d6fa4; font-size: 0.8rem; font-weight: 600; margin-top: 15px; margin-bottom: 5px;'>📦 Volumen (Quantity)</p>", unsafe_allow_html=True)
    q_min, q_max = st.slider(
        "Volumen (Quantity)",
        int(df["Quantity"].min()),
        int(df["Quantity"].max()),
        (1, 100),
        label_visibility="collapsed"
    )
    
    st.markdown("<p style='color: #1d6fa4; font-size: 0.8rem; font-weight: 600; margin-top: 15px; margin-bottom: 5px;'>📅 Rango de Operación</p>", unsafe_allow_html=True)
    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()
    
    fechas_seleccionadas = st.date_input(
        "Rango de Operación",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
 
    st.divider()
    st.markdown("<p style='color: #8fa5b8; font-size: 0.72rem; text-align: center; margin-bottom: 0px;'>Business Intelligence · Retail 2026</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8fa5b8; font-size: 0.68rem; text-align: center;'>Dataset: Online Retail (UCI ML Repository)</p>", unsafe_allow_html=True)
 
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
# ENCABEZADO GERENCIAL (Temática Retail E-Commerce)
# ─────────────────────────────────────────────
st.markdown("""
<div style="background-color: #ffffff; padding: 20px 30px; border-radius: 12px; border: 1px solid #e0e6ed; border-left: 6px solid #1d6fa4; box-shadow: 0px 4px 6px rgba(0,0,0,0.04); margin-bottom: 2rem; margin-top: 0; display: flex; align-items: center; justify-content: space-between;">
    <div>
        <h1 style="color: #1a252f; font-weight: 800; font-size: 2.1rem; margin-bottom: 0.3rem; padding: 0;">🛍️ Global E-Commerce & Retail Intelligence</h1>
        <p style="color: #7f8c8d; font-size: 1.05rem; margin: 0; font-weight: 500;">Análisis Operativo y Transaccional — <span style="color: #1d6fa4; font-weight: 700;">UK Online Retail Store (2010-2011)</span></p>
    </div>
    <div style="text-align: right; color: #e0e6ed; opacity: 0.6;">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)
 
# Tarjetas de KPI (Las líneas divisorias st.divider() fueron eliminadas para un look más limpio)
k1, k2, k3 = st.columns(3)
k1.metric("🧾 Transacciones Filtradas", f"{len(dff):,}")
k2.metric("💰 Facturación Total",       f"£{dff['TotalVenta'].sum():,.0f}")
k3.metric("🎟️ Ticket Promedio",         f"£{dff['TotalVenta'].mean():,.2f}")
 
# Añadimos un pequeño espacio transparente en lugar de una línea horizontal rígida
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# ESTRUCTURA DE PESTAÑAS (TABS)
# ─────────────────────────────────────────────
tab_mapa, tab_sunburst, tab_relaciones, tab_polar, tab_tiempo = st.tabs([
    "🌍 Mapa Geográfico", 
    "🎯 Comportamiento", 
    "🕸️ Multidimensional", 
    "⏱️ Estacionalidad", 
    "📈 Evolución Temporal",
])
 
# ── PESTAÑA 1: MAPA ──
with tab_mapa:
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
    url_geojson = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    
    escala_cero_gris = [
        [0.0, "#e0e6ed"], [0.000001, "#e0e6ed"], [0.000001, "#9ecae1"],
        [0.5, "#3182bd"], [1.0, "#08306b"]
    ]
    
    fig_mapa = px.choropleth_mapbox(
        df_mapa, geojson=url_geojson, featureidkey="properties.name", locations="Country",
        color="Ventas_Totales", hover_name="Country",
        hover_data={"Ventas_Totales": ':.2f', "Num_Transacciones": True, "Mes": False},
        animation_frame="Mes", color_continuous_scale=escala_cero_gris, range_color=[0, max_venta_mensual],
        mapbox_style="white-bg", 
        zoom=1, #CORRECCIÓN: Aumenta el zoom para evitar la repetición del mapa */
        center={"lat": 25.0, "lon": 0.0}, # Centrado ajustado a Europa/Atlántico */
        opacity=0.85
    )
    
    fig_mapa.update_layout(
        LAYOUT,
        mapbox_layers=[{
            "below": 'traces', "sourcetype": "raster", "sourceattribution": "CartoDB",
            "source": ["https://basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"]
        }],
        # 🚨 Reducimos el margen inferior al mínimo: el hueco lo genera el "pad" del slider, no el margin
        margin=dict(r=10, t=10, l=10, b=20),
        height=700,
        coloraxis_colorbar=dict(
            title="Ventas<br>Totales", thickness=15, len=0.6,
            x=1.0, y=0.5, xanchor="left", yanchor="middle",
            tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)
        )
    )
 
    # 🚨 Acercamos el mapa a los controles reduciendo el dominio vertical del mapbox
    fig_mapa.update_layout(mapbox_domain=dict(x=[0, 1], y=[0.12, 1]))
 
    # 🚨 Subimos los controles y comprimimos su "pad" interno (fuente real del espacio en blanco)
    if fig_mapa.layout.updatemenus:
        fig_mapa.layout.updatemenus[0].x = 0.05
        fig_mapa.layout.updatemenus[0].y = 0.06
        fig_mapa.layout.updatemenus[0].pad = dict(t=0, b=0, l=0, r=0)
 
    if fig_mapa.layout.sliders:
        fig_mapa.layout.sliders[0].x = 0.08
        fig_mapa.layout.sliders[0].y = 0.1
        fig_mapa.layout.sliders[0].len = 0.85
        fig_mapa.layout.sliders[0].pad = dict(t=15, b=5, l=0, r=0)
        fig_mapa.layout.sliders[0].currentvalue = dict(
            prefix="Mes: ", font=dict(size=13, color=TXT_COLOR), xanchor="left"
        )
 
    st.plotly_chart(fig_mapa, use_container_width=True, config=PLOTLY_CONFIG)
    
    with st.expander("💡 Interpretación Gerencial: Distribución Geográfica"):
        st.markdown("**Lectura:** El mapa evidencia la hegemonía absoluta del mercado local (Reino Unido) en el volumen de ingresos. Sin embargo, al interactuar con el mapa, se identifican mercados satélites consistentes en Europa (Top 3). Estratégicamente, esto indica que la cadena de suministro internacional actúa como un complemento de alto valor, mientras que la logística nacional es el núcleo duro que sostiene financieramente la operación del día a día.")
 
# ── PESTAÑA 2: SUNBURST ──
with tab_sunburst:
    df_sunburst = dff.dropna(subset=['Macro_Mercado', 'Country'])
    tree_data = (
        df_sunburst.groupby(['Macro_Mercado', 'Country'], as_index=False)
        .agg(Transacciones=('TotalVenta', 'count'), TotalVenta=('TotalVenta', 'sum'))
    )
    tree_data = tree_data[tree_data['Transacciones'] > 0].copy() # Escudo anti-warnings
    if not tree_data.empty:
        totales_por_mercado = tree_data.groupby('Macro_Mercado')['Transacciones'].transform('sum')
        tree_data.loc[tree_data['Transacciones'] < (totales_por_mercado * 0.02), 'Country'] = 'Otros (Menores)'
        tree_data = tree_data.groupby(['Macro_Mercado', 'Country'], as_index=False).agg({'Transacciones': 'sum', 'TotalVenta': 'sum'})
        tree_data['Ticket_Promedio'] = (tree_data['TotalVenta'] / tree_data['Transacciones']).fillna(0)
 
        fig_sun = px.sunburst(
            tree_data, path=[px.Constant("Global"), "Macro_Mercado", "Country"],
            values="Transacciones", color="Ticket_Promedio",
            color_continuous_scale=px.colors.sequential.Blues, hover_name="Country"
        )
        fig_sun.update_traces(
            textinfo="label", hovertemplate="<b>%{label}</b><br>Transacciones: %{value:,.0f}<br>Ticket Promedio: £%{color:,.2f}<extra></extra>",
            marker=dict(line=dict(color='white', width=1.5)),
            # 🚨 Ampliamos el dominio del propio gráfico para que "respire" y reduzca el aire alrededor
            domain=dict(x=[0.02, 0.98], y=[0.0, 1.0])
        )
        fig_sun.update_layout(
            LAYOUT,
            margin=dict(r=90, t=20, l=0, b=20),
            height=580,
            coloraxis_colorbar=dict(
                title="Ticket<br>Promedio", thickness=14, len=0.55,
                x=1.0, y=0.5, xanchor="left", yanchor="middle",
                tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)
            )
        )
 
        # 🚨 Layout en columnas: el gráfico circular queda en un contenedor más angosto
        # (evita el "aire" lateral de estirar un círculo a todo el ancho) y la columna
        # derecha se llena con métricas de apoyo en vez de quedar en blanco.
        col_chart, col_info = st.columns([2.1, 1], gap="medium")
 
        with col_chart:
            st.plotly_chart(fig_sun, use_container_width=True, config=PLOTLY_CONFIG)
 
        with col_info:
            top_pais = tree_data.loc[tree_data['TotalVenta'].idxmax()]
            top_ticket = tree_data.loc[tree_data['Ticket_Promedio'].idxmax()]
            st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
            st.metric("🏆 País líder en facturación", top_pais['Country'], f"£{top_pais['TotalVenta']:,.0f}")
            st.metric("💎 Mayor ticket promedio", top_ticket['Country'], f"£{top_ticket['Ticket_Promedio']:,.2f}")
            st.metric("🗂️ Países / Regiones activas", f"{tree_data['Country'].nunique()}")
            st.markdown(
                "<p style='color:#7f8c8d; font-size:0.85rem; line-height:1.6; margin-top:10px;'>"
                "El color representa el <b>ticket promedio</b>; el tamaño del bloque, el volumen de transacciones."
                "</p>", unsafe_allow_html=True
            )
    
    with st.expander("💡 Interpretación Gerencial: Estructura y Rentabilidad"):
        st.markdown("**Lectura:** Este gráfico revela una dualidad clave en el modelo de negocio. Mientras el Reino Unido acapara la inmensa mayoría de las transacciones (tamaño del bloque), su ticket promedio tiende a ser menor. Por el contrario, los mercados internacionales (Top 3 y Resto del Mundo) compensan su bajo volumen de transacciones con tickets de compra sustancialmente más altos (colores más intensos), sugiriendo que las exportaciones corresponden a compras mayoristas o envíos consolidados de alto valor para mitigar costos de despacho.")
 
# ── PESTAÑA 3: MULTIDIMENSIONAL ──
with tab_relaciones:
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
    fig_pc.update_layout(
        LAYOUT, 
        coloraxis_colorbar=dict(title="Ventas (Log)", x=1.05, tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)), 
        margin=dict(l=70, r=70, t=50, b=40), height=550
    )
    st.plotly_chart(fig_pc, use_container_width=True, config={'displayModeBar': True})
    st.markdown("<p style='color: #7f8c8d; font-size: 0.85rem; font-style: italic;'>Nota: Los ejes utilizan escala Logarítmica (Base e) para estabilizar la varianza extrema entre transacciones minoristas y mayoristas.</p>", unsafe_allow_html=True)
 
    with st.expander("💡 Interpretación Gerencial: Modelo de Precios y Volumen"):
        st.markdown("**Lectura:** El patrón más importante de este análisis multidimensional es el cruce de líneas desde un Volumen Comprado alto hacia un Precio Unitario bajo. Esta pendiente inversa demuestra empíricamente una Economía de Escala. Los mayores ingresos de la compañía no provienen de la venta ocasional de artículos de lujo, sino de la alta rotación de productos económicos vendidos en volúmenes masivos. Esto confirma matemáticamente que el core del negocio tiene un comportamiento fuertemente mayorista (B2B).")
 
# ── PESTAÑA 4: POLAR ──
with tab_polar:
    escala = st.radio("📐 Escala Radial (Estacionalidad):", ["Lineal", "Logarítmica"], horizontal=True)
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
 
        fig_polar = px.line_polar(
            polar_data, r="Ventas", theta="Periodo", color="Mercado", line_close=True, 
            color_discrete_sequence=COL_CAT, markers=True
        )
        # 🚨 FIX: "%{trace.name}" no es un token válido de Plotly (por eso el tooltip mostraba "-").
        # El nombre de cada traza (Mercado) se referencia con "%{fullData.name}".
        fig_polar.update_traces(fill='toself', hovertemplate="<b>%{theta}</b><br>Segmento: %{fullData.name}<br>Facturación: £%{r:,.0f}<extra></extra>")
        fig_polar.update_layout(
            LAYOUT, margin=dict(l=30, r=30, t=40, b=30), height=560,
            polar=dict(
                # 🚨 Ampliamos el dominio del polar (antes terminaba en 0.82 dejando aire libre)
                bgcolor="#eef1f7", domain=dict(x=[0.02, 0.98], y=[0.0, 1.0]),
                radialaxis=dict(visible=True, type=tipo_eje, showticklabels=False, gridcolor="white", gridwidth=1, linecolor="white"),
                angularaxis=dict(direction="clockwise", gridcolor="white", linecolor="white", tickfont=dict(color=TXT_COLOR))
            ),
            # 🚨 La leyenda ahora va debajo del gráfico, centrada y horizontal, en vez de robar una franja vertical vacía
            legend=dict(
                title="", orientation="h", yanchor="top", y=-0.05,
                xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)", font=dict(color=TXT_COLOR)
            )
        )
 
        # 🚨 Layout en columnas: el gráfico polar (circular) queda en un contenedor más
        # angosto para no estirarse contra un rectángulo ancho, y la columna derecha
        # se llena con el detalle mensual del mercado líder en vez de quedar en blanco.
        col_chart, col_info = st.columns([2.1, 1], gap="medium")
 
        with col_chart:
            st.plotly_chart(fig_polar, use_container_width=True, config=PLOTLY_CONFIG)
 
        with col_info:
            mercado_top = polar_data.groupby('Mercado')['Ventas'].sum().idxmax()
            mes_pico = polar_data.loc[polar_data['Ventas'].idxmax()]
            st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
            st.metric("📌 Mercado dominante", mercado_top)
            st.metric("🔥 Mes pico de facturación", str(mes_pico['Periodo']), f"£{mes_pico['Ventas']:,.0f}")
            st.metric("🧭 Segmentos comparados", f"{polar_data['Mercado'].nunique()}")
            st.markdown(
                "<p style='color:#7f8c8d; font-size:0.85rem; line-height:1.6; margin-top:10px;'>"
                "Cada eje representa un mes; la distancia al centro es la facturación total de ese mes por mercado."
                "</p>", unsafe_allow_html=True
            )
 
        with st.expander("💡 Interpretación Gerencial: Estacionalidad Anual"):
            st.markdown("**Lectura:** El 'reloj anual' demuestra que la estructura de ingresos es altamente estacional. Las ventas mantienen un ritmo base durante los primeros trimestres, pero experimentan una explosión comercial en el último trimestre (octubre - noviembre) impulsada por las festividades. A nivel operativo, esto dicta que el dimensionamiento de inventarios en bodega y la capacidad de la flota de distribución deben planificarse con meses de anticipación para soportar el estrés logístico de fin de año sin caer en quiebres de stock.")
 
# ── PESTAÑA 5: TIEMPO ──
with tab_tiempo:
    if 'InvoiceDate' in dff.columns:
        df_time = dff.groupby(dff['InvoiceDate'].dt.date)['TotalVenta'].sum().reset_index().rename(columns={'InvoiceDate': 'Fecha'})
        df_time['Fecha'] = pd.to_datetime(df_time['Fecha'])
 
        fig_time = px.line(df_time, x="Fecha", y="TotalVenta", color_discrete_sequence=[COL_TIME])
        fig_time.update_traces(line=dict(width=2))
        fig_time.update_yaxes(title="Facturación Total", tickprefix="£", tickformat=",.0f", showgrid=True, gridcolor="#e0e6ed")
        fig_time.update_xaxes(title="", tickformat="%b %Y", hoverformat="%d %b %Y", rangeslider_visible=True)
        fig_time.update_layout(LAYOUT, margin=dict(r=10, t=20, l=10, b=0), hovermode="x unified", height=500)
        st.plotly_chart(fig_time, use_container_width=True, config=PLOTLY_CONFIG)
        st.markdown("<p style='color: #7f8c8d; font-size: 0.85rem; font-style: italic;'>Desliza los controles inferiores para hacer zoom en días o semanas específicas.</p>", unsafe_allow_html=True)
    
    with st.expander("💡 Interpretación Gerencial: Dinámica Temporal"):
        st.markdown("Esta vista continua permite a la gerencia auditar la volatilidad diaria de las ventas y medir el impacto exacto de campañas de marketing puntuales.\n\n**Nota analítica para la comisión:** La caída abrupta que se observa en los últimos días de diciembre de 2011 no representa un desplome real en las ventas comerciales, sino que corresponde al límite temporal (fecha de corte) de la recolección de datos de nuestra muestra.")