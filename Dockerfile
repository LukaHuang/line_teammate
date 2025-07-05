FROM python:3.12-slim

WORKDIR /app

# 複製需求檔案
COPY requirements.txt .

# 安裝依賴
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 複製應用程式碼
COPY . .

# 暴露端口
EXPOSE 5000

# 啟動應用
CMD ["python", "line_bot.py"]