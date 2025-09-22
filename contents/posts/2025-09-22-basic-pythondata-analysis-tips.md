# 基础数据获取
- 选择简单，静态，无登陆的网站
- 基础语法
```
import导入库
for...in...循环遍历找到所有元素
```
- **理解BS4**
```
用于解析requests拿回来的网页HTML代码
pip install requests beautifulsoup4
from bs4 import BeautifulSoup
# 使用BeautifulSoup解析html_text
soup = BeautifulSoup(html_text, 'html.parser')

# 找到所有class为‘item’的div元素，因为每个movie都在这样一个div里
movie_list = soup.find_all('div', class_='item')

# 循环遍历每一个div
for movie in movie_list:
    # 在当前movie div里，查找class为‘title’的span标签，并获取它的文本
    title = movie.find('span', class_='title').text
    
    # 查找class为‘rating_num’的span标签，获取评分
    rating = movie.find('span', class_='rating_num').text
    
    # 打印结果
    print(f"movie：{title}，level：{rating}")
```
## **获取网页内容**
- **不要把文件名称命名成和库的名称一样的名字**
- **注意事项**
1. 状态码418(I am a teapot)
```
#找到最新的user-agent f12-networkfirst-检查-useragent
```
2. requests
```
requests.get() → 单次请求，每次都是新的
session =requests.Session()
session.get() → 保持会话，会记住cookies等信息，更像浏览器
```
3. Selenium
- 它可以自动控制一个真正的浏览器（如Chrome）来访问网站
```
pip install selenium
```
- Message: binary is not a Firefox executable
```
Selenium 找不到正确的 Firefox 浏览器可执行文件路径。我们需要告诉它 Firefox 安装在哪里。
明确指定 Firefox 的安装路径
```
- 浏览器驱动geckodriver
```
# 检查Firefox版本
firefox --version
# 检查geckodriver版本
geckodriver --version
# 权限或者配置问题
which firefox 
which geckodriver
```
- webdriver-manager
```
# 验证安装
# 先确保pip是最新版本
pip install --upgrade pip
# 重新安装webdriver_manager
pip install --force-reinstall webdriver-manager
# 验证安装
python -c "import webdriver_manager; print('webdriver_manager安装成功')"
```
- 尊重robots.txt
```
在网站域名后加 /robots.txt（如https://douban.com/robots.txt）
```

- 数据存储：学习将获取的数据保存到CSV文件
```
if news_list:
            df = pd.DataFrame({'硬件资讯': news_list})
            df.to_csv('hardware_news.csv', index=False, encoding='utf-8-sig')
            print("\n💾 数据已保存到 hardware_news.csv")
```
- 自动定时运行; 简单可视化：学习用数据生成图表
```
1. import schedule
2. 系统级定时
crontab -e
# 添加以下行（每天9点、15点、21点各运行一次）
0 9,15,21 * * * /usr/bin/python3 /path/to/your/spider.py >> /path/to/spider.log 2>&1
```


