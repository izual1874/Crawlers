
import requests  
import re  
import time  
from lxml import etree  
import csv  
import random
from urllib import parse  
    
fp = open('智联招聘.csv','wt',newline='',encoding='UTF-8')  
writer = csv.writer(fp)  
'''''地区，公司名，学历，岗位描述，薪资，福利，发布时间，工作经验，链接'''  
writer.writerow(('职位','公司','地区','学历','岗位','薪资','福利','工作经验','链接'))  
    
def info(SOU_POSITION_ID):  
    # res = requests.get(url)  
    # u = re.findall('<meta name="mobile-agent" content="format=html5; url=(.*?)" />', res.text)  
    
    # if len(u) > 0:  
        # u = u[-1]  
    # else:  
        # return  
    
    # u = 'http:' + u  
    # headers ={  
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'  
    # }  
    
    #重构 移动端 请求连接
    u = 'https://m.zhaopin.com/jobs/{}/'.format(SOU_POSITION_ID)
    #使用iPhone headers
    headers ={  
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'  
    }          
    res = requests.get(u, headers=headers)  
    selector = etree.HTML(res.text)  
    
    # # 岗位名称  
    # title = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/h1/text()')
    title = selector.xpath('//div[@class="about-position"]/div/h1/text()')
    # # 岗位薪资  
    # pay = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[1]/text()')  
    pay = selector.xpath('//div[@class="about-position"]//div[@class="job-sal fr"]/text()')
    # # 工作地点  
    # place = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[1]/text()')
    place = selector.xpath('//div[@class="companyAdd boxsizing"]/div/text()')  
    # # 公司名称  
    # companyName = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[2]/text()')
    companyName = selector.xpath('//div[@class="about-position"]/div[@class="comp-name"]/text()')  
    # # 学历  
    # edu = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[3]/text()')
    edu = selector.xpath('//div[@class="about-position"]//span[last()]/text()')  
    # # 福利  
    # walfare = selector.xpath('//*[@id="r_content"]/div[1]/div/div[3]/span/text()')
    walfare = selector.xpath('//div[@class="tag-list"]/span/text()')  
    # # 工作经验   
    # workEx = selector.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[2]/text()')
    workEx = selector.xpath('//div[@class="about-position"]//span[@class="exp"]/text()')  
    # # 岗位详细  
    # comment = selector.xpath('//*[@id="r_content"]/div[1]/div/article/div/p/text()')
    comment = selector.xpath('//div[@class="about-main"]/p/text()')  
    # # 连接
    siteUrl = res.url 
    writer.writerow((title, companyName, place, edu, comment, pay, walfare, workEx, siteUrl))  
    print(title, companyName, place, edu, comment, pay, walfare, workEx, siteUrl)  
    
def infoUrl(url):
    #加headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }  
    res = requests.get(url, headers= headers)  
    selector = res.json()
    #使用get  
    code = selector.get('code')  
    if code == 200:  
        data = selector['data']['results']  
        for i in data:  
            # href = i['positionURL']  
            # info(href) 
            # 提取ID 
            SOU_POSITION_ID = i['SOU_POSITION_ID']
            info(SOU_POSITION_ID)
            time.sleep(random.randrange(1,4))  
    
if __name__ == '__main__':  
    
    # url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=' + key + '&kt=3&lastUrlQuery=%7B%22pageSize%22:%2260%22,%22jl%22:%22489%22,%22kw%22:%22%E5%A4%A7%E6%95%B0%E6%8D%AE%22,%22kt%22:%223%22%7D'  

    #格式化字符串
    key = '大数据'      
    url = 'https://fe-api.zhaopin.com/c/i/sou?start={page}&pageSize=90&cityId=489&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={search}&kt=3&=0&_v=0.96800837&x-zp-page-request-id=e3f9167354464b00ae1d0bbe23d6bf26-1554266561356-56156'

    for i in range(1):
        page = 90*i
        json_url = url.format(page= page, search= parse.quote(key))
        infoUrl(json_url)
'''
https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&kt=3&=0&_v=0.96800837&x-zp-page-request-id=e3f9167354464b00ae1d0bbe23d6bf26-1554266561356-56156
'''

#https://sou.zhaopin.com/?jl=530&sf=0&st=0
# cityId=489, 后面的数字是地区编码 ，全国 489
# kw 要搜索内容
