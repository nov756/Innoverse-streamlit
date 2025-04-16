import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from devices import SmartHome

# Konfigurasi
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Inisialisasi Smart Home
if 'home' not in st.session_state:
    st.session_state.home = SmartHome()

# Fungsi AI Parser
def parse_command(command):
    prompt = f"""
    Anda adalah sistem kontrol smart home. Konversi perintah berikut ke format JSON:
    Perintah: "{command}"
    
    Contoh output:
    {{
        "device": "lampu/ac/pintu",
        "action": "nyala/mati/atur/buka",
        "room": "living_room/bedroom (opsional)",
        "value": "nilai (opsional)"
    }}
    """
    try:
        response = model.generate_content(prompt)
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        return eval(cleaned)
    except Exception as e:
        st.error(f"Error parsing: {str(e)}")
        return None

# UI Streamlit
st.title("🏠 Smart Home AI Controller")
command = st.text_input("🎤 Masukkan perintah suara/text:")

if st.button("Eksekusi Perintah") and command:
    with st.spinner("Memproses..."):
        parsed = parse_command(command)
        if parsed:
            result = st.session_state.home.update_device(
                device=parsed.get("device"),
                action=parsed.get("action"),
                room=parsed.get("room"),
                value=parsed.get("value")
            )
            st.success(f"✅ {result}")

# Tampilan Status
st.subheader("📊 Status Perangkat")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💡 Lampu")
    for room, status in st.session_state.home.devices["lampu"].items():
        st.write(f"{room.replace('_', ' ').title()}: {'🟢 ON' if status else '🔴 OFF'}")

with col2:
    st.markdown("### ❄️ AC")
    ac = st.session_state.home.devices["ac"]
    st.write(f"Status: {'🟢 ON' if ac['on'] else '🔴 OFF'}")
    st.write(f"Suhu: {ac['temperature']}°C")

st.markdown("### 🚪 Pintu Utama")
st.write(f"Status: {'🔓 TERBUKA' if st.session_state.home.devices['pintu'] else '🔒 TERKUNCI'}")

st.caption("Contoh perintah: 'Nyalakan lampu living room', 'Atur AC ke 22 derajat', 'Buka pintu'")