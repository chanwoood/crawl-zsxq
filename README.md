# 爬取知识星球，并制作成 PDF 电子书。


## 功能

爬取知识星球的精华区，并制作成 PDF 电子书。

## 效果图



![image.png | left | 827x448](https://cdn.yuque.com/yuque/0/2018/png/104735/1528856656437-1e9f1220-873e-41e4-8e8b-4bab75201244.png "")


## 模拟登陆

爬取的是网页版知识星球，[https://wx.zsxq.com/dweb/#](https://wx.zsxq.com/dweb/#)。
这个网站并不是依靠 cookie 来判断你是否登录，而是请求头中的 Authorization 字段。
所以，需要把 Authorization，User-Agent 换成你自己的。（注意 User-Agent 也要换成你自己的）

```python
headers = {
    'Authorization': '3704A4EE-377E-1C88-B031-0A42D9E9Bxxx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}
```

## 分析页面

登录成功后，一般我习惯右键、检查或者查看源代码。
但是这个页面比较特殊，它不把内容放到当前地址栏 URL 下，而是通过异步加载（XHR），只要找对接口就可以了。
精华区的接口：[https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&count=20](https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&count=20)
这个接口是最新 20 条数据的，还有后面数据对应不同接口，暂时还没搞。



![image.png | left | 827x710](https://cdn.yuque.com/yuque/0/2018/png/104735/1528857296860-38ce73bf-5ae7-406e-8462-10d1a298b8d0.png "")


## 制作 PDF 电子书

* 安装 wkhtmltox，[https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html) 。安装后将 bin 目录加入到环境变量。
* 安装相应依赖：pip install pdfkit
* 这个工具是把 HTML 文档转换为 PDF 格式。根据 HTML 文档中的 h 标签，也就是标题标签来自动提取出目录。
* 本来精华区是没有标题的，我把每个问题的前 6 个字符当做标题，以此区分不同问题。

## 目前还有很多问题，详见 Issues