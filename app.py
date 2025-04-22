import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Cargar datos
df = pd.read_csv('usuarios_ecobici_limpio.csv')  # Cambiá por tu ruta si es necesario

# Título de la app
st.title("Visualización de datos de usuarios")

# Selector de gráficos
opcion = st.selectbox("Seleccioná el gráfico que querés ver:", [
    "Histograma de edades",
    "Cantidad de usuarios por género",
    "Gráfico de pastel por género",
    "Evolución temporal de altas",
    "Distribución de usuarios por día de la semana",
    "Gráfico de calor por hora y día"
])

# Gráfico 1: Histograma de edades
if opcion == "Histograma de edades":
    fig, ax = plt.subplots()
    sns.histplot(df['edad'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title("Distribución de edades")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Cantidad de usuarios")
    st.pyplot(fig)

# Gráfico 2: Usuarios por género
elif opcion == "Cantidad de usuarios por género":
    fig, ax = plt.subplots()
    sns.countplot(x=df['genero'], palette='pastel', ax=ax)
    ax.set_title("Cantidad de usuarios por género")
    ax.set_xlabel("Género")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)

# Gráfico 3: Pie chart por género
elif opcion == "Gráfico de pastel por género":
    fig, ax = plt.subplots()
    df['genero'].value_counts().plot.pie(autopct='%1.1f%%', colors=['lightblue', 'lightcoral', 'lightgray'], ax=ax)
    ax.set_ylabel('')
    ax.set_title("Distribución porcentual por género")
    st.pyplot(fig)

# Gráfico 4: Evolución temporal de altas
elif opcion == "Evolución temporal de altas":
    # Convertir la columna fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Agrupar por fecha y contar usuarios
    usuarios_por_dia = df.groupby(df['fecha'].dt.date).size().reset_index(name='cantidad')
    usuarios_por_dia['fecha'] = pd.to_datetime(usuarios_por_dia['fecha'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(usuarios_por_dia['fecha'], usuarios_por_dia['cantidad'], marker='o', linestyle='-', color='purple')
    ax.set_title("Evolución temporal de altas de usuarios")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Cantidad de nuevos usuarios")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Mejorar formato de fechas en el eje x
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)

# Gráfico 5: Distribución por día de la semana
elif opcion == "Distribución de usuarios por día de la semana":
    # Convertir la columna fecha a datetime si no lo está
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Obtener el día de la semana (0=lunes, 6=domingo)
    df['dia_semana'] = df['fecha'].dt.dayofweek
    
    # Mapear números a nombres de días
    dias = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df['nombre_dia'] = df['dia_semana'].map(dias)
    
    # Contar usuarios por día
    conteo_dias = df['nombre_dia'].value_counts().reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=conteo_dias.index, y=conteo_dias.values, palette='viridis', ax=ax)
    ax.set_title("Distribución de altas por día de la semana")
    ax.set_xlabel("Día de la semana")
    ax.set_ylabel("Cantidad de usuarios")
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)

# Gráfico 6: Heatmap por hora y día
elif opcion == "Gráfico de calor por hora y día":
    # Convertir fecha y hora a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['hora'] = pd.to_datetime(df['hora']).dt.time
    
    # Extraer hora y día de la semana
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S').dt.hour
    df['dia_semana'] = df['fecha'].dt.dayofweek
    
    # Crear matriz para heatmap
    heatmap_data = pd.crosstab(df['hora'], df['dia_semana'])
    
    # Mapear números a nombres de días
    dias = {0: 'Lun', 1: 'Mar', 2: 'Mié', 3: 'Jue', 4: 'Vie', 5: 'Sáb', 6: 'Dom'}
    heatmap_data.columns = [dias[i] for i in heatmap_data.columns]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d", linewidths=.5, ax=ax)
    ax.set_title("Distribución de altas por hora y día de la semana")
    ax.set_ylabel("Hora del día")
    ax.set_xlabel("Día de la semana")
    
    plt.tight_layout()
    
    st.pyplot(fig)