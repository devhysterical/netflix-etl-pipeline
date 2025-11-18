"""
Loader Module - Tải dữ liệu vào PostgreSQL

Chức năng:
- Kết nối PostgreSQL
- Tải Dimension tables
- Tải Junction table
- Xác thực dữ liệu
"""

import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text, inspect

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import Config


class NetflixLoader:
    """Lớp tải dữ liệu vào PostgreSQL"""

    def __init__(self, database_url=None):
        """
        Khởi tạo Loader

        Parameters
        ----------
        database_url : str, optional
            URL kết nối PostgreSQL (mặc định từ Config)
        """
        self.database_url = database_url or Config.get_database_url()
        self.engine = None

    def connect(self):
        """
        Kết nối đến PostgreSQL

        Returns
        -------
        sqlalchemy.engine.Engine
            Engine kết nối
        """
        try:
            print("Connecting to PostgreSQL...")
            self.engine = create_engine(self.database_url, echo=False)

            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            print(f"Connected to {Config.DB_NAME} @ {Config.DB_HOST}:{Config.DB_PORT}")
            return self.engine

        except Exception as e:
            print(f"Connection failed: {str(e)}")
            print(f"\nDatabase URL: {self.database_url}")
            print("\nMake sure PostgreSQL is running:")
            print("  docker-compose up -d")
            raise

    def load_dim_genres(self, df_genres):
        """
        Tải dim_genres table

        Parameters
        ----------
        df_genres : pd.DataFrame
            DataFrame chứa genre data

        Returns
        -------
        int
            Số hàng được tải
        """
        print("\n" + "-" * 50)
        print("Loading dim_genres...")
        print("-" * 50)

        try:
            # Xóa dữ liệu cũ (nếu tồn tại)
            with self.engine.connect() as connection:
                connection.execute(text("TRUNCATE TABLE dim_genres CASCADE"))
                connection.commit()

            # Tải dữ liệu mới
            rows_inserted = df_genres.to_sql(
                "dim_genres",
                self.engine,
                if_exists="append",
                index=False,
            )

            print(f"Loaded {rows_inserted} genres")
            return rows_inserted

        except Exception as e:
            print(f"Error loading dim_genres: {str(e)}")
            raise

    def load_dim_movies(self, df_movies):
        """
        Tải dim_movies table

        Parameters
        ----------
        df_movies : pd.DataFrame
            DataFrame chứa movie data

        Returns
        -------
        int
            Số hàng được tải
        """
        print("\n" + "-" * 50)
        print("Loading dim_movies...")
        print("-" * 50)

        try:
            # Xóa dữ liệu cũ (nếu tồn tại)
            with self.engine.connect() as connection:
                connection.execute(text("TRUNCATE TABLE dim_movies CASCADE"))
                connection.commit()

            # Tải dữ liệu mới
            rows_inserted = df_movies.to_sql(
                "dim_movies",
                self.engine,
                if_exists="append",
                index=False,
            )

            print(f"Loaded {rows_inserted} movies")
            return rows_inserted

        except Exception as e:
            print(f"Error loading dim_movies: {str(e)}")
            raise

    def load_movies_genres(self, df_movies_genres):
        """
        Tải movies_genres junction table

        Parameters
        ----------
        df_movies_genres : pd.DataFrame
            DataFrame chứa movie-genre relationships

        Returns
        -------
        int
            Số hàng được tải
        """
        print("\n" + "-" * 50)
        print("Loading movies_genres...")
        print("-" * 50)

        try:
            # Xóa dữ liệu cũ (nếu tồn tại)
            with self.engine.connect() as connection:
                connection.execute(text("TRUNCATE TABLE movies_genres"))
                connection.commit()

            # Tải dữ liệu mới
            rows_inserted = df_movies_genres.to_sql(
                "movies_genres",
                self.engine,
                if_exists="append",
                index=False,
            )

            print(f"Loaded {rows_inserted} movie-genre relationships")
            return rows_inserted

        except Exception as e:
            print(f"Error loading movies_genres: {str(e)}")
            raise

    def load_all(self, star_schema):
        """
        Tải tất cả bảng từ Star Schema

        Parameters
        ----------
        star_schema : dict
            Dictionary chứa dim_movies, dim_genres, movies_genres

        Returns
        -------
        dict
            Dictionary chứa số lượng hàng được tải cho mỗi bảng
        """
        print("\n" + "=" * 50)
        print("LOADING DATA TO POSTGRESQL")
        print("=" * 50)

        results = {}

        try:
            # Tải theo thứ tự (genre trước, vì là FK reference)
            results["dim_genres"] = self.load_dim_genres(star_schema["dim_genres"])
            results["dim_movies"] = self.load_dim_movies(star_schema["dim_movies"])
            results["movies_genres"] = self.load_movies_genres(
                star_schema["movies_genres"]
            )

            print("\n" + "-" * 50)
            print("LOAD SUMMARY:")
            for table, count in results.items():
                print(f"  {table}: {count} rows")
            print("-" * 50)

        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

        return results

    def validate_load(self):
        """
        Kiểm tra dữ liệu đã tải

        Returns
        -------
        dict
            Thông tin kiểm tra
        """
        print("\n" + "=" * 50)
        print("VALIDATING LOADED DATA")
        print("=" * 50)

        validation = {}

        try:
            with self.engine.connect() as connection:
                # Check dim_movies
                movies_count = connection.execute(
                    text("SELECT COUNT(*) FROM dim_movies")
                ).scalar()
                validation["dim_movies_count"] = movies_count
                print(f"dim_movies: {movies_count} rows")

                # Check dim_genres
                genres_count = connection.execute(
                    text("SELECT COUNT(*) FROM dim_genres")
                ).scalar()
                validation["dim_genres_count"] = genres_count
                print(f"dim_genres: {genres_count} rows")

                # Check movies_genres
                relationships_count = connection.execute(
                    text("SELECT COUNT(*) FROM movies_genres")
                ).scalar()
                validation["movies_genres_count"] = relationships_count
                print(f"movies_genres: {relationships_count} rows")

                # Sample data
                print("\nSample movies:")
                sample_movies = pd.read_sql(
                    "SELECT movie_id, title, type, release_year FROM dim_movies LIMIT 5",
                    connection,
                )
                print(sample_movies.to_string())

                print("\nSample genres:")
                sample_genres = pd.read_sql(
                    "SELECT genre_id, genre_name FROM dim_genres LIMIT 10",
                    connection,
                )
                print(sample_genres.to_string())

        except Exception as e:
            print(f"Validation error: {str(e)}")
            raise

        return validation

    def disconnect(self):
        """Đóng kết nối"""
        if self.engine:
            self.engine.dispose()
            print("Disconnected from database")


def main():
    """Hàm main để kiểm tra Loader"""
    from extractor import NetflixExtractor
    from transformer import NetflixTransformer

    try:
        # Extract
        extractor = NetflixExtractor()
        df = extractor.extract_from_csv()

        # Transform
        transformer = NetflixTransformer(df)
        star_schema = transformer.transform()

        # Load
        loader = NetflixLoader()
        loader.connect()
        loader.load_all(star_schema)
        loader.validate_load()
        loader.disconnect()

        print("\n" + "=" * 50)
        print("✓ ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ ETL Pipeline failed: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
