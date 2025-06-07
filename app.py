import streamlit as st
import requests
import datetime


# Sayfa başlığı ve görünüm ayarı
st.set_page_config(
    page_title="GPT Erişim Paneli",
    page_icon="🤖",
    layout="centered"
)

# 🔐 Kullanıcı listesi (şifre hash'li)
USERS = {
    "isikadem@turkcell.com.tr": "sifre123",
    "ahmeteren2@turkcell.com.tr": "Erenlerden2.ci"
}


# Giriş oturumu kontrolü
if USERS.get(email) == password:
    st.session_state.authenticated = True
    st.session_state.user = email
    st.success("Giriş başarılı!")
    st.rerun()
else:
    st.error("Erişim reddedildi.")

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
