import os
import json
import hashlib
import markdown

# 读取模板内容
template = '''
<html>
    <head>
    <meta charset="utf-8">
    <title>{full_path} - CrystalNekoの资源站</title>
    </head>
    <body>
        <h1>{full_path} - CrystalNekoの资源站</h1>
        <hr>
        {info}
        <hr>
        <a href="../">../<a></br>
        {content}
    </body>
</html>
'''

dir_template = '<a href="{dir_name}/index.html">{dir_name} (dir)</a></br>'
file_template = '<a href="{file_name}">{file_name}</a></br>'

def generate_index_html(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # 忽略以点开头的文件夹和文件
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        content = ''
        full_path = os.path.relpath(root, root_dir)
        for dir_name in dirs:
            content += dir_template.format(dir_name=dir_name)
        for file_name in files:
            content += file_template.format(file_name=file_name)

        # 生成info.json
        info = {"files": [], "dirs": []}

        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as f:
                file_content = f.read()
                sha256_hash = hashlib.sha256(file_content).hexdigest()
                info["files"].append({"name": file_name, "sha256": sha256_hash})

        for dir_name in dirs:
            info["dirs"].append({"name": dir_name})

        with open(os.path.join(root, 'info.json'), 'w') as info_file:
            json.dump(info, info_file, indent=4)

        # 读取并转换info.md文件为HTML
        info_md_path = os.path.join(root, 'info.md')
        if os.path.exists(info_md_path):
            with open(info_md_path, 'r', encoding='utf-8') as md_file:
                info_md_content = md_file.read()
                info_html_content = markdown.markdown(info_md_content)
                content += '<div>{}</div>'.format(info_html_content)

        index_content = template.format(full_path=full_path, content=content)
        with open(os.path.join(root, 'index.html'), 'w') as f:
            f.write(index_content)

generate_index_html('.')
