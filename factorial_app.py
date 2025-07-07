import streamlit as st
from factorial import fact
import os

if "start" not in st.session_state:
    st.session_state.start = False

def load_users():
    """Đọc danh sách user từ file user.txt"""
    try:
        if os.path.exists("user.txt"):
            with open("user.txt", "r", encoding="utf-8") as f:
                users = [line.strip() for line in f.readlines() if line.strip()]
            return users
        else:
            st.error("File user.txt không tồn tại!")
            return []
    except Exception as e:
        st.error(f"Lỗi khi đọc file user.txt: {e}")
        return []

def login_page():
    """Trang đăng nhập"""
    st.title("Ứng dụng Tính Số Giai Thừa")
    st.markdown(
        """
        <div style='text-align: center; max-width: 800px; margin: auto;'>
            <p style='font-size:18px;'>
                Chào mừng bạn đến với ứng dụng tính số giai thừa!<br>
            </p>
            <p style='font-size: 16px; max-width: 700px; margin: auto;'>
                <b>Ứng dụng giúp bạn có thể hỗ trợ bạn tính giai thừa của một số nhanh chóng và tiện lợi<b><br><br><br>
            </p>
            <p style='font-size: 25px; max-width: 700px; margin: auto;'>
                <b>Vui lòng đăng nhập<b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Input username
    username = st.text_input("Nhập tên người dùng:")

    if st.button("Đăng nhập"):
        if username:
            users = load_users()
            if username in users:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                # Nếu user không hợp lệ, hiển thị trang chào hỏi
                st.session_state.show_greeting = True
                st.session_state.username = username
                st.rerun()
        else:
            st.warning("Vui lòng nhập tên người dùng!")

def factorial_calculator():
    """Trang tính giai thừa"""
    st.title("Ứng dụng Tính Số Giai Thừa")

    # Hiển thị thông tin user đã đăng nhập
    st.write(f"Xin chào, {st.session_state.username}!")

    # Nút đăng xuất
    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.divider()

    # Chức năng tính giai thừa
    number = st.number_input("Nhập vào một số:", min_value=0, max_value=900)

    if st.button("Tính giai thừa"):
        result = fact(number)
        st.write(f"Giai thừa của {number} là {result}")

def greeting_page():
    """Trang chào hỏi cho user không hợp lệ"""
    st.title("Xin chào!")
    st.write(f"Xin chào {st.session_state.username}!")
    st.write("Bạn không có quyền truy cập vào chức năng tính giai thừa.")

    if st.button("Quay lại đăng nhập"):
        st.session_state.show_greeting = False
        st.session_state.username = ""
        st.rerun()

def main():
    # Khởi tạo session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'show_greeting' not in st.session_state:
        st.session_state.show_greeting = False

    # Điều hướng trang dựa trên trạng thái đăng nhập
    if st.session_state.logged_in:
        factorial_calculator()
    elif st.session_state.show_greeting:
        greeting_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
