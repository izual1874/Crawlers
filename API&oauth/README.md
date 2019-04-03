# 关于 API&oauth 1.0 签名的问题
- oauth 1.0
- 参考资料。https://oauth.net/core/1.0a/#RFC2617

#2/4-19
- 目前已经掌握，签名方法
- 但是，key 藏在哪里，没找到

#3/4-19
- 继续补全文档
- oauth 1.0 验证流程
    - 请求的连接，包含 get/post ，但不包含 oauth_signature， 经过quote 变为ase_str
    - HAMC-SHA1: 对base_str 加密。HMAC-SHA1 , 中间需要KEY。该码 经过 HEX() 转 16进制。
        ```python
        h_sha1 = Hmac_Sha1(sha1_key, base_str)
        print(h_sha1)
        print(len(h_sha1))
        ```
        ```python
        b51dfe4f2f3594c79802bfc589dd2431361afd63
        40
        ```
    - hmacsha1_urlencode: urlencode 转换会比之前增长 30% ，这里需要 base_64 编码。重点，编码前需要由16转为2进制. 然后在依次 urlencode编码。
        ```python
        print(to_2)
        b'\xb5\x1d\xfeO/5\x94\xc7\x98\x02\xbf\xc5\x89\xdd$16\x1a\xfdc'
        print(to_base64)
        b'tR3+Ty81lMeYAr/Fid0kMTYa/WM='
        ```
        ```python
        url_h_sha1 = hmacsha1_urlencode(h_sha1)
        print(url_h_sha1)
        print(len(url_h_sha1))
        ```
        ```python
        tR3%2BTy81lMeYAr/Fid0kMTYa/WM%3D
        32
        ```
    - urlencode_hmacsha1 : urlencode 编码 解码为 HMAC-SHA1

