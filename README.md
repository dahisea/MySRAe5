# AASR_e5
* 根据[原教程]获取应用id、机密、refresh_token（自己复制保存，注意区分id机密，别弄混了）
   
  然后在线编辑你项目里的1.txt，将整个refresh_token覆盖粘贴进去（里面是我的数据，先删掉或者覆盖掉）。（千万不要改1.py）
  
    > refresh_token位置如图下。复制refresh_token紧接着的双引号里的内容（红竖线框起来的），不要把双引号复制进去。复制进1.txt后，留意结尾不要留空格或者空行
     
  
* 第三步，依次点击上栏Setting > Secrets > Add a new secret，新建两个secret如图：CONFIG_ID、CONFIG_KEY。

  内容分别如下: ( 把你的应用id改成你的应用id , 你的应用机密改成你的机密，单引号不要动 )
  
  CONFIG_ID
  ```shell
  id=r'你的应用id'
  ```
  CONFIG_KEY
  ```shell
  secret=r'你的应用机密'
  ```
  
  最终格式应该是类似这样的：
  
  
  
* 第四步，进入你的个人设置页面(右上角头像 Settings，不是仓库里的 Settings)，选择 Developer settings > Personal access tokens > Generate new token,

  设置名字为GITHUB_TOKEN , 然后勾选 repo , admin:repo_hook , workflow 等选项，最后点击Generate token即可。
  

  
* 第五步，点击右上角星星/star立马调用一次，再点击上面的Action就能看到每次的运行日志，看看运行状况

（必需点进去Test Api看下，api有没有调用到位，有没有出错。外面的Auto Api打勾只能说明运行是正常的，我们还需要确认10个api调用成功了，就像图里的一样。如果少了几个api，要么是注册应用的时候赋予api权限没弄好；要么是没登录激活onedrive，登录激活一下）


* 第六步，没出错的话，就搞定啦！！再看看下面的定时次数要不要修改，不打算改就不用管了。

  我设定的每小时自动运行一次，每次调用3轮（点击右上角星星/star也可以立马调用一次），你们自行斟酌修改（我也不知道保持活跃要调用多少次、多久）：

  * 定时自动启动修改地方：（在.github/workflow/python-app.yml文件里，自行百度cron定时任务格式，最短每5分钟一次）
   

   
  * 每次轮数修改地方：（在1.py最后面）
