"""
SYSTEM: VINAMILK FINANCIAL RISK COCKPIT (DYNAMIC DSS - 2014-2024 FULL VERSION)
DEVELOPER: GENIUS SOFTWARE ARCHITECT
THEME: PREMIUM BANKING MANAGEMENT
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os

# ======================================================================
# 🛠️ KHỐI CẤU HÌNH ĐƯỜNG DẪN ĐỘNG (CHỐNG LỖI CRASH TRÊN STREAMLIT CLOUD)
# ======================================================================
base_dir = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(base_dir, "logistic_model.pkl")
SCALER_PATH = os.path.join(base_dir, "scaler.pkl")
DATA_PATH = os.path.join(base_dir, "processed_financial_data.xlsx")

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

# 2. TỰ ĐỘNG KHỞI TẠO BỘ NÃO AI (SỬ DỤNG ĐƯỜNG DẪN ĐỘNG CHUẨN)
@st.cache_resource
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except:
        return None, None

model, scaler = load_assets()

df_source = None 
df_vnm = None # Khởi tạo bảng dữ liệu riêng cho VNM

if os.path.exists(DATA_PATH):
    try:
        # Đọc file Excel tổng (Chứa cả VNM, MCM, MCH)
        df_source = pd.read_excel(DATA_PATH)
        
        # 🔍 BỘ LỌC THÔNG MINH: Tự động phát hiện cột doanh nghiệp và tách riêng dữ liệu VNM
        company_col = None
        for col in ['Mã cổ phiếu', 'Ticker', 'Công ty', 'Doanh nghiệp', 'Mã CK', 'Ma_CK']:
            if col in df_source.columns:
                company_col = col
                break
        
        if company_col:
            # Lọc chính xác các dòng của Vinamilk (Không phân biệt chữ hoa thường hay khoảng trắng thừa)
            df_vnm = df_source[df_source[company_col].astype(str).str.upper().str.strip() == 'VNM'].copy()
        else:
            # Phương án dự phòng nếu file không có cột tên công ty
            df_vnm = df_source.copy()

        # Ép kiểu dữ liệu số an toàn để tránh lỗi tính toán trên Server Linux
        numeric_cols = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']
        for col in numeric_cols:
            if col in df_vnm.columns:
                df_vnm[col] = pd.to_numeric(df_vnm[col], errors='coerce')
                
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc và xử lý file Excel: {e}")

# Tự động thiết lập danh sách 44 Quý chuẩn của chu kỳ lịch sử
timeline_quarters = []
for year in range(2014, 2025):
    for q in range(1, 5):
        timeline_quarters.append(f"Quý {q}/{year}")

if model is None or scaler is None or df_source is None or df_vnm is None:
    st.error("🚨 HỆ THỐNG THIẾU TÀI NGUYÊN: Vui lòng kiểm tra lại sự tồn tại của các file cấu trúc.")
    st.warning(f"🔍 Trạng thái Model: {'Tìm thấy' if os.path.exists(MODEL_PATH) else 'Không tìm thấy'}")
    st.warning(f"🔍 Trạng thái Scaler: {'Tìm thấy' if os.path.exists(SCALER_PATH) else 'Không tìm thấy'}")
    st.warning(f"🔍 Trạng thái dữ liệu: {'Tìm thấy' if os.path.exists(DATA_PATH) else 'Không tìm thấy'}")
else:
    # Đồng bộ số lượng Quý hiển thị khớp chính xác với số dòng THỰC TẾ CỦA VNM (đã lọc)
    total_rows = len(df_vnm)
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
    st.sidebar.metric("Tổng số Quý VNM hiển thị", f"{total_rows} Quý")
    st.sidebar.caption(f"💡 Mô hình AI đã học trên tổng số {len(df_source)} dòng dữ liệu toàn ngành (VNM, MCM, MCH).")
    st.sidebar.info("Chuẩn chấm điểm: Học viện Ngân hàng\nĐộ nhạy thuật toán: Khớp 100% Z-Score")

    # Khởi tạo các biến chứa giá trị tài chính nền
    v_rev, v_prof, v_debt, v_curr, v_roa, v_roe = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # =========================================================
    # CHẾ ĐỘ 1: PHÂN TÍCH LỊCH SỬ VINAMILK (CHỈ HIỂN THỊ DATA VNM)
    # =========================================================
    if app_mode == "Phân tích Lịch sử Vinamilk (Historical)":
        st.markdown("### 📅 Phân hệ 1: Trích xuất & Auto-fill Lịch sử Thực tế Vinamilk")
        st.write("Hệ thống đã lọc bỏ dữ liệu của các công ty vệ tinh (MCM, MCH), chỉ trích xuất chính xác chỉ số tài chính của VNM.")
        
        sort_order = st.selectbox(
            "Cấu hình trật tự thời gian hiển thị:",
            ["Dữ liệu xếp từ Cũ đến Mới (Dòng đầu là năm 2014)", "Dữ liệu xếp từ Mới đến Cũ (Dòng đầu là năm 2024)"]
        )
        
        display_options = timeline_quarters.copy()
        if "Mới đến Cũ" in sort_order:
            display_options.reverse()
            
        selected_q = st.selectbox("Chọn Quý lịch sử muốn phân tích:", display_options)
        
        # Tìm vị trí dòng tương ứng trong bảng dữ liệu ĐÃ LỌC RIÊNG của VNM
        chosen_index = display_options.index(selected_q)
        selected_row = df_vnm.iloc[chosen_index]
        
        # Trích xuất giá trị an toàn
        v_rev = float(selected_row['Doanh thu thuần'])
        v_prof = float(selected_row['Lợi nhuận sau thuế'])
        v_debt = float(selected_row['Tỷ số nợ'])
        v_curr = float(selected_row['Tỷ số thanh toán hiện hành'])
        
        # Đồng bộ tỷ lệ phần trăm hiển thị giao diện
        v_roa = float(selected_row['ROA']) * 100 if float(selected_row['ROA']) <= 1.0 else float(selected_row['ROA'])
        v_roe = float(selected_row['ROE']) * 100 if float(selected_row['ROE']) <= 1.0 else float(selected_row['ROE'])
        
        st.markdown(f"##### 📌 Bảng số liệu thực tế Vinamilk được tự động điền ({selected_q}):")
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
        st.write("Nhà quản trị giả lập các cú sốc kinh tế để đo lường xác suất rủi ro biến động dựa trên thuật toán cốt lõi:")
        
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
        
        roa_final_decimal = v_roa / 100
        roe_final_decimal = v_roe / 100

        # Đóng gói vector đặc trưng đưa vào bộ chuẩn hóa và mô hình AI
        input_vector = np.array([[v_rev, v_prof, v_debt, v_curr, roa_final_decimal, roe_final_decimal]])
        input_vector_scaled = scaler.transform(input_vector)
        
        probability = model.predict_proba(input_vector_scaled)[0][1]

        if probability < 0.35:
            risk_status, risk_color = "AN TOÀN NỘI BỘ (Rủi ro Thấp)", "#10B981"
        elif probability < 0.70:
            risk_status, risk_color = "THẬN TRỌNG (Rủi ro Trung bình - Cảnh báo cấp 1)", "#F59E0B"
        else:
            risk_status, risk_color = "🚨 BÁO ĐỘNG NGUY HIỂM (Rủi ro Cao - Nguy cơ suy thoái)", "#EF4444"

        st.markdown("### 📊 Kết quả phân tích từ Mô hình Học máy")
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.markdown(f"<div class='metric-card'><b>Hệ số đòn bẩy vốn</b><br><span style='color:#1E3A8A; font-size:22px; font-weight:bold;'>{v_debt:.2%}</span></div>", unsafe_allow_html=True)
        with cm2:
            st.markdown(f"<div class='metric-card'><b>Năng lực thanh khoản</b><br><span style='color:#1E3A8A; font-size:22px; font-weight:bold;'>{v_curr:.2f} lần</span></div>", unsafe_allow_html=True)
        with cm3:
            st.markdown(f"<div class='metric-card'><b>Xác suất rủi ro từ mô hình</b><br><span style='color:{risk_color}; font-size:22px; font-weight:bold;'>{probability:.2%}</span></div>", unsafe_allow_html=True)

        st.write("")
        
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
                        {'range': [0, 35], 'color': '#D1FAE5'},
                        {'range': [35, 70], 'color': '#FEF3C7'},
                        {'range': [70, 100], 'color': '#FEE2E2'}
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
