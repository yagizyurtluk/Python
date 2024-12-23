import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import datetime

# Menü Sayfası
def menu_page():
    st.title("Uygulama Menüsü")
    st.write("Bu uygulama 3 ana bölüme sahiptir:")
    st.write("- **Yorum Kontrol (Bu Proje)**: Yorumları analiz et")
    st.write("- **Boy-Kilo Endeksi**: Boy ve kilo bilgisi ile sağlık durumu analizi yap")
    st.write("- **İletişim**: Proje hakkında geri bildirimde bulun")

# Yorum Kontrol Sayfası
def yorum_kontrol_page():
    st.title("Yorum Kontrol")
    st.write("Yorumları buraya yazın ve kategorilerine göre analiz edelim.")
    
    yorum = st.text_area("Yorumunuzu yazın:")
    btn = st.button('Kategorilendir')

    if btn:
        if yorum.strip() == "":
            st.warning("Lütfen yorumunuzu yazın.")
        else:
            model, vectorizer = build_model()

            # Yorumdan tahmin yapma
            tahmin = vectorizer.transform([yorum]).toarray()
            kategoriler = {1: "Olumlu", 0: "Olumsuz", 2: "Nötr"}
            sonuc = model.predict(tahmin)
            kategori = kategoriler.get(sonuc[0])
            st.subheader(f"Tahmin Edilen Kategori: {kategori}")

            # Zaman damgası
            zaman = datetime.datetime.now()
            st.write(f"Analiz Yapılma Zamanı: {zaman.strftime('%Y-%m-%d %H:%M:%S')}")

# Boy-Kilo Endeksi Sayfası
def boy_kilo_endeksi_page():
    st.title("Boy-Kilo Endeksi Hesaplama")
    st.write("Boy ve kilonuzu girin, ardından sağlık durumunuzu görelim.")
    
    boy = st.number_input("Boy (cm):", min_value=50, max_value=250, value=170)
    kilo = st.number_input("Kilo (kg):", min_value=20, max_value=300, value=70)

    if boy > 0 and kilo > 0:
        bmi = kilo / (boy / 100) ** 2
        st.write(f"Vücut Kitle Endeksiniz (BMI): {bmi:.2f}")

        # Kategoriler
        if bmi < 18.5:
            st.write("Durum: Zayıf")
        elif 18.5 <= bmi < 24.9:
            st.write("Durum: Normal Kilolu")
        elif 25 <= bmi < 29.9:
            st.write("Durum: Kilolu")
        else:
            st.write("Durum: Obez")
    else:
        st.warning("Lütfen geçerli boy ve kilo değerleri girin.")

# Model ve Vectorizer Kurulumu
def build_model():
    # Örnek veri, burada gerçek verinizi kullanmalısınız
    data = {'Metin': ['Bu film çok güzel', 'Berbat bir film', 'Oldukça sıkıcı', 'Harika bir deneyim'],
            'Durum': [1, 0, 2, 1]}
    df = pd.DataFrame(data)

    # Veriyi hazırlama
    vectorizer = CountVectorizer(max_features=300)
    X = vectorizer.fit_transform(df['Metin']).toarray()
    y = df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Model oluşturma
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    return model, vectorizer

# Ana Sayfa
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Menü", "Yorum Kontrol (Bu Proje)", "Boy-Kilo Endeksi"))

    if page == "Menü":
        menu_page()
    elif page == "Yorum Kontrol (Bu Proje)":
        yorum_kontrol_page()
    elif page == "Boy-Kilo Endeksi":
        boy_kilo_endeksi_page()

if __name__ == "__main__":
    main()
