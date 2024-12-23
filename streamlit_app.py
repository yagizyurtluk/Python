import streamlit as st
import pandas as pd
import string
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime

# Uygulama başlığı ve arkaplan tasarımı
st.markdown(
    """
    <style>
    body {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg');
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sol menü
def sidebar():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))
    return page

# Ana sayfa
def main_page():
    st.title("Hoşgeldiniz!")
    st.write("Projeyi buradan yönetebilirsiniz. Lütfen sol menüden bir sayfa seçin.")

# Yorum analiz sayfası
def yorum_page():
    st.title("Yorum Analizi")
    st.write("Yorumunuzu yazın ve kategorize edilmesini sağlayın.")
    
    # Kullanıcıdan yorum al
    yorum = st.text_area("Yorumunuzu girin:")
    btn = st.button('Yorumu Kategorilendir')

    if btn:
        # Yorum analizi için model
        yorum_temiz = temizle(yorum)  # Yorumun temizlenmesi
        tahmin = cv.transform([yorum_temiz]).toarray()
        sonuc = model.predict(tahmin)
        st.subheader(f"Tahmin Edilen Kategori: {kat[sonuc[0]]}")
        st.write(f"Model Skoru: {model.score(X_test, y_test):.2f}")

        # Yorum veritabanına kaydediliyor
        c.execute("INSERT INTO testler VALUES(?,?,?)", (yorum, kat[sonuc[0]], zaman))
        conn.commit()

# Yorumları temizleme
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
        sutun = sutun.replace(" " + stopword + " ", " ")
    return sutun.strip()

# Modelin ve veritabanının hazırlanması
df = pd.read_csv('yorum.csv.zip', on_bad_lines='skip', delimiter=";")
df['Metin'] = df['Metin'].apply(temizle)

cv = CountVectorizer(max_features=300)
X = cv.fit_transform(df['Metin']).toarray()
y = df['Durum']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

rf = RandomForestClassifier()
model = rf.fit(X_train, y_train)
kat = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}

# SQLite veritabanı bağlantısı
zaman = str(datetime.datetime.now())
conn = sqlite3.connect('trendyorum.sqlite3')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS testler(yorum TEXT, sonuc TEXT, zaman TEXT)")
conn.commit()

# Ana uygulama
def main():
    page = sidebar()

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

if __name__ == "__main__":
    main()
