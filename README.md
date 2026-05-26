# R_Project - Bank Customer Churn Analysis & Prediction

## Giới thiệu

Đây là đồ án cuối kỳ môn **Lập trình R cho Phân tích**. Dự án ứng dụng khoa học dữ liệu để phân tích hành vi khách hàng ngân hàng và xây dựng mô hình dự đoán khả năng khách hàng rời bỏ dịch vụ, hay còn gọi là **customer churn**.

Dự án gồm hai phần chính:

1. **Phân tích dữ liệu bằng R/R Markdown**: tiền xử lý dữ liệu, EDA, phân tích hành vi khách hàng, phân cụm và mô hình hóa.
2. **Ứng dụng dự đoán churn**: sử dụng Plumber API trong R để phục vụ mô hình Random Forest và Streamlit app bằng Python để nhập dữ liệu, xem dashboard và dự đoán churn.

## Thành viên thực hiện

**Nhóm 07**

- Võ Minh Khôi - 23133039
- Trần Thị Trà My - 23133045
- Nguyễn Vũ Quỳnh Nhi - 23133050
- Nguyễn Thị Kim Oanh - 23133053

## Mục tiêu dự án

Dự án hướng đến các mục tiêu chính:

- Tiền xử lý và làm sạch dữ liệu khách hàng ngân hàng.
- Phân tích khám phá dữ liệu để tìm các yếu tố liên quan đến churn.
- Phân tích hành vi sử dụng sản phẩm, thẻ tín dụng, mức độ hoạt động và khiếu nại của khách hàng.
- Phân cụm khách hàng để hiểu rõ từng nhóm khách hàng.
- Xây dựng mô hình học máy để dự đoán khách hàng có nguy cơ rời bỏ.
- So sánh hiệu quả giữa Decision Tree và Random Forest.
- Triển khai mô hình Random Forest thông qua API.
- Xây dựng giao diện Streamlit để lọc dữ liệu, xem dashboard và dự đoán churn.

## Bộ dữ liệu

Dữ liệu sử dụng trong dự án là bộ dữ liệu khách hàng ngân hàng, bao gồm các thông tin như:

- `CreditScore`: Điểm tín dụng
- `Geography`: Khu vực của khách hàng
- `Gender`: Giới tính
- `Age`: Tuổi
- `Tenure`: Số năm gắn bó với ngân hàng
- `Balance`: Số dư tài khoản
- `NumOfProducts`: Số lượng sản phẩm đang sử dụng
- `HasCrCard`: Khách hàng có thẻ tín dụng hay không
- `IsActiveMember`: Khách hàng có hoạt động thường xuyên hay không
- `EstimatedSalary`: Thu nhập ước tính
- `Complain`: Khách hàng có khiếu nại hay không
- `Satisfaction.Score`: Điểm hài lòng
- `Card.Type`: Loại thẻ
- `Point.Earned`: Điểm tích lũy
- `Exited`: Trạng thái rời bỏ của khách hàng

Biến mục tiêu của bài toán là `Exited`:

- `0`: Khách hàng chưa rời bỏ
- `1`: Khách hàng đã rời bỏ

Sau bước xử lý ngoại lai, bộ dữ liệu còn khoảng **9.626 khách hàng**.

## Cấu trúc project

```text
R_Project/
├── 1.Data_Preprocessing.Rmd
├── 2.Exploratory_Data_Analysis.Rmd
├── 3.Behavioral analysis.Rmd
├── 4.Data_Modeling.Rmd
├── Conclusion.Rmd
├── api.R
├── app.py
├── rf_model_churn.rds
├── src_and_data.Rproj
├── data_processed.csv
├── test_data.csv
├── sample_customers.csv
├── boxplot/
└── README.md
```

## Quy trình thực hiện

### 1. Tiền xử lý dữ liệu

File sử dụng: `1.Data_Preprocessing.Rmd`

Các bước chính:

- Đọc dữ liệu gốc.
- Kiểm tra kiểu dữ liệu.
- Kiểm tra và xử lý giá trị thiếu.
- Kiểm tra ngoại lai bằng boxplot.
- Xử lý ngoại lai bằng phương pháp IQR.
- Lưu dữ liệu đã xử lý thành `data_processed.csv`.

### 2. Phân tích khám phá dữ liệu

File sử dụng: `2.Exploratory_Data_Analysis.Rmd`

Các bước chính:

- Thống kê mô tả dữ liệu.
- Phân tích tương quan Pearson giữa các biến số.
- Phân tích Cramer's V giữa các biến phân loại.
- Phân tích đơn biến và hai biến.
- So sánh các yếu tố với biến mục tiêu `Exited`.
- Thực hiện kiểm định T-test và Chi-square.

### 3. Phân tích hành vi khách hàng

File sử dụng: `3.Behavioral analysis.Rmd`

Các nội dung chính:

- Phân tích số lượng sản phẩm khách hàng sử dụng.
- Phân tích tỷ lệ churn theo số lượng sản phẩm.
- Phân tích việc sử dụng thẻ tín dụng và loại thẻ.
- Phân tích mức độ tích cực của khách hàng.
- Phân tích điểm tích lũy.
- Phân tích mối quan hệ giữa số lượng sản phẩm và khiếu nại.
- Phân cụm khách hàng bằng K-means.
- Trực quan hóa cụm khách hàng bằng PCA.

### 4. Mô hình hóa dữ liệu

File sử dụng: `4.Data_Modeling.Rmd`

Các bước chính:

- Đọc dữ liệu từ `data_processed.csv`.
- Loại bỏ các cột định danh như `RowNumber`, `CustomerId`, `Surname`.
- Mã hóa biến phân loại bằng one-hot encoding.
- Kiểm tra mất cân bằng dữ liệu.
- Cân bằng dữ liệu bằng SMOTE.
- Chia dữ liệu thành tập huấn luyện và tập kiểm tra.
- Xây dựng mô hình Decision Tree.
- Xây dựng mô hình Random Forest.
- Đánh giá mô hình bằng confusion matrix, Accuracy, Recall, Specificity và ROC-AUC.
- Lưu mô hình Random Forest vào file `rf_model_churn.rds`.

## Kết quả mô hình

Hai mô hình được so sánh là **Decision Tree** và **Random Forest**.

| Mô hình | Accuracy | Recall | Specificity |
|---|---:|---:|---:|
| Decision Tree | 83.62% | 69.20% | 94.53% |
| Random Forest | 89.65% | 81.20% | 96.09% |

Random Forest cho kết quả tốt hơn Decision Tree ở hầu hết các chỉ số đánh giá. Vì mục tiêu của bài toán là phát hiện khách hàng có nguy cơ rời bỏ, chỉ số Recall được xem là đặc biệt quan trọng. Random Forest có Recall cao hơn, giúp giảm khả năng bỏ sót những khách hàng thật sự có nguy cơ churn.

## API dự đoán churn

File sử dụng: `api.R`

API được xây dựng bằng package **plumber** trong R. Khi chạy, API sẽ load mô hình Random Forest từ file `rf_model_churn.rds`, nhận dữ liệu khách hàng dưới dạng JSON và trả về kết quả dự đoán tại endpoint:

```text
POST /predict
```

### Chạy API

Trong Terminal, tại thư mục project, chạy:

```bash
R -e 'pr <- plumber::plumb("api.R"); pr$run(host="127.0.0.1", port=8000)'
```

API sẽ chạy tại:

```text
http://127.0.0.1:8000/predict
```

## Ứng dụng Streamlit

File sử dụng: `app.py`

Ứng dụng Streamlit có các chức năng chính:

- Hiển thị dashboard dữ liệu khách hàng.
- Lọc dữ liệu theo các cột.
- Chọn cột muốn hiển thị.
- Phân trang bảng dữ liệu.
- Hiển thị các biểu đồ boxplot nếu có thư mục `boxplot`.
- Nhập thông tin khách hàng mới để dự đoán churn.
- Upload file CSV để dự đoán churn hàng loạt.
- Tải kết quả dự đoán về dưới dạng CSV.

### Chạy Streamlit app

Mở Terminal tại thư mục project, chạy:

```bash
streamlit run app.py
```

Sau đó mở đường dẫn Streamlit hiển thị trong Terminal, thường là:

```text
http://localhost:8501
```

## Cài đặt thư viện

### Thư viện R

```r
install.packages(c(
  "tidyverse", "dplyr", "ggplot2", "gridExtra", "corrplot", "vcd",
  "smotefamily", "rpart", "randomForest", "pROC", "caret",
  "reshape2", "plotly", "factoextra", "plumber", "jsonlite"
))
```

### Thư viện Python

```bash
pip install streamlit pandas requests
```

## Cách chạy toàn bộ project

### Bước 1: Mở project trong RStudio

Mở file:

```text
src_and_data.Rproj
```

Sau đó chạy các file `.Rmd` theo thứ tự:

```text
1.Data_Preprocessing.Rmd
2.Exploratory_Data_Analysis.Rmd
3.Behavioral analysis.Rmd
4.Data_Modeling.Rmd
Conclusion.Rmd
```

### Bước 2: Chạy API R

```bash
R -e 'pr <- plumber::plumb("api.R"); pr$run(host="127.0.0.1", port=8000)'
```

### Bước 3: Chạy ứng dụng Streamlit

Mở một Terminal khác và chạy:

```bash
streamlit run app.py
```

Lưu ý: Streamlit app gọi API tại `http://127.0.0.1:8000/predict`, vì vậy cần chạy `api.R` trước khi bấm dự đoán trên giao diện Streamlit.

## Ví dụ dữ liệu gửi vào API

```json
{
  "CreditScore": 600,
  "Age": 35,
  "Tenure": 5,
  "Balance": 0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 50000,
  "Complain": 0,
  "Satisfaction.Score": 5,
  "Point.Earned": 100,
  "Geography.France": 1,
  "Geography.Germany": 0,
  "Geography.Spain": 0,
  "Gender.Female": 1,
  "Gender.Male": 0,
  "Card.Type.Diamond": 0,
  "Card.Type.Gold": 1,
  "Card.Type.Platinum": 0,
  "Card.Type.Silver": 0
}
```

## Các phát hiện chính

Một số kết quả đáng chú ý từ quá trình phân tích:

- Khiếu nại của khách hàng là yếu tố có liên hệ rất mạnh với churn.
- Khách hàng ở Đức có tỷ lệ rời bỏ cao hơn các khu vực khác.
- Khách hàng lớn tuổi có xu hướng rời bỏ cao hơn.
- Khách hàng không hoạt động thường xuyên có nguy cơ churn cao hơn.
- Số lượng sản phẩm sử dụng có ảnh hưởng đến mức độ gắn bó của khách hàng.
- Random Forest là mô hình phù hợp hơn để dự đoán churn trong dự án này.

## Đề xuất chiến lược

Dựa trên kết quả phân tích, nhóm đề xuất một số chiến lược:

- Cải thiện quy trình tiếp nhận và xử lý khiếu nại.
- Tập trung chăm sóc nhóm khách hàng có nguy cơ rời bỏ cao.
- Xây dựng chiến lược riêng cho thị trường Đức.
- Hỗ trợ khách hàng lớn tuổi bằng dịch vụ tư vấn và chăm sóc phù hợp.
- Khuyến khích khách hàng sử dụng dịch vụ thường xuyên hơn.
- Tối ưu hóa ưu đãi theo loại thẻ và nhóm sản phẩm.
- Thiết kế chiến lược chăm sóc riêng cho từng cụm khách hàng.

## Kết luận

Dự án đã hoàn thành quy trình phân tích dữ liệu từ tiền xử lý, khai phá dữ liệu, phân tích hành vi khách hàng đến xây dựng và triển khai mô hình dự đoán churn. Kết quả cho thấy Random Forest là mô hình có hiệu quả tốt hơn trong việc phát hiện khách hàng có nguy cơ rời bỏ. Ứng dụng Streamlit kết hợp Plumber API giúp người dùng có thể nhập dữ liệu mới hoặc upload file CSV để dự đoán churn một cách trực quan.

## Tác giả

Nhóm 07  
Môn Lập trình R cho Phân tích  
Trường Đại học Sư phạm Kỹ thuật TP. Hồ Chí Minh

