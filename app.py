import streamlit as st
import pandas as pd
import math
import os
import requests

# ====== CSS ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700;400&display=swap');
    .main { background-color: #e3f0ff; }
    .title { color: #1a73e8; font-size: 40px; font-weight: 700; text-align: center; margin-bottom: 0; font-family: 'Roboto', Arial, Helvetica, sans-serif;}
    .subtitle { color: #1a73e8; font-size: 20px; text-align: center; margin-top: 0; font-family: 'Roboto', Arial, Helvetica, sans-serif;}
    .stMultiSelect [data-baseweb="tag"] { background-color: #1a73e8 !important; color: white !important; }
    .stMultiSelect [data-baseweb="tag"] span { color: white !important; }
    .stMultiSelect [data-baseweb="tag"] svg { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Bank Customer Churn Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Phân tích khách hàng rời đi</div>', unsafe_allow_html=True)

# ====== Load data ======
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data_processed.csv', header=0, encoding='utf-8')
        df.columns = df.columns.str.lower().str.strip()
        for col in ['geography', 'gender', 'card.type']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.title().str.strip()
                df[col] = df[col].fillna('Unknown')
        return df
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file 'data_processed.csv'.")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi không xác định khi load dữ liệu: {e}")
        st.stop()

df = load_data()

# ====== Sidebar: Bộ lọc ======
st.sidebar.header('Bộ lọc dữ liệu')

id_cols = ['surname', 'customerid', 'rownumber']
binary_cols = [col for col in df.columns if sorted(df[col].dropna().unique().tolist()) == ['0', '1']]
num_cols = [col for col in df.columns if col not in id_cols + binary_cols and df[col].dtype in ['int64', 'float64']]
cat_cols = [col for col in df.columns if col not in id_cols and col not in binary_cols + num_cols]

filtered_df = df.copy()
for col in df.columns:
    if col in id_cols:
        val = st.sidebar.text_input(f"Nhập {col} (để trống để hiện tất cả)")
    if val:
        try:
            # Ép kiểu theo kiểu dữ liệu gốc của cột
            val = df[col].dtype.type(val)
            filtered_df = filtered_df[filtered_df[col] == val]
        except ValueError:
            st.sidebar.warning(f"Giá trị nhập cho {col} không hợp lệ!")
    elif col in binary_cols:
        selected = st.sidebar.multiselect(f"Chọn {col}", ['0', '1'])
        if selected:
            filtered_df = filtered_df[filtered_df[col].isin(selected)]
    elif col in num_cols:
        val = st.sidebar.text_input(f"Nhập giá trị {col} (để trống để hiện tất cả)")
        if val:
            try:
                val = float(val)
                filtered_df = filtered_df[filtered_df[col].astype(float) == val]
            except:
                st.sidebar.warning(f"Giá trị nhập cho {col} không hợp lệ!")
    elif col in cat_cols:
        options = sorted(df[col].astype(str).str.title().str.strip().unique().tolist())
        selected = st.sidebar.multiselect(f"Chọn {col}", options)
        if selected:
            filtered_df[col] = filtered_df[col].astype(str).str.title().str.strip()
            filtered_df = filtered_df[filtered_df[col].isin(selected)]

# ====== Chọn cột hiển thị ======
all_columns = filtered_df.columns.tolist()
selected_columns = st.multiselect("Chọn các cột muốn hiển thị", all_columns, default=all_columns)

# ====== Phân trang bảng dữ liệu ======
rows_per_page = st.selectbox("Số dòng mỗi trang", [5, 10, 20, 50], index=1)
total_rows = filtered_df.shape[0]
total_pages = math.ceil(total_rows / rows_per_page)
page = st.number_input("Trang", min_value=1, max_value=total_pages if total_pages > 0 else 1, value=1, step=1)
start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page

st.header('📊 Dữ liệu đã lọc')
st.dataframe(filtered_df[selected_columns].iloc[start_idx:end_idx])
st.write(f"Trang {page}/{total_pages if total_pages > 0 else 1}")

# ====== Hiển thị đồ thị boxplot ======
st.header("Đồ thị Boxplot")
boxplot_dir = "boxplot"
if os.path.exists(boxplot_dir):
    image_files = sorted([f for f in os.listdir(boxplot_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])
    if image_files:
        selected_img = st.selectbox("Chọn đồ thị muốn xem", ["None"] + image_files)
        if selected_img != "None":
            st.image(os.path.join(boxplot_dir, selected_img), use_container_width=True)
            # Hiển thị tên đồ thị
            st.markdown(f"**Tên đồ thị:** {selected_img}")
    else:
        st.info("Chưa có đồ thị boxplot để hiển thị.")
else:
    st.info("Chưa có thư mục 'boxplot' hoặc không tìm thấy.")

import streamlit as st
import pandas as pd
import requests

# ====== Phần dự đoán Churn bằng nhập dữ liệu mới ======
st.header("🔍 Dự đoán churn cho khách hàng")

# Danh sách các biến cần nhập, theo chuẩn model
input_columns = [
    'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
    'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember',
    'EstimatedSalary', 'Complain', 'Satisfaction.Score', 'Card.Type', 'Point.Earned'
]

# Các lựa chọn cho biến categorical
geography_options = ['France', 'Germany', 'Spain']
gender_options = ['Female', 'Male']
card_type_options = ['Diamond', 'Gold', 'Platinum', 'Silver']

with st.form("predict_form"):
    st.write("Nhập thông tin khách hàng để dự đoán:")

    col1, col2, col3 = st.columns(3)

    with col1:
        credit_score = st.number_input("Credit Score", min_value=0, max_value=1000, value=600)
        geography = st.selectbox("Geography", geography_options)
        gender = st.selectbox("Gender", gender_options)
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        tenure = st.number_input("Tenure (năm gắn bó)", min_value=0, max_value=50, value=5)

    with col2:
        balance = st.number_input("Balance (số dư)", min_value=0.0, value=0.0, format="%.2f")
        num_of_products = st.number_input("Số lượng sản phẩm", min_value=1, max_value=10, value=1)
        has_cr_card = st.selectbox("Có thẻ tín dụng (HasCrCard)", [0, 1], format_func=lambda x: "Không" if x == 0 else "Có")
        is_active_member = st.selectbox("Đang hoạt động (IsActiveMember)", [0, 1], format_func=lambda x: "Không" if x == 0 else "Có")
        estimated_salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0, format="%.2f")

    with col3:
        complain = st.selectbox("Phàn nàn (Complain)", [0, 1], format_func=lambda x: "Không" if x == 0 else "Có")
        satisfaction_score = st.slider("Satisfaction Score", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        card_type = st.selectbox("Card Type", card_type_options)
        point_earned = st.number_input("Point Earned", min_value=0, max_value=10000, value=100)

    submit = st.form_submit_button("Dự đoán Churn")

def normalize_columns_for_api(df):
    df = df.copy()

    cat_cols = ['Geography', 'Gender', 'Card.Type']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().str.strip()

    df_dummies = pd.get_dummies(df[cat_cols])
    df_dummies.columns = [col.replace(' ', '').replace('_', '.').strip() for col in df_dummies.columns]

    dummy_columns_model = [
        'Geography.France', 'Geography.Germany', 'Geography.Spain',
        'Gender.Female', 'Gender.Male',
        'Card.Type.Diamond', 'Card.Type.Gold', 'Card.Type.Platinum', 'Card.Type.Silver'
    ]
    for col in dummy_columns_model:
        if col not in df_dummies.columns:
            df_dummies[col] = 0

    numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                    'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
                    'Complain', 'Satisfaction.Score', 'Point.Earned']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df = df.drop(columns=cat_cols, errors='ignore')
    final_df = pd.concat([df, df_dummies], axis=1)

    return final_df

def predict_with_api(input_df):
    API_URL = "http://127.0.0.1:8000/predict"
    payload = input_df.to_dict(orient='records')[0]
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get('prediction', None)
    else:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")

if submit:
    input_data = {
        'CreditScore': credit_score,
        'Geography': geography,
        'Gender': gender,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_of_products,
        'HasCrCard': has_cr_card,
        'IsActiveMember': is_active_member,
        'EstimatedSalary': estimated_salary,
        'Complain': complain,
        'Satisfaction.Score': satisfaction_score,
        'Card.Type': card_type,
        'Point.Earned': point_earned
    }

    input_df = pd.DataFrame([input_data])
    proc = normalize_columns_for_api(input_df)
    st.write("Dữ liệu gửi lên API:", proc.to_dict(orient='records')[0])
    try:
        proba = predict_with_api(proc)
        st.success(f"🔮 Xác suất khách hàng rời đi: {proba}")
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi API: {e}")

# ====== Phần upload file CSV và dự đoán hàng loạt ======
st.markdown("---")
st.header("📁 Dự đoán churn từ file CSV")

uploaded_file = st.file_uploader("Tải lên file CSV chứa danh sách khách hàng", type=["csv"])

if uploaded_file is not None:
    try:
        df_csv = pd.read_csv(uploaded_file)

        st.write("📄 Dữ liệu đọc được từ file:")
        st.dataframe(df_csv.head())

        df_preprocessed = normalize_columns_for_api(df_csv)

        st.write("📦 Dữ liệu sau khi xử lý gửi đến API:")
        st.dataframe(df_preprocessed.head())

        st.write("⏳ Đang dự đoán cho từng khách hàng...")
        results = []
        for i in range(len(df_preprocessed)):
            try:
                payload = df_preprocessed.iloc[i].to_dict()
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                if response.status_code == 200:
                    pred = response.json().get('prediction', None)
                    results.append(pred)
                else:
                    results.append("Lỗi")
            except:
                results.append("Lỗi")

        df_csv['Churn_Probability'] = results
        st.success("✅ Dự đoán thành công! Kết quả:")
        st.dataframe(df_csv)

        csv_output = df_csv.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải kết quả về CSV", data=csv_output, file_name="churn_predictions.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý file: {e}")
