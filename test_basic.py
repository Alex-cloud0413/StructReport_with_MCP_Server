#!/usr/bin/env python3
# 测试基础功能（不依赖 FastMCP）
import sqlite3
import pandas as pd
import json
import re
from datetime import datetime
from typing import Optional, Dict, List

def init_database():
    """初始化数据库"""
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
    print("✅ 数据库初始化完成")

def extract_with_rules(text: str) -> Dict:
    """使用规则和正则表达式提取数据"""
    result = {
        "driver_name": None,
        "vehicle_number": None,
        "collection_task": None,
        "collection_segments": None,
        "collection_location": None,
        "collection_date": None,
        "collection_time_period": None,
        "driving_distance": None
    }
    
    # 司机姓名提取
    name_patterns = [r'采集员[：:]\s*([^，,\n]+)', r'姓名[：:]\s*([^，,\n]+)']
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            result["driver_name"] = match.group(1).strip()
            break
    
    # 车辆编号提取
    vehicle_patterns = [r'车辆编号[：:]\s*([^，,\n]+)', r'车牌[：:]\s*([^，,\n]+)']
    for pattern in vehicle_patterns:
        match = re.search(pattern, text)
        if match:
            result["vehicle_number"] = match.group(1).strip()
            break
    
    # 采集任务提取
    task_patterns = [r'采集任务[：:]\s*([^，,\n]+)', r'任务[：:]\s*([^，,\n]+)']
    for pattern in task_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_task"] = match.group(1).strip()
            break
    
    # 采集段数提取（提取数字）
    segments_patterns = [r'采集段数[：:]\s*(\d+)', r'段数[：:]\s*(\d+)']
    for pattern in segments_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_segments"] = int(match.group(1))
            break
    
    # 采集地点提取
    location_patterns = [r'采集地点[：:]\s*([^，,\n]+)', r'地点[：:]\s*([^，,\n]+)']
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_location"] = match.group(1).strip()
            break
    
    # 采集日期提取
    date_patterns = [r'采集日期[：:]\s*([0-9-/]+)', r'日期[：:]\s*([0-9-/]+)']
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_date"] = match.group(1).strip()
            break
    
    # 采集时段提取
    if '白天' in text or '白' in text:
        result["collection_time_period"] = "白天"
    elif '夜晚' in text or '夜' in text:
        result["collection_time_period"] = "夜晚"
    
    # 行驶里程提取
    distance_patterns = [r'行驶里程[：:]\s*([0-9.]+)', r'里程[：:]\s*([0-9.]+)', r'([0-9.]+)\s*公里']
    for pattern in distance_patterns:
        match = re.search(pattern, text)
        if match:
            result["driving_distance"] = float(match.group(1))
            break
    
    return result

def save_to_database(data: Dict, raw_text: str):
    """保存数据到SQLite数据库"""
    conn = sqlite3.connect('driver_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO driver_reports 
    (driver_name, vehicle_number, collection_task, collection_segments, 
     collection_location, collection_date, collection_time_period, 
     driving_distance, raw_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["driver_name"], data["vehicle_number"], data["collection_task"],
        data["collection_segments"], data["collection_location"], 
        data["collection_date"], data["collection_time_period"],
        data["driving_distance"], raw_text
    ))
    
    conn.commit()
    conn.close()

def get_collection_summary() -> Dict:
    """获取采集数据总览"""
    conn = sqlite3.connect('driver_data.db')
    df = pd.read_sql_query("SELECT * FROM driver_reports", conn)
    conn.close()
    
    if df.empty:
        return {"message": "暂无数据"}
    
    summary = {
        "total_reports": int(len(df)),
        "total_drivers": int(df['driver_name'].nunique()),
        "total_segments": int(df['collection_segments'].sum()) if not df['collection_segments'].isna().all() else 0,
        "total_distance": float(df['driving_distance'].sum()) if not df['driving_distance'].isna().all() else 0.0,
        "locations": {k: int(v) for k, v in df['collection_location'].value_counts().to_dict().items()},
        "time_periods": {k: int(v) for k, v in df['collection_time_period'].value_counts().to_dict().items()},
        "latest_update": str(df['created_at'].max())
    }
    
    return summary

def export_data_csv() -> str:
    """导出数据为CSV格式"""
    conn = sqlite3.connect('driver_data.db')
    df = pd.read_sql_query("SELECT * FROM driver_reports", conn)
    conn.close()
    
    filename = f"driver_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    return f"数据已导出到文件: {filename}"

def test_parse_driver_report():
    """测试解析功能"""
    test_text = """
    采集员：张三
    车辆编号：京A12345
    采集任务：北京市区道路采集
    采集段数：5
    采集地点：北京
    采集日期：2025-01-10
    采集时段：白天
    行驶里程：120.5公里
    """
    
    print("🧪 测试数据解析功能...")
    result = extract_with_rules(test_text)
    print(f"📊 解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 保存到数据库
    save_to_database(result, test_text)
    print("✅ 数据已保存到数据库")
    
    return result

def main():
    print("🚀 开始测试智驾数据采集系统基础功能...")
    
    # 1. 初始化数据库
    print("\n📁 步骤1: 初始化数据库")
    init_database()
    
    # 2. 测试数据解析
    print("\n📊 步骤2: 测试数据解析")
    test_result = test_parse_driver_report()
    
    # 3. 测试数据汇总
    print("\n📈 步骤3: 测试数据汇总")
    summary = get_collection_summary()
    print(f"汇总结果: {json.dumps(summary, ensure_ascii=False, indent=2)}")
    
    # 4. 测试数据导出
    print("\n📤 步骤4: 测试数据导出")
    export_result = export_data_csv()
    print(f"导出结果: {export_result}")
    
    print("\n🎉 第3步基础功能测试完成！")
    print("📝 数据库已初始化，核心功能正常工作")
    print("⚠️  注意：FastMCP 服务器启动可能需要解决环境问题")

if __name__ == "__main__":
    main()