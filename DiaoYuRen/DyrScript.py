import json, pymongo, time
from mitmproxy import ctx

def response(flow):
    fishings_url = 'https://api.diaoyu.com/app/fishings/locallist'
    shops_url = 'https://api.diaoyu.com/app/fishingshops/locallist'
    client = pymongo.MongoClient('47.99.205.188:27017')
    db = client['DYR']
    shop_col = db['DyrShops']
    shop_col.create_index([('shop_id', pymongo.ASCENDING)])
    fishings_col = db['Dyrfishings']
    fishings_col.create_index([('fishing_id', pymongo.ASCENDING)])
    # ctx.log.info('开始')
    if shops_url in flow.request.url:
        responses = flow.response.text
        result = json.loads(responses)
        data = result.get('data')
        if data != "":
            for shop in data.get('shops'):
                item = {}
                baseInfo = shop.get('baseInfo')
                item['shop_id'] = baseInfo.get('shop_id')
                item['name'] = baseInfo.get('name')
                item['thumb'] = baseInfo.get('thumb')
                item['status'] = baseInfo.get('status')
                item['score'] = baseInfo.get('score')
                item['service_status'] = baseInfo.get('service_status')
                item['address'] = baseInfo.get('address')
                item['business'] = baseInfo.get('business')
                item['telephone'] = baseInfo.get('telephone')
                item['phone_verify'] = baseInfo.get('phone_verify')
                item['admin_id'] = baseInfo.get('admin_id')
                item['desc'] = baseInfo.get('desc')
                item['region_city'] = baseInfo.get('region_city')
                item['location'] = baseInfo.get('location')
                item['format_time'] = baseInfo.get('format_time')

                shop_col.update({'shop_id': item.get('shop_id')},{'$set': item}, True)
                ctx.log.info(str(item['shop_id']))
        else:
            ctx.log.info(str(flow.response.url))

    elif fishings_url in flow.request.url:
        responses = flow.response.text
        result = json.loads(responses)
        data = result.get('data')
        if data != "":
            for fishing in data.get('fishings'):
                item = {}
                baseInfo = fishing.get('baseInfo')
                item['fishing_id'] = baseInfo.get('fishing_id')
                item['name'] = baseInfo.get('name')
                item['thumb'] = baseInfo.get('thumb')
                item['price'] = baseInfo.get('price')
                item['status'] = baseInfo.get('status')
                item['service_status'] = baseInfo.get('service_status')
                item['address'] = baseInfo.get('address')
                item['business'] = baseInfo.get('business')
                item['telephone'] = baseInfo.get('telephone')
                item['phone_verify'] = baseInfo.get('phone_verify')
                item['admin_id'] = baseInfo.get('admin_id')
                item['desc'] = baseInfo.get('desc')
                item['fishing_type'] = baseInfo.get('fishing_type')
                item['fishing_activities'] = baseInfo.get('fishing_activities')
                item['fishs'] = baseInfo.get('fishs')
                item['score'] = baseInfo.get('score')
                item['is_charge'] = baseInfo.get('is_charge')
                item['region_city'] = baseInfo.get('region_city')
                item['location'] = baseInfo.get('location')
                item['format_time'] = baseInfo.get('format_time')
                item['distance'] = baseInfo.get('distance')

                fishings_col.update({'fishing_id': item.get('fishing_id')}, {'$set': item}, True)
                ctx.log.info(str(item['fishing_id']))
        else:
            ctx.log.info(str(flow.response.url))



