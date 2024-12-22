import streamlit as st

# CSS için stil ekleme
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;  # Genel arka plan rengi
            color: #333333;  # Yazı rengi
            font-family: Arial, sans-serif;  # Yazı tipi
        }
        .sidebar .sidebar-content {
            background-color: #f7f7f7;  # Sol panelin arka plan rengi
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

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

# Streamlit için sayfa seçim
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

if __name__ == "__main__":
    main()
