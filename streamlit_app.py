import streamlit as st
image_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wallpaperflare.com%2Fsearch%3Fwallpaper%3Dplanet%2Bjupiter&psig=AOvVaw1XhuoyXdxBqLGEv7ZN6SYp&ust=1734987070774000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPCRk9SgvIoDFQAAAAAdAAAAABAE"
# CSS ile arkaplan resmi ekleme
def add_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
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

# Ana uygulama
def main():
    st.sidebar.title("Sayfa Seçimi")
    page = st.sidebar.radio("Sayfalar", ("Ana Sayfa", "Yorum Bölümü"))

    if page == "Ana Sayfa":
        main_page()
    elif page == "Yorum Bölümü":
        yorum_page()

# Arkaplan görsel URL'si
background_url = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Jupiter_%28transparent%29.png"

if __name__ == "__main__":
    add_background(background_url)
    main()
