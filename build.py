import os

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

        index_content = template.format(full_path=full_path, content=content)
        with open(os.path.join(root, 'index.html'), 'w') as f:
            f.write(index_content)

generate_index_html('.')

