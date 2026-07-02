import streamlit as st
from collections import Counter
import pandas as pd

from db import add_entry, get_entries, delete_entry, update_entry
from auth import show_register, show_login

st.set_page_config(page_title="Kişisel Günlük Uygulaması", page_icon="📘")
st.title("Kişisel Günlük Uygulaması")

if "user" not in st.session_state:
    st.session_state["user"] = None

menu = ["Giriş Yap", "Kayıt Ol"]
choice = st.sidebar.selectbox("Menü", menu)

# Üst menü
if choice == "Kayıt Ol":
    show_register()
elif choice == "Giriş Yap":
    show_login()

user = st.session_state["user"]

if user:
    st.markdown("---")
    st.subheader(f"📘 Günlük Yönetimi - {user['username']}")

    alt_menu = ["Yeni Günlük Ekle", "Günlüklerim"]
    alt_choice = st.radio("Ne yapmak istiyorsun?", alt_menu, horizontal=True)

    # Günlük ekleme
    if alt_choice == "Yeni Günlük Ekle":
        title = st.text_input("Başlık")
        content = st.text_area("Günlük Metni")
        mood = st.selectbox("Ruh Halin", ["Mutlu 😊", "Üzgün 😢", "Yorgun 😪", "Heyecanlı 🤩", "Normal 🙂"])

        if st.button("Günlüğü Kaydet"):
            if not title or not content:
                st.error("Alanlar boş bırakılamaz.")
            else:
                add_entry(user["id"], title, content, mood)
                st.success("Günlük kaydedildi!")

    # Günlük listesi
    elif alt_choice == "Günlüklerim":
        entries = get_entries(user["id"])

        if not entries:
            st.info("Henüz günlük eklemedin.")
        else:
            df = pd.DataFrame(entries, columns=["id", "user_id", "title", "content", "mood", "created_at"])
            df["date"] = pd.to_datetime(df["created_at"]).dt.date

            moods = df["mood"].tolist()
            counts = Counter(moods)

            col1, col2, col3 = st.columns(3)
            col1.metric("Mutlu 😊", counts.get("Mutlu 😊", 0))
            col2.metric("Üzgün 😢", counts.get("Üzgün 😢", 0))
            col3.metric("Yorgun 😪", counts.get("Yorgun 😪", 0))

            st.bar_chart(df["mood"].value_counts())
            st.line_chart(df.groupby("date").size())

            st.markdown("---")

            filtered_entries = entries

            if st.checkbox("Belirli tarihteki günlükleri göster"):
                selected_date = st.date_input("Tarih:")
                date_str = selected_date.strftime("%Y-%m-%d")
                filtered_entries = [e for e in filtered_entries if e[5].startswith(date_str)]

            mood_filter = st.selectbox(
                "Ruh hali filtrele:",
                ["Tümü", "Mutlu 😊", "Üzgün 😢", "Yorgun 😪", "Heyecanlı 🤩", "Normal 🙂"]
            )
            if mood_filter != "Tümü":
                filtered_entries = [e for e in filtered_entries if e[4] == mood_filter]

            search_text = st.text_input("Başlık/metin içinde ara:")
            if search_text:
                s = search_text.lower()
                filtered_entries = [e for e in filtered_entries if s in e[2].lower() or s in e[3].lower()]

            if filtered_entries:
                df_filtered = pd.DataFrame(filtered_entries, columns=["id", "user_id", "title", "content", "mood", "created_at"])
                st.download_button(
                    "📥 Filtrelenen CSV indir",
                    df_filtered.to_csv(index=False).encode("utf-8"),
                    "gunlukler.csv",
                    "text/csv"
                )

            for entry in filtered_entries:
                entry_id, _, title, content, mood, date = entry

                with st.expander(f"{title} - {date}"):
                    st.write(f"**Tarih:** {date}")
                    st.write(f"**Ruh Hali:** {mood}")
                    st.write(content)

                    txt_content = f"Başlık: {title}\nTarih: {date}\nRuh Hali: {mood}\n\n{content}"
                    st.download_button(
                        "📄 TXT olarak indir",
                        txt_content.encode("utf-8"),
                        f"gunluk_{entry_id}.txt",
                        "text/plain"
                    )

                    new_title = st.text_input("Yeni Başlık", value=title, key=f"title{entry_id}")
                    new_content = st.text_area("Yeni Metin", value=content, key=f"content{entry_id}")
                    new_mood = st.selectbox(
                        "Yeni Ruh Hali",
                        ["Mutlu 😊", "Üzgün 😢", "Yorgun 😪", "Heyecanlı 🤩", "Normal 🙂"],
                        index=["Mutlu 😊", "Üzgün 😢", "Yorgun 😪", "Heyecanlı 🤩", "Normal 🙂"].index(mood),
                        key=f"mood{entry_id}"
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("Kaydet", key=f"save{entry_id}"):
                            update_entry(entry_id, new_title, new_content, new_mood)
                            st.success("Güncellendi!")
                            st.rerun()

                    with c2:
                        if st.button("Sil", key=f"delete{entry_id}"):
                            delete_entry(entry_id)
                            st.warning("Silindi!")
                            st.rerun()

    if st.button("Çıkış Yap"):
        st.session_state["user"] = None
        st.success("Çıkış yapıldı.")

else:
    st.info("Giriş yap veya kayıt ol.")
