import streamlit as st
import sympy as sp
from scipy.integrate import dblquad
import numpy as np
import plotly.graph_objects as go

# Interfaz
def set_background_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .bienvenida-container {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 50px;
            border-radius: 20px;
            text-align: center;
        }}
        .bienvenida-container h1 {{
            color: white;
            font-size: 50px;
        }}
        .borde-letras {{
            color: orange;
            font-size: 30px;
            text-shadow:
                -2px -2px 0 #000,
                 2px -2px 0 #000,
                -2px  2px 0 #000,
                 2px  2px 0 #000,
                -2px  0px 0 #000,
                 2px  0px 0 #000,
                 0px  2px 0 #000,
                 0px -2px 0 #000;
        }}
        .stButton>button {{
            background-color: gray;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 30px;
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Lógica
def parse_function(expr_str):
    x, y = sp.symbols('x y')
    return sp.lambdify((x, y), sp.sympify(expr_str), 'numpy')

def calcular_integral(f, x_bounds, y_bounds):
    resultado, error = dblquad(f, x_bounds[0], x_bounds[1],
                               lambda x: y_bounds[0],
                               lambda x: y_bounds[1])
    return resultado

def plot_surface(f, x_bounds, y_bounds):
    x_vals = np.linspace(x_bounds[0], x_bounds[1], 100)
    y_vals = np.linspace(y_bounds[0], y_bounds[1], 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = f(X, Y)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(
        title='Superficie z = f(x, y)',
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_superficie_cuadrica(nombre):
    x, y = sp.symbols('x y')
    funciones = {
        "Elipsoide": lambda x, y: np.sqrt(1 - (x**2)/4 - (y**2)/9),
        "Hiperboloide de una hoja": lambda x, y: np.sqrt(1 + (x**2)/4 + (y**2)/9),
        "Hiperboloide de dos hojas": lambda x, y: np.sqrt(-1 + (x**2)/4 + (y**2)/9),
        "Paraboloide elíptico": lambda x, y: (x**2)/4 + (y**2)/9,
        "Paraboloide hiperbólico": lambda x, y: (x**2)/4 - (y**2)/9,
        "Cono cuádruple": lambda x, y: np.sqrt((x**2)/4 + (y**2)/9),
        "Cilindro elíptico": lambda x, y: np.sqrt(1 - (x**2)/4)  # z independiente de y
    }
    f = funciones[nombre]
    plot_surface(f, (-5, 5), (-5, 5))

# Pantalla de bienvenida
def pantalla_bienvenida():
    set_background_url("https://sdmntprnorthcentralus.oaiusercontent.com/files/00000000-3e60-622f-9f42-346fb83fd182/raw?se=2025-05-27T07%3A01%3A27Z&sp=r&sv=2024-08-04&sr=b&scid=be85f4af-bbd2-5385-838e-2f58e16a1917&skoid=e9d2f8b1-028a-4cff-8eb1-d0e66fbefcca&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-27T05%3A47%3A12Z&ske=2025-05-28T05%3A47%3A12Z&sks=b&skv=2024-08-04&sig=YWEcLUe2LzMP8o1hU4l9jo7hkAOoXVCGfUukpDBkxuY%3D")
    st.markdown(
        """
        <div class='bienvenida-container'>
            <h1>Calculadora de integrales dobles</h1>
        </div>
        <h3 class='borde-letras'>By Javier Pantoja & Sergio Florez</h3>
        """,
        unsafe_allow_html=True
    )
    if st.button("Ingresar"):
        st.session_state.pantalla = "principal"

# Pantalla principal
def pantalla_calculadora():
    st.sidebar.title("🔧 Opciones")
    mostrar_guia = st.sidebar.button("📘 Guía")

    with st.sidebar.expander("📐 Superficies cuádricas comunes"):
        superficies = [
            "Elipsoide",
            "Hiperboloide de una hoja",
            "Hiperboloide de dos hojas",
            "Paraboloide elíptico",
            "Paraboloide hiperbólico",
            "Cono cuádruple",
            "Cilindro elíptico"
        ]
        for nombre in superficies:
            if st.button(nombre):
                mostrar_superficie_cuadrica(nombre)

    st.title("🧮 Calculadora de Integrales Dobles")

    if mostrar_guia:
        with st.expander("📘 Guía de uso"):
            st.markdown("""
            ### ¿Cómo usar esta herramienta?
            1. **Selecciona una función predeterminada** o escribe la tuya propia usando `x` y `y`.
            2. **Define los límites de integración** para `x` e `y`.
            3. Presiona **"Calcular integral doble"** para obtener el resultado.
            4. Se mostrará una **gráfica 3D** de la función sobre la región definida.

            ### Ejemplos válidos de funciones personalizadas:
            - `x**2 + y**2`
            - `sin(x*y)`
            - `exp(-x**2 - y**2)`
            - `log(x + y + 1)`

            ### Advertencias:
            - Usa `**` para potencias (`x**2`, no `x^2`)
            - No ingreses raíces como `√`, usa `sqrt()`
            - Para valores absolutos, usa `Abs()`
            """)

    funciones_predeterminadas = {
        "x^2 + y^2": "x**2 + y**2",
        "sin(x) * cos(y)": "sin(x) * cos(y)",
        "exp(-x^2 - y^2)": "exp(-x**2 - y**2)",
        "x * y": "x * y",
        "sqrt(x^2 + y^2)": "sqrt(x**2 + y**2)",
        "log(x + y + 1)": "log(x + y + 1)",
        "x^3 - 3xy^2": "x**3 - 3*x*y**2",
        "abs(x - y)": "Abs(x - y)",
        "1 / (1 + x^2 + y^2)": "1 / (1 + x**2 + y**2)",
        "sin(x^2 + y^2)": "sin(x**2 + y**2)"
    }

    opcion = st.selectbox(
        "Selecciona una función predeterminada o 'Personalizada'", 
        options=["Personalizada"] + list(funciones_predeterminadas.keys())
    )

    if opcion == "Personalizada":
        expr = st.text_input("Ingresa la función f(x, y):", "x**2 + y**2")
    else:
        expr = funciones_predeterminadas[opcion]

    a = st.number_input("Límite inferior de x", value=0.0)
    b = st.number_input("Límite superior de x", value=2.0)
    c = st.number_input("Límite inferior de y", value=0.0)
    d = st.number_input("Límite superior de y", value=1.0)

    if st.button("Calcular integral doble"):
        try:
            f = parse_function(expr)
            resultado = calcular_integral(f, (a, b), (c, d))
            st.success(f"Resultado de la integral doble: {resultado:.5f}")
            plot_surface(f, (a, b), (c, d))
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Main
def main():
    if "pantalla" not in st.session_state:
        st.session_state.pantalla = "bienvenida"

    if st.session_state.pantalla == "bienvenida":
        pantalla_bienvenida()
    else:
        pantalla_calculadora()

if __name__ == "__main__":
    main()
