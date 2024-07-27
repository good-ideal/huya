import requests
import json
from gmssl import sm4, func
import base64

import execjs

key = b'fLdJQTGMDsUUTojn'

payload = json.dumps({
    "actId": "JZU172024060401",
    "openId": "+z488ZPgwCtMxRmkq9bzNDSm0ZIPzqpzVpDNmeP3niCC/TnQ+/1mrJZB2W+jvwQa"
})

headers = {
    'Host': 'gfss.fpsd.unionpay.com',
    'Cookie': 'route=94cdef37fe8f0a93d1dc55a633e1305d',
    'X-Tingyun': 'c=B|p35OnrDoP8k;x=0953057bf1974107',
    'Accept': 'application/json, text/plain, */*',
    'timestamp': '1722063445151',
    'nonce': '595100ce699b45a88ae308768cb151e1',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/json',
    'Origin': 'https://gfss.fpsd.unionpay.com',
    'Referer': 'https://gfss.fpsd.unionpay.com/gs-app/669f52330cf2479b4103bfb7/?id=5&appid=1ef7d0212fac49cf943c0b802ba40e91',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148  (com.unionpay.chsp) (cordova 4.5.4) (updebug 0) (version 1009) (UnionPay/1.0 CloudPay) (clientVersion 309) (language zh_CN) (languageFamily zh_CN) (upApplet single) (walletMode 00) ',
    'Content-Length': '103',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'sign': 'siKx1ezczZvmmoe5gv3mgn9PBcaSojRr9tY7dMa2/TThlc8N58LNbQJrYjZXGcKu'
    }

class Yun:
    
    # Ensure that the plaintext is a multiple of 16 bytes (128 bits) by padding if necessary
    def pad(self, text):
        # PKCS7 padding
        pad_len = 16 - (len(text) % 16)
        padding = chr(pad_len) * pad_len
        return text + padding

    # Unpadding function
    def unpad(self, text):
        pad_len = ord(text[-1])
        return text[:-pad_len]

    def search(self):
        #转json字符串
        encrypt_data = self.encrypt(json.dumps({
            "actId": "JZU172024060401",
            "openId": "+z488ZPgwCtMxRmkq9bzNDSm0ZIPzqpzVpDNmeP3niCC/TnQ+/1mrJZB2W+jvwQa"
        }))
        md5Str = self.md5(encrypt_data['n'])
        print("MD5: " + md5Str)
        print(encrypt_data['n'])

        # 将十六进制字符串转换为字节类型
        #需要加密的数据
        data = md5Str.encode('utf-8')
        
        # 创建SM4对象
        crypt_sm4 = sm4.CryptSM4()
        
        # 设置密钥和加密模式
        crypt_sm4.set_key(key, sm4.SM4_ENCRYPT)
        
        # 加密数据
        encrypt_value = crypt_sm4.crypt_ecb(data)
        
        # 将加密结果转换为Base64编码
        encrypt_base64 = base64.b64encode(encrypt_value).decode('utf-8')
        
        print('加密结果(Base64):', encrypt_base64)


        # # 将明文转换为字节类型
        # plaintext_bytes = bytes.fromhex(plaintext)

        # padded_plaintext = self.pad(plaintext_bytes)

        # # 创建SM4实例并设置密钥
        # cipher = sm4.CryptSM4()
        # cipher.set_key(key, sm4.SM4_ENCRYPT)

        # # 加密明文
        # encrypted_bytes = cipher.crypt_ecb(padded_plaintext)

        # # 将加密结果转换为Base64格式
        # base64_encrypted = base64.b64encode(encrypted_bytes).decode('utf-8')

        # # 输出加密结果
        # print(f'Encrypted (Base64): {base64_encrypted}')

        # Output the encrypted result
        # print(f'Encrypted (Base64): {base64_ciphertext}')
        # return

        headers['sign'] = encrypt_base64
        headers['nonce'] = encrypt_data['nonce']
        headers['timestamp'] = str(encrypt_data['timestamp'])
        print("SM4: " +  headers['sign'])
        # return
        response = requests.request("POST", 'https://gfss.fpsd.unionpay.com/gs-apply/apply/queryGraRecords', headers=headers, data=payload)
        # print(response.text)
        resp = json.loads(response.text)
        # 解析json
        if(resp['code'] == 200 and ('data' in resp) and len(resp["data"]) > 0):
            text = ''
            for data in resp["data"]:
                # print(data['graName'])
                # print('当前进度' + len(data['nodeList']))
                # print(len(data['nodeList']))
                #获取data['nodeList']有子节点个数
                if len(data['nodeList']) > 6:
                    # 发送通知 有新的结果
                    #遍历data['nodeList']的nodeName
                    for node in data['nodeList']:
                        text += node['nodeName'] + '\n'
                    # print(text)
                    self.sendMsg("yun", data['graName'] + '状态有变化，请速速查看', text)
    
    #传入一个字符串进行md5加密
    def md5(self, inputText):
        import hashlib
        m = hashlib.md5()
        m.update(inputText.encode('utf-8'))
        return m.hexdigest()


    #加密
    def encrypt(self, inputText):
            # 读取 JavaScript 文件内容
            with open("index.js", "r") as file:
                js_code = file.read()

            # 创建 JavaScript 环境并编译 JavaScript 代码
            ctx = execjs.compile(js_code)

            # 调用 JavaScript 函数
            return ctx.call("encrypt", inputText)

     # 推送消息到手机
    def sendMsg(self, group, title, msg):
        # icon = "https://www.huya.com/favicon.ico"
        icon = "https://cn.unionpay.com/upowhtml/cn/templates/material/a5817a4b821640e5a850c5b9da5687c7/1667786260807.png"
        # print('https://bark.s6.design/ZdrWZumT8QnPGUsmVjmg9k/{}/{}?group={}&icon={}'.format(title, msg, group, icon))
        requests.get(
            'https://bark.s6.design/ZdrWZumT8QnPGUsmVjmg9k/{}/{}?group={}&icon={}'.format(title, msg, group, icon))

if __name__ == '__main__':
    yun = Yun()
    yun.search()
    # 输出结果
    
    exit