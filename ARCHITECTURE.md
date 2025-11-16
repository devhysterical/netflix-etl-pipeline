# 🏗️ Netflix ETL Pipeline - Architecture Documentation

## Tổng Quan Kiến Trúc

Netflix ETL Pipeline được thiết kế theo mô hình **3-layer architecture**:

```
┌─────────────────────────────────────────────────────┐
│              DATA PRESENTATION LAYER                 │
│  (Jupyter Notebooks, SQL Queries, Analytics Tools)  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              DATABASE LAYER                          │
│  PostgreSQL (dim_movies, dim_genres, movies_genres) │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              ETL PROCESSING LAYER                    │
│  (Extract → Transform → Load Pipeline)              │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              DATA SOURCE LAYER                       │
│  (CSV File / Kaggle Dataset)                        │
└─────────────────────────────────────────────────────┘
```

---

## 1. Data Source Layer

### Chức năng

Quản lý dữ liệu thô từ các nguồn:

```
Input Sources:
├── 📄 netflix_titles.csv (Kaggle Dataset)
│   ├── 5,500+ rows
│   ├── 12 columns
│   └── ~350 KB size
└── 🌐 Kaggle API (optional download)
```

### Định dạng Dữ liệu Thô

| Column       | Type   | Description                  |
| ------------ | ------ | ---------------------------- |
| show_id      | string | Unique identifier            |
| type         | string | "Movie" or "TV Show"         |
| title        | string | Title                        |
| director     | string | Director(s) - may have NA    |
| cast         | string | Cast list                    |
| country      | string | Country (may have NA)        |
| date_added   | string | Date added - may have NA     |
| release_year | int    | Year                         |
| rating       | string | Content rating - may have NA |
| duration     | string | Duration                     |
| listed_in    | string | **Genres (comma-separated)** |
| description  | string | Description                  |

### Module

**File:** `src/extractor.py`

**Lớp:** `NetflixExtractor`

- `extract_from_csv()` - Đọc CSV
- `extract_from_kaggle()` - Download từ Kaggle API
- `validate_data()` - Kiểm tra validity
- `get_data_info()` - In thông tin

---

## 2. ETL Processing Layer

### 2.1 Extract Phase

```
CSV File
    ↓
[Read with Pandas]
    ↓
Raw DataFrame
    ↓
[Validate Schema]
    ↓
✓ Ready for Transform
```

**Input:** `netflix_titles.csv` (5,500 rows × 12 columns)
**Output:** Pandas DataFrame (raw data)
**Validation:** Check required columns exist

---

### 2.2 Transform Phase

Gồm 4 bước chính:

#### 2.2.1 Data Cleaning

```
Raw Data (5,500 rows)
    ↓
[Drop NA in: director, country, date_added, rating]
    ↓
[Drop duplicates]
    ↓
Cleaned Data (~4,800 rows)
```

**Xóa:**

- Rows với NA trong `director`
- Rows với NA trong `country`
- Rows với NA trong `date_added`
- Rows với NA trong `rating`
- Duplicate rows

**Kết quả:** Giảm 10-12% rows, tăng data quality

---

#### 2.2.2 Text Normalization

```
"  director1, director2  "
    ↓
[Strip whitespace]
    ↓
"director1, director2"
```

**Applied to:**

- director
- country
- listed_in (genres)
- title

---

#### 2.2.3 Date Normalization

```
"January 1, 2021"
    ↓
[Parse to datetime]
    ↓
2021-01-01
    ↓
[Format as YYYY-MM-DD]
    ↓
"2021-01-01"
```

**Transform:** date_added column → Standard format

---

#### 2.2.4 Genre Explosion (Explode)

**Trước:**

```
show_id: 1, title: "Movie A", listed_in: "Action, Comedy, Drama"
```

**Sau (.explode()):**

```
show_id: 1, title: "Movie A", listed_in: "Action"
show_id: 1, title: "Movie A", listed_in: "Comedy"
show_id: 1, title: "Movie A", listed_in: "Drama"
```

**Tác dụng:**

- Tạo mối quan hệ 1:N
- Chuẩn bị cho Star Schema
- Mỗi row = 1 movie-genre pair

**Module:** `src/transformer.py`

**Lớp:** `NetflixTransformer`

```python
def clean_data()           # Xóa NA & duplicates
def normalize_dates()      # Chuẩn hóa ngày
def normalize_text()       # Strip whitespace
def explode_genres()       # Tách genres
def create_star_schema()   # Tạo 3 bảng
def transform()            # Chạy tất cả
```

---

### 2.3 Star Schema Creation

Chuyển từ flat structure → normalized relational model

#### 2.3.1 Dimension Table: dim_movies

```sql
CREATE TABLE dim_movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    type VARCHAR(50),
    director VARCHAR(500),
    country VARCHAR(500),
    date_added DATE,
    release_year INTEGER,
    rating VARCHAR(20),
    duration VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP
);
```

**Đặc điểm:**

- Primary key: `movie_id` (auto-increment)
- 1 row per unique show_id
- Không có duplicate titles (unique show_id)
- Chứa tất cả thông tin phim

**Rows:** ~4,800 (duy nhất)

---

#### 2.3.2 Dimension Table: dim_genres

```sql
CREATE TABLE dim_genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) UNIQUE
);
```

**Đặc điểm:**

- Primary key: `genre_id`
- Constraint: `UNIQUE` trên `genre_name`
- Loại bỏ duplicate genres
- Danh sách tham chiếu

**Rows:** ~25 (duy nhất genres)

**Example:**

```
1 | Action & Adventure
2 | Anime
3 | Children & Family
...
25 | Stand-Up Comedy
```

---

#### 2.3.3 Junction Table: movies_genres

```sql
CREATE TABLE movies_genres (
    movie_id INTEGER (FK -> dim_movies),
    genre_id INTEGER (FK -> dim_genres),
    PRIMARY KEY (movie_id, genre_id)
);
```

**Đặc điểm:**

- Composite Primary Key: (movie_id, genre_id)
- Foreign Key: movie_id → dim_movies
- Foreign Key: genre_id → dim_genres
- Mối quan hệ N:N

**Rows:** ~10,000+ (mối quan hệ)

**Example:**

```
movie_id | genre_id
---------|----------
1        | 1  (Movie 1 is Action)
1        | 5  (Movie 1 is Comedy)
2        | 1  (Movie 2 is Action)
...
```

---

### 2.4 Schema Diagram

```
                    ┌──────────────────┐
                    │   dim_genres     │
                    ├──────────────────┤
                    │ genre_id (PK)    │
                    │ genre_name (U)   │
                    └────────┬─────────┘
                             │
                             │ FK
                             │
                    ┌────────▼──────────┐
                    │ movies_genres    │
                    ├──────────────────┤
                    │ movie_id (FK)    │◄────┐
                    │ genre_id (FK)    │     │
                    │ PK: (m_id,g_id)  │     │
                    └──────────────────┘     │ FK
                                             │
                    ┌──────────────────┐     │
                    │   dim_movies     │     │
                    ├──────────────────┤     │
                    │ movie_id (PK)───┼─────┘
                    │ title            │
                    │ type             │
                    │ director         │
                    │ country          │
                    │ date_added       │
                    │ release_year     │
                    │ rating           │
                    │ duration         │
                    │ description      │
                    └──────────────────┘
```

---

### 2.5 Load Phase

```
Transformed Data
  (3 DataFrames)
    ↓
[Create Connection]
    ↓
[Load dim_genres] ← phải load trước (FK dependency)
    ↓
[Load dim_movies]
    ↓
[Load movies_genres]
    ↓
[Validate Load]
    ↓
✓ Data in Database
```

**Module:** `src/loader.py`

**Lớp:** `NetflixLoader`

```python
def connect()              # Kết nối PostgreSQL
def load_dim_genres()      # Tải genres
def load_dim_movies()      # Tải movies
def load_movies_genres()   # Tải relationships
def load_all()             # Tải tất cả 3 bảng
def validate_load()        # Kiểm tra dữ liệu
def disconnect()           # Đóng kết nối
```

**Methods để tối ưu:**

- `to_sql()` với Pandas - Chuẩn và dễ dùng
- `COPY` command - Nhanh hơn (bulk insert)
- Truncate cũ → Append mới (idempotent)

---

## 3. Database Layer

### 3.1 PostgreSQL Container

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: netflix_db
      POSTGRES_USER: netflix_user
      POSTGRES_PASSWORD: netflix_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql
```

**Tính năng:**

- Alpine image (nhỏ, nhanh)
- Auto-init schema từ `init.sql`
- Persistent volume
- Health check

---

### 3.2 Indexing Strategy

```sql
-- Improve query performance
CREATE INDEX idx_movies_type ON dim_movies(type);
CREATE INDEX idx_movies_release_year ON dim_movies(release_year);
CREATE INDEX idx_movies_rating ON dim_movies(rating);
CREATE INDEX idx_genres_name ON dim_genres(genre_name);
```

**Tác dụng:**

- Tăng tốc độ WHERE queries
- Giảm full table scan
- Trade-off: Insert/update chậm hơn

---

### 3.3 Connection Management

```python
# SQLAlchemy Connection String
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Create engine
engine = create_engine(DATABASE_URL)

# Use connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM dim_movies"))
```

**Lợi ích:**

- Connection pooling
- Automatic cleanup
- Error handling

---

## 4. Data Presentation Layer

### 4.1 Jupyter Notebook Interface

```
notebooks/netflix_etl_pipeline.ipynb
│
├── 📌 Setup & Imports
│   ├── Import libraries
│   ├── Set Python path
│   └── Load modules
│
├── 📥 EXTRACT
│   ├── Initialize Extractor
│   ├── Read CSV
│   ├── Display info
│   └── Validate data
│
├── 🧹 TRANSFORM
│   ├── Initialize Transformer
│   ├── Run transformation
│   ├── Create Star Schema
│   └── Quality checks
│
├── 💾 LOAD
│   ├── Connect to DB
│   ├── Load 3 tables
│   ├── Validate load
│   └── Disconnect
│
└── 📊 ANALYSIS
    ├── Movies vs TV Shows
    ├── Top genres
    ├── Release year trends
    ├── Rating distribution
    └── Country analysis
```

**Advantages:**

- Interactive development
- Step-by-step execution
- Built-in visualization
- Documentation + code combined

---

### 4.2 SQL Queries

```sql
-- Analytics layer
SELECT dg.genre_name, COUNT(*) as count
FROM dim_genres dg
JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY dg.genre_id, dg.genre_name
ORDER BY count DESC;
```

**Use cases:**

- Ad-hoc analysis
- Report generation
- Data exploration
- BI tool integration

---

## 5. Configuration Management

### 5.1 Environment Variables

```python
# config/config.py
class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "netflix_db")
    DB_USER = os.getenv("DB_USER", "netflix_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "netflix_password")

    DATA_PATH = os.getenv("DATA_PATH", "./data/netflix_titles.csv")

    DATABASE_URL = f"postgresql://..."
```

**Benefits:**

- Externalize configuration
- Environment-specific settings
- Secrets management
- Easy to modify without code change

---

## 6. Error Handling & Validation

### 6.1 Extraction Errors

```python
try:
    df = extractor.extract_from_csv()
except FileNotFoundError:
    # Handle missing file
    print("CSV file not found, try Kaggle API")
except Exception as e:
    print(f"Error reading CSV: {str(e)}")
```

---

### 6.2 Transformation Errors

```python
# Validate data after cleaning
if df[critical_cols].isnull().any():
    raise ValueError("Critical columns have NULL values")
```

---

### 6.3 Load Errors

```python
try:
    loader.connect()
except ConnectionError:
    print("Cannot connect to PostgreSQL")
    print("Ensure Docker container is running: docker-compose up -d")
```

---

## 7. Performance Optimization

### 7.1 Data Processing

| Operation         | Optimization                                   |
| ----------------- | ---------------------------------------------- |
| Read CSV          | Use `chunksize` untuk file besar               |
| String operations | Gunakan `.str.` methods (vectorized)           |
| Filtering         | Hindari `iterrows()`, gunakan boolean indexing |
| Groupby           | Optimize group size                            |

### 7.2 Database

| Optimization        | Impact                |
| ------------------- | --------------------- |
| Indexes             | ~10x faster SELECT    |
| Bulk insert         | ~5x faster INSERT     |
| Connection pooling  | Mengurangi overhead   |
| Prepared statements | Prevent SQL injection |

---

## 8. Scalability Considerations

### 8.1 Untuk Dataset Besar

1. **Chunked Processing**

   ```python
   # Read large CSV in chunks
   for chunk in pd.read_csv('file.csv', chunksize=10000):
       process_chunk(chunk)
   ```

2. **Distributed Processing**

   - Spark untuk parallel processing
   - Dask untuk out-of-core computation

3. **Incremental Loading**
   - Load only new data
   - Append vs replace

### 8.2 Untuk Many Users

1. **Connection Pooling**

   - Manage connection limits

2. **Caching**

   - Cache frequently accessed data
   - Redis untuk hot data

3. **Read Replicas**
   - Separate read/write databases

---

## 9. Monitoring & Maintenance

### 9.1 Health Checks

```bash
# Check database
docker-compose exec postgres psql -U netflix_user -d netflix_db -c "SELECT COUNT(*) FROM dim_movies;"

# Check application
python src/etl_pipeline.py --validate
```

### 9.2 Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing started")
logger.error("Error occurred", exc_info=True)
```

---

## 10. Security Best Practices

1. **Secrets Management**

   - Use `.env` file (not committed)
   - Use environment variables
   - Never hardcode passwords

2. **SQL Injection Prevention**

   - Use parameterized queries
   - SQLAlchemy prevents this automatically

3. **Access Control**
   - PostgreSQL user roles
   - Database-level permissions
   - Row-level security (if needed)

---

## Workflow Diagram

```
USER/Analyst
      ↓
  Jupyter Notebook
      ↓
  ┌─────────────────┐
  │  ETL PIPELINE   │
  ├─────────────────┤
  │  Extract        │
  │  ↓              │
  │  Transform      │
  │  ↓              │
  │  Load           │
  └────────┬────────┘
           ↓
    PostgreSQL DB
    (docker-compose)
           ↓
  SQL Queries / Reports
```

---

## Summary

**Architecture Highlights:**
✓ Modular design (Extract/Transform/Load)
✓ Star Schema for analytics
✓ Docker for easy deployment
✓ Pandas for data manipulation
✓ PostgreSQL for storage
✓ Jupyter for exploration
✓ Configuration management
✓ Error handling throughout

**Technology Stack:**

- Python 3.9+ (ETL logic)
- Pandas 2.1 (Data manipulation)
- PostgreSQL 15 (Database)
- Docker (Containerization)
- Jupyter (Interactive notebooks)
- SQLAlchemy (ORM)

---

**Last Updated:** November 16, 2025  
**For questions:** See README.md or FAQ.md
