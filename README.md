# 📊 HỆ THỐNG PHÂN TÍCH DOANH THU VÀ HỖ TRỢ RA QUYẾT ĐỊNH

## Giới thiệu

Hệ thống Phân tích Doanh thu và Hỗ trợ Ra quyết định được xây dựng bằng **Python** và **Streamlit**, giúp doanh nghiệp theo dõi tình hình kinh doanh thông qua các chỉ số KPI và các biểu đồ trực quan.

Ngoài chức năng phân tích dữ liệu bán hàng, hệ thống còn tích hợp **Hệ hỗ trợ ra quyết định (Decision Support System - DSS)** nhằm hỗ trợ nhà quản lý đưa ra các quyết định kinh doanh dựa trên dữ liệu thực tế.

---

# Mục tiêu đề tài

- Thu thập và làm sạch dữ liệu bán hàng.
- Xây dựng các chỉ số KPI quan trọng.
- Phân tích doanh thu, lợi nhuận và hiệu quả kinh doanh.
- Trực quan hóa dữ liệu bằng các biểu đồ tương tác.
- Hỗ trợ nhà quản lý đưa ra quyết định dựa trên dữ liệu.

---

# Công nghệ sử dụng

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

---

# Cấu trúc dự án

```text
SuperstoreDashboard/

│

├── dashboard/
│   ├── Home.py
│   └── pages/
│       ├── 1_Overview.py
│       ├── 2_Sales.py
│       ├── 3_Profit.py
│       ├── 4_Product.py
│       ├── 5_Customer.py
│       ├── 6_Pareto.py
│       ├── 7_Map.py
│       └── 8_Decision_Support.py
│
├── data/
│   └── SampleSuperstore.csv
│
├── src/
│   ├── load_data.py
│   ├── cleaning.py
│   ├── filter.py
│   ├── analysis.py
│   └── visualization.py
│
├── requirements.txt
└── README.md
```

---

# Chức năng chính

## 1. Tổng quan (Overview)

Hiển thị các chỉ số KPI quan trọng:

- Tổng doanh thu
- Tổng lợi nhuận
- Tổng số đơn hàng
- Tổng số khách hàng

---

## 2. Phân tích doanh thu (Sales Analysis)

Bao gồm:

- Xu hướng doanh thu theo thời gian
- Tốc độ tăng trưởng doanh thu
- Doanh thu theo khu vực
- Doanh thu theo danh mục sản phẩm
- Doanh thu theo bang/khu vực
- Doanh thu theo nhóm sản phẩm

---

## 3. Phân tích lợi nhuận (Profit Analysis)

Bao gồm:

- Xu hướng lợi nhuận theo thời gian
- Tốc độ tăng trưởng lợi nhuận
- Lợi nhuận theo khu vực
- Lợi nhuận theo danh mục sản phẩm
- Mối quan hệ giữa chiết khấu và lợi nhuận

---

## 4. Phân tích sản phẩm (Product Analysis)

Bao gồm:

- Top sản phẩm có doanh thu cao nhất
- Top sản phẩm có doanh thu thấp nhất
- Top sản phẩm có lợi nhuận cao nhất
- Sản phẩm có lợi nhuận thấp nhất

---

## 5. Phân tích khách hàng (Customer Analysis)

Bao gồm:

- Top khách hàng mang lại doanh thu cao nhất
- Khách hàng có giá trị thấp
- Phân tích khách hàng theo phân khúc

---

## 6. Phân tích Pareto (Pareto Analysis)

Áp dụng nguyên lý 80/20:

- Xác định nhóm sản phẩm tạo ra phần lớn doanh thu.
- Hỗ trợ doanh nghiệp tập trung vào các sản phẩm quan trọng.

---

## 7. Trực quan hóa bản đồ (Map Visualization)

Hiển thị:

- Doanh thu theo khu vực địa lý.
- Lợi nhuận theo khu vực địa lý.

Giúp người dùng dễ dàng nhận biết khu vực kinh doanh hiệu quả hoặc kém hiệu quả.

---

## 8. Hệ hỗ trợ ra quyết định (Decision Support System)

Hệ thống hỗ trợ nhà quản lý trả lời các câu hỏi:

- Nên đầu tư vào khu vực nào?
- Nên đẩy mạnh danh mục nào?
- Nên loại bỏ sản phẩm nào?
- Nên giữ chân khách hàng nào?
- Khu vực nào đang có rủi ro?

Sau khi lựa chọn câu hỏi, hệ thống sẽ:

- Phân tích dữ liệu.
- Đưa ra kết quả đề xuất.
- Giải thích lý do.
- Đưa ra khuyến nghị.
- Xuất báo cáo kết quả.

---

# Bộ lọc dữ liệu

Hệ thống hỗ trợ lọc dữ liệu theo:

- Năm
- Khu vực
- Danh mục sản phẩm
- Phân khúc khách hàng

Các biểu đồ và báo cáo sẽ tự động cập nhật theo bộ lọc được lựa chọn.

---

# Các chỉ số KPI

Hệ thống sử dụng các KPI sau:

- Tổng doanh thu (Total Sales)
- Tổng lợi nhuận (Total Profit)
- Tổng số đơn hàng (Total Orders)
- Tổng số khách hàng (Total Customers)
- Tốc độ tăng trưởng doanh thu (Sales Growth)
- Tốc độ tăng trưởng lợi nhuận (Profit Growth)
- Tổng số lượng sản phẩm bán ra (Quantity Sold)

---

# Hướng dẫn cài đặt

## Bước 1: Tải mã nguồn

```bash
git clone <repository-url>
```

## Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## Bước 3: Khởi chạy ứng dụng

```bash
streamlit run dashboard/Home.py
```

---

# Bộ dữ liệu sử dụng

Dữ liệu sử dụng là bộ dữ liệu **Sample Superstore**.

Bao gồm các trường dữ liệu:

- Mã đơn hàng
- Ngày đặt hàng
- Khách hàng
- Phân khúc khách hàng
- Khu vực
- Bang/Tỉnh
- Danh mục sản phẩm
- Nhóm sản phẩm
- Tên sản phẩm
- Doanh thu
- Số lượng
- Chiết khấu
- Lợi nhuận

---

# Kết quả đạt được

- Xây dựng thành công Dashboard phân tích doanh thu.
- Trực quan hóa dữ liệu bằng nhiều loại biểu đồ.
- Hỗ trợ phân tích theo thời gian, khu vực, sản phẩm và khách hàng.
- Xây dựng bản đồ trực quan hóa dữ liệu.
- Tích hợp hệ hỗ trợ ra quyết định dựa trên dữ liệu thực tế.

---

# Hướng phát triển trong tương lai

- Kết nối cơ sở dữ liệu SQL Server hoặc MySQL.
- Tích hợp Machine Learning để dự báo doanh thu và lợi nhuận.
- Tự động tạo báo cáo PDF.
- Phân quyền người dùng.
- Triển khai hệ thống trên nền tảng điện toán đám mây.

---

# Thông tin thực hiện

**Sinh viên thực hiện:** Quang Nhật

**Đề tài:** Hệ thống phân tích doanh thu và hỗ trợ ra quyết định

**Công nghệ:** Python - Streamlit - Pandas - Plotly
