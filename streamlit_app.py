import streamlit as st
import pandas as pd
import string
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime

# Ana sayfa için ekran
def main_page():
    st.title("Hoşgeldiniz!")
    st.write("Burada projeyi yönetebilirsiniz. Lütfen sol taraftan seçenekleri kullanarak devam edin.")

# Yorum kısmı
def yorum_page():
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
    try:
        df = pd.read_csv('yorum.csv.zip', on_bad_lines='skip', delimiter=";")
        df['Metin'] = df['Metin'].apply(temizle)
    except Exception as e:
        st.error(f"Veri yükleme hatası: {e}")
        return

    # Özellik ve hedef değişken hazırlama
    cv = CountVectorizer(max_features=300)
    X = cv.fit_transform(df['Metin']).toarray()
    y = df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

    # Kullanıcı girdisi
    yorum = st.text_area('Yorum metnini giriniz:')
    btn = st.button('Yorumu Kategorilendir')

    if btn:
        try:
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
            conn.commit()
        except Exception as e:
            st.error(f"Tahmin işlemi sırasında hata oluştu: {e}")

    # Geçmiş test sonuçlarını gösterme
    c.execute('SELECT * FROM testler')
    testler = c.fetchall()
    if testler:
        st.write("Geçmiş Testler:")
        st.table(testler)
    else:
        st.write("Henüz geçmiş test bulunmamaktadır.")

    # Önceki testleri temizleme seçeneği
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
