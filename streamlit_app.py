import streamlit as st

# Ana ekran başlığı ve düzeni
def ana_ekran():
    st.set_page_config(page_title="Hoşgeldiniz", page_icon=":guardsman:", layout="centered")
    
    # Ana sayfa renk ve tema düzeni
    st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 40px;
            color: #2a9d8f;
            font-weight: bold;
        }
        .subheader {
            font-size: 30px;
            color: #264653;
        }
        .intro {
            font-size: 18px;
            color: #f1faee;
        }
        .box {
            border: 2px solid #2a9d8f;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">Hoşgeldiniz!</p>', unsafe_allow_html=True)
    st.markdown('<p class="intro">Streamlit uygulamanıza hoş geldiniz! Aşağıdaki seçeneklerden birini seçin:</p>', unsafe_allow_html=True)

    # Seçim yapma (sayfa içeriğine göre)
    secim = st.selectbox("Seçim Yapın", ["Yorum Kategorilendirme", "Boy ve Kilo Endeksi"])

    # Seçime göre yönlendirme
    if secim == "Yorum Kategorilendirme":
        yorum_kategorilendirme()
    elif secim == "Boy ve Kilo Endeksi":
        boy_ve_kilo_endeksi()

# Yorum Kategorilendirme sayfası
def yorum_kategorilendirme():
    st.markdown('<p class="subheader">Yorum Kategorilendirme</p>', unsafe_allow_html=True)
    st.write("Burada yorumları kategorilendiriyoruz...")  # Burada yorum.py kodları olacak

# Boy ve Kilo Endeksi sayfası
def boy_ve_kilo_endeksi():
    st.markdown('<p class="subheader">Boy ve Kilo Endeksi</p>', unsafe_allow_html=True)
    
    # Kullanıcıdan boy ve kilo girişi
    boy = st.number_input("Boyunuzu girin (metre cinsinden):", min_value=0.0, format="%.2f")
    kilo = st.number_input("Kilonuzu girin (kg cinsinden):", min_value=0)

    if boy > 0 and kilo > 0:
        # BMI hesaplaması
        bmi = kilo / (boy ** 2)
        
        # BMI değerlendirmesi
        if bmi < 18.5:
            degerlendirme = "Zayıf"
        elif 18.5 <= bmi < 24.9:
            degerlendirme = "Normal"
        elif 25 <= bmi < 29.9:
            degerlendirme = "Fazla Kilolu"
        else:
            degerlendirme = "Obez"
        
        # Sonuçları gösterme
        st.write(f"BMI Değeriniz: {bmi:.2f}")
        st.write(f"Durum: {degerlendirme}")
    else:
        st.write("Lütfen geçerli bir boy ve kilo girin.")

# Ana ekranı başlatma
if __name__ == "__main__":
    ana_ekran()
