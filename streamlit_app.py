import streamlit as st

# Arkaplana Jüpiter resmini ekleme
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
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
    st.title("Yorum Analizi")
    st.write("Yorumları buraya girip, kategoriye göre analiz edebilirsiniz.")
    yorum = st.text_area("Yorumunuzu yazın:")
    btn = st.button('Kategorilendir')

    if btn:
        # Burada yorum analizini yapacak kısmı yazabilirsin
        st.write("Yorum Kategorisi: [Burada Model Sonucu Görünecek]")

# Streamlit için sayfa seçimi
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

if __name__ == "__main__":
    main()
