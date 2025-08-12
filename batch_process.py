#!/usr/bin/env python3
# 批量处理示例数据
import sqlite3
import pandas as pd
import json
import re
from datetime import datetime
from typing import Dict

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
    name_patterns = [r'采集员[：:]\s*([^，,\n]+)', r'姓名[：:]\s*([^，,\n]+)', r'司机[：:]\s*([^，,\n]+)']
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            result["driver_name"] = match.group(1).strip()
            break
    
    # 车辆编号提取
    vehicle_patterns = [r'车辆编号[：:]\s*([^，,\n]+)', r'车牌[：:]\s*([^，,\n]+)', r'车号[：:]\s*([^，,\n]+)']
    for pattern in vehicle_patterns:
        match = re.search(pattern, text)
        if match:
            result["vehicle_number"] = match.group(1).strip()
            break
    
    # 采集任务提取
    task_patterns = [r'采集任务[：:]\s*([^，,\n]+)', r'任务[：:]\s*([^，,\n]+)', r'项目[：:]\s*([^，,\n]+)']
    for pattern in task_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_task"] = match.group(1).strip()
            break
    
    # 采集段数提取（提取数字）
    segments_patterns = [r'采集段数[：:]\s*(\d+)', r'段数[：:]\s*(\d+)', r'(\d+)\s*段']
    for pattern in segments_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_segments"] = int(match.group(1))
            break
    
    # 采集地点提取
    location_patterns = [r'采集地点[：:]\s*([^，,\n]+)', r'地点[：:]\s*([^，,\n]+)', r'位置[：:]\s*([^，,\n]+)']
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_location"] = match.group(1).strip()
            break
    
    # 采集日期提取
    date_patterns = [r'采集日期[：:]\s*([0-9-/]+)', r'日期[：:]\s*([0-9-/]+)', r'时间[：:]\s*([0-9-/]+)']
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_date"] = match.group(1).strip()
            break
    
    # 采集时段提取
    if '白天' in text or '白' in text or '上午' in text or '下午' in text:
        result["collection_time_period"] = "白天"
    elif '夜晚' in text or '夜' in text or '晚上' in text:
        result["collection_time_period"] = "夜晚"
    
    # 行驶里程提取
    distance_patterns = [r'行驶里程[：:]\s*([0-9.]+)', r'里程[：:]\s*([0-9.]+)', r'([0-9.]+)\s*公里', r'距离[：:]\s*([0-9.]+)']
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

def process_sample_data():
    """处理示例数据"""
    sample_reports = [
        """
        采集员：李四
        车辆编号：沪B67890
        采集任务：上海高速公路数据采集
        采集段数：8
        采集地点：上海
        采集日期：2025-01-11
        采集时段：夜晚
        行驶里程：200.3公里
        """,
        
        """
        司机：王五
        车牌：粤C11111
        项目：广州市区智驾测试
        段数：3
        位置：广州
        时间：2025-01-12
        白天采集
        距离：85.7公里
        """,
        
        """
        姓名：赵六
        车号：京D22222
        任务：北京环路采集任务
        采集了6段
        地点：北京
        日期：2025-01-13
        夜间作业
        里程：156.8公里
        """,
        
        """
        采集员：钱七
        车辆编号：川E33333
        采集任务：成都市智能驾驶数据收集
        采集段数：4
        采集地点：成都
        采集日期：2025-01-14
        采集时段：白天
        行驶里程：98.2公里
        """,
        
        """
        司机：孙八
        车牌号：浙F44444
        采集项目：杭州城区道路测试
        完成段数：7
        测试地点：杭州
        测试日期：2025-01-15
        下午时段
        总里程：175.6公里
        """
    ]
    
    print("🚀 开始批量处理示例数据...")
    
    for i, report_text in enumerate(sample_reports, 1):
        print(f"\n📊 处理第 {i} 条数据...")
        
        # 解析数据
        extracted_data = extract_with_rules(report_text)
        print(f"解析结果: {json.dumps(extracted_data, ensure_ascii=False)}")
        
        # 保存到数据库
        save_to_database(extracted_data, report_text.strip())
        print("✅ 数据已保存")
    
    print(f"\n🎉 批量处理完成！共处理 {len(sample_reports)} 条数据")

def get_final_summary():
    """获取最终汇总"""
    conn = sqlite3.connect('driver_data.db')
    df = pd.read_sql_query("SELECT * FROM driver_reports", conn)
    conn.close()
    
    print("\n📈 最终数据汇总:")
    print(f"📊 总报告数: {len(df)}")
    print(f"👥 司机数量: {df['driver_name'].nunique()}")
    print(f"🛣️  总采集段数: {df['collection_segments'].sum()}")
    print(f"🚗 总行驶里程: {df['driving_distance'].sum():.1f} 公里")
    
    print(f"\n📍 采集地点分布:")
    for location, count in df['collection_location'].value_counts().items():
        print(f"   {location}: {count} 次")
    
    print(f"\n⏰ 时段分布:")
    for period, count in df['collection_time_period'].value_counts().items():
        print(f"   {period}: {count} 次")
    
    # 导出最终数据
    filename = f"driver_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n📤 数据已导出到: {filename}")

if __name__ == "__main__":
    process_sample_data()
    get_final_summary()