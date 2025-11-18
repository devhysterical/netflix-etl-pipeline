# Hướng dẫn Đóng góp - Netflix ETL Pipeline

Cảm ơn bạn đã quan tâm đến đóng góp cho dự án! Hướng dẫn này sẽ giúp bạn bắt đầu.

## Quy trình Đóng góp

### 1. Fork Dự án

Click nút "Fork" trên GitHub để tạo một bản sao của dự án.

### 2. Clone Dự án Của Bạn

```bash
git clone https://github.com/YOUR_USERNAME/netflix-etl-pipeline.git
cd netflix-etl-pipeline
```

### 3. Tạo Branch Mới

```bash
git checkout -b feature/your-feature-name
# hoặc
git checkout -b fix/your-bug-fix
```

### 4. Thiết lập Môi trường Phát triển

```bash
python -m venv venv
source venv/bin/activate  # hoặc venv\Scripts\activate trên Windows
pip install -r requirements.txt
pip install -e .  # Cài đặt dự án ở chế độ phát triển
```

### 5. Thực hiện Thay đổi

- Sửa đổi mã nguồn
- Kiểm tra PEP 8 compliance
- Thêm/cập nhật docstrings
- Viết tests nếu cần

### 6. Kiểm tra Mã

```bash
# Kiểm tra PEP 8
flake8 src/ --max-line-length=88

# Định dạng mã
black src/

# Type checking (nếu có)
mypy src/
```

### 7. Commit Thay đổi

```bash
git add .
git commit -m "Add: [your feature]"
# hoặc
git commit -m "Fix: [your bug fix]"
```

**Commit message guidelines:**

- Add: Thêm tính năng mới
- Fix: Sửa lỗi
- Docs: Cập nhật tài liệu
- Refactor: Tái cấu trúc mã
- Test: Thêm tests

### 8. Push Branch

```bash
git push origin feature/your-feature-name
```

### 9. Tạo Pull Request

1. Truy cập GitHub repository
2. Click "Compare & pull request"
3. Mô tả thay đổi của bạn
4. Submit PR

---

## Hướng dẫn Mã hóa

### Tiêu chuẩn PEP 8

Tất cả mã phải tuân thủ [PEP 8](https://www.python.org/dev/peps/pep-0008/):

- Max line length: 88 ký tự
- 4 spaces cho indentation
- snake_case cho function/variable names
- PascalCase cho class names

### Docstrings

Sử dụng Google-style docstrings:

```python
def extract_data(file_path: str) -> pd.DataFrame:
    """
    Trích xuất dữ liệu từ tệp CSV.

    Parameters
    ----------
    file_path : str
        Đường dẫn tới tệp CSV

    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu

    Raises
    ------
    FileNotFoundError
        Nếu tệp không tìm thấy
    """
    pass
```

### Type Hints

Sử dụng type hints cho clarity:

```python
def load_data(
    df: pd.DataFrame,
    table_name: str,
    batch_size: int = 1000
) -> int:
    """Load data and return number of rows inserted."""
    pass
```

### Comments

- Sử dụng comments để giải thích WHY, không phải WHAT
- Giữ comments ngắn gọn
- Cập nhật comments khi thay đổi logic

---

## Cấu trúc Dự án

```
src/
├── extractor.py     # Trích xuất dữ liệu
├── transformer.py   # Chuyển đổi dữ liệu
├── loader.py        # Tải dữ liệu
└── etl_pipeline.py  # Main pipeline

config/
└── config.py        # Configuration

notebooks/
└── netflix_etl_pipeline.ipynb  # Analysis notebook

docker/
└── init.sql         # Database schema

tests/               # Test files
├── test_extractor.py
├── test_transformer.py
└── test_loader.py
```

---

## Viết Tests

Nếu thêm tính năng mới, vui lòng viết tests:

```python
# tests/test_extractor.py
import pytest
from src.extractor import NetflixExtractor

def test_extract_from_csv():
    extractor = NetflixExtractor()
    df = extractor.extract_from_csv()

    assert df is not None
    assert len(df) > 0
    assert 'title' in df.columns
```

Chạy tests:

```bash
pytest tests/ -v
```

---

## Pull Request Guidelines

### Tiêu đề PR

- Rõ ràng và mô tả
- Ví dụ: "Add: Data validation for genre column"

### Mô tả PR

```markdown
## Description

Ngắn gọn mô tả những gì PR làm.

## Related Issue

Closes #123 (nếu có)

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?

Giải thích cách bạn đã test thay đổi này.

## Checklist

- [ ] Mã tuân thủ PEP 8
- [ ] Thêm docstrings
- [ ] Viết tests
- [ ] Cập nhật README
```

---

## Báo cáo Lỗi

Nếu tìm thấy lỗi, tạo Issue với:

```markdown
## Description

Mô tả lỗi rõ ràng.

## Reproduction Steps

1. ...
2. ...
3. ...

## Expected Behavior

Phải xảy ra gì?

## Actual Behavior

Thực tế xảy ra gì?

## Environment

- Python version: 3.9.x
- OS: Windows/macOS/Linux
- Docker version: x.x.x
```

---

## Hỏi Đáp

### Làm cách nào để chạy tests?

```bash
pytest tests/ -v
```

### Làm cách nào để kiểm tra linting?

```bash
flake8 src/ --max-line-length=88
```

### Làm cách nào để định dạng mã?

```bash
black src/
```

---

## Liên hệ

Nếu có câu hỏi, vui lòng:

1. Tạo một [Discussion](https://github.com/devhysterical/netflix-etl-pipeline/discussions)
2. Hoặc tạo một [Issue](https://github.com/devhysterical/netflix-etl-pipeline/issues)

---

## Cảm ơn!

Cảm ơn bạn đã đóng góp! 🙏

**Happy Coding!**
