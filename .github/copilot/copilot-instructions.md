# 🎯 Hướng dẫn Tùy chỉnh cho GitHub Copilot

## 📦 Ngữ cảnh Dự án

Kho lưu trữ này chứa mã nguồn và tài nguyên cho một đường ống **ETL (Extract, Transform, Load)** được thiết kế để xử lý tập dữ liệu **Netflix Movies & TV Shows**.

Mục tiêu chính là thực hiện làm sạch và chuyển đổi dữ liệu thô, áp dụng mô hình hóa dữ liệu (Star Schema), sau đó tải dữ liệu đã được cấu trúc hóa vào cơ sở dữ liệu **PostgreSQL** để phục vụ cho mục đích phân tích.

---

## ✨ Công nghệ & Thư viện Chính

- **Trích xuất/Chuyển đổi Dữ liệu:** Python với thư viện **Pandas**.
- **Môi trường Phát triển:** **Jupyter Notebooks**.
- **Tải Dữ liệu:** Cơ sở dữ liệu **PostgreSQL** (sử dụng thư viện như Psycopg2 hoặc SQLAlchemy).

---

## 🛠️ Các Bước & Yêu cầu Cụ thể của Đường ống ETL

Copilot nên ưu tiên các gợi ý và đoạn mã tạo điều kiện thuận lợi cho các bước sau, đảm bảo mã nguồn mạnh mẽ, hiệu quả và tuân theo phong cách Pythonic.

### 1. 📥 Trích xuất Dữ liệu (E - Extract)

- **Nguồn:** Tập dữ liệu thô **Netflix Movies & TV Shows**.
- **Nhiệm vụ:** Mã nguồn nên tập trung vào việc đọc dữ liệu từ tệp CSV hoặc thiết lập kết nối để tải thông qua **Kaggle CLI/API** nếu cần. Thao tác khởi đầu là `pd.read_csv()`.

### 2. 🧹 Chuyển đổi Dữ liệu (T - Transform)

#### A. Làm sạch Dữ liệu

- **Xử lý Giá trị Thiếu (NA):** **Loại bỏ (drop)** các hàng có giá trị NA trong các cột quan trọng (ví dụ: `director`, `country`, `date_added`, `rating`).
- **Phân tách Thể loại (Genre):** Cột `listed_in` (chứa nhiều thể loại) **phải được phân rã/tách (explode)** để mỗi hàng chỉ chứa một thể loại duy nhất, chuẩn bị cho việc tạo bảng chiều.

#### B. Chuẩn hóa & Mô hình hóa

- **Chuẩn hóa Ngày tháng:** Chuyển đổi cột ngày tháng (`date_added`) thành định dạng chuẩn của Pandas datetime, sau đó chuyển sang định dạng **`YYYY-MM-DD`** phù hợp cho PostgreSQL.
- **Mô hình hóa:** Áp dụng mô hình **Star Schema** bằng cách tạo các bảng chiều (Dimension Tables):
  1.  **`dim_movies`**: Chứa thông tin chi tiết về phim/chương trình.
  2.  **`dim_genres`**: Chứa danh sách các thể loại **duy nhất** (`genre_name`) và ID của chúng (`genre_id`).

### 3. 💾 Tải Dữ liệu (L - Load)

- **Đích đến:** Cơ sở dữ liệu **PostgreSQL**.
- **Nhiệm vụ:** Thiết lập kết nối cơ sở dữ liệu và tải các DataFrames đã chuyển đổi (`dim_movies`, `dim_genres`) vào các bảng tương ứng. Ưu tiên sử dụng các phương pháp **chèn hàng loạt (bulk insertion)** như `to_sql` của Pandas hoặc các lệnh `COPY` của Psycopg2 để tối ưu hiệu suất.

## 🏗️ Yêu cầu về Tài liệu và Môi trường (README & Docker)

Ngoài mã nguồn ETL, Copilot phải hỗ trợ tạo ra các file tài liệu và cấu hình cần thiết để thiết lập môi trường dự án một cách nhanh chóng.

### 4. 📄 Tài liệu Dự án

- **Nhiệm vụ:** Tạo file **`README.md`** chi tiết để hướng dẫn người dùng thiết lập và chạy dự án.
- **Nội dung Bắt buộc trong README.md:**
  1.  **Mô tả Dự án:** Tóm tắt ngắn gọn về mục tiêu ETL.
  2.  **Yêu cầu Hệ thống:** Liệt kê các công cụ cần thiết (**Python, Pandas, Docker, Psycopg2/SQLAlchemy**).
  3.  **Hướng dẫn Khởi động Nhanh:** Các bước thực hiện từ đầu đến cuối:
      - **A. Clone Dự án:** Lệnh `git clone ...`.
      - **B. Thiết lập Môi trường Docker:** Hướng dẫn cách sử dụng `docker-compose.yml` (hoặc lệnh `docker run` tương đương) để khởi tạo container **PostgreSQL**. Cung cấp thông tin kết nối mặc định (host, port, user, password).
      - **C. Cài đặt Phụ thuộc Python:** Lệnh `pip install -r requirements.txt`.
      - **D. Chạy ETL:** Hướng dẫn người dùng chạy Jupyter Notebook chính hoặc script ETL.

### 5. 🐳 Cấu hình Cơ sở Dữ liệu Docker

- **Công nghệ:** Sử dụng **Docker** để đóng gói và chạy cơ sở dữ liệu **PostgreSQL**.
- **Nhiệm vụ:** Copilot nên gợi ý các cấu hình liên quan đến Docker, như nội dung mẫu cho file **`docker-compose.yml`** để dễ dàng tạo ra service PostgreSQL cần thiết cho bước Load (L).

---

## 💡 Thực tiễn Mã hóa Ưu tiên & Điều kiện Bắt buộc

- **TUÂN THỦ THIẾT KẾ:** **Luôn luôn phản hồi bằng tiếng Việt, tuân thủ và ưu tiên các quy tắc, cấu trúc bảng, và logic nghiệp vụ đã được định nghĩa trong file Detailed Design của dự án.**
- **Hiệu suất Pandas:** Ưu tiên **vectorization** của Pandas thay vì các vòng lặp Python thông thường.
- **Xử lý Lỗi:** Bao gồm các khối `try...except` cho các thao tác đọc tệp và kết nối cơ sở dữ liệu.
- **Tiêu chuẩn:** Tuân thủ các quy tắc mã hóa **PEP 8**.
