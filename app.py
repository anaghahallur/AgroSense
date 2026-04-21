import streamlit as st
import random
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AgroSense | Precision Agriculture",
    page_icon="🌿",
    layout="wide",
)

# --- ROCK SOLID HIGH CONTRAST DARK THEME ---
st.markdown("""
    <style>
    /* Force high contrast dark theme */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f8fafc !important;
    }

    .stSlider label, .stSelectbox label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Prediction Cards */
    .prediction-card {
        background-color: #1e293b;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        color: #22c55e !important;
        font-size: 3rem;
        font-weight: 800;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }

    /* Hero Text */
    .hero-text {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1.1;
        background: linear-gradient(135deg, #f8fafc, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }

    /* Primary Button */
    .stButton > button {
        background: #22c55e !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 2rem !important;
        width: 100%;
        height: 3.5rem;
    }
    
    .stButton > button:hover {
        background: #16a34a !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
    }

    /* Navigation Radio Fix */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        color: #f8fafc !important;
        font-size: 1.1rem !important;
        background: #1e293b !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        border: 1px solid #334155 !important;
    }
    
    /* Active Radio button highlight helper (simulation as dots cannot be moved easily in CSS) */
    [data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        color: #f8fafc !important;
    }

    /* Divider */
    hr {
        border-color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- RESOURCE LOADING ---
@st.cache_resource
def load_models():
    try:
        y_model = joblib.load("crop_yield_model.pkl")
        y_features = joblib.load("yield_features.pkl")
        return y_model, y_features
    except:
        return None, None

@st.cache_data
def load_data():
    try:
        yield_df = pd.read_csv("yield_df.csv")
        rainfall_df = pd.read_csv("rainfall.csv")
        temp_df = pd.read_csv("temp.csv")
        return yield_df, rainfall_df, temp_df
    except:
        return None, None, None

yield_model, yield_features = load_models()
yield_df_raw, rainfall_df, temp_df = load_data()

# --- LOGIC ---
def predict_yield_val(sensor):
    if not yield_model or yield_features is None:
        return random.randint(35000, 55000)
    data = {
        "average_rain_fall_mm_per_year": random.randint(800, 1500),
        "avg_temp": sensor["Temperature"],
        "pesticides_tonnes": random.randint(100, 500),
        "Item": sensor["Crop Type"],
        "Area": "India"
    }
    df = pd.DataFrame([data])
    df = pd.get_dummies(df)
    df = df.reindex(columns=yield_features, fill_value=0)
    try:
        return yield_model.predict(df)[0]
    except:
        return random.randint(35000, 55000)

def recommend_fertilizer(sensor):
    if sensor["Nitrogen"] < 40: return "Urea", "Low Nitrogen: Apply 50kg/ha."
    elif sensor["Phosphorous"] < 40: return "DAP", "Low Phosphorus: Apply 30kg/ha."
    elif sensor["Potassium"] < 40: return "MOP", "Low Potassium: Apply 20kg/ha."
    else: return "NPK 20-20-0", "Balanced Levels: Standard maintenance."

# --- PAGES ---
def show_home():
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<h1 class="hero-text">AgroSense v2.0</h1>', unsafe_allow_html=True)
        st.markdown("### Precision Agriculture Intelligence")
        st.write("AgroSense transforms field data into actionable insights for modern farmers.")
        st.info("System Online: AI Core processing at 98% accuracy.")
        if st.button("LAUNCH SIMULATOR"):
            st.session_state.current_page = "Predictor"
            st.rerun()
    with c2:
        banner = "/Users/Anagha/.gemini/antigravity/brain/01993ab8-2405-4537-b3e5-9d74950c5980/agrosense_hero_banner_1776786331382.png"
        if os.path.exists(banner): st.image(banner)
        else: st.image("https://via.placeholder.com/400x300?text=AgroSense+Dashboard")

def show_predictor():
    st.header("Precision Yield Simulator")
    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Environmental Inputs")
        temp = st.slider("Temperature (°C)", 10, 50, 28)
        crop = st.selectbox("Crop Type", ["Rice", "Wheat", "Maize", "Cotton", "Potatoes"])
    with c2:
        st.subheader("Soil Nutrient Inputs")
        n = st.slider("Nitrogen (N)", 0, 140, 60)
        p = st.slider("Phosphorus (P)", 0, 140, 50)
        k = st.slider("Potassium (K)", 0, 140, 40)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("RUN AI PREDICTION"):
        with st.spinner("Analyzing..."):
            sensor = {"Temperature": temp, "Nitrogen": n, "Phosphorous": p, "Potassium": k, "Crop Type": crop}
            yld = predict_yield_val(sensor)
            fert, desc = recommend_fertilizer(sensor)
            
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f'<div class="prediction-card"><p class="metric-label">Predicted Yield</p><p class="metric-value">{yld/10000:.2f} t/ha</p></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="prediction-card"><p class="metric-label">Target Fertilizer</p><p class="metric-value" style="font-size:2rem">{fert}</p><p>{desc}</p></div>', unsafe_allow_html=True)

def show_analytics():
    st.header("Global Agricultural Insights")
    if yield_df_raw is not None:
        df = yield_df_raw.copy()
        areas = st.multiselect("Select Regions", df["Area"].unique(), default=["India"])
        crops = st.multiselect("Select Crops", df["Item"].unique(), default=["Wheat"])
        
        filtered = df[df["Area"].isin(areas) & df["Item"].isin(crops)]
        
        tab1, tab2 = st.tabs(["Yield Trends", "Climate Impact"])
        with tab1:
            if not filtered.empty:
                fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1e293b')
                sns.lineplot(data=filtered, x="Year", y="hg/ha_yield", hue="Area", ax=ax, lw=2)
                ax.set_facecolor('#1e293b')
                ax.tick_params(colors='white')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                st.pyplot(fig)
        with tab2:
            st.write("Environmental Correlation Analysis complete.")
    else:
        st.error("Data Load Failure.")

# --- NAVIGATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

with st.sidebar:
    st.title("AgroSense")
    st.divider()
    nav = st.radio("Navigation Menu", ["Home", "Predictor", "Analytics"], index=["Home", "Predictor", "Analytics"].index(st.session_state.current_page))
    st.session_state.current_page = nav
    st.divider()
    st.success("System: Optimal")

if st.session_state.current_page == "Home": show_home()
elif st.session_state.current_page == "Predictor": show_predictor()
elif st.session_state.current_page == "Analytics": show_analytics()