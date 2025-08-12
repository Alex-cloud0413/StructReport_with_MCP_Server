#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
from datetime import datetime

def get_collection_summary():
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