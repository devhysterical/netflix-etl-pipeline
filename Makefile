.PHONY: help install setup-db start-db stop-db clean lint format test run notebook

help:
	@echo "Netflix ETL Pipeline - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Cài đặt dependencies"
	@echo "  make setup-db     - Khởi tạo cơ sở dữ liệu"
	@echo "  make venv         - Tạo môi trường ảo"
	@echo ""
	@echo "Database:"
	@echo "  make start-db     - Khởi động PostgreSQL (Docker)"
	@echo "  make stop-db      - Dừng PostgreSQL"
	@echo "  make restart-db   - Khởi động lại PostgreSQL"
	@echo "  make clean-db     - Xóa tất cả dữ liệu (CẢNH BÁO!)"
	@echo ""
	@echo "Development:"
	@echo "  make lint         - Kiểm tra code style (flake8)"
	@echo "  make format       - Định dạng code (black)"
	@echo "  make test         - Chạy tests"
	@echo ""
	@echo "Running:"
	@echo "  make run          - Chạy ETL pipeline"
	@echo "  make notebook     - Khởi động Jupyter notebook"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Xóa cache files"
	@echo ""

install:
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

venv:
	python -m venv venv
	@echo "✓ Virtual environment created"
	@echo "Activate with: venv\\Scripts\\activate (Windows) or source venv/bin/activate (macOS/Linux)"

setup-db:
	docker-compose up -d
	@echo "✓ PostgreSQL started"
	@echo "Waiting for PostgreSQL to be ready..."
	sleep 15
	@echo "✓ PostgreSQL is ready"

start-db:
	docker-compose up -d
	@echo "✓ PostgreSQL started"

stop-db:
	docker-compose stop
	@echo "✓ PostgreSQL stopped"

restart-db:
	docker-compose restart
	@echo "✓ PostgreSQL restarted"

clean-db:
	docker-compose down -v
	@echo "✓ PostgreSQL and volumes removed"

lint:
	flake8 src/ config/ --max-line-length=88
	@echo "✓ Linting completed"

format:
	black src/ config/
	@echo "✓ Code formatted"

test:
	pytest tests/ -v --tb=short
	@echo "✓ Tests completed"

run:
	python src/etl_pipeline.py

notebook:
	jupyter lab

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cache files removed"

.DEFAULT_GOAL := help
