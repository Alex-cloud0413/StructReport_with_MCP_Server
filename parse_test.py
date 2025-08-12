#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
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
    
    # 采集段数提取（提取数字，包括70+这种格式）
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
            # 处理8.10这种格式，转换为2025-08-10
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

def main():
    report_text = "采集员：方少东车辆编号：LY-005-31781采集任务：黄灯闪烁路口/与行人二轮车交互采集段数：70+采集地点：合肥采集日期：8.10采集时段：白天行驶里程:  273"
    
    print("原始汇报文本:")
    print(report_text)
    print("\n" + "="*50 + "\n")
    
    result = extract_with_rules(report_text)
    
    print("解析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n" + "="*50 + "\n")
    print("格式化输出:")
    print(f"采集员: {result['driver_name']}")
    print(f"车辆编号: {result['vehicle_number']}")
    print(f"采集任务: {result['collection_task']}")
    print(f"采集段数: {result['collection_segments']}")
    print(f"采集地点: {result['collection_location']}")
    print(f"采集日期: {result['collection_date']}")
    print(f"采集时段: {result['collection_time_period']}")
    print(f"行驶里程: {result['driving_distance']} 公里")

if __name__ == "__main__":
    main()