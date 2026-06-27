# 🚀 Dashboard E-Commerce Online Retail

Dashboard interactivo de análisis de datos construido con **Streamlit** y **Plotly**.

---

## 📁 Estructura del proyecto

```
dashboard_retail/
├── app_retail.py       ← Código principal del dashboard
├── requirements.txt    ← Librerías necesarias
├── .gitignore          ← Archivos excluidos de Git
├── README.md           ← Esta guía
└── retail_limpio.csv   ← ⚠️ Agregar manualmente (no está en el repo)
```

> **Importante:** El archivo `retail_limpio.csv` NO se sube al repositorio.
> Cada integrante debe copiarlo manualmente a la carpeta del proyecto.

---

## ⚙️ Configuración inicial (hacer UNA sola vez)

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/dashboard-retail.git
cd dashboard-retail
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Agregar el archivo de datos
Copia `retail_limpio.csv` dentro de la carpeta `dashboard-retail/`.

### 5. Ejecutar el dashboard
```bash
streamlit run app_retail.py
```
El navegador se abrirá automáticamente en `http://localhost:8501`

---

## 🤝 Flujo de trabajo en equipo (Git colaborativo)

### Antes de empezar a trabajar cada día
```bash
git pull origin main          # Bajar los últimos cambios del equipo
```

### Al terminar cambios propios
```bash
git add app_retail.py         # Agregar los archivos modificados
git commit -m "descripción breve del cambio"
git push origin main          # Subir al repositorio compartido
```

### Si hay conflictos
VS Code los marca visualmente. Elige qué versión conservar y luego:
```bash
git add app_retail.py
git commit -m "resuelve conflicto en sección X"
```

---

## 🌿 Buenas prácticas para trabajar en equipo

| Práctica | Por qué |
|---|---|
| Cada uno trabaja en su propia **rama** (`git checkout -b nombre/feature`) | Evita pisar el trabajo de otros |
| Hacer **commits pequeños y frecuentes** | Más fácil revertir errores |
| Escribir mensajes de commit descriptivos | El equipo entiende qué cambió |
| Nunca subir `retail_limpio.csv` al repo | Protege los datos y evita archivos pesados |
| Hacer `git pull` antes de empezar | Evita conflictos innecesarios |

---

## 🧩 Extensión recomendada en VS Code

Instala la extensión **GitLens** para ver el historial de cambios directamente en el editor.
