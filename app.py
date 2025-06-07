import streamlit as st
import requests
import datetime
import bcrypt

# Sayfa başlığı ve görünüm ayarı
st.set_page_config(
    page_title="GPT Erişim Paneli",
    page_icon="🤖",
    layout="centered"
)

# 🔐 Kullanıcı listesi (şifre hash'li)
USERS = {
    "isikadem@turkcell.com.tr": "$2b$12$6TGhdU0C/Otxg1Efu23QCOHt0Ue5Wp4sCN12rV0u0kC5HQZ.y6Kj2",       # sifre123
    "ahmeteren2@turkcell.com.tr": "$2b$12$BNmLdz3ih1o9gfJP0UBkL.yFDcT0ccdcPVg2BTlrz6u08Y7HpX3Pe"      # Erenlerden2.ci
}

# Giriş oturumu kontrolü
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Giriş ekranı
if not st.session_state.authenticated:
    st.title("🔐 Giriş Yap")
    st.markdown("Lütfen e-posta ve şifrenizi girin:")
    email = st.text_input("📧 E-posta")
    password = st.text_input("🔑 Şifre", type="password")

    if st.button("Giriş"):
        hashed = USERS.get(email)
        if hashed and bcrypt.checkpw(password.encode(), hashed.encode()):
            st.session_state.authenticated = True
            st.session_state.user = email
            st.success("Giriş başarılı!")
            st.rerun()
        else:
            st.error("Erişim reddedildi.")
    st.stop()

# Giriş başarılıysa chat arayüzü
st.title("🤖 GPT-4o Sohbet Asistanı")
st.markdown(f"👋 Hoş geldin, **{st.session_state.user}**!")
st.markdown("Aşağıya bir soru yaz ve Enter'a bas:")

user_input = st.text_input("💬 Soru", placeholder="Örnek: Yapay zeka nedir?")

if st.button("🚀 Gönder") and user_input:
    with st.spinner("GPT yanıtlıyor..."):
        try:
            response = requests.post(
                "https://api.puter.com/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": user_input}]
                }
            )
            reply = response.json()["choices"][0]["message"]["content"]
            st.markdown(f"**🧠 GPT:** {reply}")

            # Log kaydı
            log_entry = f"[{datetime.datetime.now()}] {st.session_state.user}\nSoru: {user_input}\nYanıt: {reply}\n\n"
            with open("chat_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
