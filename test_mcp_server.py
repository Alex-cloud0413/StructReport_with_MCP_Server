#!/usr/bin/env python3
"""
Test script for Driver Data MCP Server

测试智驾数据MCP服务器核心功能的脚本。
"""

import asyncio
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path("src")))

async def test_mcp_server():
    """测试MCP服务器功能"""
    print("🚀 测试智驾数据MCP服务器核心功能")
    print("=" * 50)
    
    try:
        # 导入核心模块
        from main import (
            init_database, 
            parse_driver_report, 
            get_collection_summary, 
            export_data_csv,
            extract_with_rules
        )
        print("✅ 核心模块导入成功")
        
        # 测试数据库初始化
        print("\n🔍 测试数据库初始化...")
        init_database()
        print("✅ 数据库初始化成功")
        
        # 测试数据解析
        print("\n🔍 测试数据解析功能...")
        test_report = """
        采集员：张三
        车辆编号：京A12345
        采集任务：城市道路数据采集
        采集段数：5
        采集地点：北京市朝阳区
        采集日期：2025-01-10
        采集时段：白天
        行驶里程：120.5公里
        """
        
        # 测试规则提取
        extracted_data = await extract_with_rules(test_report)
        print(f"✅ 数据解析成功: {extracted_data}")
        
        # 测试完整的数据处理流程
        print("\n🔍 测试完整数据处理流程...")
        result = await parse_driver_report(test_report)
        print(f"✅ 数据处理完成: {result}")
        
        # 测试数据汇总
        print("\n🔍 测试数据汇总功能...")
        summary = await get_collection_summary()
        print(f"✅ 数据汇总成功: {summary}")
        
        # 测试数据导出
        print("\n🔍 测试数据导出功能...")
        export_result = await export_data_csv()
        print(f"✅ 数据导出成功: {export_result}")
        
        print("\n🎉 所有核心功能测试通过！")
        print("\n📋 MCP服务器功能说明：")
        print("1. parse_driver_report: 解析司机汇报文本")
        print("2. get_collection_summary: 获取采集数据总览")
        print("3. export_data_csv: 导出数据为CSV格式")
        print("4. 自动数据库存储和管理")
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

def test_basic_imports():
    """测试基本导入"""
    print("🔍 测试基本模块导入...")
    
    try:
        import pandas as pd
        print("✅ pandas 导入成功")
        
        import sqlite3
        print("✅ sqlite3 导入成功")
        
        import json
        print("✅ json 导入成功")
        
        import re
        print("✅ re 导入成功")
        
        from datetime import datetime
        print("✅ datetime 导入成功")
        
        from typing import Dict, List
        print("✅ typing 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 基本模块导入失败: {e}")
        return False

async def main():
    """主函数"""
    # 测试基本导入
    if not test_basic_imports():
        print("\n❌ 基本模块导入失败，请检查依赖安装")
        return
    
    # 测试MCP服务器功能
    await test_mcp_server()

if __name__ == "__main__":
    asyncio.run(main())
