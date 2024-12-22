import streamlit as st

# Ana ekran
def ana_ekran():
    st.title("Hoşgeldiniz")
    st.write("Lütfen bir seçenek seçin:")
    secim = st.radio("Seçenekler", ["Yorum Kategorilendirme", "Boy ve Kilo Endeksi"])

    if secim == "Yorum Kategorilendirme":
        yorum_kategorilendirme()
    elif secim == "Boy ve Kilo Endeksi":
        boy_ve_kilo_endeksi()

# Yorum kategorilendirme fonksiyonu
def yorum_kategorilendirme():
    st.header("Yorum Kategorilendirme")
    st.write("Burada yorumları kategorilendiriyoruz...")  # Burada yorum.py kodları olacak

# Boy ve Kilo Endeksi fonksiyonu
def boy_ve_kilo_endeksi():
    st.header("Boy ve Kilo Endeksi")
    
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
