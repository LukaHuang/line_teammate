FROM python:3.12-slim

WORKDIR /app

# 複製需求檔案
COPY requirements.txt .

# 安裝依賴
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 複製應用程式碼
COPY . .

# 暴露端口 (Zeabur 會動態設定)
EXPOSE $PORT

# 安裝 curl 用於健康檢查
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5000}/health || exit 1

# 啟動應用
CMD ["python", "line_bot.py"]