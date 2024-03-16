#!/bin/bash

# 获取脚本所在的相对目录
SCRIPT_DIR=$(dirname "$0")

# 在目录下生成 index.html 文件
find "$SCRIPT_DIR" -type d -execdir sh -c '
    local dir="$0"
    local content="<html>
<head>
<meta charset=\"utf-8\">
<title>$dir</title>
</head>
<body>
<h1>$dir</h1>
<hr>"

    # 添加上级目录链接
    if [[ "$dir" != "$SCRIPT_DIR" ]]; then
        content+="\n<a href=\"../\">../</a><br>"
    fi

    # 遍历目录中的文件和文件夹，添加链接
    local item
    for item in "$dir"/*; do
        item=${item##*/}
        if [[ -d $item ]]; then
            content+="\n<a href=\"$item/\">$item</a>/ (Directory)<br>"
            # 递归处理子目录（由于已经内联，不再需要函数调用）
            (
                cd "$item" || exit
                content+="\n$(generate_subindex)\n"
            )
        else
            content+="\n<a href=\"$item\">$item</a><br>"
        fi
    done

    content+="\n</body>
</html>"
    echo "$content" > index.html
' {} \;

generate_subindex() {
    local subdir=$1
    local subdir_content="<html>
<head>
<meta charset=\"utf-8\">
<title>$subdir</title>
</head>
<body>
<h1>$subdir</h1>
<hr>"

    # 在子目录中遍历文件和子目录
    # ... （重复 generate_index 函数中处理子目录的部分逻辑）

    subdir_content+="\n</body>
</html>"
    echo "$subdir_content"
}