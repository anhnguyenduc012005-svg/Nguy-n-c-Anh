"""
SYSTEM: FINANCIAL RISK TRAINING ENGINE (LOGISTIC REGRESSION)
DEVELOPER: GENIUS SOFTWARE ARCHITECT
PERIOD: 2014 - 2024 (QUARTERLY DATA)
CAMPUS: BANKING ACADEMY OF VIETNAM (HVNH)
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib

def main():
    print("="*70)
    print("🚀 ĐANG KHỞI CHẠY ENGINE HUẤN LUYỆN TOÀN DIỆN CHU KỲ 2014 - 2024")
    print("="*70)
    
    # 🛠️ THAY ĐỔI: Quét trực tiếp file Excel (.xlsx)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "processed_financial_data.xlsx")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Không tìm thấy tệp dữ liệu chiến lược tại: {data_path}\n"
                                f"👉 Hãy chắc chắn bạn đã để file Excel 'processed_financial_data.xlsx' vào đúng thư mục BTL.AI!")
        
    # Đọc file excel (Mặc định đọc Sheet đầu tiên)
    df = pd.read_excel(data_path)
    print(f"✔️ Nạp dữ liệu Excel thành công! Tìm thấy {len(df)} chu kỳ Quý báo cáo (2014 - 2024).")
    
    # 2. TÍCH HỢP THUẬT TOÁN GÁN NHÃN THEO QUY CHUẨN TOÁN HỌC CỦA NHÓM TRƯỞNG
    def calculate_risk_score(row):
        score = 0
        if row['ROA'] < 0.02:  
            score += 1
        if row['ROE'] < 0.05:  
            score += 1
        if row['Tỷ số nợ'] > 0.6:  
            score += 1
        if row['Tỷ số thanh toán hiện hành'] < 1.0:  
            score += 1
        return score

    df['Risk_Score'] = df.apply(calculate_risk_score, axis=1)
    df['Rui_ro'] = np.where(df['Risk_Score'] >= 1, 1, 0)
    
    # 3. ĐỊNH NGHĨA BIẾN ĐỘC LẬP (X) VÀ BIẾN MỤC TIÊU (Y)
    features_list = ['Doanh thu thuần', 'Lợi nhuận sau thuế', 'Tỷ số nợ', 'Tỷ số thanh toán hiện hành', 'ROA', 'ROE']
    df_clean = df.dropna(subset=features_list + ['Rui_ro'])
    X = df_clean[features_list]
    y = df_clean['Rui_ro']
    
    # 4. PHÂN CHIA TẬP TRAIN/TEST (80/20) CÂN BẰNG THÀNH PHẦN
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 5. CHUẨN HÓA Z-SCORE
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 6. KHỞI TẠO VÀ KHỚP MÔ HÌNH HỒI QUY LOGISTIC
    model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # 7. KIỂM THỬ ĐÁNH GIÁ ĐỘ CHÍNH XÁC NỘI BỘ
    y_pred = model.predict(X_test_scaled)
    
    print("\n" + "="*20 + " KẾT QUẢ ĐÁNH GIÁ HIỆU NĂNG MÔ HÌNH " + "="*20)
    print(f"✔️ Accuracy (Độ chính xác tổng thể):  {accuracy_score(y_test, y_pred):.4f}")
    print(f"✔️ F1-Score (Chỉ số F1 cân bằng):     {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print("="*70)
    
    # 8. XUẤT BẢN BỘ NÃO HỌC MÁY
    model_path = os.path.join(base_dir, 'logistic_model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler.pkl')
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"\n[THÀNH CÔNG] Đã lưu bộ não mô hình tại:\n -> {model_path}\n -> {scaler_path}")

if __name__ == "__main__":
    main()
