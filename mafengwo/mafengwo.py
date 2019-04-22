from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import requests, re
import pymongo
from time import sleep

client = pymongo.MongoClient('192.168.17.129:27017')
db = client['mafengwo']
col = db['shanxizijia']
col.create_index([('uid_url', pymongo.ASCENDING)])

url = 'http://www.mafengwo.cn/i/7984212.html'
mfw_url = 'http://www.mafengwo.cn/search/q.php?q=%E9%99%95%E8%A5%BF%E8%87%AA%E9%A9%BE%E6%B8%B8&p={page}&t=notes&kt=1'
# url2 = 'http://www.mafengwo.cn/search/q.php?q=%E9%99%95%E8%A5%BF%E8%87%AA%E9%A9%BE%E6%B8%B8&t=notes&seid=381BDA8E-AC12-44F4-883F-8E9DE038F333&mxid=&mid=&mname=&kt=1'
option = Options()
option.add_argument('--headless')
browser = Chrome(options=option)
# browser = Chrome()
wait = WebDriverWait(browser, 10)
def wait_all_elements(data):
    global wait
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, data)))
    return elements
def wait_element(data):
    global wait
    element = wait.until(EC.presence_of_element_located((By.XPATH, data)))
    return element
def get_data(url):
    try:
        browser.get(url)
        item = {}
        title = wait_element('//h1[@style="white-space: nowrap; overflow-wrap: normal;"]')
        other = wait_all_elements('//div[@class="tarvel_dir_list clearfix"]/ul/li')
        line = wait_all_elements('//a[@class="catalog_line _j_cataloglink"]')
        uid = wait_element('//div[@data-cs-t="ginfo_person_operate"]/a')
        name = wait_element('//div[@data-cs-t="ginfo_person_operate"]/strong/a')
        # content = wait_all_elements('//p[@class="_j_note_content _j_seqitem"]')
        # 动态加载 http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=7984212&iid=267680502&seq=268538593&back=0
        item['title'] = title.text
        item['other'] = [i.text for i in other]
        # item['line'] = [i.text for i in line]
        item['line'] = [i.get_attribute('title') for i in line]
        item['uid_url'] = uid.get_attribute('href')
        item['name'] = name.text
        # item['content'] = [i.text for i in content]
        print(item)
        return item
    except Exception as e:
        print(e)
        return False

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
}
cookies = {
    'Cookie': 'mfw_uuid=5cb9d09c-2a49-c228-5659-9fdfac896e75; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1555681436%3B%7D; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A19%3A%22pagelet.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-04-21+11%3A50%3A34%22%3B%7D; __mfwothchid=referrer%7Cwww.baidu.com; __mfwlv=1555836468; __mfwvn=6; __mfwlt=1555839805; uva=s%3A264%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-04-19%22%3Bs%3A2%3A%22lt%22%3Bi%3A1555681438%3Bs%3A10%3A%22last_refer%22%3Bs%3A137%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Doz_Ipvv0o8U8V8RuqSfavwNZbC1VcmmuUIjtqlTKfls9NR2fOpZokRWF5h-iIVtD%26wd%3D%26eqid%3Df053a4ac001001d8000000055cb9d090%22%3Bs%3A5%3A%22rhost%22%3Bs%3A13%3A%22www.baidu.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1555681438%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A13%3A%22www.baidu.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5cb9d09c-2a49-c228-5659-9fdfac896e75; UM_distinctid=16a35d6e484158-05dc27c53d65b9-4c312c7c-144000-16a35d6e48523f; CNZZDATA30065558=cnzz_eid%3D1326230818-1555679707-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1555837457; PHPSESSID=nkukk6jcursj9gmt7a3i9nju82; mafengwo=01d15b2d6cff958a44f850bf447aca5e_5176135_5cbbd6808e7457.49263088_5cbbd6808e7484.87762611; mfw_uid=5176135; uol_throttle=5176135',
}
for i in range(9, 16):  #8未完
    try:
        page_url = mfw_url.format(page=i)
        resp = requests.get(page_url, headers= headers, cookies= cookies)
        data = etree.HTML(resp.text)
        urls = data.xpath('//div[@class="att-list"]/ul/li//h3/a/@href')
        # print(urls)
        for url in urls:
            item = get_data(url)
            if item != False:
                col.update({'uid_url':item['uid_url']}, {'$set':item}, True)
                sleep(4)
    except Exception as e:
        print(e)

# get_data(url)
# browser.get(url)


browser.close()
