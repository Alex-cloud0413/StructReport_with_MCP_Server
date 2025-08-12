#!/usr/bin/env python3
# 测试数据库初始化
import sqlite3
import sys
import os

def init_database():
    """初始化数据库"""
    try:
        conn = sqlite3.connect('driver_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS driver_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT,
            vehicle_number TEXT,
            collection_task TEXT,
            collection_segments INTEGER,
            collection_location TEXT,
            collection_date TEXT,
            collection_time_period TEXT,
            driving_distance REAL,
            raw_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ 数据库初始化成功！")
        print("📁 数据库文件: driver_data.db")
        
        # 验证表结构
        conn = sqlite3.connect('driver_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 数据库表: {tables}")
        
        cursor.execute("PRAGMA table_info(driver_reports);")
        columns = cursor.fetchall()
        print("📋 表结构:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始初始化智驾数据采集数据库...")
    success = init_database()
    
    if success:
        print("\n✅ 第3步完成：数据库初始化成功！")
        print("📝 下一步可以测试 MCP 服务器功能")
    else:
        print("\n❌ 数据库初始化失败，请检查错误信息")
        sys.exit(1)