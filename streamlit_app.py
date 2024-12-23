import streamlit as st
import pandas as pd
import string
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime

# CSS ile arkaplan resmi ekleme
def add_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Ana sayfa için ekran
def main_page():
    st.title("Hoşgeldiniz!")
    st.write("Burada projeyi yönetebilirsiniz. Lütfen sol taraftan seçenekleri kullanarak devam edin.")

# Yorum kısmı
def yorum_page():
    # Uygulama başlığı ve arkaplan tasarımı
    st.title("Metin Analizi ve Kategorilendirme Uygulaması")
    
    # SQLite veritabanı bağlantısı
    zaman = str(datetime.datetime.now())
    conn = sqlite3.connect('trendyorum.sqlite3')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS testler(yorum TEXT, sonuc TEXT, zaman TEXT)")
    conn.commit()

    # Veriyi yükleme ve temizleme fonksiyonu
    def temizle(sutun):
        stopwords = ['fakat', 'lakin', 'ancak', 'acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç',
                     'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem',
                     'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl',
                     'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm',
                     've', 'veya', 'ya', 'yani']
        semboller = string.punctuation
        sutun = sutun.lower()

        for sembol in semboller:
            sutun = sutun.replace(sembol, " ")
        for stopword in stopwords:
            s = " " + stopword + " "
            sutun = sutun.replace(s, " ")
        sutun = sutun.replace("  ", " ")
        return sutun

    # Veri yükleme
    df = pd.read_csv('yorum.csv.zip', on_bad_lines='skip', delimiter=";")
    df['Metin'] = df['Metin'].apply(temizle)

    # Özellik ve hedef değişken hazırlama
    cv = CountVectorizer(max_features=300)
    X = cv.fit_transform(df['Metin']).toarray()
    y = df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

    # Kullanıcı girdisi
    yorum = st.text_area('Yorum metnini giriniz:')
    btn = st.button('Yorumu Kategorilendir')

    if btn:
        rf = RandomForestClassifier()
        model = rf.fit(X_train, y_train)
        skor = model.score(X_test, y_test)

        tahmin = cv.transform(np.array([yorum])).toarray()
        kat = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}

        sonuc = model.predict(tahmin)
        s = kat.get(sonuc[0])
        st.subheader(f"Tahmin Edilen Kategori: {s}")
        st.write(f"Model Skoru: {skor:.2f}")

        c.execute("INSERT INTO testler VALUES(?,?,?)", (yorum, s, zaman))
       
