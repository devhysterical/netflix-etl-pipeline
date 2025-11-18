# Các Câu Hỏi Thường Gặp

## Cài đặt & Setup

### Q1: Tôi cần cài đặt gì trước?

**A:** Bạn cần:

- Python 3.9+
- Docker & Docker Compose
- Git
- Khoảng 2GB RAM

Kiểm tra:

```bash
python --version
docker --version
git --version
```

---

### Q2: Docker là gì? Tại sao cần Docker?

**A:** Docker là công cụ containerization. Chúng tôi dùng Docker để:

- Chạy PostgreSQL mà không cần cài đặt trực tiếp
- Đảm bảo môi trường nhất quán trên tất cả máy
- Dễ dàng khởi động/tắt database

Sử dụng:

```bash
docker-compose up -d    # Khởi động
docker-compose down     # Tắt
```

---

### Q3: Làm sao tạo virtual environment?

**A:**

```bash
# Tạo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

---

## Dữ liệu & CSV

### Q4: Tôi lấy dữ liệu ở đâu?

**A:** 2 cách:

**Cách 1: Manual (Khuyến nghị)**

1. Vào https://www.kaggle.com/datasets/shivamb/netflix-shows
2. Tải `netflix_titles.csv`
3. Đặt vào `data/` folder

**Cách 2: Kaggle CLI**

```bash
# Cần Kaggle API setup
python src/extractor.py
```

---

### Q5: File CSV có định dạng gì?

**A:** Định dạng CSV chuẩn:

- Dòng đầu: Column headers
- Các dòng tiếp: Data rows
- Phân cách bằng `,`
- Encoding: UTF-8

Columns cần có:

- show_id, type, title, director, country, date_added, release_year, rating, duration, listed_in, description

---

### Q6: Tập dữ liệu lớn bao nhiêu?

**A:**

- ~5,500 rows
- ~350 KB (CSV file)
- ~25 genres
- ~120 countries

Không quá lớn, tốc độ xử lý < 1 phút.

---

## ETL Pipeline

### Q7: ETL là gì?

**A:**

- **E**xtract: Trích xuất dữ liệu từ CSV
- **T**ransform: Làm sạch, chuẩn hóa, tách thể loại
- **L**oad: Tải vào PostgreSQL database

---

### Q8: Quy trình chuyển đổi (Transform) là gì?

**A:**

1. **Làm sạch:** Xóa NA trong cột bắt buộc
2. **Chuẩn hóa:** Chuyển ngày sang YYYY-MM-DD
3. **Tách thể loại:** Split "listed_in" thành rows riêng (explode)
4. **Star Schema:** Tạo 3 bảng (dim_movies, dim_genres, movies_genres)

---

### Q9: Star Schema là gì?

**A:** Mô hình database tối ưu cho analytics:

```
                dim_movies
                    │
         ┌──────────┼──────────┐
         │          │          │
    movie_id    title ...   genres
         │                     │
    ┌────┴─────────────────────┤
    │                          │
    └──────movies_genres────────┘
              │
           dim_genres
```

Lợi ích:

- Truy vấn nhanh
- Tránh duplicate data
- Dễ mở rộng

---

## Database & PostgreSQL

### Q10: PostgreSQL là cái gì?

**A:** PostgreSQL là một relational database management system (RDBMS):

- Open source
- Mạnh mẽ & reliable
- Hỗ trợ advanced features
- Miễn phí

---

### Q11: Thông tin kết nối mặc định là gì?

**A:**

```
Host: localhost
Port: 5432
Database: netflix_db
Username: netflix_user
Password: netflix_password
```

Trong docker-compose.yml, các giá trị này có thể thay đổi.

---

### Q12: Làm cách nào kết nối trực tiếp vào database?

**A:**

```bash
# Cách 1: psql trong container
docker-compose exec postgres psql -U netflix_user -d netflix_db

# Cách 2: Sử dụng GUI tools
# DBeaver, pgAdmin, DataGrip, v.v.
# Host: localhost, Port: 5432
```

---

### Q13: Làm cách nào xem dữ liệu đã tải?

**A:**

```sql
-- Đếm hàng
SELECT COUNT(*) FROM dim_movies;
SELECT COUNT(*) FROM dim_genres;
SELECT COUNT(*) FROM movies_genres;

-- Xem sample
SELECT * FROM dim_movies LIMIT 10;
SELECT * FROM dim_genres LIMIT 20;

-- Truy vấn phức tạp
SELECT dg.genre_name, COUNT(mg.movie_id) as count
FROM dim_genres dg
LEFT JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY dg.genre_id, dg.genre_name
ORDER BY count DESC;
```

---

## Jupyter Notebook

### Q14: Jupyter Notebook là gì?

**A:** Jupyter Notebook là:

- Interactive development environment
- Giống như shell nhưng với features của IDE
- Mix code, output, và documentation
- Perfect cho data exploration & analysis

---

### Q15: Làm cách nào chạy Jupyter?

**A:**

```bash
# Khởi động Jupyter Lab (recommended)
jupyter lab

# Hoặc Jupyter Notebook
jupyter notebook

# Sẽ mở browser ở http://localhost:8888
```

---

### Q16: Làm cách nào chạy từng cell trong notebook?

**A:**

- Click vào cell
- Nhấn `Shift + Enter` hoặc click "Run" button
- Hoặc `Ctrl + Enter` để chạy mà không move xuống
- `Kernel > Restart Kernel` để reset state

---

## Troubleshooting

### Q17: "Connection refused" - PostgreSQL không kết nối được?

**A:**

```bash
# Kiểm tra container
docker-compose ps

# Khởi động lại
docker-compose restart

# Hoặc xóa và tạo lại
docker-compose down
docker-compose up -d

# Đợi 15 giây cho PostgreSQL khởi động
sleep 15
```

---

### Q18: "File not found" - CSV không tìm thấy?

**A:**

1. Kiểm tra tệp có ở `data/netflix_titles.csv` không
2. Tên file phải đúng chính xác (case-sensitive trên Linux)
3. Tải lại từ Kaggle nếu cần

```bash
# Kiểm tra
ls -la data/
```

---

### Q19: "ModuleNotFoundError" - Module không tìm thấy?

**A:**

```bash
# Kiểm tra virtual environment được activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Cài lại requirements
pip install -r requirements.txt

# Hoặc upgrade pip
pip install --upgrade pip
```

---

### Q20: Port 5432 đang được sử dụng?

**A:**

```bash
# Tìm process chiếm port
# Windows
netstat -ano | findstr :5432

# macOS/Linux
lsof -i :5432

# Hoặc xóa container Docker cũ
docker-compose down
docker system prune -a
docker-compose up -d
```

---

## Mở rộng & Học tập

### Q21: Tôi có thể sửa đổi quy trình Transform không?

**A:** Có! Sửa `src/transformer.py`:

1. Thêm validation rules mới
2. Thay đổi cách tách thể loại
3. Thêm cột mới
4. v.v.

Ví dụ:

```python
def custom_transformation(self):
    # Your custom logic here
    self.df['new_column'] = self.df['existing'].apply(custom_func)
```

---

### Q22: Tôi có thể thêm các bảng khác không?

**A:** Có! Các bước:

1. Thêm SQL vào `docker/init.sql` để tạo bảng
2. Tạo hàm load trong `src/loader.py`
3. Gọi hàm trong `load_all()` method

---

### Q23: Làm cách nào để học thêm?

**A:** Tài liệu:

- Pandas: https://pandas.pydata.org/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Docker: https://docs.docker.com/
- Jupyter: https://jupyter.org/documentation/

---

### Q24: Tôi có thể đóng góp vào dự án không?

**A:** Có! Xem `CONTRIBUTING.md`:

1. Fork dự án
2. Tạo feature branch
3. Commit & push
4. Create Pull Request

---

## Tips & Tricks

### Q25: Làm cách nào tối ưu hiệu suất?

**A:**

```python
# Sử dụng vectorization thay vì loop
# Bad:
for idx, row in df.iterrows():
    df.at[idx, 'col'] = process(row['value'])

# Good:
df['col'] = df['value'].apply(process)
```

---

### Q26: Làm cách nào debug một cell trong notebook?

**A:**

```python
# Thêm print statements
print("Current state:")
print(df.head())
print(df.info())

# Hoặc sử dụng Python debugger
import pdb
pdb.set_trace()  # Sẽ pause tại đây
```

---

### Q27: Làm cách nào lưu DataFrame thành CSV?

**A:**

```python
df.to_csv('output.csv', index=False)
```

---

### Q28: Làm cách nào reset database?

**A:**

```bash
# Xóa tất cả data (giữ schema)
docker-compose exec postgres psql -U netflix_user -d netflix_db -c "TRUNCATE TABLE movies_genres CASCADE;"

# Hoặc xóa toàn bộ database
docker-compose down -v
docker-compose up -d
```

---

## Cần Giúp?

### Q29: Tôi gặp lỗi không được liệt kê ở đây?

**A:**

1. Kiểm tra error message carefully
2. Google error message
3. Tạo Issue trên GitHub: https://github.com/devhysterical/netflix-etl-pipeline/issues
4. Cung cấp:
   - Error message đầy đủ
   - OS & versions
   - Steps to reproduce

---

### Q30: Làm cách nào liên hệ với developer?

**A:**

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- GitHub: @devhysterical

---

## Tóm tắt

**Nếu bạn nhớ 5 thứ này:**

1. Extract CSV → Pandas DataFrame
2. Transform → Làm sạch, chuẩn hóa, tách
3. Load → Vào PostgreSQL
4. Verify → Query & validate
5. Learn → Documentation & examples

**Bạn sẽ thành công!**

---

**Last Updated:** November 16, 2025  
**For more help:** Check README.md or CONTRIBUTING.md
