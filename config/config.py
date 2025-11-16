"""
Config Module - Cấu hình cho Netflix ETL Pipeline
"""

import os
from dotenv import load_dotenv

# Load environment variables từ .env file
load_dotenv()


class Config:
    """Lớp cấu hình chính"""

    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "netflix_db")
    DB_USER = os.getenv("DB_USER", "netflix_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "netflix_password")

    # Database Connection String
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Data Configuration
    DATA_PATH = os.getenv("DATA_PATH", "./data/netflix_titles.csv")

    # Kaggle Configuration (Optional)
    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "")
    KAGGLE_KEY = os.getenv("KAGGLE_KEY", "")

    # ETL Configuration
    BATCH_SIZE = 1000  # Kích thước batch cho tải dữ liệu
    CHUNK_SIZE = 10000  # Kích thước chunk khi đọc CSV lớn

    @staticmethod
    def get_database_url():
        """Lấy URL kết nối cơ sở dữ liệu"""
        return Config.DATABASE_URL

    @staticmethod
    def get_data_path():
        """Lấy đường dẫn tệp dữ liệu"""
        return Config.DATA_PATH

    @staticmethod
    def validate_config():
        """Kiểm tra cấu hình cơ sở dữ liệu"""
        required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing_vars = [
            var for var in required_vars if not getattr(Config, var, None)
        ]

        if missing_vars:
            raise ValueError(f"Missing configuration variables: {missing_vars}")

        return True
