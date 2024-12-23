import streamlit as st
import random
import time

# Başlık
st.title("Yılan Oyunu")

# Sol menü
menu = ["Menü", "Yorum", "Game"]
secim = st.sidebar.radio("Seçim Yapın", menu)

# Game Slotu
if secim == "Game":
    st.subheader("Yılan Oyunu")

    # Oyun için gerekli verileri saklamak
    if "yilan" not in st.session_state:
        st.session_state.yilan = [(5, 5)]  # Başlangıçta yılanın koordinatları
        st.session_state.yiyecek = (random.randint(0, 9), random.randint(0, 9))  # Yiyeceğin başlangıç koordinatları
        st.session_state.direction = "RIGHT"  # Başlangıç yönü
        st.session_state.running = False  # Oyun başlatılmamış
        st.session_state.score = 0  # Skor

    # Oyun başlatma
    if not st.session_state.running:
        st.session_state.running = True
        st.session_state.yilan = [(5, 5)]
        st.session_state.score = 0
        st.session_state.yiyecek = (random.randint(0, 9), random.randint(0, 9))
        st.session_state.direction = "RIGHT"
        st.experimental_rerun()

    # PC için kontrol (klavye ok tuşları)
    key = st.text_input("Kontrol (PC): W - Yukarı, A - Sol, S - Aşağı, D - Sağ", "")
    key = key.upper()

    if key == "W" and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
    elif key == "A" and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
    elif key == "S" and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
    elif key == "D" and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

    # Mobil için kontrol (dokunmatik ekran okları)
    if st.button("Yukarı"):
        if st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"
    if st.button("Sol"):
        if st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"
    if st.button("Aşağı"):
        if st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"
    if st.button("Sağ"):
        if st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"

    # Yılanın hareketi
    head = st.session_state.yilan[0]
    if st.session_state.direction == "UP":
        new_head = (head[0] - 1, head[1])
    elif st.session_state.direction == "DOWN":
        new_head = (head[0] + 1, head[1])
    elif st.session_state.direction == "LEFT":
        new_head = (head[0], head[1] - 1)
    elif st.session_state.direction == "RIGHT":
        new_head = (head[0], head[1] + 1)

    # Yılanın çarpma durumu
    if new_head in st.session_state.yilan or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= 10 or new_head[1] >= 10:
        st.session_state.running = False
        st.write(f"Oyun Bitti! Skorunuz: {st.session_state.score}")
        st.button("Yeniden Başlat", on_click=lambda: st.session_state.running = False)
    else:
        st.session_state.yilan = [new_head] + st.session_state.yilan[:-1]

    # Yiyecek yendiyse
    if new_head == st.session_state.yiyecek:
        st.session_state.yilan.append(st.session_state.yilan[-1])  # Yılanı uzat
        st.session_state.score += 1
        st.session_state.yiyecek = (random.randint(0, 9), random.randint(0, 9))  # Yeni yiyecek

    # Oyun tahtasını çizme
    game_board = [[" " for _ in range(10)] for _ in range(10)]
    for (x, y) in st.session_state.yilan:
        game_board[x][y] = "■"
    x, y = st.session_state.yiyecek
    game_board[x][y] = "🍎"

    # Tahtayı göster
    st.write("Oyun Tahtası:")
    for row in game_board:
        st.write(" ".join(row))

    # Skoru gösterme
    st.write(f"Skor: {st.session_state.score}")

    # Yeniden başlatmak için buton
    if not st.session_state.running:
        if st.button("Yeniden Başlat"):
            st.session_state.running = True
            st.session_state.score = 0
            st.session_state.yilan = [(5, 5)]
            st.session_state.direction = "RIGHT"
            st.session_state.yiyecek = (random.randint(0, 9), random.randint(0, 9))
            st.experimental_rerun()

    # Oyun hızını ayarlamak için gecikme ekleyin
    time.sleep(0.2)  # 0.2 saniyede bir adım atacak
