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
        padding: 20px 24px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.03);
        border-left: 5px solid #1d6fa4;
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 15px rgba(29,111,164,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #7f8c8d !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #1a252f !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 5px;
    }
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
        font-family: 'Inter', Arial, sans-serif;
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

    /* 7. Contenedores de Gráficos */
    [data-testid="stPlotlyChart"] {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e0e6ed;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.04);
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
# 🚨 Se eliminaron COL_SEQ y COL_DIV: eran variables heredadas de una
#    versión previa de diseño que nunca llegaron a usarse en ningún gráfico.
# ─────────────────────────────────────────────
COL_MULTI     = px.colors.diverging.Tealrose
COL_TIME      = "#1d6fa4"
COL_CAT       = ["#1d6fa4", "#f4a261", "#2a9d8f"]
TXT_COLOR     = "#4a5568"

LAYOUT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Inter, Arial, sans-serif", size=13, color=TXT_COLOR),
    margin=dict(t=55, l=20, r=20, b=25),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TXT_COLOR)),
)

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'scrollZoom': False
}

# 🚨 Nombres de país que el GeoJSON no reconoce con la grafía del dataset.
#    Se aplica SOLO al armar el mapa (locations); el resto del dashboard
#    sigue mostrando el nombre original en leyendas y tooltips.
MAPEO_PAISES_GEOJSON = {
    "EIRE": "Ireland",
    "USA": "United States of America",
    "RSA": "South Africa",
}


# ═════════════════════════════════════════════
# FUNCIONES DE DATOS (carga, filtros, KPIs)
# ═════════════════════════════════════════════
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


def detectar_columna_invoice(df):
    """Busca la columna que identifica cada factura (varía según la versión del dataset)."""
    for candidato in ["Invoice", "InvoiceNo", "InvoiceID", "Numero_Factura"]:
        if candidato in df.columns:
            return candidato
    return None


def aplicar_filtros(df, mercados, q_min, q_max, start_date, end_date, col_invoice):
    """
    Aplica los filtros globales del sidebar y devuelve el DataFrame maestro (dff).

    🚨 FIX: el filtro de Volumen (Quantity) antes comparaba línea por línea
    (df["Quantity"].between(q_min, q_max)), lo que podía dejar una factura
    "mutilada": algunas de sus líneas dentro del rango y otras fuera, mientras
    calcular_kpis() la seguía contando como 1 factura completa y sumaba solo
    la facturación de las líneas sobrevivientes -> Ticket Promedio y
    Facturación Total quedaban subestimados sin ningún aviso.

    Ahora el volumen se mide como el TOTAL de unidades por factura (sumando
    todas sus líneas), y la factura se incluye o excluye COMPLETA según ese
    total. Así ninguna factura puede quedar parcialmente representada.

    Si el dataset no trae columna de factura, se hace un fallback explícito
    al filtro por línea (documentado, no silencioso).
    """
    base = df[
        (df["Macro_Mercado"].isin(mercados)) &
        (df["InvoiceDate"] >= start_date) &
        (df["InvoiceDate"] <= end_date)
    ]

    if col_invoice and col_invoice in base.columns:
        qty_por_factura = base.groupby(col_invoice)["Quantity"].sum()
        facturas_calificadas = qty_por_factura[qty_por_factura.between(q_min, q_max)].index
        return base[base[col_invoice].isin(facturas_calificadas)]
    else:
        # Fallback: sin columna de factura no hay forma de agrupar, se filtra por línea.
        return base[base["Quantity"].between(q_min, q_max)]


def calcular_kpis(dff, col_invoice):
    """
    🚨 FIX: en este dataset cada fila es una LÍNEA de producto dentro de una factura,
    no una transacción completa. Si existe la columna de factura, contamos facturas
    únicas y calculamos el ticket promedio agrupando primero por factura. Si esa
    columna no existe en el CSV, hacemos un fallback transparente a nivel de línea
    (y el rótulo del KPI cambia para no inducir a error).
    """
    facturacion_total = dff["TotalVenta"].sum()

    if col_invoice and col_invoice in dff.columns:
        n_transacciones = dff[col_invoice].nunique()
        ticket_promedio = dff.groupby(col_invoice)["TotalVenta"].sum().mean()
        es_por_factura = True
    else:
        n_transacciones = len(dff)
        ticket_promedio = dff["TotalVenta"].mean()
        es_por_factura = False

    return n_transacciones, facturacion_total, ticket_promedio, es_por_factura


def normalizar_paises_geojson(df_mapa, columna="Country"):
    """Crea 'Country_Geo': la grafía que el GeoJSON reconoce (EIRE->Ireland, etc.)."""
    df_mapa = df_mapa.copy()
    df_mapa["Country_Geo"] = df_mapa[columna].replace(MAPEO_PAISES_GEOJSON)
    return df_mapa


# ═════════════════════════════════════════════
# FUNCIONES DE VISUALIZACIÓN (una por gráfico)
# ═════════════════════════════════════════════
def crear_mapa(dff, col_invoice):
    """
    🚨 FIX: "Num_Transacciones" contaba líneas de producto (.count() sobre
    TotalVenta), igual que el bug ya corregido en las tarjetas KPI y el sunburst.
    Ahora agrupa por factura única (nunique) cuando la columna existe; si no,
    hace fallback explícito a nivel de línea y cambia la etiqueta del hover
    para no llamar "transacciones" a algo que no lo es.
    """
    if col_invoice and col_invoice in dff.columns:
        df_mapa = (
            dff.groupby(['Country', 'Mes'], as_index=False)
            .agg(Ventas_Totales=('TotalVenta', 'sum'), Num_Facturas=(col_invoice, 'nunique'))
        )
        col_volumen, etiqueta_volumen = 'Num_Facturas', 'Facturas'
    else:
        df_mapa = (
            dff.groupby(['Country', 'Mes'], as_index=False)
            .agg(Ventas_Totales=('TotalVenta', 'sum'), Num_Lineas=('TotalVenta', 'count'))
        )
        col_volumen, etiqueta_volumen = 'Num_Lineas', 'Líneas de producto'

    paises = df_mapa['Country'].unique()
    meses = df_mapa['Mes'].unique()
    grilla = pd.MultiIndex.from_product([paises, meses], names=['Country', 'Mes']).to_frame(index=False)

    df_mapa = pd.merge(grilla, df_mapa, on=['Country', 'Mes'], how='left')
    df_mapa = df_mapa.fillna({'Ventas_Totales': 0, col_volumen: 0})
    df_mapa = df_mapa.sort_values('Mes')

    # 🚨 Normalización de nombres para que calcen con el featureidkey del GeoJSON
    df_mapa = normalizar_paises_geojson(df_mapa, columna="Country")

    max_venta_mensual = df_mapa['Ventas_Totales'].max() if not df_mapa.empty else 1
    url_geojson = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

    escala_cero_gris = [
        [0.0, "#e0e6ed"], [0.000001, "#e0e6ed"], [0.000001, "#9ecae1"],
        [0.5, "#3182bd"], [1.0, "#08306b"]
    ]

    fig_mapa = px.choropleth_mapbox(
        df_mapa, geojson=url_geojson, featureidkey="properties.name",
        locations="Country_Geo",  # 🚨 nombre normalizado -> hace match con el GeoJSON
        color="Ventas_Totales", hover_name="Country",  # el hover muestra el nombre original
        custom_data=[col_volumen],
        animation_frame="Mes", color_continuous_scale=escala_cero_gris, range_color=[0, max_venta_mensual],
        mapbox_style="white-bg",
        zoom=1,
        center={"lat": 25.0, "lon": 0.0},
        opacity=0.85
    )

    # 🚨 hover_data de Plotly Express no permite anteponer el símbolo £ a los números,
    # así que se reemplaza por un hovertemplate manual. Como el mapa es animado (tiene
    # un frame por mes), hay que aplicarlo también a cada frame, no solo a la traza inicial.
    plantilla_hover = (
        "<b>%{hovertext}</b><br>"
        "Facturación: £%{z:,.2f}<br>"
        f"{etiqueta_volumen}: " + "%{customdata[0]:,.0f}<extra></extra>"
    )
    fig_mapa.update_traces(hovertemplate=plantilla_hover)
    for frame in fig_mapa.frames:
        for traza in frame.data:
            traza.hovertemplate = plantilla_hover

    fig_mapa.update_layout(
        LAYOUT,
        mapbox_layers=[{
            "below": 'traces', "sourcetype": "raster", "sourceattribution": "CartoDB",
            "source": ["https://basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"]
        }],
        margin=dict(r=10, t=10, l=10, b=20),
        height=700,
        coloraxis_colorbar=dict(
            title="Facturación<br>Total (£)", thickness=15, len=0.6,
            x=1.0, y=0.55, xanchor="left", yanchor="middle",
            tickprefix="£", tickformat=",.0f",
            tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)
        )
    )
    fig_mapa.update_layout(mapbox_domain=dict(x=[0, 1], y=[0.12, 1]))

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

    return fig_mapa


def crear_sunburst(dff, col_invoice):
    """
    🚨 FIX: igual que en las tarjetas KPI superiores, "Transacciones" aquí antes
    contaba líneas de producto (.count() sobre TotalVenta), no facturas. Eso hacía
    que el "Ticket Promedio" de esta pestaña fuera incomparable con el de las
    tarjetas (que sí es por factura). Ahora ambos usan la misma metodología:
    se agrupa por factura única cuando la columna existe; si no, se hace un
    fallback explícito a nivel de línea y se etiqueta como tal (sin llamarlo
    "ticket promedio" para no insinuar algo que el dato no mide).
    """
    df_sunburst = dff.dropna(subset=['Macro_Mercado', 'Country'])

    if col_invoice and col_invoice in df_sunburst.columns:
        tree_data = (
            df_sunburst.groupby(['Macro_Mercado', 'Country'], as_index=False)
            .agg(Volumen=(col_invoice, 'nunique'), TotalVenta=('TotalVenta', 'sum'))
        )
        etiqueta_volumen = "Facturas"
        etiqueta_ticket = "Ticket Promedio"
    else:
        tree_data = (
            df_sunburst.groupby(['Macro_Mercado', 'Country'], as_index=False)
            .agg(Volumen=('TotalVenta', 'count'), TotalVenta=('TotalVenta', 'sum'))
        )
        etiqueta_volumen = "Líneas de producto"
        etiqueta_ticket = "Venta Promedio por Línea"

    tree_data = tree_data[tree_data['Volumen'] > 0].copy()
    if tree_data.empty:
        return None, None, etiqueta_volumen, etiqueta_ticket

    totales_por_mercado = tree_data.groupby('Macro_Mercado')['Volumen'].transform('sum')
    tree_data.loc[tree_data['Volumen'] < (totales_por_mercado * 0.02), 'Country'] = 'Otros (Menores)'
    tree_data = tree_data.groupby(['Macro_Mercado', 'Country'], as_index=False).agg({'Volumen': 'sum', 'TotalVenta': 'sum'})
    tree_data['Ticket_Promedio'] = (tree_data['TotalVenta'] / tree_data['Volumen']).fillna(0)

    fig_sun = px.sunburst(
        tree_data, path=[px.Constant("Global"), "Macro_Mercado", "Country"],
        values="Volumen", color="Ticket_Promedio",
        color_continuous_scale=px.colors.sequential.Blues, hover_name="Country"
    )
    fig_sun.update_traces(
        textinfo="label",
        hovertemplate=(
            f"<b>%{{label}}</b><br>{etiqueta_volumen}: %{{value:,.0f}}"
            f"<br>{etiqueta_ticket}: £%{{color:,.2f}}<extra></extra>"
        ),
        marker=dict(line=dict(color='white', width=1.5)),
        domain=dict(x=[0.02, 0.98], y=[0.0, 1.0])
    )
    fig_sun.update_layout(
        LAYOUT,
        margin=dict(r=90, t=20, l=0, b=20),
        height=580,
        coloraxis_colorbar=dict(
            title=f"{etiqueta_ticket} (£)".replace(" ", "<br>", 1), thickness=14, len=0.55,
            x=1.0, y=0.5, xanchor="left", yanchor="middle",
            tickprefix="£", tickformat=",.0f",
            tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)
        )
    )
    return fig_sun, tree_data, etiqueta_volumen, etiqueta_ticket


def crear_paralelas(dff):
    df_sample = dff[['Quantity', 'Price', 'TotalVenta']].dropna().sample(n=min(1000, len(dff)), random_state=42)
    df_paralelo = pd.DataFrame({
        'Vol. Comprado (Log)':        np.log1p(df_sample['Quantity'].clip(lower=0)),
        'Precio Unit. (Log £)':       np.log1p(df_sample['Price'].clip(lower=0)),
        'Facturación (Log £)':        np.log1p(df_sample['TotalVenta'].clip(lower=0)),
    })

    fig_pc = px.parallel_coordinates(
        df_paralelo, dimensions=['Vol. Comprado (Log)', 'Precio Unit. (Log £)', 'Facturación (Log £)'],
        color="Facturación (Log £)", color_continuous_scale=COL_MULTI,
    )
    # 🚨 Nota: los ejes están en escala logarítmica, así que anteponer "£" directo
    # a los números del eje sería engañoso (mostrarían ln(precio), no el precio real).
    # Por eso la unidad monetaria se indica en el nombre de la dimensión/colorbar,
    # y se explicita en el texto de apoyo bajo el gráfico.
    fig_pc.update_layout(
        LAYOUT,
        coloraxis_colorbar=dict(title="Facturación<br>(Log £)", x=1.05, tickfont=dict(color=TXT_COLOR), title_font=dict(color=TXT_COLOR)),
        margin=dict(l=70, r=70, t=50, b=40), height=550
    )
    return fig_pc


def crear_polar(dff, tipo_eje):
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
    # 🚨 FIX: "%{trace.name}" no es un token válido de Plotly (por eso el tooltip mostraba "Segmento: -").
    # El nombre de cada traza (Mercado) se referencia con "%{fullData.name}".
    fig_polar.update_traces(fill='toself', hovertemplate="<b>%{theta}</b><br>Segmento: %{fullData.name}<br>Facturación: £%{r:,.0f}<extra></extra>")
    fig_polar.update_layout(
        LAYOUT, margin=dict(l=30, r=30, t=40, b=30), height=560,
        polar=dict(
            bgcolor="#eef1f7", domain=dict(x=[0.02, 0.98], y=[0.0, 1.0]),
            radialaxis=dict(visible=True, type=tipo_eje, showticklabels=False, gridcolor="white", gridwidth=1, linecolor="white"),
            angularaxis=dict(direction="clockwise", gridcolor="white", linecolor="white", tickfont=dict(color=TXT_COLOR))
        ),
        legend=dict(
            title="", orientation="h", yanchor="top", y=-0.05,
            xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)", font=dict(color=TXT_COLOR)
        )
    )
    return fig_polar, polar_data


def crear_tiempo(dff):
    df_time = dff.groupby(dff['InvoiceDate'].dt.date)['TotalVenta'].sum().reset_index().rename(columns={'InvoiceDate': 'Fecha'})
    df_time['Fecha'] = pd.to_datetime(df_time['Fecha'])

    fig_time = px.line(df_time, x="Fecha", y="TotalVenta", color_discrete_sequence=[COL_TIME])
    fig_time.update_traces(line=dict(width=2))
    fig_time.update_yaxes(title="Facturación Total", tickprefix="£", tickformat=",.0f", showgrid=True, gridcolor="#e0e6ed")
    fig_time.update_xaxes(title="", tickformat="%b %Y", hoverformat="%d %b %Y", rangeslider_visible=True)
    fig_time.update_layout(LAYOUT, margin=dict(r=10, t=20, l=10, b=0), hovermode="x unified", height=500)
    return fig_time, df_time


# ═════════════════════════════════════════════
# CARGA DE DATOS Y DETECCIÓN DE COLUMNA DE FACTURA
# ═════════════════════════════════════════════
df = cargar_datos()
COL_INVOICE = detectar_columna_invoice(df)

# ─────────────────────────────────────────────
# SIDEBAR – FILTROS GLOBALES MÁSTER
# ─────────────────────────────────────────────
with st.sidebar:
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

    # 🚨 FIX: los límites y el valor por defecto del slider ahora se calculan sobre
    # el TOTAL de unidades por factura (no por línea), coherente con aplicar_filtros().
    # El valor por defecto es el rango completo -> igual que Mercado y Fecha,
    # por defecto ningún filtro esconde datos; el usuario decide si acota.
    if COL_INVOICE and COL_INVOICE in df.columns:
        qty_por_factura_global = df.groupby(COL_INVOICE)["Quantity"].sum()
        qty_min_bound, qty_max_bound = int(qty_por_factura_global.min()), int(qty_por_factura_global.max())
        etiqueta_qty = "📦 Volumen por Factura (unidades totales)"
    else:
        qty_min_bound, qty_max_bound = int(df["Quantity"].min()), int(df["Quantity"].max())
        etiqueta_qty = "📦 Volumen (Quantity por línea)"

    st.markdown(f"<p style='color: #1d6fa4; font-size: 0.8rem; font-weight: 600; margin-top: 15px; margin-bottom: 5px;'>{etiqueta_qty}</p>", unsafe_allow_html=True)
    q_min, q_max = st.slider(
        etiqueta_qty,
        qty_min_bound,
        qty_max_bound,
        (qty_min_bound, qty_max_bound),
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

dff = aplicar_filtros(df, mercados, q_min, q_max, start_date, end_date, COL_INVOICE)

if dff.empty:
    st.warning("No hay datos para los criterios seleccionados. Ajusta los filtros.")
    st.stop()

# ─────────────────────────────────────────────
# ENCABEZADO GERENCIAL
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

# 🚨 FIX: cada fila del dataset es una línea de producto, no una factura completa.
# calcular_kpis() cuenta facturas únicas y promedia el ticket a nivel de factura
# cuando existe la columna correspondiente; si no, hace un fallback honesto a nivel
# de línea y cambia el rótulo para no insinuar algo que el dato no respalda.
n_transacciones, facturacion_total, ticket_promedio, es_por_factura = calcular_kpis(dff, COL_INVOICE)

k1, k2, k3 = st.columns(3)
if es_por_factura:
    k1.metric("🧾 Facturas Filtradas", f"{n_transacciones:,}")
    k3.metric("🎟️ Ticket Promedio (por factura)", f"£{ticket_promedio:,.2f}")
else:
    k1.metric("🧾 Líneas Filtradas", f"{n_transacciones:,}")
    k3.metric("🎟️ Venta Promedio (por línea)", f"£{ticket_promedio:,.2f}")
k2.metric("💰 Facturación Total", f"£{facturacion_total:,.0f}")

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
    fig_mapa = crear_mapa(dff, COL_INVOICE)
    st.plotly_chart(fig_mapa, use_container_width=True, config=PLOTLY_CONFIG)

    with st.expander("💡 Interpretación Gerencial: Distribución Geográfica"):
        st.markdown(
            "**Lectura:** Reino Unido concentra la gran mayoría de la facturación, "
            "mientras que Alemania, Francia e Irlanda destacan como mercados internacionales "
            "complementarios. El slider mensual permite observar si esta distribución se mantiene "
            "estable a lo largo del año o si algún mercado gana peso en fechas puntuales."
        )

# ── PESTAÑA 2: SUNBURST ──
with tab_sunburst:
    fig_sun, tree_data, etiqueta_volumen, etiqueta_ticket = crear_sunburst(dff, COL_INVOICE)

    # Definimos los datos reales antes de cualquier agrupación para contar bien los países
    df_sunburst = dff.dropna(subset=['Country']) 
    paises_activos = df_sunburst["Country"].nunique()

    if fig_sun is None:
        st.info("No hay datos suficientes para construir el gráfico jerárquico con los filtros actuales.")
    else:
        col_chart, col_info = st.columns([2.1, 1], gap="medium")

        with col_chart:
            st.plotly_chart(fig_sun, use_container_width=True, config=PLOTLY_CONFIG)

        with col_info:
            top_pais = tree_data.loc[tree_data['TotalVenta'].idxmax()]
            top_ticket = tree_data.loc[tree_data['Ticket_Promedio'].idxmax()]
            
            st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
            st.metric("🏆 País líder en facturación", top_pais['Country'], f"£{top_pais['TotalVenta']:,.0f}")
            st.metric(f"💎 Mayor {etiqueta_ticket.lower()}", top_ticket['Country'], f"£{top_ticket['Ticket_Promedio']:,.2f}")
            
            # 👇 CORRECCIÓN APLICADA AQUÍ: Usamos la variable paises_activos
            st.metric("🗂️ Países / Regiones activas", f"{paises_activos}")
            
            st.markdown(
                f"<p style='color:#7f8c8d; font-size:0.85rem; line-height:1.6; margin-top:10px;'>"
                f"El color representa el <b>{etiqueta_ticket.lower()}</b>; el tamaño del bloque, el volumen de {etiqueta_volumen.lower()}."
                f"</p>", unsafe_allow_html=True
            )

    with st.expander("💡 Interpretación Gerencial: Estructura y Rentabilidad"):
        st.markdown(
            "**Lectura:** Los mercados internacionales presentan menor volumen de transacciones, "
            "pero mayor venta promedio que el Reino Unido. Esto podría ser compatible con compras de "
            "mayor tamaño o valor por envío, aunque el dataset no incorpora información logística "
            "(costos de despacho, tipo de cliente) que permita confirmarlo directamente."
        )

# ── PESTAÑA 3: MULTIDIMENSIONAL ──
with tab_relaciones:
    fig_pc = crear_paralelas(dff)
    st.plotly_chart(fig_pc, use_container_width=True, config={'displayModeBar': True})
    st.markdown("<p style='color: #7f8c8d; font-size: 0.85rem; font-style: italic;'>Nota: Precio Unitario y Facturación están expresados en libras esterlinas (£) antes de aplicar la escala logarítmica (Base e), la cual se usa para estabilizar la varianza extrema entre transacciones minoristas y mayoristas.</p>", unsafe_allow_html=True)

    with st.expander("💡 Interpretación Gerencial: Modelo de Precios y Volumen"):
        st.markdown(
            "**Lectura:** Se observa que las transacciones de mayor volumen suelen asociarse a "
            "productos de menor precio unitario. Este patrón es compatible con compras mayoristas, "
            "aunque el dataset no contiene tipo de cliente, costos ni condiciones comerciales que "
            "permitan confirmar directamente un comportamiento B2B."
        )

# ── PESTAÑA 4: POLAR ──
with tab_polar:
    escala = st.radio("📐 Escala Radial (Estacionalidad):", ["Lineal", "Logarítmica"], horizontal=True)
    tipo_eje = 'log' if 'Log' in escala else 'linear'

    fig_polar, polar_data = crear_polar(dff, tipo_eje)

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
    fig_time, df_time = crear_tiempo(dff)
    st.plotly_chart(fig_time, use_container_width=True, config=PLOTLY_CONFIG)
    st.markdown("<p style='color: #7f8c8d; font-size: 0.85rem; font-style: italic;'>Desliza los controles inferiores para hacer zoom en días o semanas específicas.</p>", unsafe_allow_html=True)

    with st.expander("💡 Interpretación Gerencial: Dinámica Temporal"):
        # 🚨 FIX: "impacto exacto de campañas" no es una afirmación que el dataset respalde
        # (no existe una variable de campañas), y la fecha de corte real se calcula desde
        # los propios datos en vez de asumir "fin de diciembre".
        fecha_corte = max_date.strftime('%d-%m-%Y')
        st.markdown(
            "Esta vista continua permite a la gerencia identificar fechas con aumentos o caídas "
            "de facturación, que posteriormente podrían relacionarse con campañas, festividades u "
            "otros eventos externos al dataset.\n\n"
            f"**Nota analítica para la comisión:** la caída final que se observa corresponde al "
            f"corte de la muestra el **{fecha_corte}** y no necesariamente a una caída real del negocio."
        )