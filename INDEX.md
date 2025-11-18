# Netflix ETL Pipeline - Documentation Index

Chào mừng đến với Netflix ETL Pipeline! Đây là chỉ mục tài liệu để giúp bạn tìm thấy những gì bạn cần.

---

## Bắt Đầu Nhanh Chóng

**Nếu bạn chỉ có 5 phút:**
→ Đọc [QUICKSTART.md](QUICKSTART.md)

**Nếu bạn có 15 phút:**
→ Đọc [README.md](README.md) (Bỏ qua phần Troubleshooting nếu bạn cấp tốc)

**Nếu bạn có 30 phút:**
→ Đọc toàn bộ [README.md](README.md)

---

## Tài Liệu Chi Tiết

### Giới thiệu & Tổng Quan

| Tài liệu                                   | Mục đích                        | Độ dài  |
| ------------------------------------------ | ------------------------------- | ------- |
| [README.md](README.md)                     | Tài liệu chính với mô tả đầy đủ | 10 phút |
| [QUICKSTART.md](QUICKSTART.md)             | Khởi động nhanh (5 bước)        | 5 phút  |
| [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) | Tóm tắt toàn bộ dự án           | 5 phút  |

### Kiến Trúc & Thiết Kế

| Tài liệu                                 | Mục đích                    | Độ dài  |
| ---------------------------------------- | --------------------------- | ------- |
| [ARCHITECTURE.md](ARCHITECTURE.md)       | Chi tiết kiến trúc hệ thống | 15 phút |
| [docker-compose.yml](docker-compose.yml) | Cấu hình Docker             | 2 phút  |
| [docker/init.sql](docker/init.sql)       | Schema cơ sở dữ liệu        | 2 phút  |

### Hướng Dẫn Sử Dụng

| Tài liệu                             | Mục đích                    | Độ dài  |
| ------------------------------------ | --------------------------- | ------- |
| [FAQ.md](FAQ.md)                     | Câu hỏi thường gặp (30 Q&A) | 10 phút |
| [SQL_EXAMPLES.sql](SQL_EXAMPLES.sql) | 100+ ví dụ SQL queries      | 10 phút |

### Phát Triển & Đóng Góp

| Tài liệu                           | Mục đích            | Độ dài |
| ---------------------------------- | ------------------- | ------ |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Hướng dẫn đóng góp  | 5 phút |
| [Makefile](Makefile)               | Automation commands | 2 phút |

---

## Theo Mục Đích Sử Dụng

### Tôi muốn Khởi động Dự án

1. Đọc: [QUICKSTART.md](QUICKSTART.md)
2. Chạy các lệnh

### Tôi muốn Hiểu Cách Hoạt động

1. Đọc: [README.md](README.md) - Section "🛠️ Các Bước & Yêu cầu Cụ thể"
2. Đọc: [ARCHITECTURE.md](ARCHITECTURE.md)

### Tôi muốn Xem Ví dụ Code

1. Mở: `src/extractor.py`, `src/transformer.py`, `src/loader.py`
2. Xem: `notebooks/netflix_etl_pipeline.ipynb`
3. Chạy Jupyter: `jupyter lab`

### Tôi muốn Truy vấn Dữ liệu

1. Đọc: [SQL_EXAMPLES.sql](SQL_EXAMPLES.sql)
2. Copy-paste vào psql hoặc DBeaver
3. Chỉnh sửa theo nhu cầu

### Tôi muốn Tìm Câu trả lời

1. Kiểm tra: [FAQ.md](FAQ.md)
2. Nếu không tìm thấy → Tạo GitHub Issue

### Tôi muốn Đóng góp

1. Đọc: [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork & create PR

---

## Cấu Trúc Thư mục

```
netflix-etl-pipeline/
│
├── TÀI LIỆU
│   ├── README.md              ← Chính (5 phút)
│   ├── QUICKSTART.md          ← Nhanh (5 phút)
│   ├── ARCHITECTURE.md        ← Kiến trúc (15 phút)
│   ├── CONTRIBUTING.md        ← Phát triển
│   ├── FAQ.md                 ← Q&A
│   ├── SQL_EXAMPLES.sql       ← Queries
│   ├── PROJECT_SUMMARY.txt    ← Tóm tắt
│   └── INDEX.md               ← File này
│
├── SOURCE CODE
│   ├── src/
│   │   ├── extractor.py       ← Extract step
│   │   ├── transformer.py     ← Transform step
│   │   ├── loader.py          ← Load step
│   │   └── etl_pipeline.py    ← Main script
│   │
│   ├── config/
│   │   └── config.py          ← Configuration
│   │
│   └── notebooks/
│       └── netflix_etl_pipeline.ipynb ← Main notebook
│
├── DOCKER
│   ├── docker-compose.yml     ← Docker config
│   └── docker/
│       └── init.sql           ← DB schema
│
├── CONFIGURATION
│   ├── requirements.txt       ← Dependencies
│   ├── .env.example           ← Environment template
│   ├── .gitignore             ← Git rules
│   ├── Makefile               ← Automation
│   └── LICENSE                ← MIT License
│
├── DEVELOPMENT
│   └── .vscode/
│       ├── settings.json
│       └── extensions.json
│
└── DATA
    └── data/
        └── netflix_titles.csv ← Dataset (add here)
```

---

## Tìm Kiếm Nhanh

### Bạn cần...

**Cài đặt & Setup**

- [QUICKSTART.md](QUICKSTART.md) - Các bước khởi động

**Hiểu ETL là gì**

- [README.md](README.md) - Section "🛠️ Các Bước"
- [ARCHITECTURE.md](ARCHITECTURE.md) - Section "ETL Processing Layer"

**Chạy Code**

- [notebooks/netflix_etl_pipeline.ipynb](notebooks/netflix_etl_pipeline.ipynb)
- `python src/etl_pipeline.py`
- `make run`

**Sửa/Tuỳ chỉnh Code**

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [src/transformer.py](src/transformer.py)

**Truy vấn Database**

- [SQL_EXAMPLES.sql](SQL_EXAMPLES.sql) - 100+ ví dụ
- Sử dụng DBeaver, pgAdmin, hoặc psql

**Docker**

- [docker-compose.yml](docker-compose.yml) - Config
- [README.md](README.md) - Section "Quản lý Docker"

**Khắc phục Lỗi**

- [README.md](README.md) - Section "Khắc phục Sự cố"
- [FAQ.md](FAQ.md) - Section "Troubleshooting"

**Database Schema**

- [ARCHITECTURE.md](ARCHITECTURE.md) - Section "Database Layer"
- [docker/init.sql](docker/init.sql) - SQL definitions

---

## Đọc Theo Thứ Tự

### Cho Người Bắt Đầu

1. [QUICKSTART.md](QUICKSTART.md) - Get started
2. [README.md](README.md) - Understand project
3. [FAQ.md](FAQ.md) - Answer questions
4. Run notebook - Hands-on experience

### Cho Developers

1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. [src/](src/) - Review code
3. [CONTRIBUTING.md](CONTRIBUTING.md) - Contribute
4. [SQL_EXAMPLES.sql](SQL_EXAMPLES.sql) - Queries

### Cho Data Analysts

1. [SQL_EXAMPLES.sql](SQL_EXAMPLES.sql) - Query examples
2. [README.md](README.md) - Section "Ví dụ Truy vấn"
3. Setup database → Run queries

---

## Quick Commands

```bash
# Setup (5 minutes)
git clone https://github.com/devhysterical/netflix-etl-pipeline.git
cd netflix-etl-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d

# Run ETL
python src/etl_pipeline.py

# Or Jupyter (interactive)
jupyter lab

# Check database
docker-compose exec postgres psql -U netflix_user -d netflix_db -c "SELECT COUNT(*) FROM dim_movies;"

# Stop everything
docker-compose down
```

---

## Cần Giúp?

1. **Kiểm tra FAQ.md** - Có thể câu hỏi của bạn đã được trả lời
2. **Kiểm tra README.md Troubleshooting** - Giải pháp chung
3. **Tạo GitHub Issue** - Báo cáo bug hoặc đặt câu hỏi
4. **Tạo Discussion** - Thảo luận ideas

---

## Thống Kê Tài liệu

| Tài liệu         | Dòng | Độ dài  |
| ---------------- | ---- | ------- |
| README.md        | 600+ | 15 phút |
| ARCHITECTURE.md  | 500+ | 15 phút |
| FAQ.md           | 400+ | 10 phút |
| SQL_EXAMPLES.sql | 300+ | 10 phút |
| QUICKSTART.md    | 200+ | 5 phút  |
| CONTRIBUTING.md  | 250+ | 8 phút  |

**Total Documentation:** 2000+ lines, 1 hour read time

---

## Checklist Khởi Động

- [ ] Clone dự án: `git clone ...`
- [ ] Đọc QUICKSTART.md
- [ ] Tạo venv: `python -m venv venv`
- [ ] Cài dependencies: `pip install -r requirements.txt`
- [ ] Khởi động Docker: `docker-compose up -d`
- [ ] Tải CSV: `data/netflix_titles.csv`
- [ ] Chạy ETL: `python src/etl_pipeline.py`
- [ ] Xác nhận thành công

---

## Learning Path

```
START
  ↓
QUICKSTART.md (5 min)
  ↓
README.md (15 min)
  ↓
Jupyter Notebook (20 min)
  ↓
SQL_EXAMPLES.sql (10 min)
  ↓
ARCHITECTURE.md (15 min)
  ↓
CONTRIBUTING.md (5 min)
  ↓
MASTERY! 🎉
```

---

## Tài Liệu Bổ Sung

Sắp có thêm:

- [ ] Video tutorial
- [ ] API documentation
- [ ] Performance tuning guide
- [ ] Advanced analytics recipes
- [ ] Deployment guide (AWS/GCP)

---

## Liên Kết Hữu ích

### Official Documentation

- [Pandas](https://pandas.pydata.org/docs/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Docker](https://docs.docker.com/)
- [Jupyter](https://jupyter.org/documentation/)

### Dataset

- [Kaggle: Netflix Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

### Repository

- [GitHub: netflix-etl-pipeline](https://github.com/devhysterical/netflix-etl-pipeline)

---

## Version & Updates

**Current Version:** 1.0.0  
**Last Updated:** November 16, 2025  
**License:** MIT  
**Author:** devhysterical

---

## Tips

- Use `Ctrl+F` (Cmd+F) to search in documentation
- Open documentation in VS Code for better formatting
- Pin frequently used docs in your browser
- Keep SQL_EXAMPLES.sql open while querying
- Read ARCHITECTURE.md for deep understanding

---

**Ready to start? → Go to [QUICKSTART.md](QUICKSTART.md)**
