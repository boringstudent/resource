document.addEventListener('DOMContentLoaded', function() {
    const baseUrl = window.location.origin; // 获取当前页面的域名

    document.querySelectorAll('a').forEach(function(link) {
        let href = link.getAttribute('href');

        if (href && href.startsWith('/') && !href.startsWith('//')) {
            // 处理相对路径
            link.addEventListener('click', function(e) {
                e.preventDefault(); // 阻止默认跳转行为
                window.location.href = baseUrl + href; // 手动跳转
            });
        }
    });
});

