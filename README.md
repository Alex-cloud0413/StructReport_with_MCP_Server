# StrucReport with MCP Server

智驾数据采集汇总半自动化方案的MCP Server实现。

## 项目简介

本项目是一个基于MCP (Model Context Protocol) 的服务器，用于自动化处理智驾相关的数据采集、汇总和分析任务。

## 核心功能

### 🚗 智能数据解析
- **parse_driver_report**: 自动解析司机汇报文本，提取结构化数据
- 支持多种文本格式和字段顺序
- 智能识别错别字和缺失字段
- 自动数据验证和清洗

### 📊 数据管理
- **get_collection_summary**: 获取采集数据总览和统计信息
- **export_data_csv**: 导出数据为CSV格式
- SQLite数据库自动存储和管理
- 支持多种数据查询和汇总

### 🔧 技术特性
- 基于FastMCP框架的现代MCP服务器
- 异步处理支持
- 正则表达式 + 规则匹配的数据提取
- 可扩展的LLM集成接口

## 项目结构

```
driver-data-mcp-server/
├── venv/                 # Python虚拟环境
├── requirements.txt      # 项目依赖
├── README.md            # 项目说明文档
├── test_mcp_server.py   # MCP服务器功能测试
└── src/                 # 源代码目录
    ├── __init__.py
    └── main.py          # 核心MCP服务器实现
```

## 安装和运行

### 1. 激活虚拟环境
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行MCP服务器
```bash
python src/main.py
```

### 4. 测试功能
```bash
python test_mcp_server.py
```

## 使用示例

### 解析司机汇报文本
```python
from main import parse_driver_report

# 示例汇报文本
report_text = """
采集员：张三
车辆编号：京A12345
采集任务：城市道路数据采集
采集段数：5
采集地点：北京市朝阳区
采集日期：2025-01-10
采集时段：白天
行驶里程：120.5公里
"""

# 解析数据
result = await parse_driver_report(report_text)
print(result)
```

### 获取数据汇总
```python
from main import get_collection_summary

# 获取采集数据总览
summary = await get_collection_summary()
print(summary)
```

### 导出数据
```python
from main import export_data_csv

# 导出为CSV格式
export_result = await export_data_csv()
print(export_result)
```

## 数据库结构

```sql
CREATE TABLE driver_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_name TEXT,           -- 司机姓名
    vehicle_number TEXT,        -- 车辆编号
    collection_task TEXT,       -- 采集任务
    collection_segments INTEGER, -- 采集段数
    collection_location TEXT,   -- 采集地点
    collection_date TEXT,       -- 采集日期
    collection_time_period TEXT, -- 采集时段
    driving_distance REAL,      -- 行驶里程
    raw_text TEXT,             -- 原始文本
    created_at TIMESTAMP        -- 创建时间
);
```

## 开发状态

- [x] 项目结构创建
- [x] 核心MCP Server实现
- [x] 数据解析和提取功能
- [x] 数据库存储和管理
- [x] 数据汇总和导出
- [ ] LLM API集成
- [ ] 高级数据分析
- [ ] Web界面
- [ ] 测试和部署

## 下一步计划

1. **LLM集成**: 集成Claude、GPT等LLM API，提升文本解析准确性
2. **数据分析**: 添加数据可视化、趋势分析等功能
3. **Web界面**: 开发用户友好的Web管理界面
4. **API扩展**: 支持更多数据格式和来源
5. **性能优化**: 优化大数据量处理性能

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

MIT License

