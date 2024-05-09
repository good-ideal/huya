import requests
import json
import sys

import execjs



url = "https://api.tfxing.com/interCity/customer"

payload = json.dumps({
    "optid": "get_classes_list",
    "terminal": "1",
    "version": "4",
    "common_param": {
        "page_index": "1",
        "page_size": "999",
        "is_paging": "1",
        "is_couting": "0"
    },
    "business_param": {
        "start_area_id": "2370",
        "arrive_area_id": "2380",
        "start_date": "2024-05-11",
        "get_on_site_id": 86,
        "get_down_site_id": -1,
        "send_time": "18:00-21:00",
        "line_sub_id": ''
    }
})

# 86 = 驷马桥地铁站

headers = {
  'Host': 'api.tfxing.com',
  'Origin': 'https://www.tfxing.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Referer': 'https://www.tfxing.com',
  'Connection': 'keep-alive',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Accept': 'application/json, text/plain, */*',
  'Content-Type': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br, zstd'
}

class TianFu:
       
    def search(self):
        encrypt_data = self.encrypt(payload)
        response = requests.request("POST", url, headers=headers, data=encrypt_data)
        # print(response.text)
        result = self.decrypt(response.text)
        resp = result
        # 解析json
        if(resp['result_state'] == 0 and ('result' in resp) and len(resp["result"]) > 0):
            text = '';
            searchData = json.loads(payload)
            for promotion in resp["result"]:
                # 0 有票 1 无票  is_sell_out
                if(promotion["is_sell_out"] == 0):
                    # 余票多少？
                    text += (promotion["header_tag"] + " 发车时间："+ promotion['send_time'] + " " + promotion["sell_num_show"] + "票\r\n")
            # print("{}剩余多少".format(searchData["keyword"],meituan_left_number))
            if len(text) != 0:
                print(text)
                # 发送通知 有票了
                self.sendMsg("tianfuxing", searchData["business_param"]["start_date"] + "有票啦！", text)

    #加密
    def encrypt(self, inputText):
        # 读取 JavaScript 文件内容
        with open("des3.js", "r") as file:
            js_code = file.read()

        # 创建 JavaScript 环境并编译 JavaScript 代码
        ctx = execjs.compile(js_code)

        # 调用 JavaScript 函数
        return ctx.call("encrypt", inputText);

    #解密
    def decrypt(self, inputText):
        # 读取 JavaScript 文件内容
        with open("des3.js", "r") as file:
            js_code = file.read()

        # 创建 JavaScript 环境并编译 JavaScript 代码
        ctx = execjs.compile(js_code)

        # 调用 JavaScript 函数
        return json.loads(ctx.call("decrypt", inputText));

     # 推送消息到手机
    def sendMsg(self, group, title, msg):
        # icon = "https://www.huya.com/favicon.ico"
        icon = "https://cdn.blog.s6.design/upload/2024/05/20240509112202394.png"
        # print('https://bark.s6.design/ZdrWZumT8QnPGUsmVjmg9k/{}/{}?group={}&icon={}'.format(title, msg, group, icon))
        requests.get(
            'https://bark.s6.design/ZdrWZumT8QnPGUsmVjmg9k/{}/{}?group={}&icon={}'.format(title, msg, group, icon))


if __name__ == '__main__':
    print('参数列表:', str(sys.argv))
    if(len(sys.argv) >= 1):
        # json字符串转对象
        payload = json.loads(payload)
        payload['business_param']['start_area_id'] = sys.argv[1]
        payload['business_param']['arrive_area_id'] = sys.argv[2]
        payload['business_param']['start_date'] = sys.argv[3]
        payload['business_param']['send_time'] = sys.argv[4]
        payload['business_param']['get_on_site_id'] = sys.argv[5]
        payload['business_param']['get_down_site_id'] = sys.argv[6]
        # json对象转字符串json
        payload = json.dumps(payload)
    xc = TianFu()
    xc.search()
    # 输出结果
    
    exit
