#!/usr/bin/env python3
# 简单测试脚本
print("🧪 开始简单测试...")

try:
    import sqlite3
    print("✅ SQLite3 导入成功")
    
    # 测试数据库连接
    conn = sqlite3.connect('driver_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"✅ 数据库连接成功，表: {tables}")
    conn.close()
    
    import pandas as pd
    print("✅ Pandas 导入成功")
    
    import json
    print("✅ JSON 导入成功")
    
    import re
    print("✅ RE 导入成功")
    
    from datetime import datetime
    print("✅ DateTime 导入成功")
    
    from typing import Optional, Dict, List
    print("✅ Typing 导入成功")
    
    print("\n🎉 基础模块测试全部通过！")
    
    # 尝试导入 FastMCP
    print("\n📦 测试 FastMCP 导入...")
    from fastmcp import FastMCP
    print("✅ FastMCP 导入成功")
    
    # 创建 MCP 服务器对象
    mcp = FastMCP("driver-data-server")
    print("✅ MCP 服务器对象创建成功")
    
    print("\n🚀 所有测试通过！可以尝试启动服务器")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()