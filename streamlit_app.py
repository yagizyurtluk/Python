import streamlit as st

# Ana sayfa için ekran
def main_page():
    st.title("Hoşgeldiniz!")
    st.write("Burada projeyi yönetebilirsiniz. Lütfen sol taraftan seçenekleri kullanarak devam edin.")

# Yorum kısmı
def yorum_page():
    st.title("Yorum Analizi")
    st.write("Yorumları buraya girip, kategoriye göre analiz edebilirsiniz.")
    yorum = st.text_area("Yorumunuzu yazın:")
    btn = st.button('Kategorilendir')

    if btn:
        # Burada yorum analizini yapacak kısmı yazabilirsin
        st.write("Yorum Kategorisi: [Burada Model Sonucu Görünecek]")

# Boy-Kilo Endeksi Hesaplama
def bki_page():
    st.title("Boy ve Kilo Endeksi Hesaplama")
    st.write("Lütfen boy ve kilo bilgilerinizi girin:")
    boy = st.number_input("Boy (cm):", min_value=1, max_value=300, step=1)
    kilo = st.number_input("Kilo (kg):", min_value=1, max_value=300, step=1)

    if st.button("Hesapla"):
        # BMI hesaplama
        boy_metre = boy / 100
        bki = kilo / (boy_metre ** 2)
        st.write(f"Vücut Kitle Endeksiniz: {bki:.2f}")
        if bki < 18.5:
            st.write("Zayıf")
        elif 18.5 <= bki < 24.9:
            st.write("Normal kilolu")
        elif 25 <= bki < 29.9:
            st.write("Fazla kilolu")
        else:
            st.write("Obez")

# Streamlit için sayfa seçim
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü", "Boy-Kilo Endeksi"))

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()
    elif page == "Boy-Kilo Endeksi":
        bki_page()

if __name__ == "__main__":
    main()
