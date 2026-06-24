import streamlit as st
import pandas as pd
import joblib

model = joblib.load('rent_model.pkl')
columns = joblib.load('rent_columns.pkl')
encoders = joblib.load('rent_encoders.pkl')

st.set_page_config(page_title="German Rent Estimator", page_icon="🏠", layout="centered")

# --- styling ---
st.markdown("""
<style>
.stApp { background-color: #F2F0E9; }
h1 { font-family: Georgia, serif; color: #2E3D33; }
.price-card {
    background: #2E3D33; color: #F2F0E9; border-radius: 14px;
    padding: 28px; text-align: center; margin-top: 18px;
}
.price-card .amount { font-family: Georgia, serif; font-size: 46px; font-weight: 700; }
.price-card .label { font-size: 14px; letter-spacing: 1px; text-transform: uppercase; opacity: .8; }
</style>
""", unsafe_allow_html=True)

st.title("German Rent Estimator")
st.write("Estimate the monthly base rent (Kaltmiete) for an apartment in Germany.")

# helper: encode a text choice to the number the model expects
def enc(col, value):
    classes = encoders[col]
    return classes.index(value) if value in classes else 0

col1, col2 = st.columns(2)

with col1:
    regio1 = st.selectbox("State (Bundesland)", sorted(encoders['regio1']))
    living = st.number_input("Living space (m²)", min_value=10, max_value=400, value=70)
    rooms = st.number_input("Number of rooms", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    year = st.number_input("Year built", min_value=1850, max_value=2025, value=1990)

with col2:
    regio2 = st.selectbox("City / District", sorted(encoders['regio2']))
    flat = st.selectbox("Type of flat", sorted(encoders['typeOfFlat']))
    cond = st.selectbox("Condition", sorted(encoders['condition']))
    floor = st.number_input("Floor", min_value=0, max_value=30, value=2)

st.write("Features:")
c1, c2, c3 = st.columns(3)
kitchen = c1.checkbox("Fitted kitchen")
balcony = c1.checkbox("Balcony")
cellar = c2.checkbox("Cellar")
lift = c2.checkbox("Lift")
garden = c3.checkbox("Garden")
newly = c3.checkbox("Newly built")

if st.button("Estimate rent", type="primary"):
    row = pd.DataFrame([[0]*len(columns)], columns=columns)
    row['livingSpace'] = living
    row['noRooms'] = rooms
    row['yearConstructed'] = year
    row['floor'] = floor
    row['regio1'] = enc('regio1', regio1)
    row['regio2'] = enc('regio2', regio2)
    row['typeOfFlat'] = enc('typeOfFlat', flat)
    row['condition'] = enc('condition', cond)
    row['hasKitchen'] = int(kitchen)
    row['balcony'] = int(balcony)
    row['cellar'] = int(cellar)
    row['lift'] = int(lift)
    row['garden'] = int(garden)
    row['newlyConst'] = int(newly)

    price = model.predict(row)[0]
    st.markdown(f"""
    <div class="price-card">
        <div class="label">Estimated base rent</div>
        <div class="amount">€{price:,.0f}<span style="font-size:20px;"> / month</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Base rent (Kaltmiete) excludes utilities and heating.")
