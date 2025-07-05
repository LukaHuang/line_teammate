#!/bin/bash

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 升級 pip
pip install --upgrade pip

# 安裝依賴套件
pip install -r simple_requirements.txt

echo "虛擬環境設置完成！"
echo "使用 'source venv/bin/activate' 來啟動虛擬環境"
echo "使用 'deactivate' 來關閉虛擬環境"