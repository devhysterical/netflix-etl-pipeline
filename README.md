# 🎬 Netflix ETL Pipeline

## 📋 Mô tả Dự án

Đây là một đường ống **ETL (Extract, Transform, Load)** được thiết kế để xử lý tập dữ liệu **Netflix Movies & TV Shows**. Pipeline thực hiện các nhiệm vụ:

1. **Trích xuất (Extract):** Đọc dữ liệu từ tệp CSV
2. **Chuyển đổi (Transform):** Làm sạch dữ liệu, chuẩn hóa định dạng, áp dụng Star Schema
3. **Tải (Load):** Lưu trữ dữ liệu đã cấu trúc vào PostgreSQL

Kết quả cuối cùng là một cơ sở dữ liệu được mô hình hóa tốt, phục vụ cho mục đích phân tích và báo cáo.

---

## ✨ Công nghệ & Thư viện Chính

| Công nghệ                 | Mục đích                            |
| ------------------------- | ----------------------------------- |
| **Python 3.9+**           | Ngôn ngữ lập trình chính            |
| **Pandas**                | Xử lý và chuyển đổi dữ liệu         |
| **Jupyter Notebook**      | Môi trường phát triển interactif    |
| **PostgreSQL**            | Cơ sở dữ liệu đích                  |
| **Psycopg2 / SQLAlchemy** | Kết nối và tương tác với PostgreSQL |
| **Docker**                | Đóng gói và chạy PostgreSQL         |

---

## 🛠️ Yêu cầu Hệ thống

Đảm bảo máy của bạn có cài đặt:

- **Python 3.9+** ([Tải về](https://www.python.org/downloads/))
- **pip** (Cài sẵn khi cài Python)
- **Docker & Docker Compose** ([Tải về](https://www.docker.com/products/docker-desktop))
- **Git** ([Tải về](https://git-scm.com/))

### Kiểm tra cài đặt

```bash
python --version
pip --version
docker --version
docker-compose --version
git --version
```

---

## 🚀 Hướng dẫn Khởi động Nhanh

### Bước 1: Clone Dự án

```bash
git clone https://github.com/devhysterical/netflix-etl-pipeline.git
cd netflix-etl-pipeline
```

### Bước 2: Thiết lập Môi trường ảo Python

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate
```

### Bước 3: Cài đặt Phụ thuộc Python

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình Biến Môi trường

```bash
# Tạo file .env từ template
cp .env.example .env

# Mở file .env và cập nhật thông tin nếu cần (tuỳ chọn)
# Giá trị mặc định đã được cấu hình cho Docker
```

**Thông tin kết nối mặc định (Docker):**

- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `netflix_db`
- **Username:** `netflix_user`
- **Password:** `netflix_password`

### Bước 5: Khởi động PostgreSQL với Docker

```bash
# Chạy Docker Compose để khởi tạo PostgreSQL
docker-compose up -d

# Kiểm tra trạng thái container
docker-compose ps
```

**Chú ý:** Container tên `netflix_postgres` sẽ khởi động và PostgreSQL sẽ sẵn sàng trong vòng 10-15 giây. Kiểm tra logs nếu cần:

```bash
docker-compose logs netflix_postgres
```

### Bước 6: Chạy ETL Pipeline

#### Cách A: Sử dụng Jupyter Notebook (Khuyến nghị)

```bash
# Khởi động Jupyter Lab
jupyter lab

# Hoặc Jupyter Notebook
jupyter notebook
```

Sau đó, mở file `notebooks/netflix_etl_pipeline.ipynb` trong trình duyệt web và chạy từng cell theo thứ tự.

#### Cách B: Chạy Python Script trực tiếp

```bash
python src/etl_pipeline.py
```

---

## 📁 Cấu Trúc Dự Án

```
netflix-etl-pipeline/
├── data/                      # Thư mục chứa dữ liệu CSV
│   └── netflix_titles.csv     # Tập dữ liệu Netflix
├── notebooks/                 # Jupyter Notebooks
│   └── netflix_etl_pipeline.ipynb
├── src/                       # Source code Python
│   ├── __init__.py
│   ├── extractor.py          # Module trích xuất dữ liệu
│   ├── transformer.py        # Module chuyển đổi dữ liệu
│   ├── loader.py             # Module tải dữ liệu
│   └── etl_pipeline.py       # Script ETL chính
├── config/                    # Cấu hình
│   └── config.py             # File cấu hình chính
├── docker/                    # Docker configuration
│   └── init.sql              # Script khởi tạo cơ sở dữ liệu
├── .env.example              # Template biến môi trường
├── .gitignore                # Git ignore rules
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
└── README.md                 # File này
```

---

## 📥 Bước 1: Trích xuất Dữ liệu (Extract)

**Tệp liên quan:** `src/extractor.py`

### Cách lấy dữ liệu

#### Cách 1: Tải từ Kaggle (Tự động)

Nếu bạn có tài khoản Kaggle:

```bash
# Đặt thông tin Kaggle vào .env
# KAGGLE_USERNAME=your_username
# KAGGLE_KEY=your_api_key

# Chạy extractor
python src/extractor.py
```

#### Cách 2: Tải thủ công

1. Truy cập [Kaggle Netflix Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)
2. Tải file `netflix_titles.csv`
3. Đặt file vào thư mục `data/`

Cấu trúc dữ liệu thô:

- `show_id`: ID duy nhất
- `type`: "Movie" hoặc "TV Show"
- `title`: Tên phim/chương trình
- `director`: Tên đạo diễn (có thể có NA)
- `cast`: Danh sách diễn viên
- `country`: Quốc gia sản xuất
- `date_added`: Ngày thêm vào Netflix
- `release_year`: Năm phát hành
- `rating`: Xếp hạng nội dung
- `duration`: Thời lượng (phim: phút, TV Show: mùa)
- `listed_in`: Danh sách thể loại (phân cách bằng dấu phẩy)
- `description`: Mô tả

---

## 🧹 Bước 2: Chuyển đổi Dữ liệu (Transform)

**Tệp liên quan:** `src/transformer.py`

### Quá trình chuyển đổi

#### A. Làm sạch Dữ liệu

1. **Xử lý Giá trị Thiếu (NA):**

   - Xóa các hàng có NA trong cột: `director`, `country`, `date_added`, `rating`
   - Giữ lại các hàng có NA trong cột `cast` (không bắt buộc)

2. **Phân tách Thể loại:**

   - Cột `listed_in` chứa nhiều thể loại (ví dụ: "Action, Adventure, Comedy")
   - Sử dụng `.explode()` để tách thành các hàng riêng biệt
   - Mỗi hàng sẽ chứa chỉ một thể loại duy nhất

   **Ví dụ:**

   ```
   Trước:  title="Movie A", listed_in="Action, Comedy"
   Sau:
           title="Movie A", listed_in="Action"
           title="Movie A", listed_in="Comedy"
   ```

#### B. Chuẩn hóa Dữ Liệu

1. **Chuẩn hóa Ngày tháng:**

   - Chuyển `date_added` thành định dạng Pandas datetime
   - Chuyển sang định dạng `YYYY-MM-DD` cho PostgreSQL
   - Xóa dấu khoảng trắng thừa

2. **Chuẩn hóa Văn bản:**
   - Strip khoảng trắng thừa ở đầu/cuối
   - Chuẩn hóa tên thể loại (trim whitespace)

#### C. Tạo Star Schema

Áp dụng mô hình Star Schema:

```
                    dim_movies
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   movies_genres    genre_id      movie_id
        │               │
        └───────────────┘
                │
            dim_genres
```

**Bảng Chiều 1: `dim_movies`**

- `movie_id` (PK): ID duy nhất
- `title`: Tên phim/chương trình
- `type`: "Movie" hoặc "TV Show"
- `director`: Đạo diễn
- `country`: Quốc gia
- `date_added`: Ngày thêm (YYYY-MM-DD)
- `release_year`: Năm phát hành
- `rating`: Xếp hạn
- `duration`: Thời lượng
- `description`: Mô tả

**Bảng Chiều 2: `dim_genres`**

- `genre_id` (PK): ID duy nhất
- `genre_name`: Tên thể loại (UNIQUE)

**Bảng Kết nối: `movies_genres`**

- `movie_id` (FK): Tham chiếu `dim_movies`
- `genre_id` (FK): Tham chiếu `dim_genres`
- PK: (`movie_id`, `genre_id`)

---

## 💾 Bước 3: Tải Dữ liệu (Load)

**Tệp liên quan:** `src/loader.py`

### Quá trình tải

1. **Kết nối PostgreSQL:**

   ```python
   from sqlalchemy import create_engine

   engine = create_engine(
       f"postgresql://user:password@host:port/database"
   )
   ```

2. **Tải Bảng Chiều:**

   - Tải `dim_genres` trước (khóa ngoài dependency)
   - Tải `dim_movies` sau

3. **Tải Bảng Kết nối:**
   - Tải `movies_genres` cuối cùng

### Phương pháp Tối ưu

- Sử dụng `to_sql()` của Pandas với `if_exists='append'` để chèn dữ liệu
- Hoặc sử dụng `COPY` command của Psycopg2 cho tốc độ cao hơn

### Xác thực Dữ liệu

Sau khi tải, chạy các truy vấn kiểm tra:

```sql
-- Kiểm tra số lượng bản ghi
SELECT COUNT(*) FROM dim_movies;
SELECT COUNT(*) FROM dim_genres;
SELECT COUNT(*) FROM movies_genres;

-- Kiểm tra dữ liệu mẫu
SELECT * FROM dim_movies LIMIT 5;
SELECT * FROM dim_genres LIMIT 10;
```

---

## 📊 Ví dụ Truy vấn

Sau khi tải xong, bạn có thể chạy các truy vấn phân tích:

```sql
-- Số lượng phim vs TV Shows
SELECT type, COUNT(*) as count
FROM dim_movies
GROUP BY type;

-- Top 10 thể loại phổ biến nhất
SELECT genre_name, COUNT(movie_id) as movie_count
FROM dim_genres dg
JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY genre_name
ORDER BY movie_count DESC
LIMIT 10;

-- Phim theo năm phát hành
SELECT release_year, COUNT(*) as count
FROM dim_movies
GROUP BY release_year
ORDER BY release_year DESC;

-- Phim theo xếp hạn
SELECT rating, COUNT(*) as count
FROM dim_movies
GROUP BY rating
ORDER BY count DESC;
```

---

## 🐳 Quản lý Docker

### Khởi động Services

```bash
# Khởi động background
docker-compose up -d

# Khởi động và xem logs
docker-compose up
```

### Kiểm tra Trạng thái

```bash
# Liệt kê các container đang chạy
docker-compose ps

# Xem logs của PostgreSQL
docker-compose logs netflix_postgres

# Xem logs real-time
docker-compose logs -f
```

### Kết nối trực tiếp đến PostgreSQL

```bash
# Sử dụng psql trong container
docker-compose exec postgres psql -U netflix_user -d netflix_db

# Hoặc sử dụng DBeaver, pgAdmin, v.v.
```

### Dừng Services

```bash
# Dừng nhưng giữ container
docker-compose stop

# Dừng và xóa container
docker-compose down

# Dừng và xóa tất cả volumes (Cẩn thận!)
docker-compose down -v
```

---

## 🔧 Khắc phục Sự cố

### Vấn đề: PostgreSQL không kết nối được

**Giải pháp:**

```bash
# Kiểm tra container đang chạy
docker-compose ps

# Kiểm tra logs
docker-compose logs netflix_postgres

# Khởi động lại container
docker-compose restart

# Hoặc xóa và tạo lại
docker-compose down -v
docker-compose up -d
```

### Vấn đề: Module không tìm thấy

```bash
# Đảm bảo môi trường ảo được kích hoạt
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Vấn đề: Jupyter Notebook không mở

```bash
# Cài đặt lại Jupyter
pip install --upgrade jupyter jupyterlab

# Chạy với URL cụ thể
jupyter lab --no-browser --ip=localhost --port=8888
```

---

## 📝 Ghi chú Quan trọng

1. **Dữ liệu Nhạy cảm:** File `.env` chứa thông tin mật khẩu - Không commit vào Git
2. **Volumes Docker:** Dữ liệu PostgreSQL được lưu trong volume `postgres_data` - Xóa volume sẽ mất dữ liệu
3. **Hiệu suất:** Với tập dữ liệu lớn, quá trình transform có thể mất vài phút
4. **PEP 8:** Toàn bộ mã tuân thủ tiêu chuẩn Python PEP 8

---

## 📚 Tài liệu Tham khảo

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Jupyter Documentation](https://jupyter.org/documentation)

---

## 👨‍💻 Tác giả

**GitHub:** [@devhysterical](https://github.com/devhysterical)

---

## 📄 Giấy phép

Dự án này được cấp phép dưới giấy phép MIT. Xem file `LICENSE` để biết chi tiết.

---

## 💬 Hỗ trợ

Nếu gặp vấn đề hoặc có câu hỏi, vui lòng tạo một **Issue** trên GitHub hoặc liên hệ qua email.

---

**Cập nhật lần cuối:** November 16, 2025
