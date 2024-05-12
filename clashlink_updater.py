import os
import json
import re
from datetime import datetime, timedelta
import yaml
from jinja2 import Environment, FileSystemLoader
import subprocess

# 加载项目配置
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
with open('config.json', 'r') as f:
    config = json.load(f)

# 获取当前日期
current_date = datetime.now()

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Step 1 & 2: 同时渲染URL模板和机场配置模板
airport_configs = []
airport_config_template = env.get_template('airport_config_template.jinja2')
url_template = env.get_template('url_template.jinja2')

for days_back in range(config['retain_days']):
    all_urls = []
    date = current_date - timedelta(days=days_back)

    # 渲染URL模板
    url = url_template.render(current_date=date)

    lines = url.split('\n')

    # 添加非注释行且非空的行到all_urls列表
    all_urls.extend([line for line in lines if line and not line.startswith('#')])

    # 渲染机场配置模板
    for url_index, urls_for_day in enumerate(all_urls):
        formatted_date = date.strftime('%y%m%d')  # 格式化日期为 'yyMMdd'
        airport_config = airport_config_template.render(
            url=urls_for_day,
            url_index=url_index,  # URL序号
            current_date=formatted_date
        )
        airport_configs.append(airport_config)

# Step 3: 替换clashlink.yaml中proxy-groups之前的内容为生成的机场配置
with open('clashlink.yaml', 'r+', encoding='utf-8') as f:
    file_content = f.read()

    # 查找proxy-groups出现的位置
    proxy_groups_start = re.search(r'^proxy-groups:', file_content, re.MULTILINE).start()
    original_proxy_groups_content = "\n\n# 策略组\n"+ file_content[proxy_groups_start:]

    # 在输出的开头添加指定文本
    header_text = "# 代理集合（获取机场订阅链接内的所有节点）\nproxy-providers:\n"

    # 替换proxy-groups之前的所有内容为生成的机场配置
    new_file_content = header_text + '\n\n'.join(airport_configs) + original_proxy_groups_content 

    f.seek(0)  # 将文件指针移动到文件开始位置
    f.write(new_file_content)  # 写入修改后的文件内容
    f.truncate()  # 裁剪文件以适应新的数据大小

# Step 4: 提交更新到Git仓库（假设已经配置好Git）
try:
    # 切换到项目根目录（假设当前脚本在项目根目录）
    subprocess.run(['git', 'checkout', 'main'], check=True)
    subprocess.run(['git', 'pull', 'origin', 'main'], check=True)  # 更新最新代码（可选）
    subprocess.run(['git', 'add', 'clashlink.yaml'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Update clashlink.yaml with the latest airport configurations'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)  # 推送到远程主分支
except subprocess.CalledProcessError as e:
    print(f"Git operation failed: {e}")

print("Clashlink configuration update completed.")