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
st.title("Metin Analizi ve Kategorilendirme")

# Sol menü (Yalnızca bir kez tanımlandı)
menu = ["Menü", "Yorum", "Game"]  # Yeni seçenek ekledik
secim = st.sidebar.radio("Seçim Yapın", menu)

# Veritabanı bağlantısını aç
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
    sutun = sutun.strip()  # Fazla boşlukları temizle
    return sutun

# Veri yükleme ve temizleme
df = pd.read_csv('yorum.csv.zip', on_bad_lines='skip', delimiter=";")
df['Metin'] = df['Metin'].apply(temizle)

# Özellik ve hedef değişken
cv = CountVectorizer(max_features=300)
X = cv.fit_transform(df['Metin']).toarray()
y = df['Durum']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

# Modeli sadece bir kez eğit
rf = RandomForestClassifier()
model = rf.fit(X_train, y_train)

# Menüye göre içerik göster
if secim == "Menü":
    st.subheader("Menü Seçimi")
    st.write("Burada menü ile ilgili seçenekler ve açıklamalar olacak.")
    # Burada istediğiniz menü seçeneklerini ekleyebilirsiniz.

elif secim == "Yorum":
    # Kullanıcı girişi
    yorum = st.text_area('Yorumunuzu yazın:')
    btn = st.button('Kategorilendir')

    if btn:
        # Yorum tahmini
        tahmin = cv.transform([yorum]).toarray()
        kat = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}
        sonuc = model.predict(tahmin)
        s = kat.get(sonuc[0])

        # Sonuçları gösterme
        st.subheader(f"Tahmin Edilen Kategori: {s}")

        # Model skoru
        skor = model.score(X_test, y_test)
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

elif secim == "Game":
    # Yeni Game slotunun içeriği
    st.subheader("Game Slotu")
    st.write("Burada oyun ile ilgili seçenekler olacak.")
    # Buraya oyunla ilgili istediğiniz içerikleri ekleyebilirsiniz.
