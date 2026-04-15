import streamlit as st
import numpy as np
from datetime import datetime
import pytz

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Weather App", layout="wide")

ist = pytz.timezone("Asia/Kolkata")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.title {
    text-align: center;
    font-size: 40px;
    color: white;
}
.datetime {
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
}
div.stButton {
    display: flex;
    justify-content: center;
}
.footer {
    text-align: center;
    color: white;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🌦️ Smart Weather Prediction System</div>', unsafe_allow_html=True)

# ---------------- TIME ----------------
now = datetime.now(ist)
st.markdown(
    f'<div class="datetime">📅 {now.strftime("%d-%m-%Y")} | ⏰ {now.strftime("%H:%M:%S")}</div>',
    unsafe_allow_html=True
)

# ---------------- LOCATIONS ----------------
raw_locations = """
adilabad agar agra ahmadnagar aizawl ajmer akola alappuzha aligarh alirajpur
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
vellore visakhapatnam warangal yamunanagar yavatmal zunheboto kanyakumari
"""

locations = sorted(set(raw_locations.split()))

# ---------------- INPUT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    location = st.selectbox("📍 Location", locations)

with col2:
    time = st.selectbox("⏰ Time (24hr)", [f"{i:02d}:00" for i in range(24)])
    hour = int(time.split(":")[0])

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOCATION OFFSET ----------------
def get_temp_offset(location):
    if location in ["chennai", "madurai", "hyderabad"]:
        return 3
    elif location in ["shimla", "srinagar"]:
        return -5
    elif location in ["mumbai", "goa", "visakhapatnam"]:
        return 2
    else:
        return 0

# ---------------- WEATHER LOGIC ----------------
def predict_weather(location, hour):

    base = 30 + get_temp_offset(location)

    # Temperature logic
    if 12 <= hour <= 16:
        temp = base + 4
    elif 0 <= hour <= 5:
        temp = base - 5
    elif 6 <= hour <= 10:
        temp = base - 2
    else:
        temp = base

    # ✅ FIXED RAIN LOGIC (more balanced)
    if temp > 35:
        rain = np.random.randint(5, 30)
    elif 28 <= temp <= 35:
        rain = np.random.randint(20, 60)
    else:
        rain = np.random.randint(30, 80)

    clear = 100 - rain

    return temp, rain, clear

# ---------------- BUTTON ----------------
if st.button("🔮 Predict Weather"):

    now = datetime.now(ist)

    temp, rain, clear = predict_weather(location, hour)

    st.markdown("## 📊 Prediction Results")
    st.write(f"📅 Date: {now.strftime('%d-%m-%Y')}")
    st.write(f"⏰ Time: {now.strftime('%H:%M:%S')}")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temperature", f"{temp}°C")
    col2.metric("🌧️ Rain", f"{rain}%")
    col3.metric("🌤️ Clear", f"{clear}%")

    # ---------------- FINAL DAY/NIGHT LOGIC ----------------
    if 6 <= hour < 18:
        if rain >= 60:
            st.warning(f"🌧️ Rainy weather in {location}")
        elif rain >= 30:
            st.info(f"🌦️ Cloudy weather in {location}")
        else:
            st.success(f"☀️ Sunny weather in {location}")

    else:
        if rain >= 60:
            st.warning(f"🌧️ Rain expected tonight in {location}")
        elif rain >= 30:
            st.info(f"🌥️ Cloudy night in {location}")
        else:
            st.success(f"🌙 Clear night sky in {location}")

# ---------------- FOOTER ----------------
st.markdown('<div class="footer">BY - SAMYAK PRAVEEN KUMAR</div>', unsafe_allow_html=True)
