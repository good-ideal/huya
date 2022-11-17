import os
import time
import requests
import json
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class HuYa:
    def __init__(self, dri: webdriver.Chrome):
        self.url_userIndex = "https://i.huya.com/"
        self.driver = dri

    def login_check(self):
        try:
            # 切回第一个主页
            driver.switch_to.window(driver.window_handles[0])
            status = self.driver.find_elements_by_class_name("uesr_n")
        except:
            status = []
        if len(status) == 1:
            username = status[0].get_attribute("textContent")
            print("用户名:{} 登录成功.".format(username))
            return True
        return False

    def login(self, data):
        self.driver.get(self.url_userIndex)

        self.driver.implicitly_wait(2)  # 等待跳转
        if self.login_check():
            return True

        self.driver.switch_to.frame('UDBSdkLgn_iframe')
        js = '''
            document.getElementsByClassName("input-login")[0].click();
        '''
        self.driver.execute_script(js)
        time.sleep(2)
        # qq登录
        self.qqlogin(data)
        return
        time.sleep(2)
        # 如果没有登录成功，就使用扫码登录
        if not self.login_check():
            self.driver.get(self.url_userIndex)
            self.driver.switch_to.frame('UDBSdkLgn_iframe')
            self.driver.execute_script(
                'document.getElementsByClassName("quick-icon")[0].click();')
            time.sleep(1)
            qr_url = self.driver.execute_script(
                'return document.getElementById("qr-image").src;')
            print("login requires authentication, you have to scan the QR code to sign in.\nQR-code url:{}".format(qr_url))
            self.get_qr("cailong", qr_url)
            requests.get(
                'https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/虎牙登陆二维码扫码?url={}'.format(qr_url))
            while not self.login_check():
                time.sleep(0.1)

    # qq登录
    def qqlogin(self, data):
        third_login_item = self.driver.find_elements(
            By.CLASS_NAME, "third-login-item")
        third_login_item[1].click()
        time.sleep(2)
        cls = driver.window_handles
        # 切换到新开的qq登录窗口
        driver.switch_to.window(cls[1])
        # 到iframe里面
        driver.switch_to.frame('ptlogin_iframe')
        loginBtn = driver.find_element(By.ID, "switcher_plogin")
        # 点击账号密码登录
        loginBtn.click()
        qq = data['qq']
        qqpwd = data['pwd']
        # 输入qq账号密码
        inputUandP = '''
            document.getElementById('u').value = "''' + str(qq) + '''";
            document.getElementById('p').value = "''' + str(qqpwd) + '''";
        '''
        driver.execute_script(inputUandP)
        # 授权并登录
        driver.find_element(By.ID, "login_button").click()

    def into_room(self, room_id, n):
        s = int(self.get_hul())
        # print("The remaining HL is {}".format(s))
        if s < n and s != 0:
            n = s
            print('The remaining HL is not enough for room:{}.'.format(room_id))
        elif s == 0:
            print('当前背包虎粮： 0. \nroom:{} send failure'.format(room_id))
            return False
        self.driver.get("https://huya.com/{}".format(room_id))
        self.driver.implicitly_wait(2)  # 等待跳转
        print("Enter room:{}".format(room_id))
        time.sleep(2)

        # 每日打卡福利
        chatHostPic = self.driver.find_element(By.ID, "chatHostPic")
        # 悬浮到按钮上
        ActionChains(driver).move_to_element(chatHostPic).perform()
        # 加点延迟，让他完全渲染出来在获取
        time.sleep(3)
        # 获取打卡按钮
        spans = chatHostPic.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.text == "打卡领取":
                span.click()
                print('每日打卡福利领取成功')
                break

        gifts = self.driver.find_elements(
            by=By.CLASS_NAME, value="player-face-gift")
        gift_hl_id = -1
        for index, item in enumerate(gifts):
            if item.get_attribute("propsid") == "4":
                gift_hl_id = index

        # aa[1].click()
        for i in range(n):
            print('当前虎粮在列表:{}位'.format(gift_hl_id))
            time.sleep(2)
            confirmBtn = self.driver.execute_script('''
                gifts = document.getElementsByClassName("player-face-gift");
                gifts[''' + str(gift_hl_id) + '''].click()
                if(document.getElementsByClassName("btn confirm").length != 0){
                    document.getElementsByClassName("btn confirm")[0].click();
                }
                return 1;
            ''')
            print('确认按钮:{}存在'.format(confirmBtn))
            # self.driver.execute_script('''
            #     gifts[''' + str(gift_hl_id) + '''].click();
            #     console.log(111111111111111111111,document.getElementsByClassName("btn confirm").length);
            #     if(document.getElementsByClassName("btn confirm").length != 0){
            #         document.getElementsByClassName("btn confirm")[0].click();
            #     }
            # ''')
            print('Room:{} send out the {}th HL.'.format(room_id, i))
            time.sleep(1)

    def get_hul(self):
        # 进入充值页面查询虎粮
        self.driver.get("https://hd.huya.com/pay/index.html?source=web")
        self.driver.implicitly_wait(2)  # 等待跳转
        self.driver.execute_script(
            'document.getElementsByClassName("nav")[0].getElementsByTagName("li")[4].click();')
        time.sleep(1)
        n = self.driver.execute_script('''
            lis = document.getElementsByTagName("li");
            for(var i=0;i<lis.length;i++){
                if(lis[i].title.search("虎粮") != -1){
                    return lis[i].getAttribute("data-num");
                }
            } 
            return 0;
        ''')

        print("背包虎粮:{}".format(n))
        return n

    def get_qr(self, usn, url, attach_cookie=False):
        sess = requests.Session()
        # 将selenium的cookies放到session中, 虎牙的验证码不带cookie也能访问, 绝绝子
        if attach_cookie:
            cookies = self.driver.get_cookies()
            sess.headers.clear()
            for cookie in cookies:
                sess.cookies.set(cookie['name'], cookie['value'])

        ret = sess.get(url)
        with open('qr-{}.png'.format(usn), 'wb') as f:
            print("qr-code saved success.")
            f.write(ret.content)


if __name__ == '__main__':
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
    chrome_options.add_argument("no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
    chrome_options.add_argument("disable-extensions")  # 禁用扩展
    chrome_options.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
    chrome_options.add_argument("disable-translate")  # 禁用翻译
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument(
        "blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度

    # 这里读取配置
    with open('config/account.json', "r") as f:
        row_datas = json.load(f)
        # 如果希望下次使用的时候不登录，可以把chrome data保存，但是只能同一时间同一个浏览器用
        # 如果有多个用户也可以保存多个chrome data
        for row in row_datas:
            path_chrome_data = os.getcwd() + '/chromeData/' + row['qq']
            if not Path(path_chrome_data).exists():
                os.makedirs(path_chrome_data)
            chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)

            driver = webdriver.Chrome(chrome_options=chrome_options)

            hy = HuYa(driver)

            hy.login(row)

    # 北枫的直播号572329 虎粮数
    #hy.into_room(572329, 50)
    # driver.quit()
    # requests.get('https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/虎牙虎粮赠送完成')
