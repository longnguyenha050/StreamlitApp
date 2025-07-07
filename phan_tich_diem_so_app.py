import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image


if "start" not in st.session_state:
    st.session_state.start = False

# Hàm tính điểm trung bình
def calculate_average(scores):
    return sum(scores) / len(scores)

# Hàm phân loại điểm
def percentage_distribution(scores):
    bins = {'90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, '<60': 0}
    for score in scores:
        if score >= 90:
            bins['90-100'] += 1
        elif score >= 80:
            bins['80-89'] += 1
        elif score >= 70:
            bins['70-79'] += 1
        elif score >= 60:
            bins['60-69'] += 1
        else:
            bins['<60'] += 1
    return bins

# Trang chính phân tích dữ liệu
def show_analysis_page():
    st.title("Phân tích dữ liệu điểm số học sinh")

    # Upload file
    st.markdown("<h3 style='text-align: center;'>Chọn file Excel</h3>", unsafe_allow_html=True)

    with st.expander("📁 Hướng dẫn chọn file Excel"):
        st.markdown("""
        **Lưu ý:** File Excel cần có một cột tên **'Điểm số'**.  
        Ví dụ:
        """)
        huong_dan_img_path = "instruction.png"
        try:
            img_hd = Image.open(huong_dan_img_path)
            st.image(img_hd, caption="Ví dụ định dạng file Excel", width=250)
        except FileNotFoundError:
            st.warning("Không tìm thấy ảnh hướng dẫn.")

    uploaded_file = st.file_uploader("", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        scores = df["Điểm số"].dropna().astype(float).tolist()

        if scores:
            # Tính thống kê cơ bản
            st.write("Tổng số học sinh:", len(scores), "Điểm trung bình:", round(calculate_average(scores), 2))

            # Tìm học sinh điểm cao nhất và thấp nhất
            max_score = df["Điểm số"].max()
            min_score = df["Điểm số"].min()

            top_students = df[df["Điểm số"] == max_score]
            low_students = df[df["Điểm số"] == min_score]

            # Hiển thị học sinh cao điểm nhất
            st.subheader("Học sinh có điểm cao nhất")
            st.dataframe(top_students)

            # Hiển thị học sinh thấp điểm nhất
            st.subheader("Học sinh có điểm thấp nhất")
            st.dataframe(low_students)

            st.subheader("Biểu đồ phân bố điểm của học sinh")
            # Phân loại và vẽ biểu đồ
            dist = percentage_distribution(scores)
            labels = list(dist.keys())
            values = list(dist.values())

            fig, ax = plt.subplots(figsize=(1, 1))
            ax.pie(values, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 3.5})
            ax.axis("equal")
            plt.tight_layout(pad=0.1)

            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300)
            buf.seek(0)
            img = Image.open(buf)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img, width=300)

# Trang chủ
def show_home_page():
    st.title("Ứng dụng Phân tích Điểm số Học sinh")

    st.markdown(
        """
        <div style='text-align: center; max-width: 800px; margin: auto;'>
            <p style='font-size:18px;'>
                Chào mừng bạn đến với ứng dụng phân tích dữ liệu điểm số!<br><br>
            </p>
            <p style='font-size: 16px; max-width: 700px; margin: auto;'>
                Ứng dụng giúp giáo viên hoặc quản lý lớp học <b>phân tích nhanh dữ liệu điểm số học sinh</b> từ file Excel.
                Chỉ với vài cú click chuột, bạn có thể:
                <ul style='text-align: left; font-size: 15px;'>
                    <div style='text-align: center;'>
                        <ul style='display: inline-block; text-align: left; font-size: 15px;'>
                            <li>Xem điểm trung bình</li>
                            <li>Xác định học sinh có điểm cao / thấp nhất</li>
                            <li>Xem biểu đồ phân bố điểm số</li>
                        </ul>
                    </div>
                </ul>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Nút chuyển sang trang phân tích
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Bắt đầu", use_container_width=True):  
            st.session_state.start = True
            st.rerun()

# Giao diện chính
def main():
    if st.session_state.start:
        show_analysis_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()
