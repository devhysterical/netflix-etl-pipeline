-- ============================================================================
-- NETFLIX ETL PIPELINE - SQL QUERY EXAMPLES
-- ============================================================================
-- Các ví dụ truy vấn hữu ích sau khi tải dữ liệu vào PostgreSQL

-- Connection: localhost:5432 | netflix_db | netflix_user:netflix_password
-- ============================================================================


-- ============================================================================
-- 1. BASIC STATISTICS
-- ============================================================================

-- 1.1 Đếm tổng số movies và TV shows
SELECT type, COUNT(*) as count
FROM dim_movies
GROUP BY type
ORDER BY count DESC;

-- Output: Movies, TV Show


-- 1.2 Đếm tổng số genres
SELECT COUNT(*) as total_genres
FROM dim_genres;

-- Output: ~25


-- 1.3 Đếm tổng relationships
SELECT COUNT(*) as total_relationships
FROM movies_genres;

-- Output: ~10,000+


-- ============================================================================
-- 2. GENRE ANALYSIS
-- ============================================================================

-- 2.1 Top 15 genres by frequency
SELECT 
    dg.genre_id,
    dg.genre_name,
    COUNT(mg.movie_id) as movie_count
FROM dim_genres dg
LEFT JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY dg.genre_id, dg.genre_name
ORDER BY movie_count DESC
LIMIT 15;

-- Output: International Movies, Dramas, Comedies...


-- 2.2 Genres with only 1 movie (rare genres)
SELECT 
    dg.genre_id,
    dg.genre_name,
    COUNT(mg.movie_id) as movie_count
FROM dim_genres dg
LEFT JOIN movies_genres mg ON dg.genre_id = mg.genre_id
GROUP BY dg.genre_id, dg.genre_name
HAVING COUNT(mg.movie_id) = 1
ORDER BY dg.genre_name;


-- 2.3 Movies in specific genre (e.g., Action)
SELECT 
    dm.movie_id,
    dm.title,
    dm.type,
    dm.release_year
FROM dim_movies dm
JOIN movies_genres mg ON dm.movie_id = mg.movie_id
JOIN dim_genres dg ON mg.genre_id = dg.genre_id
WHERE dg.genre_name = 'Action & Adventure'
ORDER BY dm.release_year DESC
LIMIT 20;


-- ============================================================================
-- 3. RELEASE YEAR ANALYSIS
-- ============================================================================

-- 3.1 Movies by release year (top 20)
SELECT 
    release_year,
    COUNT(*) as count
FROM dim_movies
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 20;


-- 3.2 Trend: Movies added per year (last 10 years)
SELECT 
    EXTRACT(YEAR FROM TO_DATE(date_added, 'YYYY-MM-DD'))::INT as year_added,
    COUNT(*) as count
FROM dim_movies
WHERE date_added IS NOT NULL
GROUP BY EXTRACT(YEAR FROM TO_DATE(date_added, 'YYYY-MM-DD'))
ORDER BY year_added DESC
LIMIT 10;


-- 3.3 Movies vs TV Shows by release year
SELECT 
    release_year,
    type,
    COUNT(*) as count
FROM dim_movies
GROUP BY release_year, type
ORDER BY release_year DESC
LIMIT 20;


-- ============================================================================
-- 4. RATING ANALYSIS
-- ============================================================================

-- 4.1 Content distribution by rating
SELECT 
    rating,
    COUNT(*) as count,
    ROUND(COUNT(*)::NUMERIC / 
          (SELECT COUNT(*) FROM dim_movies)::NUMERIC * 100, 2) as percentage
FROM dim_movies
GROUP BY rating
ORDER BY count DESC;

-- Common ratings: PG, TV-14, TV-MA, R, PG-13


-- 4.2 TV-MA rated content (most mature)
SELECT 
    movie_id,
    title,
    type,
    release_year
FROM dim_movies
WHERE rating = 'TV-MA'
ORDER BY release_year DESC
LIMIT 20;


-- 4.3 Family-friendly content (G, PG)
SELECT 
    movie_id,
    title,
    type,
    release_year,
    rating
FROM dim_movies
WHERE rating IN ('G', 'PG')
ORDER BY release_year DESC
LIMIT 30;


-- ============================================================================
-- 5. COUNTRY ANALYSIS
-- ============================================================================

-- 5.1 Top 20 countries by movie production
SELECT 
    country,
    COUNT(*) as count
FROM dim_movies
WHERE country IS NOT NULL
GROUP BY country
ORDER BY count DESC
LIMIT 20;

-- Top: United States, India, Canada...


-- 5.2 Movies from specific country
SELECT 
    movie_id,
    title,
    type,
    release_year
FROM dim_movies
WHERE country = 'United States'
ORDER BY release_year DESC
LIMIT 20;


-- 5.3 International coproductions (multiple countries)
-- Note: Data shows one country per row after transformation
-- To find coproductions, would need to check original data


-- ============================================================================
-- 6. CONTENT ANALYSIS
-- ============================================================================

-- 6.1 Find movies by title pattern
SELECT 
    movie_id,
    title,
    type,
    release_year,
    rating
FROM dim_movies
WHERE LOWER(title) LIKE '%christmas%'
ORDER BY release_year DESC;


-- 6.2 Movies with directors (not null)
SELECT 
    movie_id,
    title,
    type,
    director,
    release_year
FROM dim_movies
WHERE director IS NOT NULL
ORDER BY release_year DESC
LIMIT 20;


-- 6.3 Recently added content (last 6 months)
SELECT 
    movie_id,
    title,
    type,
    date_added,
    release_year
FROM dim_movies
WHERE date_added IS NOT NULL
ORDER BY date_added DESC
LIMIT 30;


-- ============================================================================
-- 7. ADVANCED ANALYTICS
-- ============================================================================

-- 7.1 Average release year by movie type
SELECT 
    type,
    ROUND(AVG(release_year)::NUMERIC, 1) as avg_release_year,
    MIN(release_year) as oldest,
    MAX(release_year) as newest
FROM dim_movies
GROUP BY type;


-- 7.2 Movies with multiple genres (most versatile)
SELECT 
    dm.movie_id,
    dm.title,
    COUNT(mg.genre_id) as genre_count
FROM dim_movies dm
JOIN movies_genres mg ON dm.movie_id = mg.movie_id
GROUP BY dm.movie_id, dm.title
ORDER BY genre_count DESC
LIMIT 20;


-- 7.3 Genre diversity score
SELECT 
    dg.genre_id,
    dg.genre_name,
    COUNT(DISTINCT dm.type) as type_diversity,
    COUNT(mg.movie_id) as total_movies
FROM dim_genres dg
JOIN movies_genres mg ON dg.genre_id = mg.genre_id
JOIN dim_movies dm ON mg.movie_id = dm.movie_id
GROUP BY dg.genre_id, dg.genre_name
ORDER BY type_diversity DESC;


-- 7.4 Complete data for specific movie
SELECT 
    dm.movie_id,
    dm.title,
    dm.type,
    dm.director,
    dm.country,
    dm.release_year,
    dm.rating,
    dm.duration,
    STRING_AGG(dg.genre_name, ', ') as genres,
    dm.description
FROM dim_movies dm
LEFT JOIN movies_genres mg ON dm.movie_id = mg.movie_id
LEFT JOIN dim_genres dg ON mg.genre_id = dg.genre_id
WHERE LOWER(dm.title) LIKE '%stranger things%'
GROUP BY dm.movie_id, dm.title, dm.type, dm.director, 
         dm.country, dm.release_year, dm.rating, dm.duration, dm.description;


-- ============================================================================
-- 8. DATA QUALITY CHECKS
-- ============================================================================

-- 8.1 Check for null values in critical fields
SELECT 
    'director' as column_name,
    COUNT(*) as null_count
FROM dim_movies
WHERE director IS NULL
UNION ALL
SELECT 
    'country',
    COUNT(*)
FROM dim_movies
WHERE country IS NULL
UNION ALL
SELECT 
    'date_added',
    COUNT(*)
FROM dim_movies
WHERE date_added IS NULL
UNION ALL
SELECT 
    'rating',
    COUNT(*)
FROM dim_movies
WHERE rating IS NULL;


-- 8.2 Verify referential integrity
-- Check if all genre_ids in movies_genres exist in dim_genres
SELECT COUNT(*) as orphan_records
FROM movies_genres mg
WHERE NOT EXISTS (
    SELECT 1 FROM dim_genres dg
    WHERE dg.genre_id = mg.genre_id
);

-- Should return: 0


-- 8.3 Check for orphaned genre records
SELECT COUNT(*) as unused_genres
FROM dim_genres dg
WHERE NOT EXISTS (
    SELECT 1 FROM movies_genres mg
    WHERE mg.genre_id = dg.genre_id
);

-- Should return: 0


-- ============================================================================
-- 9. SEARCH & FILTER EXAMPLES
-- ============================================================================

-- 9.1 Search movies (multi-criteria)
SELECT 
    movie_id,
    title,
    type,
    release_year,
    rating
FROM dim_movies
WHERE type = 'Movie'
  AND release_year >= 2010
  AND rating IN ('PG-13', 'PG', 'R')
  AND country = 'United States'
ORDER BY release_year DESC
LIMIT 30;


-- 9.2 Find unwatched classics (old movies)
SELECT 
    movie_id,
    title,
    release_year,
    rating
FROM dim_movies
WHERE type = 'Movie'
  AND release_year < 1990
ORDER BY release_year ASC;


-- 9.3 Recent TV Shows in specific genres
SELECT 
    dm.movie_id,
    dm.title,
    dm.release_year,
    STRING_AGG(dg.genre_name, ', ') as genres
FROM dim_movies dm
JOIN movies_genres mg ON dm.movie_id = mg.movie_id
JOIN dim_genres dg ON mg.genre_id = dg.genre_id
WHERE dm.type = 'TV Show'
  AND dm.release_year >= 2018
GROUP BY dm.movie_id, dm.title, dm.release_year
ORDER BY dm.release_year DESC
LIMIT 30;


-- ============================================================================
-- 10. EXPORT DATA
-- ============================================================================

-- 10.1 Export to CSV (using psql command line)
-- \COPY (
--     SELECT * FROM dim_movies ORDER BY movie_id
-- ) TO '/path/to/export.csv' WITH CSV HEADER;


-- 10.2 Full view with all data joined
CREATE OR REPLACE VIEW vw_netflix_full AS
SELECT 
    dm.movie_id,
    dm.title,
    dm.type,
    dm.director,
    dm.country,
    dm.date_added,
    dm.release_year,
    dm.rating,
    dm.duration,
    STRING_AGG(dg.genre_name, ', ' ORDER BY dg.genre_name) as genres,
    dm.description
FROM dim_movies dm
LEFT JOIN movies_genres mg ON dm.movie_id = mg.movie_id
LEFT JOIN dim_genres dg ON mg.genre_id = dg.genre_id
GROUP BY dm.movie_id, dm.title, dm.type, dm.director, dm.country,
          dm.date_added, dm.release_year, dm.rating, dm.duration, dm.description;

-- Use view:
-- SELECT * FROM vw_netflix_full WHERE type = 'Movie' LIMIT 10;


-- ============================================================================
-- NOTES
-- ============================================================================
-- - All dates are in YYYY-MM-DD format
-- - Some fields may be NULL (handle with IS NULL)
-- - Use STRING_AGG() for joining multiple genres
-- - Remember to handle NULL values in WHERE clauses
-- - Use indexes for better query performance on large datasets
-- - LOWER() for case-insensitive searches
-- - LIKE for pattern matching (% = wildcard)

-- ============================================================================
-- USEFUL TIPS
-- ============================================================================

-- Tip 1: Check execution plan
-- EXPLAIN ANALYZE SELECT ...;

-- Tip 2: Count rows without loading all data
-- SELECT COUNT(*) FROM dim_movies;

-- Tip 3: Get summary statistics
-- SELECT 
--     COUNT(*) as total,
--     COUNT(DISTINCT type) as types,
--     COUNT(DISTINCT rating) as ratings
-- FROM dim_movies;

-- Tip 4: Pagination (offset/limit)
-- SELECT * FROM dim_movies LIMIT 10 OFFSET 20;

-- Tip 5: Random sampling
-- SELECT * FROM dim_movies ORDER BY RANDOM() LIMIT 10;

-- ============================================================================
-- END OF SQL EXAMPLES
-- ============================================================================
-- Last Updated: November 16, 2025
-- For more help, see README.md
