#!/bin/bash

# 获取当前目录
CURRENT_DIR=$(pwd)

# 构建文件和文件夹列表
FILES_AND_DIRS=$(ls -1)

# 构建 HTML 内容
HTML_CONTENT="<!DOCTYPE HTML>
<html>
<head>
<meta charset=\"utf-8\">
<title>$CURRENT_DIR</title>
</head>
<body>
<h1>$CURRENT_DIR</h1>
<hr>"

# 添加上级目录链接
HTML_CONTENT+="\n<a href=\"../\">../</a><br>"

# 遍历文件和文件夹，添加链接
while IFS= read -r ITEM; do
    HTML_CONTENT+="\n<a href=\"$ITEM\">$ITEM</a><br>"
done <<< "$FILES_AND_DIRS"

HTML_CONTENT+="\n</body>
</html>"

# 在当前目录及子目录下添加 index.html 文件
find . -type d -exec sh -c 'echo "$0" > "$0/index.html"' {} \;

# 在当前目录及子目录下添加 index.html 文件的内容
find . -type f -name 'index.html' -exec sh -c "echo '$HTML_CONTENT' > {}" \;

