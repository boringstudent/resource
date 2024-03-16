find -type d -execdir bash -c '
# 生成目录索引的函数
generate_index() {
    local dir=$1
    local content="<html>
<head>
<meta charset=\"utf-8\">
<title>$dir</title>
</head>
<body>
<h1>/$dir</h1>
<hr>"
    
    # 添加上级目录链接
    if [[ "$dir" != "." ]]; then
        content+="<a href=\"../\">../</a><br>"
    fi

    # 遍历目录中的文件和文件夹，添加链接
    local item
    for item in *; do
        if [[ -d $item ]]; then
            content+="<a href=\"$item/\">$item</a>/ (Directory)<br>"
            # 递归调用生成子目录的索引
            (cd "$item" && generate_index "/$dir/$item")
        else
            content+="<a href=\"$item\">$item</a><br>"
        fi
    done

    content+="</body>
</html>"
    echo "$content" > index.html
}
generate_index "$(basename "$PWD")"' {} \;
