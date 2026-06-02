import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

# ======================================================================
# 🛠️ 1. CẤU HÌNH ĐƯỜNG DẪN THÔNG MINH (TỰ ĐỘNG CHUI VÀO ĐÚNG THƯ MỤC)
# ======================================================================
# Lấy chính xác địa chỉ của thư mục đang chứa file App.py này (thư mục BTL.AI)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Ghép tên file vào đúng địa chỉ thư mục đó
MODEL_PATH = os.path.join(base_dir, "logistic_model.pkl")
SCALER_PATH = os.path.join(base_dir, "scaler.pkl")
DATA_PATH = os.path.join(base_dir, "processed_financial_data.xlsx")

# ======================================================================
# 🧠 ĐỊNH NGHĨA HÀM LOAD TÀI NGUYÊN (BẮT BUỘC ĐẶT TRƯỚC KHI GỌI)
# ======================================================================
@st.cache_resource
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except Exception as e:
        return None, None

# ======================================================================
# 🚀 KHỞI CHẠY HỆ THỐNG VÀ NẠP DỮ LIỆU
# ======================================================================
model, scaler = load_assets()
df_source = None

if os.path.exists(DATA_PATH):
    try:
        df_source = pd.read_excel(DATA_PATH)
        # Ép kiểu dữ liệu số tuyệt đối để chống lỗi Crash trên Cloud
        numeric_cols = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']
        for col in numeric_cols:
            if col in df_source.columns:
                df_source[col] = pd.to_numeric(df_source[col], errors='coerce')
        df_source = df_source.dropna(subset=numeric_cols)
    except Exception as e:
        st.error(f"❌ Lỗi khi nạp dữ liệu Excel: {e}")

# Kiểm tra an toàn tài nguyên (Chế độ dò tìm lỗi chi tiết)
if model is None or scaler is None or df_source is None:
    st.error("🚨 HỆ THỐNG THIẾU TÀI NGUYÊN TRÊN CLOUD! BẢNGKÊ CHI TIẾT:")
    
    # Bật radar quét từng file một
    st.warning(f"🔍 1. Tìm thấy file '{MODEL_PATH}': **{os.path.exists(MODEL_PATH)}**")
    st.warning(f"🔍 2. Tìm thấy file '{SCALER_PATH}': **{os.path.exists(SCALER_PATH)}**")
    st.warning(f"🔍 3. Tìm thấy file '{DATA_PATH}': **{os.path.exists(DATA_PATH)}**")
    
    if os.path.exists(DATA_PATH) and df_source is None:
        st.error("⚠️ Phân tích: File Excel CÓ tồn tại trên GitHub, nhưng hệ thống không thể đọc được. "
                 "Nguyên nhân 99% là do Server chưa cài được thư viện `openpyxl`. "
                 "Hãy kiểm tra lại file `requirements.txt` đã viết đúng chính tả chưa!")
                 
    st.stop()

# ======================================================================
# 📊 GIAO DIỆN BẢNG ĐIỀU KHIỂN (DASHBOARD)
# ======================================================================
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🚀 Đài Chỉ Huy (Cockpit) Dự Báo Rủi Ro Tài Chính</h1>", unsafe_allow_html=True)
st.markdown("---")

# 1. Chọn kỳ báo cáo linh hoạt
if 'Quý' in df_source.columns:
    quarters = df_source['Quý'].astype(str).tolist()
elif 'Quarter' in df_source.columns:
    quarters = df_source['Quarter'].astype(str).tolist()
else:
    quarters = [f"Kỳ báo cáo {i+1}" for i in range(len(df_source))]

selected_q = st.selectbox("📌 Chọn kỳ báo cáo tài chính để phân tích dự báo:", options=quarters)

# 2. Trích xuất dòng dữ liệu và tính toán thuật toán
idx = quarters.index(selected_q)
row_data = df_source.iloc[idx]
features = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']

# Xử lý ma trận đầu vào
X_input = row_data[features].values.reshape(1, -1)
X_scaled = scaler.transform(X_input)
probability = model.predict_proba(X_scaled)[0][1]

# 3. Định tuyến trạng thái rủi ro
if probability < 0.35:
    risk_color = '#10B981' # Xanh an toàn
    risk_status = "AN TOÀN"
elif probability < 0.70:
    risk_color = '#F59E0B' # Vàng cảnh báo
    risk_status = "CẢNH BÁO CAO"
else:
    risk_color = '#EF4444' # Đỏ nguy hiểm
    risk_status = "NGUY HIỂM (RỦI RO ĐÌNH TRỆ)"

# 4. Bảng số liệu thực tế
st.markdown("### 📊 Thông số tài chính cốt lõi đầu vào")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Doanh thu thuần", f"{row_data['Doanh thu thuần']:,.0f}")
c2.metric("Lợi nhuận ST", f"{row_data['Lợi nhuận sau thuế']:,.0f}")
c3.metric("Tỷ số nợ", f"{row_data['Tỷ số nợ']:.2f}")
c4.metric("Thanh toán HH", f"{row_data['Tỷ số thanh toán hiện hành']:.2f}")
c5.metric("Chỉ số ROA", f"{row_data['ROA']:.2%}")
c6.metric("Chỉ số ROE", f"{row_data['ROE']:.2%}")

st.markdown("---")

# ======================================================================
# 📈 KHỐI ĐỒ THỊ TRỰC QUAN HÓA (Đã dọn sạch lỗi cú pháp)
# ======================================================================
g1, g2 = st.columns(2)
with g1:
    st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>⏱️ Kim đồng hồ đo lường xác suất rủi ro</h4>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=float(probability * 100),
        number={'suffix': "%", 'font': {'size': 36, 'color': risk_color}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': risk_color},
               'steps': [{'range': [0, 35], 'color': '#D1FAE5'},
                         {'range': [35, 70], 'color': '#FEF3C7'},
                         {'range': [70, 100], 'color': '#FEE2E2'}]}))
    fig_gauge.update_layout(height=300, margin=dict(l=30, r=30, t=30, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

with g2:
    st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>⚖️ Trọng số tác động của các biến tài chính</h4>", unsafe_allow_html=True)
    coefs = model.coef_[0]
    feature_names_display = ['Doanh thu', 'Lợi nhuận ST', 'Tỷ số nợ', 'Thanh toán HH', 'Chỉ số ROA', 'Chỉ số ROE']
    df_importance = pd.DataFrame({'Biến tài chính': feature_names_display, 'Hệ số tác động': coefs})
    df_importance['Mức độ ảnh hưởng tuyệt đối'] = df_importance['Hệ số tác động'].abs()
    df_importance = df_importance.sort_values(by='Mức độ ảnh hưởng tuyệt đối', ascending=True)
    
    fig_bar = px.bar(df_importance, x='Hệ số tác động', y='Biến tài chính', orientation='h',
                     color='Hệ số tác động', color_continuous_scale='RdYlGn_r')
    fig_bar.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ======================================================================
# 🧠 BÁO CÁO KHUYẾN NGHỊ ĐIỀU HÀNH
# ======================================================================
st.markdown(f"### 💡 Báo cáo Khuyến nghị Chiến lược (Trạng thái: <span style='color:{risk_color};'>{risk_status}</span>)", unsafe_allow_html=True)

v_debt = row_data['Tỷ số nợ']
v_curr = row_data['Tỷ số thanh toán hiện hành']

if v_debt > 0.6:
    cap_text, cap_adv = f"🚨 CẢNH BÁO: Tỷ số đòn bẩy chạm ngưỡng {v_debt:.2f}.", "Nhanh chóng cơ cấu lại các khoản vay để giảm áp lực trả nợ."
else:
    cap_text, cap_adv = f"✅ Tỷ số nợ kiểm soát an toàn ở mức {v_debt:.2f}.", "Tiếp tục duy trì cơ cấu vốn hiện tại để tối ưu hóa chi phí."

if v_curr < 1.0:
    liq_text, liq_adv = f"🚨 CẢNH BÁO THANH KHOẢN: Hệ số thanh toán đạt {v_curr:.2f} lần.", "Cần kích hoạt quỹ tiền mặt dự phòng và đẩy nhanh thu hồi nợ."
else:
    liq_text, liq_adv = f"✅ Hệ số thanh toán hiện hành an toàn đạt {v_curr:.2f} lần.", "Dòng tiền ổn định, có thể linh hoạt tối ưu hóa dòng tiền nhàn rỗi."

st.markdown(f"""
<div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0;'>
    <p><b>1. Đánh giá Đòn bẩy tài chính (Capital Structure):</b> <span style='color:#334155;'>{cap_text}</span></p>
    <p style='color:#1E3A8A;'>👉 <b>Giải pháp đề xuất:</b> {cap_adv}</p><br>
    <p><b>2. Đánh giá Khả năng phòng thủ (Liquidity):</b> <span style='color:#334155;'>{liq_text}</span></p>
    <p style='color:#1E3A8A;'>👉 <b>Giải pháp đề xuất:</b> {liq_adv}</p>
</div>
""", unsafe_allow_html=True)
