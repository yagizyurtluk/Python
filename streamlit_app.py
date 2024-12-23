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

# Başlık
st.title("Metin Analizi ve Kategorilendirme Uygulaması")

# SQLite veritabanı bağlantısı
zaman = str(datetime.datetime.now())
conn = sqlite3.connect('trendyorum.sqlite3')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS testler(yorum TEXT, sonuc TEXT, zaman TEXT)")
conn.commit()

# Yorumları temizleme fonksiyonu
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

    # Veritabanına kaydetme
    c.execute("INSERT INTO testler VALUES(?,?,?)", (yorum, s, zaman))
    conn.commit()

# Geçmiş test sonuçlarını gösterme
c.execute('SELECT * FROM testler')
testler = c.fetchall()
st.write("Geçmiş Testler:")
st.table(testler)

# Önceki testleri temizleme seçeneği
if st.button("Önbelleği Temizle"):
    c.execute("DELETE FROM testler")
    conn.commit()
    st.success("Önbellek temizlendi.")
