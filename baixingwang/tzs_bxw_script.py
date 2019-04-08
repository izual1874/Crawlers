import json, pymongo, time
from mitmproxy import ctx

def response(flow):
    tzs_url = 'http://www.baixing.com/api/mobile/canyin/ad?'

    client = pymongo.MongoClient('localhost:27017')
    db = client['BXW']
    tzs_bxw = db['tzs_bxw']

    if tzs_url in flow.request.url:
        response = flow.response.text
        result = json.get('result')  #result is list
        for children in result:
            zero = children[0]
            display = zero.get('display')
            content = display.get('content')
            user = content.get('user')
            item = dict()
            item['tel'] = user.get('mobile')
            item['addr'] = (content.get('lat'), content.get('lng'))
            item['title'] = content.get('title')
            item['company'] = content.get('company')
            item['company_id'] = user.get('id')    #http://www.baixing.com/weishop/w198202633/
            item['subtitle'] = user.get('subtitle')
            item['stamp'] = content.get('time')
            item['id'] = content.get('source').get('id')  #http://shanghai.baixing.com/canyin/a1113294917.html?from=spb
            tzs_bxw.update({'id':item.get('id')}, {'$set':item}, True)