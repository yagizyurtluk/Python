import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime
import string

# Başlık
st.title("Hoşgeldiniz")

# Sol panelden hangi sayfa seçileceğini belirlemek
page = st.sidebar.selectbox("Sayfa Seçin", ["Ana Sayfa", "Yorum Kategorilendirme"])

# Veritabanı bağlantısı
conn = sqlite3.connect('trendyorum.sqlite3')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS testler(yorum TEXT, sonuc TEXT, zaman TEXT)")
conn.commit()

# Yorum temizleme fonksiyonu
def temizle(sutun):
    stopwords = ['fakat', 'lakin', 'ancak', 'acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey']
    sutun = sutun.lower()
    for sembol in string.punctuation:
        sutun = sutun.replace(sembol, " ")
    for stopword in stopwords:
        sutun = sutun.replace(f" {stopword} ", " ")
    return sutun

# Yorum Kategorilendirme Sayfası
if page == "Yorum Kategorilendirme":
    st.subheader("Yorum Kategorilendirme")

    # Veri yükleme
    df = pd.read_csv('yorum.csv.zip', on_bad_lines='skip', delimiter=";")
    df['Metin'] = df['Metin'].apply(temizle)

    # Özellik ve hedef değişken
    cv = CountVectorizer(max_features=300)
    X = cv.fit_transform(df['Metin']).toarray()
    y = df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

    # Kullanıcı girişi
    yorum = st.text_area('Yorumunuzu yazın:')
    btn = st.button('Kategorilendir')

    if btn:
        # Model eğitimi
        rf = RandomForestClassifier()
        model = rf.fit(X_train, y_train)
        skor = model.score(X_test, y_test)

        # Yorum tahmini
        tahmin = cv.transform([yorum]).toarray()
        kat = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}
        sonuc = model.predict(tahmin)
        s = kat.get(sonuc[0])

        # Sonuçları gösterme
        st.subheader(f"Tahmin Edilen Kategori: {s}")
        st.write(f"Model Skoru: {skor:.2f}")

        # Sonuçları veritabanına kaydetme
        zaman = str(datetime.datetime.now())
        c.execute("INSERT INTO testler VALUES(?,?,?)", (yorum, s, zaman))
        conn.commit()

    # Geçmiş test sonuçları
    c.execute('SELECT * FROM testler')
    testler = c.fetchall()
    st.write("Geçmiş Testler:")
    st.table(testler)

    # Önbellek temizleme
    if st.button("Önbelleği Temizle"):
        c.execute("DELETE FROM testler")
        conn.commit()
        st.success("Önbellek temizlendi.")

# Ana Sayfa
elif page == "Ana Sayfa":
    st.subheader("Ana Sayfaya Hoşgeldiniz!")
    st.write("Buradan istediğiniz sayfayı seçebilirsiniz.")
