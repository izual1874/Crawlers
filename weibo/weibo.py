from selenium.webdriver import  Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import re, time
from lxml import etree
import pymongo
import requests
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
}
start_url = 'https://weibo.com/'
search_url = 'https://s.weibo.com/weibo?q=%E5%9B%BD%E5%BA%86&scope=ori&suball=1&timescope=custom:{start}:{end}'
#**************************************************
#mongo 设置
client = pymongo.MongoClient('192.168.17.129:27017')
db = client['WeiBo']
col_qd = db['WeiBo_QianDao']
col_qd.create_index([('weibo_url', pymongo.ASCENDING)])

def save_qd(item):
    col_qd.update({'weibo_url': item.get('weibo_url')}, {'$set': item}, True)
def close_mongo():
    client.close()
#*********************************************
#保存， response 最好是str
def save_datas(response):
    item = {}
    if not isinstance(response, str):
        response = response.text
    cards = re.findall('<!--card-wrap-->(.*?)<!--/card-wrap-->', response, re.S)
    print('该页有 {}条。'.format(len(cards)))
    for card in cards:
        html = etree.HTML(card)
        uid = html.xpath('//div[@class="avator"]/a/@href')[0]
        item['uid'] = re.findall('/(\d+)\?', uid)[0]
        item['name'] = html.xpath('//a[@class="name"]/@nick-name')[0]
        item['location'] = html.xpath('//p[@class="txt"]/a/i[contains(text(),"2")]/../text()')
        item['location_url'] = html.xpath('//p[@class="txt"]/a/i[contains(text(),"2")]/../@href')
        dates= html.xpath('//p[@class="from"]/a[1]/text()')[0]
        item['dates'] = re.findall('(\d+年\d+月\d+日 \d+:\d+)', dates)
        item['device'] = html.xpath('//p/a[@rel="nofollow"]/text()')
        item['weibo_url'] = html.xpath('//p[@class="from"]/a[1]/@href')[0]
        # print(item)
        if html.xpath('//p[@class="txt"]/a/i[@class="wbicon"]/text()=2'):
            save_qd(item)
#***************************************************
# 获取 cookies
def get_cookies(num):
    # user = '14785107068'
    # pwd = 'lxq69688'
    n = num % 2
    users = ['hua327145@163.com----ZJOstb254Cl', '14785107068----lxq69688']
    user = users[n]
    one_user = (user).split('----')
    user, pwd = one_user[0], one_user[1]
    option = FirefoxProfile()
    option.set_preference("dom.webnotifications.enabled",False)
    browser = Firefox(option)
    wait = WebDriverWait(browser, 120)
    browser.delete_all_cookies()
    browser.get(start_url)
    submit = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="W_login_form"]/div[@class="info_list login_btn"]/a')))
    sleep(1)
    submit.click()
    user_element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="loginname"]')))
    # user_element.clear()
    sleep(1)
    user_element.send_keys(user)
    print('账号:', user)
    pwd_element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    # pwd_element.clear()
    sleep(1)
    pwd_element.send_keys(pwd)
    print('密码:', pwd)
    submit = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="W_login_form"]/div[@class="info_list login_btn"]/a')))
    submit.click()
    print('点击登陆！')
    # sleep(2)
    user_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="gn_nav_list"]/li[5]//em[2]')))
    print('登陆用户：', user_btn.text)
    #条件 确认是否登陆
    cookies = browser.get_cookies()
    cookie = ';'.join(i['name'] + '=' + i['value'] for i in cookies)
    browser.close()
    cookies = {
        'Cookie': cookie,
    }
    return cookies
#***************************************************
# 请求该页及下一页
def request_next(url):
    global headers, cookies
    response = requests.get(url, cookies= cookies, headers= headers)
    if response.status_code == 200:
        save_datas(response)
        response = etree.HTML(response.text)            #下一页
        pages = response.xpath('//ul[@class="s-scroll"]/li/a/@href')
        next_page = response.xpath('//div[@class="m-page"]//a[@class="next"]/@href')
        if next_page != []:
            next_page = next_page[0]
            if next_page in pages:
                next_url = 'https://s.weibo.com' + next_page
                sleep(2)
                # print(next_url)
                now_crawl = re.findall('2018-(.*?):2018-(.*?)&page=(\d+)', next_url)
                print('抓取到：', now_crawl)
                return request_next(next_url)
    elif response.status_code in [302, 403, 504]:
        cookies = get_cookies(random.choice([0,1]))
        return request_next(url)

#*****************************************************
def start_date():
    start_stamp = 1514736600.0
    time_str = '%Y-%M-%d-%H'
    for i in range(167):
        start_time = time.strftime(time_str, time.localtime(float(start_stamp)))
        end_time = time.strftime(time_str, time.localtime(float(start_stamp + 3600)))
        start_stamp += 3600
        # print(start_time, '*'*20, end_time )
        yield (start_time, end_time)


#****************************************************
if __name__ == '__mian__':
    count = 0
    num = 1
    cookies = get_cookies(num)
    for date in start_date():
        url = search_url.format(start=date[0], end=date[1])
        count += 1
        if count == 3:
            count = 0
            num += 1
            sleep(3)
            cookies = get_cookies(num)
            request_next(url)

        close_mongo()