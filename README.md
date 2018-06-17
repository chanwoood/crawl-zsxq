# 爬取知识星球，并制作成 PDF 电子书。


## 功能

爬取知识星球的精华区，并制作成 PDF 电子书。

## 效果图

![效果图.png](https://upload-images.jianshu.io/upload_images/5690299-7aac8142d7794a17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 用法

```python
if __name__ == '__main__':
    start_url = 'https://api.zsxq.com/v1.10/groups/454584445828/topics?scope=digests&count=20'
    make_pdf(get_data(start_url))
```

把 start_url 改为你需要爬取的星球的相应 url 。

还有安装好 wkhtmltox ，参考后面的「制作 PDF 电子书」。

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

这个接口是最新 20 条数据的，还有后面数据对应不同接口，这就是后面要说的翻页。

![image.png | left | 827x710](https://cdn.yuque.com/yuque/0/2018/png/104735/1528857296860-38ce73bf-5ae7-406e-8462-10d1a298b8d0.png "")


## 制作 PDF 电子书

* 安装 wkhtmltox，[https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html) 。安装后将 bin 目录加入到环境变量。
* 安装相应依赖：pip install pdfkit
* 这个工具是把 HTML 文档转换为 PDF 格式。根据 HTML 文档中的 h 标签，也就是标题标签来自动提取出目录。
* 本来精华区是没有标题的，我把每个问题的前 6 个字符当做标题，以此区分不同问题。






下面进阶完美操作：
## 爬取图片

很明显，在返回的数据中的 images 键就是图片，只需提取 large 的，即高清的 url 即可。

关键在于将图片标签 img 插入到 HTML 文档。

我使用 BeautifulSoup 操纵 DOM 的方式。

需要注意的是，有可能图片不止一张，所以需要用 for 循环全部迭代出来

```python
if content.get('images'):
    soup = BeautifulSoup(html_template, 'html.parser')
    for img in content.get('images'):
        url = img.get('large').get('url')
        img_tag = soup.new_tag('img', src=url)
        soup.body.append(img_tag)
        html_img = str(soup)
        html = html_img.format(title=title, text=text)
```

## 翻页问题

* [https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&count=20&end\_time=2018-04-12T15%3A49%3A13.443%2B0800](https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&amp;count=20&amp;end_time=2018-04-12T15%3A49%3A13.443%2B0800)

* 路径后面的 end_time 表示加载帖子的最后日期，以此达到翻页。

* 这个 end_time 是经过 url 转义了的，可以通过 urllib.parse.quote 方法进行转义，关键是找出这个 end_time 是从那里来的。

* 经过我细细观察发现：每次请求返回 20 条帖子，最后一条贴子就与下一条链接的 end_time 有关系。

* 例如最后一条帖子的 create_time 是 2018-01-10T11:49:39.668+0800，那么下一条链接的 end\_time 就是 2018-01-10T11:49:39.667+0800，注意，一个 668，一个 667 , 两者相差 1。
```python
end_time = create_time[:20]+str(int(create_time[20:23])-1)+create_time[23:]
```

* 翻页到最后返回的数据是：
```json
{"succeeded":true,"resp_data":{"topics":[]}}
```

故以 `next_page = rsp.json().get('resp_data').get('topics')` 来判断是否有下一页。

## 制作精美 PDF

通过 css 样式来控制字体大小、布局、颜色等，详见 test.css 文件。

再将此文件引入到 options 字段中。

```python
    options = {
        "user-style-sheet": "test.css",
        ...
        }
```

## 最难搞的问题是：Old iron, give me a star ! ! !