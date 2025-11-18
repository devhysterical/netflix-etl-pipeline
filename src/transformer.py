"""
Transformer Module - Chuyển đổi và làm sạch dữ liệu Netflix

Chức năng:
- Xóa giá trị NA
- Tách thể loại (explode)
- Chuẩn hóa ngày tháng
- Tạo Star Schema (Dimension tables)
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class NetflixTransformer:
    """Lớp chuyển đổi dữ liệu Netflix"""

    def __init__(self, df):
        """
        Khởi tạo Transformer

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame thô cần chuyển đổi
        """
        self.df = df.copy()
        self.original_rows = len(df)

    def clean_data(self):
        """
        Bước 1: Làm sạch dữ liệu

        - Xóa NA trong các cột quan trọng: director, country, date_added, rating
        - Loại bỏ duplicate rows
        - Reset index

        Returns
        -------
        pd.DataFrame
            DataFrame đã làm sạch
        """
        print("\n" + "=" * 50)
        print("STEP 1: CLEANING DATA")
        print("=" * 50)

        initial_rows = len(self.df)

        # Định nghĩa các cột bắt buộc (không được NA)
        required_columns = ["director", "country", "date_added", "rating"]

        # Kiểm tra và in thông tin NA
        print(f"\nMissing values before cleaning:")
        for col in required_columns:
            na_count = self.df[col].isna().sum()
            na_percent = (na_count / len(self.df)) * 100
            print(f"  {col}: {na_count} ({na_percent:.2f}%)")

        # Xóa NA trong các cột bắt buộc
        self.df = self.df.dropna(subset=required_columns)

        # Xóa duplicate rows
        self.df = self.df.drop_duplicates()

        # Reset index
        self.df = self.df.reset_index(drop=True)

        final_rows = len(self.df)
        removed_rows = initial_rows - final_rows

        print(f"\nRows removed: {removed_rows}")
        print(f"Rows remaining: {final_rows}")
        print("Data cleaning completed")

        return self.df

    def normalize_dates(self):
        """
        Bước 2: Chuẩn hóa ngày tháng

        - Chuyển date_added thành datetime
        - Format thành YYYY-MM-DD
        - Strip whitespace

        Returns
        -------
        pd.DataFrame
            DataFrame với ngày đã chuẩn hóa
        """
        print("\n" + "=" * 50)
        print("STEP 2: NORMALIZING DATES")
        print("=" * 50)

        try:
            # Convert to datetime
            self.df["date_added"] = pd.to_datetime(self.df["date_added"], errors="coerce")

            # Format as YYYY-MM-DD
            self.df["date_added"] = self.df["date_added"].dt.strftime("%Y-%m-%d")

            # Check for any remaining NaT
            na_dates = self.df["date_added"].isna().sum()
            if na_dates > 0:
                print(f"⚠ Warning: {na_dates} invalid dates found")

            print("Date normalization completed")
            print(f"Sample dates: {self.df['date_added'].head(3).values}")

        except Exception as e:
            print(f"Error normalizing dates: {str(e)}")
            raise

        return self.df

    def normalize_text(self):
        """
        Bước 3: Chuẩn hóa văn bản

        - Strip whitespace từ các cột text
        - Chuẩn hóa tên thể loại

        Returns
        -------
        pd.DataFrame
            DataFrame với văn bản đã chuẩn hóa
        """
        print("\n" + "=" * 50)
        print("STEP 3: NORMALIZING TEXT")
        print("=" * 50)

        text_columns = ["director", "country", "listed_in", "title"]

        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.strip()
                print(f"Normalized text in column: {col}")

        return self.df

    def explode_genres(self):
        """
        Bước 4: Tách thể loại (Explode)

        - Cột listed_in chứa nhiều thể loại phân cách bằng ','
        - Tách thành các hàng riêng biệt
        - Strip whitespace từ mỗi thể loại

        Returns
        -------
        pd.DataFrame
            DataFrame với genres đã tách
        """
        print("\n" + "=" * 50)
        print("STEP 4: EXPLODING GENRES")
        print("=" * 50)

        initial_rows = len(self.df)

        # Split listed_in by comma and explode
        self.df["listed_in"] = self.df["listed_in"].str.split(",")
        self.df = self.df.explode("listed_in")

        # Strip whitespace từ mỗi genre
        self.df["listed_in"] = self.df["listed_in"].str.strip()

        # Remove duplicates (title + genre)
        self.df = self.df.drop_duplicates(subset=["show_id", "listed_in"])

        # Reset index
        self.df = self.df.reset_index(drop=True)

        final_rows = len(self.df)

        print(f"Rows before explode: {initial_rows}")
        print(f"Rows after explode: {final_rows}")
        print(f"Unique genres: {self.df['listed_in'].nunique()}")
        print("Genre explosion completed")

        return self.df

    def create_star_schema(self):
        """
        Bước 5: Tạo Star Schema

        Tạo 3 bảng:
        1. dim_movies: Thông tin phim
        2. dim_genres: Danh sách thể loại
        3. movies_genres: Kết nối N-N

        Returns
        -------
        dict
            Dictionary chứa 3 DataFrames: dim_movies, dim_genres, movies_genres
        """
        print("\n" + "=" * 50)
        print("STEP 5: CREATING STAR SCHEMA")
        print("=" * 50)

        # 1. Tạo dim_genres
        print("\n1. Creating dim_genres...")
        dim_genres = (
            self.df[["listed_in"]]
            .drop_duplicates()
            .reset_index(drop=True)
            .rename(columns={"listed_in": "genre_name"})
        )
        dim_genres["genre_id"] = range(1, len(dim_genres) + 1)
        dim_genres = dim_genres[["genre_id", "genre_name"]]

        print(f"   Created {len(dim_genres)} unique genres")

        # 2. Tạo dim_movies
        print("\n2. Creating dim_movies...")
        dim_movies_temp = (
            self.df[
                [
                    "show_id",
                    "type",
                    "title",
                    "director",
                    "country",
                    "date_added",
                    "release_year",
                    "rating",
                    "duration",
                    "description",
                ]
            ]
            .drop_duplicates(subset=["show_id"])
            .reset_index(drop=True)
        )

        # Create mapping of show_id to movie_id before dropping show_id
        show_id_to_movie_id = pd.DataFrame({
            "show_id": dim_movies_temp["show_id"],
            "movie_id": range(1, len(dim_movies_temp) + 1)
        })

        # Create final dim_movies without show_id
        dim_movies = dim_movies_temp.copy()
        dim_movies["movie_id"] = range(1, len(dim_movies) + 1)

        # Reorder columns (without show_id)
        dim_movies = dim_movies[
            [
                "movie_id",
                "title",
                "type",
                "director",
                "country",
                "date_added",
                "release_year",
                "rating",
                "duration",
                "description",
            ]
        ]

        print(f"   Created {len(dim_movies)} unique movies")

        # 3. Tạo mapping show_id -> movie_id
        print("\n3. Creating movies_genres junction table...")

        # Tạo movies_genres table
        movies_genres = self.df[["show_id", "listed_in"]].drop_duplicates()

        movies_genres = movies_genres.merge(
            show_id_to_movie_id, on="show_id", how="left"
        )
        movies_genres = movies_genres.merge(
            dim_genres, left_on="listed_in", right_on="genre_name", how="left"
        )

        movies_genres = movies_genres[["movie_id", "genre_id"]].drop_duplicates()
        movies_genres = movies_genres.dropna()
        movies_genres["movie_id"] = movies_genres["movie_id"].astype(int)
        movies_genres["genre_id"] = movies_genres["genre_id"].astype(int)

        print(f"   Created {len(movies_genres)} movie-genre relationships")

        # Summary
        print("\n" + "-" * 50)
        print("STAR SCHEMA SUMMARY:")
        print(f"  dim_movies: {len(dim_movies)} rows")
        print(f"  dim_genres: {len(dim_genres)} rows")
        print(f"  movies_genres: {len(movies_genres)} rows")
        print("-" * 50)

        return {
            "dim_movies": dim_movies,
            "dim_genres": dim_genres,
            "movies_genres": movies_genres,
        }

    def transform(self):
        """
        Thực hiện tất cả bước chuyển đổi

        Returns
        -------
        dict
            Dictionary chứa 3 DataFrames của Star Schema
        """
        print("\n" + "=" * 80)
        print("NETFLIX DATA TRANSFORMATION PIPELINE")
        print("=" * 80)

        # Execute transformation steps
        self.clean_data()
        self.normalize_dates()
        self.normalize_text()
        self.explode_genres()
        star_schema = self.create_star_schema()

        print("\n" + "=" * 80)
        print("TRANSFORMATION COMPLETED SUCCESSFULLY")
        print("=" * 80 + "\n")

        return star_schema


def main():
    """Hàm main để kiểm tra Transformer"""
    from extractor import NetflixExtractor

    try:
        # Extract data
        extractor = NetflixExtractor()
        df = extractor.extract_from_csv()

        # Transform data
        transformer = NetflixTransformer(df)
        star_schema = transformer.transform()

        # Print sample data
        print("\n" + "=" * 50)
        print("SAMPLE DATA")
        print("=" * 50)
        print("\ndim_movies (first 5):")
        print(star_schema["dim_movies"].head())
        print("\ndim_genres (first 10):")
        print(star_schema["dim_genres"].head(10))
        print("\nmovies_genres (first 10):")
        print(star_schema["movies_genres"].head(10))

    except Exception as e:
        print(f"Error in transformation: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
