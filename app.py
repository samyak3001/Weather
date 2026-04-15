import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Weather App", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stMetric"] {
    background: #1f2937;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOCATION LIST ----------------
locations = """adilabad agar agra ahmadnagar aizawl ajmer akola alappuzha aligarh alirajpur
allahabad almora alwar ambala amethi amravati amreli amritsar anand anantapur
anantnag anugul anuppur araria ariyalur arwal ashoknagar auraiya aurangabad
azamgarh badgam bagalkot bageshwar baghpat bahraich balaghat balangir baleshwar
ballia balod baloda bazar balrampur banda bangalore banka bankura banswara
bara banki baramula baran barddhaman bareilly bargarh barmer barnala barpeta
barwani bastar basti baudh begusarai belgaum bellary betul bhagalpur bhavnagar
bhilwara bhind bhiwani bhopal bidar bijapur bijnor bikaner bilaspur bokaro
bongaigaon budaun bulandshahr bundi burhanpur buxar chamba chamoli chandauli
chandigarh chandrapur chennai chhatarpur chhindwara chikmagalur chitradurga
chittoor churu coimbatore cuddalore cuttack dehradun deoghar deoria dewas
dhanbad dhar dharmapuri dharwad dhule dibrugarh dimapur dindigul dindori diu
doda dumka dungarpur durg east godavari ernakulam erode etah etawah faizabad
faridabad farrukhabad fatehpur firozabad firozpur gadag gandhinagar ganganagar
ganjam gaya ghaziabad ghazipur giridih goa gonda gorakhpur gulbarga guna guntur
gurdaspur gurgaon gwalior hamirpur hanumangarh hardoi haridwar hassan haveri
hazaribagh hisar hoshiarpur hugli idukki imphal indore jabalpur jaipur jaisalmer
jalandhar jalgaon jalna jalor jalpaiguri jammu jamnagar jamui jaunpur jhabua
jhansi jharsuguda jind jodhpur jorhat junagadh kadapa kaithal kancheepuram
kangra kannur kanpur karnal karur kasaragod kathua katihar katni kendrapara
khagaria khammam khandwa khargone kheda khordha kishanganj kolar kolhapur
kolkata kollam koppal koraput korba kota kottayam kozhikode krishna krishnagiri
kurnool lakhimpur latur lucknow ludhiana madurai malappuram mandsaur mathura
meerut mirzapur moga moradabad morena mumbai munger murshidabad muzaffarnagar
muzaffarpur mysore nagapattinam nagaur nagpur nalgonda namakkal nanded
nandurbar navsari nawada nellore new delhi nizamabad osmanabad palakkad pali
palwal panipat panna parbhani patiala patna perambalur pilibhit pithoragarh
puducherry pudukkottai pune puri purnia raichur raigarh raipur rajkot ranchi
ratlam ratnagiri rewa rohtak saharanpur saharsa salem samastipur sambalpur
sangli sangrur satara satna sehore seoni shimla shimoga sikar siwan solan
solapur sonipat srinagar sultanpur surat surendranagar thanjavur
thiruvananthapuram thrissur tiruchirappalli tirunelveli tiruppur
tiruvannamalai tonk tumkur udaipur udupi ujjain unnao vadodara varanasi
vellore visakhapatnam warangal yamunanagar yavatmal zunheboto kanyakumari""".split()

# ---------------- UI ----------------
st.title("🌆 Smart Weather Prediction")

col1, col2 = st.columns(2)

location = col1.selectbox("📍 Select Location", sorted(locations))

time_options = [f"{i:02d}:00" for i in range(24)]
selected_time = col2.selectbox("⏰ Select Time (24-hour)", time_options)

hour = int(selected_time.split(":")[0])

# ---------------- BUTTON ----------------
if st.button("🔮 Predict Weather"):

    # -------- DAY / NIGHT LOGIC --------
    if 6 <= hour <= 17:
        phase = "Day 🌞"
        base_temp = np.random.uniform(28, 35)

        if base_temp > 33:
            weather = np.random.choice(["Sunny ☀️", "Sunny ☀️", "Cloudy ☁️"])
        elif base_temp > 27:
            weather = np.random.choice(["Cloudy ☁️", "Sunny ☀️"])
        else:
            weather = "Rainy 🌧️"

    else:
        phase = "Night 🌙"
        base_temp = np.random.uniform(22, 28)

        if base_temp > 26:
            weather = np.random.choice(["Clear 🌙", "Cloudy ☁️"])
        elif base_temp > 24:
            weather = np.random.choice(["Cloudy ☁️", "Clear 🌙"])
        else:
            weather = np.random.choice(["Rainy 🌧️", "Cloudy ☁️"])

    # -------- VALUES --------
    temp = round(base_temp, 2)
    feels_like = round(temp + np.random.uniform(1, 3), 2)
    wind = round(np.random.uniform(2, 8), 1)

    # ---------------- OUTPUT ----------------
    st.success(f"Prediction for {location} at {selected_time}")

    col3, col4, col5 = st.columns(3)
    col3.metric("🌤 Weather", weather)
    col4.metric("🌡 Temperature", f"{temp} °C")
    col5.metric("🔥 Feels Like", f"{feels_like} °C")

    st.metric("🌬 Wind Speed", f"{wind} km/h")
    st.markdown(f"### 🕓 Mode: {phase}")

    # ---------------- GRAPH ----------------
    st.markdown("## 📊 Hourly Weather")

    hours = list(range(24))
    temp_data = np.random.uniform(22, 35, 24)
    humidity_data = np.random.uniform(60, 90, 24)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hours,
        y=temp_data,
        mode='lines+markers',
        name='Temperature',
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=hours,
        y=humidity_data,
        mode='lines+markers',
        name='Humidity',
        line=dict(width=3)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Hour (24H)",
        yaxis_title="Value"
    )

    st.plotly_chart(fig, use_container_width=True)
