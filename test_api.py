#!/usr/bin/env python3
# 测试 API 服务器
import requests
import json
import time

def test_api_server():
    """测试 API 服务器功能"""
    base_url = "http://localhost:8080"
    
    print("🧪 开始测试 API 服务器...")
    
    # 1. 测试健康检查
    print("\n📍 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"响应: {response.json()}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("💡 请先启动 API 服务器: python src/api_server.py")
        return False
    
    # 2. 测试根路径
    print("\n📍 测试根路径...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 根路径访问成功")
            print(f"API 信息: {response.json()}")
        else:
            print(f"❌ 根路径访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 根路径测试失败: {e}")
    
    # 3. 测试数据解析 API
    print("\n📊 测试数据解析 API...")
    test_data = {
        "report_text": """
        采集员：测试司机
        车辆编号：测试A001
        采集任务：API测试任务
        采集段数：3
        采集地点：测试城市
        采集日期：2025-01-10
        采集时段：白天
        行驶里程：88.8公里
        """
    }
    
    try:
        response = requests.post(f"{base_url}/rpc/parse_driver_report", json=test_data)
        if response.status_code == 200:
            print("✅ 数据解析 API 测试成功")
            result = response.json()
            print(f"解析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 数据解析 API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 数据解析 API 测试异常: {e}")
    
    # 4. 测试数据汇总 API
    print("\n📈 测试数据汇总 API...")
    try:
        response = requests.get(f"{base_url}/rpc/get_collection_summary")
        if response.status_code == 200:
            print("✅ 数据汇总 API 测试成功")
            result = response.json()
            print(f"汇总结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 数据汇总 API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 数据汇总 API 测试异常: {e}")
    
    # 5. 测试数据导出 API
    print("\n📤 测试数据导出 API...")
    try:
        response = requests.get(f"{base_url}/rpc/export_data_csv")
        if response.status_code == 200:
            print("✅ 数据导出 API 测试成功")
            result = response.json()
            print(f"导出结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 数据导出 API 测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 数据导出 API 测试异常: {e}")
    
    print("\n🎉 API 服务器测试完成！")
    return True

if __name__ == "__main__":
    test_api_server()