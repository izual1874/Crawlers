from urllib import parse
import base64
import hmac, hashlib

base_str = 'GET&http%3A%2F%2Fphotos.example.net%2Fphotos&file%3Dvacation.jpg%26oauth_consumer_key%3Ddpf43f3p2l4k3l03%26oauth_nonce%3Dkllo9940pd9333jh%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1191242096%26oauth_token%3Dnnch734d00sl2jdk%26oauth_version%3D1.0%26size%3Doriginal'
sha1_key = 'kd94hf93k423kf44&pfkkdhi9sl3r4s00'
oauth_signature="tR3%2BTy81lMeYAr%2FFid0kMTYa%2FWM%3D"


# get HMAC-SHA1
def Hmac_Sha1(key, base_str):
    import hmac, hashlib
    key = key.encode('utf8')
    base_str = base_str.encode('utf8')
    Hmac = hmac.new(key, base_str, hashlib.sha1)
    Hmac = Hmac.digest()
    return Hmac.hex()

def hmacsha1_urlencode(hmacsha1):
    to_2 = bytes.fromhex(hmacsha1)
    to_base64 = base64.b64encode(to_2)
    to_urlencode = parse.quote(to_base64)
    return to_urlencode

def urlencode_hmacsha1(encode_str):
    un_url = parse.unquote(encode_str)
    un_base64 = base64.b64decode(un_url.encode('utf8'))
    to_hex = un_base64.hex()
    return to_hex

a = '%2F9aBPAqTZ9pOxNtRmkDJ8Ci111A%3D'
print(urlencode_hmacsha1(a))