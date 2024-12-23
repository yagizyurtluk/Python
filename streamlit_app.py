import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime
import string
import pygame
import random

# Başlık
st.title("Metin Analizi ve Kategorilendirme")

# Sol menü
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
    # Yılan oyunu - Game slotu
    st.subheader("Yılan Oyunu")
    st.write("Yılan oyununu oynamaya başlayın! PC için ok tuşları, mobil için dokunma ile oynayın.")
    
    # Pygame setup
    pygame.init()

    # Oyun ekranı boyutları
    ekran_genislik = 600
    ekran_yukseklik = 400
    ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
    pygame.display.set_caption('Yılan Oyunu')

    # Yılanın başlangıç parametreleri
    yilan_boyu = 10
    yilan_hizi = 15

    # Oyun döngüsü
    oyun_bitti = False
    yilan_koordinatlari = [[100, 50], [90, 50], [80, 50]]
    yilan_yonu = "SAĞ"
    yem_koordinatlari = [random.randrange(1, (ekran_genislik//yilan_boyu)) * yilan_boyu,
                         random.randrange(1, (ekran_yukseklik//yilan_boyu)) * yilan_boyu]
    yem_yenildi = False

    clock = pygame.time.Clock()

    while not oyun_bitti:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and yilan_yonu != "SAĞ":
                    yilan_yonu = "SOL"
                elif event.key == pygame.K_RIGHT and yilan_yonu != "SOL":
                    yilan_yonu = "SAĞ"
                elif event.key == pygame.K_UP and yilan_yonu != "AŞAĞI":
                    yilan_yonu = "YUKARI"
                elif event.key == pygame.K_DOWN and yilan_yonu != "YUKARI":
                    yilan_yonu = "AŞAĞI"

        if yilan_yonu == "SOL":
            yilan_koordinatlari[0][0] -= yilan_boyu
        if yilan_yonu == "SAĞ":
            yilan_koordinatlari[0][0] += yilan_boyu
        if yilan_yonu == "YUKARI":
            yilan_koordinatlari[0][1] -= yilan_boyu
        if yilan_yonu == "AŞAĞI":
            yilan_koordinatlari[0][1] += yilan_boyu

        # Yılanın kendisine çarpması
        if yilan_koordinatlari[0] in yilan_koordinatlari[1:]:
            oyun_bitti = True

        # Yılanın ekran dışına çıkması
        if yilan_koordinatlari[0][0] >= ekran_genislik or yilan_koordinatlari[0][0] < 0 or yilan_koordinatlari[0][1] >= ekran_yukseklik or yilan_koordinatlari[0][1] < 0:
            oyun_bitti = True

        # Yılanın yem yemesi
        yeni_baslangic = []
        yeni_baslangic.append(yilan_koordinatlari[0])
        yilan_koordinatlari = yeni_baslangic + yilan_koordinatlari[:-1]

        if yilan_koordinatlari[0] == yem_koordinatlari:
            yem_yenildi = True
            yem_koordinatlari = [random.randrange(1, (ekran_genislik//yilan_boyu)) * yilan_boyu,
                                 random.randrange(1, (ekran_yukseklik//yilan_boyu)) * yilan_boyu]
            yilan_koordinatlari.append([0, 0])

        ekran.fill((0, 0, 0))  # Ekranı temizle

        # Yılanı çiz
        for blok in yilan_koordinatlari:
            pygame.draw.rect(ekran, (0, 255, 0), (blok[0], blok[1], yilan_boyu, yilan_boyu))

        # Yemi çiz
        pygame.draw.rect(ekran, (255, 0, 0), (yem_koordinatlari[0], yem_koordinatlari[1], yilan_boyu, yilan_boyu))

        pygame.display.update()

        clock.tick(yilan_hizi)

    pygame.quit()
