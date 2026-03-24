import streamlit as st
import math

st.set_page_config(page_title="Diseño de Capacidad M/M/1", layout="centered")

st.title("📊 Diseño Inverso de Capacidad - Modelo M/M/1")

st.markdown("""
Esta aplicación calcula la **tasa mínima de servicio (μ)** necesaria 
para cumplir un nivel de servicio en una cola M/M/1.
""")

# Entradas
st.sidebar.header("Parámetros de entrada")

lambda_rate = st.sidebar.number_input(
    "Tasa de llegada λ (clientes/hora)", 
    min_value=0.1, 
    value=30.0
)

Wq_max_min = st.sidebar.number_input(
    "Tiempo máximo en cola (minutos)", 
    min_value=0.1, 
    value=2.0
)

# Conversión a horas
Wq_max = Wq_max_min / 60

# Cálculo de μ mínima
# Resolviendo: λ / (μ(μ - λ)) ≤ Wq_max
# Forma cuadrática: μ² - λμ - λ/Wq_max ≥ 0

a = 1
b = -lambda_rate
c = -lambda_rate / Wq_max

discriminant = b**2 - 4*a*c

if discriminant > 0:
    mu_min = (-b + math.sqrt(discriminant)) / (2*a)
    mu_practico = math.ceil(mu_min)

    # Métricas con μ práctico
    rho = lambda_rate / mu_practico
    Lq = (lambda_rate**2) / (mu_practico * (mu_practico - lambda_rate))
    L = lambda_rate / (mu_practico - lambda_rate)
    Wq = Lq / lambda_rate
    W = L / lambda_rate

    # Mostrar resultados
    st.subheader("📌 Resultados")

    st.write(f"**μ mínimo teórico:** {mu_min:.2f} clientes/hora")
    st.write(f"**μ recomendado (práctico):** {mu_practico} clientes/hora")

    st.subheader("📊 Indicadores del sistema")

    st.write(f"**Utilización (ρ):** {rho:.4f}")
    st.write(f"**Clientes en cola (Lq):** {Lq:.4f}")
    st.write(f"**Clientes en sistema (L):** {L:.4f}")
    st.write(f"**Tiempo en cola (Wq):** {Wq*60:.2f} minutos")
    st.write(f"**Tiempo total (W):** {W*60:.2f} minutos")

    # Validación
    st.subheader("✅ Validación del nivel de servicio")

    if Wq <= Wq_max:
        st.success("El sistema cumple el tiempo máximo de espera.")
    else:
        st.error("El sistema NO cumple el nivel de servicio.")

    # Interpretación
    st.subheader("🧠 Interpretación")

    st.markdown(f"""
    - El sistema necesita una capacidad de al menos **{mu_practico} clientes/hora**.
    - La utilización es del **{rho*100:.2f}%**, lo cual indica un sistema saludable.
    - El tiempo de espera es **{Wq*60:.2f} minutos**, cumpliendo la restricción.
    
    📌 **Conclusión gerencial:**
    
    Para garantizar un servicio de alta calidad, la empresa debe operar con 
    suficiente margen entre λ y μ. Diseñar con poca holgura generaría 
    congestión y mala experiencia del cliente.
    """)

else:
    st.error("No se pudo calcular la solución. Verifique los datos.")