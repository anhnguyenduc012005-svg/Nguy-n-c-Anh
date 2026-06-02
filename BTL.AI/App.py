import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

# ======================================================================
# 🛠️ CẤU HÌNH TRANG VÀ ĐƯỜNG DẪN DÀNH CHO CLOUD
# ======================================================================
st.set_page_config(page_title="Cockpit Dự Báo Rủi Ro", page_icon="🚀", layout="wide")

MODEL_PATH = "logistic_model.pkl"
SCALER_PATH = "scaler.pkl"
DATA_PATH = "processed_financial_data.xlsx"

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

# Kiểm tra an toàn tài nguyên
if model is None or scaler is None or df_source is None:
    st.error(f"🚨 HỆ THỐNG THIẾU TÀI NGUYÊN TRÊN CLOUD:\n"
             f"👉 Yêu cầu trên kho GitHub phải có đủ 3 file: '{MODEL_PATH}', '{SCALER_PATH}', '{DATA_PATH}'")
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

selected_q = st.selectbox("📌 Chọn kỳ báo cáo tài chính để phân
