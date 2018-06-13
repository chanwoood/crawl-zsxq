import requests
import json
import os
import pdfkit

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h3>{title}</h3>
<p>{text}</p>
</body>
</html>
"""

def get_data():

    url = 'https://api.zsxq.com/v1.10/groups/2421112121/topics?scope=digests&count=20'
        
    headers = {
        'Authorization': '3704A4EE-377E-1C88-B030-0A42D9E9Bxxx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    rsp = requests.get(url, headers=headers)
    with open('stormzhang.json', 'w', encoding='utf-8') as f:        # 将返回数据写入 a.json 方便查看
        f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))

    htmls = []
    with open('stormzhang.json', encoding='utf-8') as f:
        for topic in json.loads(f.read()).get('resp_data').get('topics'):
            content = topic.get('question', topic.get('talk', topic.get('task')))
            # print(content)
            text = content.get('text')
            title = text[:6]
            html = html_template.format(title=title, text=text)
            htmls.append(html)
    return htmls

def make_pdf(htmls):
    html_files = []
    for index, html in enumerate(htmls):
        file = str(index) + ".html"
        html_files.append(file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)

    options = {
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [
            ("cookie-name1", "cookie-value1"), ("cookie-name2", "cookie-value2")
        ],
        "outline-depth": 10,
    }
    try:
        pdfkit.from_file(html_files, "stormzhang.pdf", options=options)
    except Exception as e:
        print(e)

    for file in html_files:
        os.remove(file)

    print("已制作电子书 stormzhang.pdf 在当前目录！")
    
if __name__ == '__main__':
    make_pdf(get_data())