import streamlit as st

# Yorumları işleyen fonksiyon
def yorum_islemleri(yorum):
    # Burada yorumla ilgili işlemleri yapabilirsin
    # Örneğin, yorumun pozitif mi negatif mi olduğunu anlamak
    if "iyi" in yorum.lower():
        return "Olumlu"
    elif "kötü" in yorum.lower():
        return "Olumsuz"
    else:
        return "Nötr"

# Ana sayfa için başlık
st.title("Hoşgeldiniz")

# Sağda gösterilecek olan kısmı
st.subheader("Yorumlarınızı Yazın:")

# Kullanıcıdan yorum alma
yorum = st.text_area("Yorumunuzu yazın:")
btn = st.button("Yorum Gönder")

# Yorum gönderildiğinde işlemi başlat
if btn:
    # Yorumunuzu yorum_islemleri fonksiyonu ile işleme
    sonuc = yorum_islemleri(yorum)
    st.write(f"Yorum Sonucu: {sonuc}")

# Ekranı iki sütun şeklinde bölelim
col1, col2 = st.columns(2)

# Sol kısımda yorum.py'deki kodları göstermek için
with col1:
    st.subheader("Yorum Kodu:")
    code = '''
# yorum.py

def yorum_islemleri(yorum):
    # Burada yorumla ilgili işlemleri yapabilirsin
    # Örneğin, yorumun pozitif mi negatif mi olduğunu anlamak
    if "iyi" in yorum.lower():
        return "Olumlu"
    elif "kötü" in yorum.lower():
        return "Olumsuz"
    else:
        return "Nötr"
    '''
    st.code(code, language='python')
