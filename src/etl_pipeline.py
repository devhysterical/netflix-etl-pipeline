"""
ETL Pipeline Main Script

Thực hiện toàn bộ quy trình Extract -> Transform -> Load
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractor import NetflixExtractor
from src.transformer import NetflixTransformer
from src.loader import NetflixLoader


def main():
    """Hàm main thực hiện ETL pipeline"""

    print("\n" + "=" * 80)
    print("NETFLIX ETL PIPELINE")
    print("=" * 80)

    try:
        # Step 1: Extract
        print("\n[Step 1/3] EXTRACTING DATA...")
        extractor = NetflixExtractor()
        df = extractor.extract_from_csv()
        extractor.validate_data(df)

        # Step 2: Transform
        print("\n[Step 2/3] TRANSFORMING DATA...")
        transformer = NetflixTransformer(df)
        star_schema = transformer.transform()

        # Step 3: Load
        print("\n[Step 3/3] LOADING DATA...")
        loader = NetflixLoader()
        loader.connect()
        loader.load_all(star_schema)
        loader.validate_load()
        loader.disconnect()

        print("\n" + "=" * 80)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYou can now query the data from PostgreSQL:")
        print("  - Host: localhost")
        print("  - Port: 5432")
        print("  - Database: netflix_db")
        print("  - User: netflix_user")
        print("=" * 80 + "\n")

    except Exception as e:
        print("\n" + "=" * 80)
        print("ETL PIPELINE FAILED!")
        print("=" * 80)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure Docker PostgreSQL is running: docker-compose up -d")
        print("2. Ensure data file exists: data/netflix_titles.csv")
        print("3. Check .env configuration")
        print("=" * 80 + "\n")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
