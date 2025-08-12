#!/usr/bin/env python3
# 测试 MCP 服务器基础功能
import asyncio
import sys

async def test_mcp_imports():
    """测试 MCP 相关导入"""
    try:
        from fastmcp import FastMCP
        print("✅ FastMCP 导入成功")
        
        import pandas as pd
        print("✅ Pandas 导入成功")
        
        import sqlite3
        print("✅ SQLite3 导入成功")
        
        import json
        print("✅ JSON 导入成功")
        
        import re
        print("✅ RE 导入成功")
        
        from datetime import datetime
        print("✅ DateTime 导入成功")
        
        from typing import Optional, Dict, List
        print("✅ Typing 导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

async def test_mcp_server_creation():
    """测试 MCP 服务器创建"""
    try:
        from fastmcp import FastMCP
        mcp = FastMCP("driver-data-server")
        print("✅ MCP 服务器对象创建成功")
        return True
    except Exception as e:
        print(f"❌ MCP 服务器创建失败: {e}")
        return False

async def main():
    print("🧪 开始测试 MCP 服务器基础功能...")
    
    # 测试导入
    print("\n📦 测试模块导入:")
    import_success = await test_mcp_imports()
    
    if not import_success:
        print("❌ 模块导入失败，无法继续")
        return False
    
    # 测试服务器创建
    print("\n🚀 测试 MCP 服务器创建:")
    server_success = await test_mcp_server_creation()
    
    if server_success:
        print("\n✅ MCP 服务器基础功能测试通过！")
        print("📝 可以尝试启动完整的 MCP 服务器")
        return True
    else:
        print("\n❌ MCP 服务器测试失败")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        if result:
            print("\n🎉 第3步基础测试完成！")
        else:
            print("\n💥 测试失败，需要检查环境配置")
            sys.exit(1)
    except Exception as e:
        print(f"💥 测试过程中出现异常: {e}")
        sys.exit(1)