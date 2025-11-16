-- Create Dimension Tables for Star Schema

-- Bảng chiều: dim_genres
CREATE TABLE IF NOT EXISTS dim_genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL UNIQUE
);

-- Bảng chiều: dim_movies
CREATE TABLE IF NOT EXISTS dim_movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    director VARCHAR(500),
    country VARCHAR(500),
    date_added DATE,
    release_year INTEGER,
    rating VARCHAR(20),
    duration VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng kết nối: movies_genres (Many-to-Many)
CREATE TABLE IF NOT EXISTS movies_genres (
    movie_id INTEGER NOT NULL REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES dim_genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

-- Tạo index để cải thiện hiệu suất truy vấn
CREATE INDEX IF NOT EXISTS idx_movies_type ON dim_movies(type);
CREATE INDEX IF NOT EXISTS idx_movies_release_year ON dim_movies(release_year);
CREATE INDEX IF NOT EXISTS idx_movies_rating ON dim_movies(rating);
CREATE INDEX IF NOT EXISTS idx_genres_name ON dim_genres(genre_name);
