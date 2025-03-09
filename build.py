import datetime
import os
import json
import hashlib
import markdown
import shutil

# 读取模板内容
template = """
<html>
    <head>
        <meta charset="utf-8">
        <title>{full_path} - CrystalNekoの资源站</title>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: url('https://www.loliapi.com/acg') fixed;
                background-size: cover;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
            }}
            .entry {{
                text-decoration: none !important;
                color: #333 !important;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                margin: 8px 0;
                background: rgba(245, 245, 245, 0.9);
                border-radius: 8px;
                transition: all 0.3s;
            }}
            .entry:hover {{
                transform: translateX(10px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                background: rgba(235, 245, 255, 0.9);
            }}
            .file-info {{
                display: flex;
                gap: 15px;
                color: #666;
                font-size: 0.9em;
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }}
            a {{
                color: #2c82c9;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📁 {full_path}</h1>
            {info}
            <div style="margin: 20px 0;">
                <a href="../" style="font-size: 1.1em;">⬆ 上级目录</a>
            </div>
            {content}
            <hr>
            <div style="text-align: center;">
                <img src="https://moe-counter.glitch.me/get/@CrystalNeko" alt="访问计数">
            </div>
        </div>
    </body>
</html>
"""

dir_template = """
<a href="{dir_name}/index.html" class="entry">
    <span>📂 {dir_name}</span>
    <span class="file-info">
        <span>{size}</span>
    </span>
</a>
"""

file_template = """
<a href="{file_name}" class="entry">
    <span>📄 {file_name}</span>
    <span class="file-info">
        <span>{size}</span>
        <span>{mtime}</span>
    </span>
</a>
"""

def get_dir_size(start_path):  # 新增目录大小计算函数
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}PB"


def copy_files(source_dir, output_dir):
    """将非隐藏文件/目录复制到output目录"""
    for root, dirs, files in os.walk(source_dir):
        # 排除隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # 排除隐藏文件
        files = [f for f in files if not f.startswith('.')]

        # 计算目标路径
        rel_path = os.path.relpath(root, source_dir)
        dest_dir = os.path.join(output_dir, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        # 复制文件
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy2(src, dst)

def generate_index_html(root_dir):
    """在指定目录生成索引文件"""
    for root, dirs, files in os.walk(root_dir):
        # 忽略隐藏文件和目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # 计算路径信息
        rel_path = os.path.relpath(root, root_dir)
        full_path = rel_path if rel_path != '.' else ''

        content = ''
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            dir_size = format_size(get_dir_size(dir_path))
            content += dir_template.format(dir_name=dir_name, size=dir_size)
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md']:
                file_path = os.path.join(root, file_name)
                file_size = format_size(os.path.getsize(file_path))
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                content += file_template.format(
                    file_name=file_name,
                    size=file_size,
                    mtime=mtime
                )

        # 生成info.json
        info = {"files": [], "dirs": []}
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md']:
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path)
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                with open(file_path, 'rb') as f:
                    sha256_hash = hashlib.sha256(f.read()).hexdigest()
                info["files"].append({
                    "name": file_name,
                    "sha256": sha256_hash,
                    "size": file_size,
                    "mtime": mtime
                })
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            dir_size = get_dir_size(dir_path)
            info["dirs"].append({
                "name": dir_name,
                "size": dir_size
            })

        # 写入info.json
        with open(os.path.join(root, 'info.json'), 'w') as f:
            json.dump(info, f, indent=4)

        # 处理info.md
        info_md_path = os.path.join(root, 'info.md')
        info_placeholder = ''
        if os.path.exists(info_md_path):
            with open(info_md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                info_html = markdown.markdown(md_content)
                info_placeholder = f'<div>{info_html}</div>'

        # 生成index.html
        index_content = template.format(
            full_path=full_path or 'Home',
            content=content,
            info=info_placeholder
        )
        with open(os.path.join(root, 'index.html'), 'w') as f:
            f.write(index_content)

if __name__ == "__main__":
    source_dir = '.'  # 源目录
    output_dir = 'output'  # 输出目录

    # 创建output目录
    os.makedirs(output_dir, exist_ok=True)

    # 复制文件到output目录
    copy_files(source_dir, output_dir)

    # 生成索引文件（以output目录为根）
    generate_index_html(output_dir)