#!/usr/bin/env python3

import sys
import os

def check_environment():
    """檢查必要的環境變數"""
    required_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ 缺少環境變數:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("✅ 所有必要的環境變數都已設定")
        return True

def check_imports():
    """檢查所有必要的模組是否可以導入"""
    try:
        import flask
        import linebot
        import openai
        import requests
        print("✅ 所有必要的模組都可以導入")
        return True
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

if __name__ == "__main__":
    print("🔍 進行健康檢查...")
    
    env_ok = check_environment()
    imports_ok = check_imports()
    
    if env_ok and imports_ok:
        print("✅ 健康檢查通過")
        sys.exit(0)
    else:
        print("❌ 健康檢查失敗")
        sys.exit(1)