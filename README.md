# clashlink-updater

**clashlink-updater** 是一个 Python 项目，旨在每天定时根据指定的 URL 模板和机场配置模板，生成并更新 `clashlink.yaml` 订阅配置文件，以便为 Clash 客户端提供最新的代理配置。

## 功能概述

- **定时任务**：每天按照预定时间自动执行更新流程。
- **URL 模板渲染**：根据提供的 URL 模板和参数，动态生成获取机场配置数据的 URL。
- **数据获取**：通过 HTTP 请求获取机场配置数据。
- **机场配置模板渲染**：使用 Jinja2 模板引擎，根据机场配置模板和实际数据，生成 Clash 兼容的机场配置。
- **配置文件更新**：将生成的机场配置合并到 `clashlink.yaml` 文件中，同时根据保留天数清理过期配置。
- **日志记录**：详细记录程序运行状态、错误信息和重要操作，便于问题排查。

## 快速开始

### 环境要求

- Python 3.8+ (推荐使用最新稳定版)
- 请确保已安装项目所需的依赖库，可通过运行以下命令安装：
```bash
pip install -r requirements.txt

### 配置说明
编辑 config.json 文件以适应您的需求。该文件包含以下配置项：

url_template: URL 模板字符串，使用 Jinja2 语法。
airport_config_template: 机场配置模板字符串，同样使用 Jinja2 语法。
retain_days: 保留配置的天数，超过此天数的旧配置将被清理。
（其他可能的配置项，如请求超时、代理设置等）

### 运行项目
在命令行中，导航到项目根目录并运行主程序：

bash
python clashlink_updater.py

### 定时任务设置
为了实现每日定时自动更新，请根据您的操作系统设置定时任务（如 Windows 的任务计划程序、Linux 的 cron 作业等），确保每天在期望的时间执行上述命令。

### 贡献与反馈
欢迎对项目提出改进建议、报告问题或贡献代码。如有任何疑问或需要帮助，请在 GitHub 上创建 issue 或直接联系项目维护者。

### 版权与许可
clashlink-updater 项目采用 MIT License 开源发布。使用时请遵守相关条款。

Copyright © [Spincat] and contributors. All rights reserved.