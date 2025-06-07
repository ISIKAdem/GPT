import streamlit as st
import requests

# Yetkili kullanıcılar
USERS = {
    "isikadem@turkcell.com.tr": "sifre123"
}

# Oturum kontrolü
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Giriş ekranı
if not st.session_state.authenticated:
    st.title("Giriş Yap")
    email = st.text_input("E-posta")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if email in USERS and USERS[email] == password:
            st.session_state.authenticated = True
            st.session_state.user = email
            st.success("Giriş başarılı!")
            st.experimental_rerun()  # Girişten sonra sayfayı yenile
        else:
            st.error("Erişim reddedildi.")
    st.stop()

# Chat ekranı
st.title("GPT-4o Chat Arayüzü (Ücretsiz)")

user_input = st.text_input("Bir soru yazın:")

if st.button("Gönder") and user_input:
    with st.spinner("GPT düşünüyor..."):
        try:
            response = requests.post(
                "https://api.puter.com/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                }
            )
            reply = response.json()["choices"][0]["message"]["content"]
            st.markdown(f"**GPT:** {reply}")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
