#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
from datetime import datetime
import re
from typing import Dict

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
    print("数据库初始化完成")

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
    name_patterns = [r'采集员[：:]\s*([^，,\n车]+)', r'姓名[：:]\s*([^，,\n]+)']
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            result["driver_name"] = match.group(1).strip()
            break
    
    # 车辆编号提取
    vehicle_patterns = [r'车辆编号[：:]\s*([^，,\n采]+)', r'车牌[：:]\s*([^，,\n]+)']
    for pattern in vehicle_patterns:
        match = re.search(pattern, text)
        if match:
            result["vehicle_number"] = match.group(1).strip()
            break
    
    # 采集任务提取
    task_patterns = [r'采集任务[：:]\s*([^，,\n采]+)', r'任务[：:]\s*([^，,\n]+)']
    for pattern in task_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_task"] = match.group(1).strip()
            break
    
    # 采集段数提取
    segments_patterns = [r'采集段数[：:]\s*(\d+)\+?', r'段数[：:]\s*(\d+)\+?']
    for pattern in segments_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_segments"] = int(match.group(1))
            break
    
    # 采集地点提取
    location_patterns = [r'采集地点[：:]\s*([^，,\n采]+)', r'地点[：:]\s*([^，,\n]+)']
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            result["collection_location"] = match.group(1).strip()
            break
    
    # 采集日期提取
    date_patterns = [r'采集日期[：:]\s*([0-9.-/]+)', r'日期[：:]\s*([0-9.-/]+)']
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1).strip()
            if re.match(r'^\d{1,2}\.\d{1,2}$', date_str):
                month, day = date_str.split('.')
                result["collection_date"] = f"2025-{month.zfill(2)}-{day.zfill(2)}"
            else:
                result["collection_date"] = date_str
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
    print("数据已保存到数据库")

def get_collection_summary():
    """获取采集数据总览"""
    try:
        conn = sqlite3.connect('driver_data.db')
        df = pd.read_sql_query('SELECT * FROM driver_reports', conn)
        conn.close()
        
        if df.empty:
            return {'message': '暂无数据'}
        
        summary = {
            'total_reports': len(df),
            'total_drivers': df['driver_name'].nunique(),
            'total_segments': int(df['collection_segments'].sum()) if df['collection_segments'].notna().any() else 0,
            'total_distance': float(df['driving_distance'].sum()) if df['driving_distance'].notna().any() else 0,
            'locations': df['collection_location'].value_counts().to_dict(),
            'time_periods': df['collection_time_period'].value_counts().to_dict(),
            'latest_update': df['created_at'].max() if 'created_at' in df.columns else 'N/A'
        }
        
        return summary
    except Exception as e:
        return {'error': str(e)}

def main():
    # 初始化数据库
    init_database()
    
    # 解析并保存数据
    report_text = "采集员：方少东车辆编号：LY-005-31781采集任务：黄灯闪烁路口/与行人二轮车交互采集段数：70+采集地点：合肥采集日期：8.10采集时段：白天行驶里程:  273"
    
    print("正在解析司机汇报...")
    extracted_data = extract_with_rules(report_text)
    save_to_database(extracted_data, report_text)
    
    # 获取总览
    print("\n" + "="*50)
    summary = get_collection_summary()
    print('采集数据总览:')
    print('='*50)
    
    if 'error' in summary:
        print(f'错误: {summary["error"]}')
    elif 'message' in summary:
        print(summary['message'])
    else:
        print(f'总汇报数量: {summary["total_reports"]}')
        print(f'参与司机数: {summary["total_drivers"]}')
        print(f'总采集段数: {summary["total_segments"]}')
        print(f'总行驶里程: {summary["total_distance"]} 公里')
        print(f'最后更新时间: {summary["latest_update"]}')
        print()
        print('采集地点分布:')
        for location, count in summary['locations'].items():
            print(f'  {location}: {count} 次')
        print()
        print('采集时段分布:')
        for period, count in summary['time_periods'].items():
            print(f'  {period}: {count} 次')

if __name__ == "__main__":
    main()