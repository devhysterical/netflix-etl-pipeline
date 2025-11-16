"""
Extractor Module - Trích xuất dữ liệu Netflix

Chức năng:
- Đọc dữ liệu từ CSV
- Tải dữ liệu từ Kaggle (tuỳ chọn)
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import Config


class NetflixExtractor:
    """Lớp trích xuất dữ liệu Netflix"""

    def __init__(self, data_path=None):
        """
        Khởi tạo Extractor

        Parameters
        ----------
        data_path : str, optional
            Đường dẫn tệp CSV (mặc định từ Config)
        """
        self.data_path = data_path or Config.get_data_path()

    def extract_from_csv(self):
        """
        Trích xuất dữ liệu từ tệp CSV

        Returns
        -------
        pd.DataFrame
            DataFrame chứa dữ liệu Netflix

        Raises
        ------
        FileNotFoundError
            Nếu tệp CSV không tìm thấy
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"File not found: {self.data_path}")

        try:
            print(f"Reading data from {self.data_path}...")
            df = pd.read_csv(self.data_path)
            print(f"✓ Extracted {len(df)} rows and {len(df.columns)} columns")
            print(f"Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"✗ Error reading CSV: {str(e)}")
            raise

    def extract_from_kaggle(self):
        """
        Tải dữ liệu từ Kaggle API

        Returns
        -------
        pd.DataFrame
            DataFrame chứa dữ liệu Netflix

        Note
        ----
        Yêu cầu Kaggle API configured:
        - ~/.kaggle/kaggle.json chứa credentials
        - hoặc KAGGLE_USERNAME và KAGGLE_KEY trong .env
        """
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            print("Authenticating with Kaggle API...")
            api = KaggleApi()
            api.authenticate()

            dataset_name = "shivamb/netflix-shows"
            download_path = "./data"

            print(f"Downloading dataset from Kaggle: {dataset_name}...")
            api.dataset_download_files(dataset_name, path=download_path, unzip=True)

            print(f"✓ Dataset downloaded to {download_path}")

            # Read the CSV file
            csv_file = os.path.join(download_path, "netflix_titles.csv")
            return self.extract_from_csv_with_path(csv_file)

        except Exception as e:
            print(f"✗ Error downloading from Kaggle: {str(e)}")
            print("Please download manually from:")
            print("https://www.kaggle.com/datasets/shivamb/netflix-shows")
            raise

    def extract_from_csv_with_path(self, path):
        """
        Trích xuất từ CSV với đường dẫn cụ thể

        Parameters
        ----------
        path : str
            Đường dẫn tệp CSV

        Returns
        -------
        pd.DataFrame
            DataFrame chứa dữ liệu
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        print(f"Reading data from {path}...")
        df = pd.read_csv(path)
        print(f"✓ Extracted {len(df)} rows and {len(df.columns)} columns")
        return df

    def get_data_info(self, df):
        """
        In thông tin về DataFrame

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame cần kiểm tra
        """
        print("\n" + "=" * 50)
        print("DATA INFORMATION")
        print("=" * 50)
        print(f"Shape: {df.shape}")
        print(f"\nColumn Names and Types:")
        print(df.dtypes)
        print(f"\nMissing Values:")
        print(df.isnull().sum())
        print(f"\nFirst few rows:")
        print(df.head())
        print("=" * 50 + "\n")

    def validate_data(self, df):
        """
        Kiểm tra tính hợp lệ của dữ liệu

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame cần kiểm tra

        Returns
        -------
        bool
            True nếu dữ liệu hợp lệ
        """
        required_columns = [
            "show_id",
            "type",
            "title",
            "director",
            "country",
            "date_added",
            "release_year",
            "rating",
            "duration",
            "listed_in",
            "description",
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            print(f"✗ Missing columns: {missing_cols}")
            return False

        print("✓ All required columns present")
        return True


def main():
    """Hàm main để kiểm tra Extractor"""
    extractor = NetflixExtractor()

    try:
        # Try to read from CSV
        df = extractor.extract_from_csv()
        extractor.validate_data(df)
        extractor.get_data_info(df)

    except FileNotFoundError as e:
        print(f"✗ {str(e)}")
        print("\nTry downloading from Kaggle...")
        try:
            df = extractor.extract_from_kaggle()
            extractor.validate_data(df)
            extractor.get_data_info(df)
        except Exception as kaggle_error:
            print(f"✗ Kaggle download failed: {str(kaggle_error)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
