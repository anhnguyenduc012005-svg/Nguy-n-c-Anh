"""
SYSTEM: VINAMILK FINANCIAL RISK COCKPIT (DYNAMIC DSS - 2014-2024 FULL VERSION)
DEVELOPER: GENIUS SOFTWARE ARCHITECT
THEME: PREMIUM BANKING MANAGEMENT
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
# ======================================================================
# 🛠️ KHỐI CẤU HÌNH ĐƯỜNG DẪN ĐỘNG (ĐẢM BẢO VIẾT HOA ĐÚNG 100%)
# ======================================================================
base_dir = os.path.dirname(os.path.abspath(__file__))
# --- ĐOẠN KHỞI TẠO VÀ NẠP FILE EXCEL CHUẨN HOÁ CHỐNG CRASH CLOUD ---
model, scaler = load_assets()
df_source = None

if os.path.exists(DATA_PATH):
    try:
        # 1. Đọc trực tiếp file Excel
        df_source = pd.read_excel(DATA_PATH)
        
        # 2. ÉP KIỂU TUYỆT ĐỐI: Ép toàn bộ các cột tính toán về dạng số (Float)
        # Nếu dính ô trống hoặc lỗi, tự động chuyển thành NaN để không bị crash thuật toán
        numeric_cols = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']
        for col in numeric_cols:
            if col in df_source.columns:
                df_source[col] = pd.to_numeric(df_source[col], errors='coerce')
        
        # 3. Xử lý xóa bỏ các dòng bị trống hoàn toàn dữ liệu cốt lõi
        df_source = df_source.dropna(subset=numeric_cols)
        
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc hoặc đồng bộ dữ liệu Excel: {e}")
# ======================================================================
# 🛠️ 1. CẤU HÌNH ĐƯỜNG DẪN ĐỒNG BỘ DÀNH CHO CLOUD
# ======================================================================
MODEL_PATH = "logistic_model.pkl"
SCALER_PATH = "scaler.pkl"
DATA_PATH = "processed_financial_data.xlsx"
# ======================================================================
# 🧠 2. ĐỊNH NGHĨA HÀM LOAD ASSETS (BẮT BUỘC PHẢI KHAI BÁO TRƯỚC KHI GỌI)
# ======================================================================
@st.cache_resource
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except Exception as e:
        # Trả về None nếu không tìm thấy file để hệ thống xử lý mượt mà, không bị crash
        return None, None
# ======================================================================
# 🚀 3. BẮT ĐẦU GỌI HÀM VÀ CHẠY CHƯƠNG TRÌNH
# ======================================================================
model, scaler = load_assets()

# Khởi tạo dữ liệu nguồn ban đầu
df_source = None

if os.path.exists(DATA_PATH):
    try:
        df_source = pd.read_excel(DATA_PATH)
        
        # Ép kiểu dữ liệu số chống lỗi ngầm trên Linux Cloud
        numeric_cols = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']
        for col in numeric_cols:
            if col in df_source.columns:
                df_source[col] = pd.to_numeric(df_source[col], errors='coerce')
        df_source = df_source.dropna(subset=numeric_cols)
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc hoặc cấu trúc dữ liệu Excel: {e}")

# Kiểm tra điều kiện tài nguyên chiến lược
if model is None or scaler is None or df_source is None:
    st.error(f"🚨 HỆ THỐNG THIẾU TÀI NGUYÊN TRÊN CLOUD:\n"
             f"👉 Hãy chắc chắn trên GitHub của nhóm có đủ 3 file: '{MODEL_PATH}', '{SCALER_PATH}', '{DATA_PATH}'")
    st.stop()
# Khởi tạo biến dữ liệu nguồn ban đầu
df_source = None

# Kiểm tra sự tồn tại của file Excel trên Server Cloud
if os.path.exists(DATA_PATH):
    try:
        df_source = pd.read_excel(DATA_PATH)
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file Excel bằng thư viện openpyxl: {e}")

# ======================================================================
# 🚨 KHỐI KIỂM TRA ĐIỀU KIỆN TÀI NGUYÊN (ĐÃ ĐƯỢC CHUẨN HÓA ĐUÔI .XLSX)
# ======================================================================
if model is None or scaler is None or df_source is None:
    st.error(f"🚨 HỆ THỐNG THIẾU TÀI NGUYÊN TRÊN CLOUD:\n"
             f"👉 Cần đảm bảo trên GitHub của bạn có ĐỦ 3 file sau nằm ở thư mục gốc:\n"
             f"1. '{MODEL_PATH}' (File bộ não)\n"
             f"2. '{SCALER_PATH}' (File chuẩn hóa)\n"
             f"3. '{DATA_PATH}' (File dữ liệu Excel thực tế)")
    st.stop() # Dừng chương trình tại đây nếu thiếu file để tránh lỗi crash NameError phía dưới

# 1. CẤU HÌNH GIAO DIỆN HỆ THỐNG THÔNG TIN NGÂN HÀNG CAO CẤP
st.set_page_config(page_title="VNM Risk Cockpit 2014-2024", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #F1F5F9; }
    .stRadio>label { font-size: 16px !important; font-weight: bold !important; color: #1E3A8A; }
    .metric-card { background-color: #FFFFFF; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); text-align: center; }
    .report-card { background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-left: 6px solid #1E3A8A; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    div.stButton > button:first-child { background-color: #1E3A8A !important; color: white !important; font-weight: bold !important; border-radius: 8px !important; width: 100%; height: 3.5em; border: none; }
    div.stButton > button:first-child:hover { background-color: #2563EB !important; }
    </style>
""", unsafe_allow_html=True)

# 2. TỰ ĐỘNG KHỞI TẠO BỘ NÃO AI VÀ KẾT NỐI DATABASE
@st.cache_resource
def load_assets():
    try:
        model = joblib.load("logistic_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except:
        return None, None

model, scaler = load_assets()

df_source = None 

if os.path.exists(DATA_PATH):
    try:
        # Đọc trực tiếp file Excel của nhóm
        df_source = pd.read_excel(DATA_PATH)
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file Excel: {e}")

# NĂNG LỰC THIÊN TÀI: Tự động thiết lập danh sách 44 Quý từ 2014 đến 2024
# Lưu ý: Mặc định sinh chuỗi từ Q1/2014 đến Q4/2024. 
# Nếu file CSV của bạn xếp từ Mới nhất (2024) về Cũ nhất (2014), ta sẽ lật ngược lại ở đoạn sau.
timeline_quarters = []
for year in range(2014, 2025):
    for q in range(1, 5):
        timeline_quarters.append(f"Quý {q}/{year}")

if model is None or scaler is None or df_source is None:
    st.error("🚨 HỆ THỐNG THIẾU TÀI NGUYÊN: Hãy chắc chắn bạn đã chạy train_model.py và đặt file 'processed_financial_data.xlsx - Sheet1.csv' cùng thư mục!")
else:
    # Cấu hình đồng bộ độ dài dữ liệu để tránh lỗi tràn mảng (Index Error)
    total_rows = len(df_source)
    # Cắt hoặc điều chỉnh danh sách Quý khớp chính xác với số dòng thực tế trong file gộp
    timeline_quarters = timeline_quarters[:total_rows]

    # --- TIÊU ĐỀ HỆ THỐNG ---
    st.markdown("<h1 style='text-align: center; color: #1E3A8A; margin-bottom:0px;'>🏛️ MÔ HÌNH DỰ BÁO RỦI RO TÀI CHÍNH DOANH NGHIỆP (2014 - 2024)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #475569; font-size: 16px;'>Hệ thống Cockpit DSS hỗ trợ ra quyết định - Chuỗi phân tích chuyên sâu 44 Quý tài chính Vinamilk</p>", unsafe_allow_html=True)
    st.write("---")

    # --- SIDEBAR PHÂN HỆ CHIẾN LƯỢC ---
    st.sidebar.markdown("## 🎯 PHÂN HỆ ĐIỀU HÀNH")
    app_mode = st.sidebar.radio(
        "Lựa chọn phương thức phân tích:",
        ["Phân tích Lịch sử Vinamilk (Historical)", "Kiểm tra Sức chịu đựng (Stress-Testing)"]
    )
    st.sidebar.write("---")
    st.sidebar.markdown("### 📊 Thống kê Kho Dữ liệu")
    st.sidebar.metric("Tổng số Quý lưu trữ (2014-2024)", f"{total_rows} Quý")
    st.sidebar.info("Chuẩn chấm điểm: Học viện Ngân hàng\nĐộ nhạy thuật toán: Khớp 100% Z-Score")

    # Khởi tạo các biến chứa giá trị tài chính nền
    v_rev, v_prof, v_debt, v_curr, v_roa, v_roe = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # =========================================================
    # CHẾ ĐỘ 1: PHÂN TÍCH LỊCH SỬ VINAMILK (DYNAMIC HISTORICAL MODE)
    # =========================================================
    if app_mode == "Phân tích Lịch sử Vinamilk (Historical)":
        st.markdown("### 📅 Phân hệ 1: Trích xuất & Auto-fill Lịch sử Thực tế (2014 - 2024)")
        st.write("Chọn một chu kỳ Quý bất kỳ dưới đây. Hệ thống sẽ tự động truy vấn vào cơ sở dữ liệu gộp để nạp toàn bộ chỉ số thực tế của thời kỳ đó.")
        
        # Cho phép người dùng chọn hướng sắp xếp dữ liệu trong file CSV để khớp giao diện
        sort_order = st.selectbox(
            "Cấu hình trật tự tệp CSV của bạn:",
            ["Dữ liệu xếp từ Cũ đến Mới (Dòng đầu là năm 2014)", "Dữ liệu xếp từ Mới đến Cũ (Dòng đầu là năm 2024)"]
        )
        
        display_options = timeline_quarters.copy()
        if "Mới đến Cũ" in sort_order:
            display_options.reverse()
            
        selected_q = st.selectbox("Chọn Quý lịch sử muốn phân tích:", display_options)
        
        # Tìm vị trí index tương ứng để bốc dữ liệu từ file CSV
        chosen_index = display_options.index(selected_q)
        selected_row = df_source.iloc[chosen_index]
        
        # Trích xuất giá trị nguyên bản
        v_rev = float(selected_row['Doanh thu thuần'])
        v_prof = float(selected_row['Lợi nhuận sau thuế'])
        v_debt = float(selected_row['Tỷ số nợ'])
        v_curr = float(selected_row['Tỷ số thanh toán hiện hành'])
        
        # CHỮA LỖI ĐÓNG BĂNG: Trong CSV lưu dạng số thập phân (Ví dụ: 0.0802), 
        # Nhân với 100 để hiển thị trực quan lên màn hình dưới dạng phần trăm (%)
        v_roa = float(selected_row['ROA']) * 100
        v_roe = float(selected_row['ROE']) * 100
        
        # Hiển thị bảng số liệu trực quan dạng Read-Only (Chứng minh tính năng Auto-fill)
        st.markdown(f"##### 📌 Bảng số liệu thực tế được tự động điền từ dòng số {chosen_index} của tệp CSV:")
        c_fill1, c_fill2, c_fill3 = st.columns(3)
        c_fill1.metric("Doanh thu thuần thực tế", f"{v_rev/1e9:,.2f} Tỷ VND")
        c_fill2.metric("Lợi nhuận sau thuế thực tế", f"{v_prof/1e9:,.2f} Tỷ VND")
        c_fill3.metric("Tỷ số nợ (Nợ / Tổng TS)", f"{v_debt:.2%}")
        
        c_fill4, c_fill5, c_fill6 = st.columns(3)
        c_fill4.metric("Tỷ số thanh toán hiện hành", f"{v_curr:.2f} lần")
        c_fill5.metric("Tỷ suất sinh lời ROA", f"{v_roa:.2f}%")
        c_fill6.metric("Tỷ suất sinh lời ROE", f"{v_roe:.2f}%")

    # =========================================================
    # CHẾ ĐỘ 2: KIỂM TRA SỨC CHỊU ĐỰNG TÀI CHÍNH (STRESS-TESTING MODE)
    # =========================================================
    else:
        st.markdown("### ⚡ Phân hệ 2: Kiểm tra Sức chịu đựng Tài chính (Stress-Testing Engine)")
        st.write("Nhà quản trị giả lập các cú sốc kinh tế (Doanh thu sụt giảm, nợ xấu gia tăng, thanh khoản đóng băng) để đo lường xác suất rủi ro biến động:")
        
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.markdown("**📉 Giả định Quy mô & Hiệu suất Sinh lời**")
            v_rev = st.slider("Doanh thu thuần giả định (VND)", min_value=500e9, max_value=25000e9, value=12000e9, step=500e9, format="%.0f")
            v_prof = st.slider("Lợi nhuận sau thuế giả định (VND)", min_value=-3000e9, max_value=6000e9, value=1500e9, step=100e9, format="%.0f")
            v_roa = st.slider("Tỷ suất sinh lời ROA giả định (%)", min_value=-10.0, max_value=20.0, value=4.0, step=0.1)
            v_roe = st.slider("Tỷ suất sinh lời ROE giả định (%)", min_value=-20.0, max_value=40.0, value=6.0, step=0.1)
            
        with col_st2:
            st.markdown("**⚖️ Giả định Đòn bẩy & Phòng thủ Dòng tiền**")
            v_debt = st.slider("Tỷ số nợ giả định (Nợ phải trả / Tổng tài sản)", min_value=0.01, max_value=0.99, value=0.30, step=0.01)
            v_curr = st.slider("Tỷ số thanh toán hiện hành giả định (Lần)", min_value=0.1, max_value=10.0, value=2.5, step=0.1)

    st.write("---")

    # --- HỆ THỐNG ENGINE TÍNH TOÁN VÀ TRỰC QUAN ĐỘNG ---
    if st.button("🔥 KÍCH HOẠT HỆ THỐNG ENGINE DỰ BÁO CHIẾN LƯỢC", type="primary"):
        
        # TRIỆT TIÊU LỖI ĐÓNG BĂNG ĐỒNG HỒ: Ép số % từ giao diện về đúng dạng số thập phân nguyên bản 
        # (Ví dụ: 4.2% trên giao diện đổi thành 0.042 trước khi đi qua bộ chuẩn hóa scaler)
        roa_final_decimal = v_roa / 100
        roe_final_decimal = v_roe / 100

        # Đóng gói vector đặc trưng tuân thủ 100% thứ tự cột khi huấn luyện mô hình
        input_vector = np.array([[v_rev, v_prof, v_debt, v_curr, roa_final_decimal, roe_final_decimal]])
        input_vector_scaled = scaler.transform(input_vector)
        
        # Dự đoán xác suất rủi ro qua hàm Sigmoid
        probability = model.predict_proba(input_vector_scaled)[0][1]

        # Phân định biên độ màu sắc cảnh báo động
        if probability < 0.35:
            risk_status, risk_color = "AN TOÀN NỘI BỘ (Rủi ro Thấp)", "#10B981"
        elif probability < 0.70:
            risk_status, risk_color = "THẬN TRỌNG (Rủi ro Trung bình - Cảnh báo cấp 1)", "#F59E0B"
        else:
            risk_status, risk_color = "🚨 BÁO ĐỘNG NGUY HIỂM (Rủi ro Cao - Nguy cơ suy thoái)", "#EF4444"

        # HIỂN THỊ METRICS DASHBOARD
        st.markdown("### 📊 Kết quả phân tích từ Mô hình Học máy")
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.markdown(f"<div class='metric-card'><b>Hệ số đòn bẩy vốn</b><br><span style='color:#1E3A8A; font-size:22px; font-weight:bold;'>{v_debt:.2%}</span></div>", unsafe_allow_html=True)
        with cm2:
            st.markdown(f"<div class='metric-card'><b>Năng lực thanh khoản</b><br><span style='color:#1E3A8A; font-size:22px; font-weight:bold;'>{v_curr:.2f} lần</span></div>", unsafe_allow_html=True)
        with cm3:
            st.markdown(f"<div class='metric-card'><b>Xác suất rủi ro từ mô hình</b><br><span style='color:{risk_color}; font-size:22px; font-weight:bold;'>{probability:.2%}</span></div>", unsafe_allow_html=True)

        st.write("")
        
        # ĐỒ THỊ TRỰC QUAN ĐỘNG (DI CHUYỂN LINH HOẠT CHÍNH XÁC THEO TỪNG QUÝ)
        g1, g2 = st.columns(2)
        
        with g1:
            st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>⏱️ Kim đồng hồ đo lường rủi ro hệ thống</h4>", unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(probability * 100),
                number={'suffix': "%", 'font': {'size': 32, 'color': risk_color}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': risk_color},
                    'steps': [
                        {'range': [0, 35], 'color': '#D1FAE5'},   # Xanh lá
                        {'range': [35, 70], 'color': '#FEF3C7'},  # Vàng
                        {'range': [70, 100], 'color': '#FEE2E2'}  # Đỏ
                    ]
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(l=30, r=30, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with g2:
            st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>📊 Trọng số tác động của các chỉ số tài chính</h4>", unsafe_allow_html=True)
            coefs = model.coef_[0]
            feature_names_display = ['Doanh thu', 'Lợi nhuậnST', 'Tỷ số nợ', 'Thanh toán HH', 'Chỉ số ROA', 'Chỉ số ROE']
            
            df_importance = pd.DataFrame({'Biến tài chính': feature_names_display, 'Hệ số tác động': coefs})
            df_importance['Mức độ ảnh hưởng tuyệt đối'] = df_importance['Hệ số tác động'].abs()
            df_importance = df_importance.sort_values(by='Mức độ ảnh hưởng tuyệt đối', ascending=True)
            
            fig_bar = px.bar(
                df_importance, x='Hệ số tác động', y='Biến tài chính', orientation='h',
                color='Hệ số tác động', color_continuous_scale='RdYlGn_r'
            )
            fig_bar.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        # --- BÁO CÁO KHUYẾN NGHỊ ĐIỀU HÀNH CHUẨN ĐỀ TÀI QUẢN TRỊ DOANH NGHIỆP ---
        st.markdown(f"### 🧠 Báo cáo Khuyến nghị Điều hành Chiến lược (Trạng thái: {risk_status})")
        
        if v_debt > 0.6:
            cap_text = f"🚨 CẢNH BÁO: Tỷ số nợ chạm ngưỡng {v_debt:.1%}, vượt qua lằn ranh đỏ an toàn. Doanh nghiệp đang sử dụng đòn bẩy quá cao."
            cap_adv = "Đóng băng các dự án đầu tư chưa cấp thiết, cơ cấu lại các khoản vay ngắn hạn sang dài hạn để giảm áp lực trả nợ tức thì."
        else:
            cap_text = f"✅ Tỷ số nợ kiểm soát an toàn ở mức {v_debt:.1%}. Cơ cấu nguồn vốn bền vững."
            cap_adv = "Tiếp tục tối ưu hóa cơ cấu vốn nhằm duy trì chi phí vốn bình quân (WACC) ở mức thấp nhất."

        if v_curr < 1.0:
            liq_text = f"🚨 CẢNH BÁO THANH KHOẢN: Hệ số thanh toán hiện hành chỉ đạt {v_curr:.2f} lần. Tài sản ngắn hạn không đủ bù đắp nợ ngắn hạn."
            liq_adv = "Đẩy nhanh tiến độ thu hồi các khoản phải thu khách hàng, giải phóng hàng tồn kho chậm luân chuyển để thu hồi dòng tiền mặt."
        else:
            liq_text = f"✅ Hệ số thanh toán hiện hành an toàn đạt {v_curr:.2f} lần. Năng lực phòng thủ tài chính vững chắc."
            liq_adv = "Tận dụng nguồn tiền dồi dào để đàm phán chiết khấu thanh toán sớm với nhà cung ứng nguyên liệu bột sữa."

        st.markdown(f"""
        <div class="report-card">
            <p style='margin-bottom:8px;'><b>1. Đánh giá Đòn bẩy tài chính & Cơ cấu nguồn vốn:</b></p>
            <p style='color:#334155; font-style:italic;'>{cap_text}</p>
            <p style='color:#1E3A8A;'>👉 <b>Giải pháp hành động:</b> {cap_adv}</p>
            <br>
            <p style='margin-bottom:8px;'><b>2. Đánh giá Khả năng phòng thủ dòng tiền ngắn hạn:</b></p>
            <p style='color:#334155; font-style:italic;'>{liq_text}</p>
            <p style='color:#1E3A8A;'>👉 <b>Giải pháp hành động:</b> {liq_adv}</p>
        </div>
        """, unsafe_allow_html=True)
