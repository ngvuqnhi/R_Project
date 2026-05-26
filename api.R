library(plumber)
library(jsonlite)
library(randomForest)

# Load model một lần khi khởi chạy server
model <- readRDS("rf_model_churn.rds")
required_vars <- names(model$forest$xlevels)

#* @apiTitle Customer Churn Prediction API

#* Dự đoán khả năng khách rời đi
#* @post /predict
function(req) {
  tryCatch({
    # Đọc và chuyển đổi dữ liệu JSON
    json_input <- req$postBody
    input_list <- fromJSON(json_input)
    # Chuyển thành data.frame
    df <- as.data.frame(input_list)
    colnames(df) <- make.names(colnames(df))

    # Thêm các cột còn thiếu trong model, gán giá trị mặc định = 0
    missing_cols <- setdiff(required_vars, colnames(df))
    if (length(missing_cols) > 0) {
      for (col in missing_cols) {
        df[[col]] <- 0
      }
    }

    # Sắp xếp đúng thứ tự các cột
    df <- df[, required_vars, drop = FALSE]

    # Dự đoán (kết quả nhị phân)
    prediction <- predict(model, df)

    # (Tuỳ chọn) Nếu muốn trả cả xác suất:
    # probs <- predict(model, df, type = "prob")

    # Trả kết quả
    list(
      prediction = as.character(prediction)
      # , probability = probs[,2]  # nếu muốn thêm xác suất rời đi
    )

  }, error = function(e) {
    list(error = paste("Lỗi đầu vào hoặc dự đoán:", e$message))
  })
}
