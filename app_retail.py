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

LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter,Arial,sans-serif", size=12),
    margin=dict(t=40, b=40, l=40, r=40),
)

# ─────────────────────────────────────────────
# CARGA DE DATOS (local en lugar de Google Drive)
# ─────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    # El CSV debe estar en la misma carpeta que este script
    ruta = Path(__file__).parent / "retail_limpio.csv"

    if not ruta.exists():
        st.error(
            f"❌ Archivo no encontrado: `{ruta}`\n\n"
            "Copia `retail_limpio.csv` a la carpeta del proyecto y recarga."
        )
        st.stop()

    df = pd.read_csv(ruta)
    df = df[df['TotalVenta'] > 0]

    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

    coord_paises = {
        'United Kingdom':       (55.3781,  -3.4360),
        'Germany':              (51.1657,  10.4515),
        'France':               (46.2276,   2.2137),
        'EIRE':                 (53.1424,  -7.6921),
        'Spain':                (40.4637,  -3.7492),
        'Netherlands':          (52.1326,   5.2913),
        'Belgium':              (50.5039,   4.4699),
        'Switzerland':          (46.8182,   8.2275),
        'Portugal':             (39.3999,  -8.2245),
        'Australia':            (-25.2744, 133.7751),
        'Norway':               (60.4720,   8.4689),
        'Italy':                (41.8719,  12.5674),
        'Channel Islands':      (49.3723,  -2.3644),
        'Finland':              (61.9241,  25.7482),
        'Cyprus':               (35.1264,  33.4299),
        'Sweden':               (60.1282,  18.6435),
        'Austria':              (47.5162,  14.5501),
        'Denmark':              (56.2639,   9.5018),
        'Japan':                (36.2048, 138.2529),
        'Israel':               (31.0461,  34.8516),
        'Singapore':            ( 1.3521, 103.8198),
        'USA':                  (37.0902, -95.7129),
        'Poland':               (51.9194,  19.1451),
        'Canada':               (56.1304, -106.3468),
        'Iceland':              (64.9631, -19.0208),
        'Greece':               (39.0742,  21.8243),
        'RSA':                  (-30.5595, 22.9375),
        'United Arab Emirates': (23.4241,  53.8478),
        'Malta':                (35.9375,  14.3754),
        'Lebanon':              (33.8547,  35.8623),
        'Lithuania':            (55.1694,  23.8813),
        'European Community':   (50.8503,   4.3517),
        'Brazil':               (-14.2350, -51.9253),
        'Bahrain':              (26.0667,  50.5577),
        'Saudi Arabia':         (23.8859,  45.0792),
        'Czech Republic':       (49.8175,  15.4730),
    }

    df['Lat'] = df['Country'].map(lambda x: coord_paises.get(x, (None, None))[0])
    df['Lon'] = df['Country'].map(lambda x: coord_paises.get(x, (None, None))[1])
    return df

df = cargar_datos()

# ─────────────────────────────────────────────
# SIDEBAR – FILTROS GLOBALES
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

dff = df[
    (df["Macro_Mercado"].isin(mercados)) &
    (df["Quantity"].between(q_min, q_max))
]

if dff.empty:
    st.warning("No hay datos. Ajusta los filtros.")
    st.stop()

# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
st.title("Análisis de Datos E-commerce")
k1, k2, k3 = st.columns(3)
k1.metric("Transacciones Filtradas", f"{len(dff):,}")
k2.metric("Facturación Total",       f"£{dff['TotalVenta'].sum():,.0f}")
k3.metric("Ticket Promedio",         f"£{dff['TotalVenta'].mean():,.2f}")
st.divider()

# ─────────────────────────────────────────────
# FILA 1: Mapa + Sunburst
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Distribución Geográfica y Volumen")
    map_data = (
        dff.dropna(subset=['Lat', 'Lon'])
        .groupby('Country', as_index=False)
        .agg({'TotalVenta': 'sum', 'Quantity': 'sum',
              'Lat': 'first', 'Lon': 'first', 'Macro_Mercado': 'first'})
    )
    fig_map = px.scatter_mapbox(
        map_data, lat="Lat", lon="Lon",
        size="TotalVenta", color="TotalVenta",
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=45, zoom=1.5,
        center={"lat": 45.0, "lon": 10.0}, opacity=0.7,
        mapbox_style="carto-positron", hover_name="Country",
        hover_data={"Lat": False, "Lon": False,
                    "TotalVenta": ":,.2f", "Quantity": True}
    )
    fig_map.update_layout(**LAYOUT, margin=dict(r=0, t=0, l=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("2. Comportamiento de Compra (Sunburst)")
    st.caption("Tamaño = Transacciones | Verde = Alta Rentabilidad (£) | Rojo = Baja")

    tree_data = (
        dff.groupby(['Macro_Mercado', 'Country'], as_index=False)
        .agg(Transacciones=('TotalVenta', 'count'), TotalVenta=('TotalVenta', 'sum'))
    )
    tree_data['Ticket_Promedio'] = tree_data['TotalVenta'] / tree_data['Transacciones']

    fig_sun = px.sunburst(
        tree_data,
        path=[px.Constant("Global"), "Macro_Mercado", "Country"],
        values="Transacciones", color="Ticket_Promedio",
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=dff['TotalVenta'].mean(),
        hover_name="Country"
    )
    fig_sun.update_traces(
        textinfo="label+value",
        texttemplate="%{label}<br>%{value:,.0f} txs",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Transacciones: %{value:,.0f}<br>"
            "Ticket Promedio: £%{color:,.2f}<extra></extra>"
        )
    )
    fig_sun.update_layout(**LAYOUT, margin=dict(r=0, t=20, l=0, b=0))
    st.plotly_chart(fig_sun, use_container_width=True)

# ─────────────────────────────────────────────
# FILA 2: Coordenadas Paralelas + Radar
# ─────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Relaciones Multidimensionales")
    st.info("Nota: Ejes en escala Logarítmica para evidenciar patrones ocultos por valores extremos.")

    df_sample = (
        dff[['Quantity', 'Price', 'TotalVenta']].dropna()
        .sample(n=min(1000, len(dff)), random_state=42)
    )
    df_paralelo = pd.DataFrame({
        'Vol. Comprado (Log)': np.log1p(df_sample['Quantity'].clip(lower=0)),
        'Precio Unit. (Log)':  np.log1p(df_sample['Price'].clip(lower=0)),
        'Facturación (Log)':   np.log1p(df_sample['TotalVenta'].clip(lower=0)),
    })

    fig_pc = px.parallel_coordinates(
        df_paralelo,
        dimensions=['Vol. Comprado (Log)', 'Precio Unit. (Log)', 'Facturación (Log)'],
        color="Facturación (Log)",
        color_continuous_scale=px.colors.diverging.Tealrose,
    )
    fig_pc.update_layout(
        **LAYOUT,
        coloraxis_colorbar=dict(title="Ventas (Log)", x=1.15),
        margin=dict(l=70, r=70, t=40, b=40)
    )
    st.plotly_chart(fig_pc, use_container_width=True)

with col4:
    st.subheader("4. Facturación Radial Top 6")

    escala = st.radio(
        "Escala del Polígono:",
        ["Logarítmica (Recomendada)", "Lineal (Muestra la asimetría)"],
        horizontal=True
    )
    tipo_eje = 'log' if 'Log' in escala else 'linear'

    top_paises = (
        dff.groupby("Country", as_index=False)["TotalVenta"]
        .sum().nlargest(6, "TotalVenta")
    )
    fig_radar = px.line_polar(
        top_paises, r="TotalVenta", theta="Country",
        line_close=True, markers=True,
        color_discrete_sequence=['#e63946'],
        hover_name="Country"
    )
    fig_radar.update_traces(
        fill='toself',
        hovertemplate="<b>%{theta}</b><br>Facturación Total: £%{r:,.0f}<extra></extra>"
    )
    fig_radar.update_layout(
        **LAYOUT,
        polar=dict(radialaxis=dict(visible=True, type=tipo_eje, showticklabels=False))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# GRÁFICO 5: Evolución Temporal
# ─────────────────────────────────────────────
if 'InvoiceDate' in dff.columns:
    st.subheader("5. Evolución Temporal de la Facturación (2010 - 2011)")
    st.caption("Desliza las barras inferiores para hacer zoom en meses o campañas específicas.")

    df_time = (
        dff.groupby(dff['InvoiceDate'].dt.date)['TotalVenta']
        .sum().reset_index()
        .rename(columns={'InvoiceDate': 'Fecha'})
    )
    df_time['Fecha'] = pd.to_datetime(df_time['Fecha'])

    fig_time = px.line(df_time, x="Fecha", y="TotalVenta",
                       color_discrete_sequence=['#457b9d'])
    fig_time.update_traces(line=dict(width=2))
    fig_time.update_yaxes(title="Facturación Total", tickprefix="£",
                          tickformat=",.0f", showgrid=True)
    fig_time.update_xaxes(title="", tickformat="%b %Y",
                          hoverformat="%d %b %Y", rangeslider_visible=True)
    fig_time.update_layout(**LAYOUT, margin=dict(r=0, t=20, l=0, b=0),
                           hovermode="x unified")
    st.plotly_chart(fig_time, use_container_width=True)
else:
    st.info("No se detectó la columna 'InvoiceDate' para generar el gráfico de evolución temporal.")
