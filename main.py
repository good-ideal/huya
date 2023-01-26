import os
import time
import requests
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
            status = self.driver.find_elements(
                by=By.CLASS_NAME, value="uesr_n")
        except:
            status = []
        if len(status) == 1:
            username = status[0].get_attribute("textContent")
            print("user:{} has logged in.".format(username))
            return True
        return False

    def login(self, username, password):
        self.driver.get(self.url_userIndex)
        print("user:{} start to login.".format(username))
        self.driver.implicitly_wait(2)  # 等待跳转
        if self.login_check():
            return True

        self.driver.switch_to.frame('UDBSdkLgn_iframe')
        js = '''
            document.getElementsByClassName("input-login")[0].click();
            document.getElementsByClassName("udb-input-account")[0].value = "''' + str(username) + '''";
            document.getElementsByClassName("udb-input-pw")[0].value = "''' + str(password) + '''";
            document.getElementById("login-btn").click();
        '''
        self.driver.execute_script(js)
        self.driver.implicitly_wait(2)  # 等待跳转
        if not self.login_check():
            self.driver.get(self.url_userIndex)
            self.driver.switch_to.frame('UDBSdkLgn_iframe')
            self.driver.execute_script(
                'document.getElementsByClassName("quick-icon")[0].click();')
            time.sleep(1)
            qr_url = self.driver.execute_script(
                'return document.getElementById("qr-image").src;')
            print("user:{} login requires authentication, you have to scan the QR code to sign in.\nQR-code url:{}".format(username, qr_url))
            self.get_qr(username, qr_url)
            requests.get(
                'https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/虎牙登陆二维码扫码?url={}'.format(qr_url))
            while not self.login_check():
                time.sleep(0.1)

    def into_room(self, room_id, n):

        # 验证普通虎粮
        # s = int(self.get_hul())
        # print("当前有{}个虎粮".format(s))

        self.driver.get("https://huya.com/{}".format(room_id))
        self.driver.implicitly_wait(2)  # 等待跳转
        print("Enter room:{}".format(room_id))

        time.sleep(2)

        # 每日打卡
        self.dayCard()

        # 领取宝箱
        self.getTreasure(room_id)

        # 赠送超级虎粮
        self.send_super_gift(room_id, 10)

        # 赠送普通虎粮
        n = self.send_hl()

        # 每日打卡福利
        chatHostPic = self.driver.find_element(By.ID, "chatHostPic")
        # 悬浮到按钮上
        ActionChains(self.driver).move_to_element(chatHostPic).perform()
        # 加点延迟，让他完全渲染出来在获取
        time.sleep(3)
        # 统计
        ems = chatHostPic.find_elements(By.TAG_NAME, "em")
        qmdtext = ""
        for index, em in enumerate(ems):
            print(em.text)
            # 第三个是今日亲密度数量
            if index == 3:
                qmdtext += "今日增加亲密度{},".format(em.text)
            # 第四个是还差多少亲密度升级
            if index == 4:
                qmdtext += "还差{}点亲密度".format(em.text)
        print(qmdtext)

        # 打卡 发送统计
        self.sendMsg("qmd", "亲密度统计", qmdtext)
        self.sendMsg("huliang", "虎粮赠送统计", "本次送出虎粮{}个".format(n))

    # 每日打卡 前提是必须要已经进入了该房间
    def dayCard(self):
        # 每日打卡福利
        chatHostPic = self.driver.find_element(By.ID, "chatHostPic")
        # 悬浮到按钮上
        ActionChains(self.driver).move_to_element(chatHostPic).perform()
        # 加点延迟，让他完全渲染出来在获取
        time.sleep(3)
        # 获取打卡按钮
        tagas = chatHostPic.find_elements(By.TAG_NAME, "a")
        for tag in tagas:
            print(tag.text)
            if tag.text == "打卡":
                tag.click()
                print('每日打卡福利领取成功')
                break

    # 赠送普通虎粮 可以一次性赠送完成
    def send_hl(self):
        num = 0
        # 点击背包按钮
        package = self.driver.find_element(By.ID, "player-package-btn")
        package.click()

        # 等渲染完成
        self.driver.implicitly_wait(3)

        iframes = self.driver.find_elements_by_tag_name("iframe")

        # 循环iframes
        for iframe in iframes:
            # 通过iframe路径判断哪一个是背包的iframe
            # print(iframe.get_attribute("src"))
            # 判断iframe中src是否包含webPackage 如果包含就切换到该iframe
            if "webPackage" in iframe.get_attribute("src"):
                self.driver.switch_to.frame(iframe)
                break

        packs = self.driver.find_elements(By.CLASS_NAME, "m-gift-item p")
        print("背包数量：{}".format(len(packs)))
        for index, item in enumerate(packs):
            # 获取物品的名称 判断是虎粮吗 如果是就获取数量，然后赠送
            if "虎粮" in item.text:
                count = item.parent.find_element(By.CLASS_NAME, "c-count")
                # 获取虎粮数量
                print("剩余{}: {}".format(item.text, count.text))
                # 悬浮到按钮上
                ActionChains(self.driver).move_to_element(item).perform()
                # 加点延迟，让他完全渲染出来在获取
                time.sleep(2)
                numInput = self.driver.find_element(By.TAG_NAME, "input")
                # 点击一下输入框
                numInput.click()
                # 给输入框赋值
                numInput.send_keys(count.text)
                num = count.text
                # 点击赠送按钮
                sendBtn = self.driver.find_element(By.CLASS_NAME, "c-send")
                if sendBtn:
                    sendBtn.click()
                # 这里点击赠送后可能会弹出一个提示 确定赠送按钮，那么这里在手动点一下确定按钮
                # 确认按钮
                time.sleep(1)
                self.driver.execute_script(
                    'document.getElementsByClassName("btn-success")[0] && document.getElementsByClassName("btn-success")[0].click()')
                # 刷新当前网页
                self.driver.switch_to.default_content()
                self.driver.refresh()
                self.driver.implicitly_wait(2)
                break
        return num
        # 获取虎粮数量
        # num = item.find_element(By.CLASS_NAME, "num").text
        # # 赠送虎粮
        # self.send_gift(num)
        # break
        # if item.get_attribute("propsid") == "4":
        #     gift_hl_id = index

        # gifts = self.driver.find_elements(
        #     by=By.CLASS_NAME, value="player-face-gift")
        # gift_hl_id = -1
        # for index, item in enumerate(gifts):
        #     if item.get_attribute("propsid") == "4":
        #         gift_hl_id = index

        # # aa[1].click()
        # for i in range(n):
        #     print('当前虎粮在列表:{}位'.format(gift_hl_id))
        #     time.sleep(2)
        #     confirmBtn = self.driver.execute_script('''
        #         gifts = document.getElementsByClassName("player-face-gift");
        #         gifts[''' + str(gift_hl_id) + '''].click()
        #         if(document.getElementsByClassName("btn confirm").length != 0){
        #             document.getElementsByClassName("btn confirm")[0].click();
        #         }
        #         return 1;
        #     ''')
        #     print('房间号:{} 赠送第{}个虎粮.'.format(room_id, i))
        #     time.sleep(1)

    # 领取宝箱

    def getTreasure(self, room_id):
        # 2022 7.14 更新后未直播没有宝箱按钮
        exceptfail = False
        try:
            # 宝箱按钮
            playerChest = self.driver.find_element(
                By.CLASS_NAME, "player-chest")
            # 悬浮到按钮上
            ActionChains(driver).move_to_element(playerChest).perform()
        except:
            print("没有宝箱按钮")
            self.driver.get("https://huya.com/{}".format(11336726))
            self.driver.implicitly_wait(2)  # 等待跳转
            print("Enter room:{}".format(11336726))
            exceptfail = True
            time.sleep(2)
            # 宝箱按钮
            playerChest = self.driver.find_element(
                By.CLASS_NAME, "player-chest")
            # 悬浮到按钮上
            ActionChains(driver).move_to_element(playerChest).perform()

        # 加点延迟，让他完全渲染出来在获取
        time.sleep(1)

        # 2022.11.8 更新后没有li标签了采用class获取
        # playerBox = playerChest.find_elements(
        #     by=By.TAG_NAME, value="li")
        playerBox = playerChest.find_elements(
            by=By.CLASS_NAME, value="box-item")

        print("宝箱数量：{}".format(len(playerBox)))
        for index, player in enumerate(playerBox):
            print(player.text)
            if not player.text.startswith("x"):
                # 有倒计时的宝箱
                if player.text.startswith("0") or player.text == "请稍后":
                    self.now()
                    # 睡眠10分10秒 后在领取
                    time.sleep(610)
                    self.driver.execute_script(
                        'document.getElementsByClassName("player-box-stat3")[' + str(
                            index) + '].click();'
                    )
                    time.sleep(2)
                if player.text == "领取":
                    self.driver.execute_script(
                        'document.getElementsByClassName("player-box-stat3")[' + str(
                            index) + '].click();'
                    )
                    time.sleep(1)

                # 打印获取领取到的奖励内容
                content = self.driver.execute_script(
                    'return document.getElementsByClassName("player-box-stat4")[' + str(
                        index) + '].innerText;'
                )
                self.now()
                print('领取宝箱成功')
        if exceptfail:
            self.driver.get("https://huya.com/{}".format(room_id))
            self.driver.implicitly_wait(2)  # 等待跳转

    # 赠送超级虎粮
    def send_super_gift(self, room_id, number):
        # 点击更多礼物 2023.1.26 更新后需要点击更多礼物按钮
        self.driver.find_element(
            by=By.CLASS_NAME, value="player-face-arrow").click()

        # 赠送超级虎粮
        gifts = self.driver.find_elements(
            by=By.CLASS_NAME, value="gift-panel-item")
        gift_hl_id = -1
        for index, item in enumerate(gifts):
            if item.get_attribute("propsid") == "20699":
                gift_hl_id = index

        # aa[1].click()
        for i in range(number):
            print('当前超级虎粮在列表:{}位'.format(gift_hl_id))
            time.sleep(2)
            confirmBtn = self.driver.execute_script('''
                gifts = document.getElementsByClassName("gift-panel-item");
                gifts[''' + str(gift_hl_id) + '''].click();
                setTimeout(function(){
                    if(document.getElementsByClassName('create-layer').length != 0){
                        document.getElementsByClassName('create-layer')[0].remove();
                    }
                    if(document.getElementsByClassName('create-layer-mask').length != 0){
                        document.getElementsByClassName('create-layer-mask')[0].remove();
                    }
                },1000)
                if(document.getElementsByClassName("btn confirm").length != 0){
                    document.getElementsByClassName("btn confirm")[0].click();
                }
                return 1;
            ''')
            print('房间号:{} 赠送第{}个超级虎粮.'.format(room_id, i))
            time.sleep(1)

    # 获取背包虎粮数量
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

    # 获取登录二维码
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

    # 打印当前时间
    def now(self):
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print("当前时间：{}".format(current_time))

    # 推送消息到手机
    def sendMsg(self, group, title, msg):
        icon = "https://www.huya.com/favicon.ico"
        print('https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/{}/{}?group={}&icon={}'.format(title, msg, group, icon))
        requests.get(
            'https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/{}/{}?group={}&icon={}'.format(title, msg, group, icon))


if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
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

    # 如果希望下次使用的时候不登录，可以把chrome data保存，但是只能同一时间同一个浏览器用
    # 如果有多个用户也可以保存多个chrome data
    path_chrome_data = os.getcwd() + '/chromeData'
    if not Path(path_chrome_data).exists():
        os.mkdir(path_chrome_data)
    chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)
    # chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    hy = HuYa(driver)

    hy.login(username="cailong", password="cailong")
    # 北枫的直播号572329 虎粮数
    hy.into_room(572329, 50)
    driver.quit()
    # requests.get('https://api.day.app/tBDuDKqMZ9EqPC5RojvYdF/虎牙虎粮赠送完成')
