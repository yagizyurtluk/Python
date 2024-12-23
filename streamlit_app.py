import streamlit as st
import pandas as pd
import string
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime

# Arka plan ekleme fonksiyonu
def add_background(image_url):
    # Görselin boyutunu ayarlayacak CSS kodu
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: contain;  /* Görselin boyutunu ekrana sığacak şekilde ayarlama */
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center center; /* Görselin merkezi ekranda */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Arka plan görsel URL'si (Jüpiter gezegeni görseli)
background_url = "https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg"
add_background(background_url)

# Uygulama başlığı
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

# Sol Menü ve Sayfa Seçimi
def main_page():
    st.write("Hoşgeldiniz! Burada projeyi yönetebilirsiniz. Sol menüden seçenekleri kullanarak devam edin.")

def yorum_page():
    st.title("Yorum Analizi")
    st.write("Yorumları buraya girip, kategoriye göre analiz edebilirsiniz.")
    yorum = st.text_area("Yorumunuzu yazın:")
    btn = st.button('Kategorilendir')

    if btn:
        if yorum.strip() == "":  # Yorum boş bırakıldığında uyarı
            st.warning("Lütfen yorumunuzu yazın.")
        else:
            rf = RandomForestClassifier()
            model = rf.fit(X_train, y_train)
            skor = model.score(X_test, y_test)

            tahmin = cv.transform(np.array([yorum])).toarray()
            kat = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}

            sonuc = model.predict(tahmin)
            s = kat.get(sonuc[0])
            st.subheader(f"Tahmin Edilen Kategori: {s}")
            st.write(f"Model Skoru: {skor:.2f}")

            # Veritabanına ekleme
            c.execute("INSERT INTO testler VALUES(?,?,?)", (yorum, s, zaman))
            conn.commit()

            # Geçmiş test sonuçlarını gösterme
            c.execute('SELECT * FROM testler')
            testler = c.fetchall()
            st.write("Geçmiş Testler:")
            st.table(testler)

            # Önbelleği Temizleme
            if st.button("Önbelleği Temizle"):
                c.execute("DELETE FROM testler")
                conn.commit()
                st.success("Önbellek temizlendi.")

# Ana uygulama
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

if __name__ == "__main__":
    main()
