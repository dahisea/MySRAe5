# -*- coding: UTF-8 -*-
import requests as req
import json, sys, time, random

# 先注册azure应用,确保应用有以下权限:
# files: Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user: User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail: Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# 注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用

# 定义文件路径
path = sys.path[0] + r'/1.txt'
# 定义成功调用的次数
num1 = 0

# 定义获取token的函数
def gettoken(refresh_token):
    # 定义请求头
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # 定义请求参数
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    # 发送post请求
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # 解析响应结果
    jsontxt = json.loads(html.text)
    # 获取新的token
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    return access_token

# 定义测试接口可用性的函数
def main():
    # 打开文件
    fo = open(path, "r+")
    # 读取文件内容
    refresh_token = fo.read()
    # 关闭文件
    fo.close()
    # 使用全局变量
    global num1
    # 获取当前时间
    localtime = time.asctime(time.localtime(time.time()))
    # 获取token
    access_token = gettoken(refresh_token)
    # 定义请求头
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    # 打印开始时间
    print('此次运行开始时间为 :', localtime)
    # 定义接口列表
    urls = [
        r'https://graph.microsoft.com/v1.0/me/drive/root',
        r'https://graph.microsoft.com/v1.0/me/drive',
        r'https://graph.microsoft.com/v1.0/drive/root',
        r'https://graph.microsoft.com/v1.0/users',
        r'https://graph.microsoft.com/v1.0/me/messages',
        r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        r'https://graph.microsoft.com/v1.0/me/drive/root/children',
        r'https://api.powerbi.com/v1.0/myorg/apps',
        r'https://graph.microsoft.com/v1.0/me/mailFolders',
        r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
    ]
    # 遍历接口列表
    for i, url in enumerate(urls):
        try:
            # 发送get请求
            if req.get(url, headers=headers).status_code == 200:
                # 成功调用次数加一
                num1 += 1
                # 打印成功信息
                print(f"{i+1}调用成功{num1}次")
        except:
            # 打印异常信息
            print("pass")
            pass

# 循环执行6次
for _ in range(6):
    main()
    # 随机等待一段时间
    for i in range(random.randint(100, 300), 0, -1):
        time.sleep(1)
