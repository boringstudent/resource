#!/bin/bash

# 获取脚本所在的相对目录
SCRIPT_DIR=$(dirname "$0")

# 引用函数文件
source functions.sh

# 在当前目录及子目录下生成 index.html 文件
find "$SCRIPT_DIR" -type d -exec sh -c 'generate_index "$0" > "$0/index.html"' {} \;

