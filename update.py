# -*- coding: UTF-8 -*-
import requests as req
import json, sys, time

# 先注册azure应用,确保应用有以下权限:
# files: Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user: User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail: Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# 注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用

# 定义文件路径
path = sys.path[0] + r'/1.txt'

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
    # 将新的token写入文件
    with open(path, 'w+') as f:
        f.write(refresh_token)

# 定义主函数
def main():
    # 打开文件
    fo = open(path, "r+")
    # 读取文件内容
    refresh_token = fo.read()
    # 关闭文件
    fo.close()
    # 调用获取token的函数
    gettoken(refresh_token)

# 执行主函数
main()
