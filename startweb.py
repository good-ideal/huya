import tornado.web
import tornado.ioloop
import json


class IndexHander(tornado.web.RequestHandler):
    def get(self):
        self.render("html/index.html")


class AccountListHander(tornado.web.RequestHandler):
    # 获取账号
    def get(self):
        with open('config/account.json', "r") as f:
            row_data = json.load(f)
            self.write(json.dumps(row_data))

    # 保存账号
    def post(self):
        data = json.loads(self.request.body)
        with open('config/account.json', "r") as f:
            row_data = json.load(f)
            for row in row_data:
                if row['qq'] == data['qq']:
                    row['pwd'] = data['pwd']
                    print(row)
                    print(row_data)
                    break
        with open('config/account.json', "w") as f:
            json.dump(row_data, f, ensure_ascii=False)
        rooms = data['rooms']
        # 找到对应对象的账号
        with open('config/anchor.json', "r", encoding='UTF-8') as f:
            row_data = json.load(f)
            row_data[data['qq']] = rooms
            # print(row_data)
        with open('config/anchor.json', "w", encoding='UTF-8') as f:
            json.dump(row_data, f, ensure_ascii=False)

# 账号下的主播列表


class AnchorHander(tornado.web.RequestHandler):
    def get(self):
        account = self.get_argument("account")
        with open('config/anchor.json', "r", encoding='UTF-8') as f:
            row_data = json.load(f)
            # 获取对应账户的主播和赠送的虎粮数量
            self.write(json.dumps(row_data[account], ensure_ascii=False))


if __name__ == '__main__':
    app = tornado.web.Application(
        [(r"/", IndexHander),  (r"/accounts", AccountListHander), (r"/accounts/anchor", AnchorHander)])
    app.listen(8110)
    tornado.ioloop.IOLoop.current().start()
