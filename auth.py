import streamlit as st
from db import register_user, login_user


def show_register():
    st.subheader("Yeni Hesap Oluştur")

    new_user = st.text_input("Kullanıcı Adı", key="reg_user")
    new_pass = st.text_input("Şifre", type="password", key="reg_pass")
    new_pass2 = st.text_input("Şifre (Tekrar)", type="password", key="reg_pass2")

    if st.button("Kayıt Ol", key="reg_btn"):
        if not new_user or not new_pass:
            st.error("Kullanıcı adı ve şifre boş olamaz.")
        elif new_pass != new_pass2:
            st.error("Şifreler aynı değil.")
        else:
            if register_user(new_user, new_pass):
                st.success("Hesap oluşturuldu.")
            else:
                st.error("Bu kullanıcı adı zaten kullanılıyor.")


def show_login():
    st.subheader("Günlük Uygulamasına Giriş Yapın")

    username = st.text_input("Kullanıcı Adı", key="login_user")
    password = st.text_input("Şifre", type="password", key="login_pass")

    if st.button("Giriş", key="login_btn"):
        user = login_user(username, password)
        if user:
            st.session_state["user"] = {"id": user[0], "username": user[1]}
            st.success(f"Hoş geldin, {user[1]}!")
        else:
            st.error("Kullanıcı adı veya şifre hatalı.")
