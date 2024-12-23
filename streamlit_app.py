import streamlit as st

# Ana ekran
def main_page():
    st.title("Hoşgeldiniz!")
    st.subheader("Yorum analizine başlamak için sağdaki menüyü kullanın!")
    st.write("Bu uygulama ile yorumlarınızı analiz edebilir, çeşitli kategorilere ayırabilirsiniz.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg", caption="Jüpiter", use_column_width=True)

# Yorum ekranı
def yorum_page():
    st.title("Yorum Analizi")
    st.write("Yorumunuzu buraya girin ve kategorilendirmesini görmek için butona tıklayın.")
    yorum = st.text_area("Yorumunuzu yazın:")
    btn = st.button('Yorumu Kategorilendir')

    if btn:
        # Burada yorum analizi için bir model çalıştırılacak.
        # Örneğin, basit bir model skoru ve kategorisi ekleyelim
        if yorum.strip() == "":
            st.error("Lütfen bir yorum giriniz.")
        else:
            # Model sonuçları burada olacak
            sonuc = "Olumlu"  # Örnek sonuç
            skor = 85  # Örnek skor
            st.subheader(f"Yorum Kategorisi: {sonuc}")
            st.write(f"Model Skoru: {skor}%")

# Sol paneldeki sayfa seçimi
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))
    
    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

if __name__ == "__main__":
    main()
