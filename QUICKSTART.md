---
layout: default
title: Quick Start Guide
nav_order: 2
---

# Quick Start Guide - Netflix ETL Pipeline

## 5 Phút để Bắt đầu

### Yêu cầu

- Docker & Docker Compose
- Python 3.9+
- Git

### Các bước

#### 1️⃣ Clone và vào thư mục dự án

```bash
git clone https://github.com/devhysterical/netflix-etl-pipeline.git
cd netflix-etl-pipeline
```

#### 2️⃣ Tạo môi trường ảo

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3️⃣ Cài đặt dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Khởi động PostgreSQL

```bash
docker-compose up -d
```

Đợi 15 giây để PostgreSQL khởi động xong. Kiểm tra:

```bash
docker-compose ps
```

#### 5️⃣ Chuẩn bị dữ liệu

**Option A: Tải thủ công**

1. Tải từ [Kaggle Netflix Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)
2. Đặt `netflix_titles.csv` vào thư mục `data/`

**Option B: Tải tự động (nếu có Kaggle API)**

```bash
python src/extractor.py
```

#### 6️⃣ Chạy ETL Pipeline

**Cách A: Jupyter Notebook (Khuyến nghị)**

```bash
jupyter lab
# Mở: notebooks/netflix_etl_pipeline.ipynb
# Chạy từng cell theo thứ tự
```

**Cách B: Python Script**

```bash
python src/etl_pipeline.py
```

#### 7. Confirm success

Bạn sẽ thấy output tương tự:

```
✓ Extracted 12345 rows
✓ Data cleaning completed
✓ Date normalization completed
✓ Genre explosion completed
✓ Loading dim_genres...
✓ Loaded 25 genres
✓ Loading dim_movies...
✓ Loaded 5000 movies
```

---

## Truy vấn Dữ liệu

Sau khi hoàn thành, bạn có thể truy vấn:

### Kết nối Database

```bash
# Từ terminal
docker-compose exec postgres psql -U netflix_user -d netflix_db

# Hoặc sử dụng DBeaver, pgAdmin, etc.
# Host: localhost
# Port: 5432
# User: netflix_user
# Password: netflix_password
```

### Ví dụ Truy vấn

```sql
-- Top 10 genres
SELECT genre_name, COUNT(movie_id) as count
FROM dim_genres dg
JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY genre_name
ORDER BY count DESC
LIMIT 10;

-- Movies by year
SELECT release_year, COUNT(*) as count
FROM dim_movies
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 20;
```

---

## Khắc phục Sự cố

| Vấn đề                | Giải pháp                                     |
| --------------------- | --------------------------------------------- |
| `Connection refused`  | `docker-compose up -d`                        |
| `File not found`      | Tải dữ liệu vào `data/netflix_titles.csv`     |
| `ModuleNotFoundError` | `pip install -r requirements.txt`             |
| `Port 5432 in use`    | `docker-compose down && docker-compose up -d` |

---

## Cấu trúc Dự án

```
netflix-etl-pipeline/
├── data/                    # CSV data file
├── notebooks/               # Jupyter Notebooks
│   └── netflix_etl_pipeline.ipynb
├── src/                     # Python modules
│   ├── extractor.py        # Extract step
│   ├── transformer.py      # Transform step
│   ├── loader.py           # Load step
│   └── etl_pipeline.py     # Main script
├── config/                  # Configuration
│   └── config.py
├── docker/                  # Docker files
│   └── init.sql            # Database schema
├── docker-compose.yml       # Docker compose
├── requirements.txt         # Python dependencies
└── README.md               # Full documentation
```

---

## Thống kê Dữ liệu

Dataset Netflix chứa:

- **~5,000 Phim & TV Shows**
- **~25 Thể loại**
- **~120 Quốc gia**
- **~10 Xếp hạng nội dung**
- **Khoảng thời gian: 1920-2021**

---

## Đọc Thêm

- [Full README](README.md) - Tài liệu chi tiết
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Docs](https://docs.docker.com/)

---

**Bạn đã sẵn sàng! Hãy bắt đầu khám phá dữ liệu Netflix! 🎬**
