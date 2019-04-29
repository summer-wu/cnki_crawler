# readme
+ 帮网友查文献引用数，就是【发现123条结果】这里的123。因为数据量太多，六千多条，所以考虑用程序实现。
+ 一开始想用http请求，后来发现cnki做了很多限制，无法简单发请求。所以改为selenium控制浏览器

# 文件
+ bookdata目录，原始数据。
+ fetchedHTML目录，保存从cnki抓取下来的数据
+ final目录，最终结果。
+ cnkiDriver.py 驱动chrome点击页面、输入文字
+ fetcher.py 循环下载
+ htmlParser.py 全部下载完毕后，解析html文件
+ selenium01.side 它是Selenium IDE（chrome extension）生成的文件，只是辅助写程序。

# 原始数据
+ 原始数据中有 书名、作者。程序中只使用书名查询。
