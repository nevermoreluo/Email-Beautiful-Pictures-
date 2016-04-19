
github第一发 :)
欢迎指正。
thx:frokaikan

python2脚本
库依赖:requests，bs4，PIL
功能:发送美图电子邮件给好友



所有设置选项均填制在config.py内，
设置包含：

必填项：
收件人To可填写多人以逗号分隔('xxxx@qq.com,zzz@gmail.com')
发件人From，密码Password，以及发件人邮箱的SMTPServer，126的邮箱即填写'smtp.126.com'

选填项：
需要发送的邮件标题:title
美图的数量:Picture_quantity
是否保存图片到本地，True保存，False不保存:Save_pic
保存图片的文件夹位置:Dirname
所有设置填写好后，执行send.py即可收到邮件了哟


