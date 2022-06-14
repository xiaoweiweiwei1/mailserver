from socket import *
import base64

import easygui as t
list = ['smtp.qq.com','smtp.163.com']
mailserver=t.choicebox('选择邮件服务器','mailserver',list)

message = ['你的相应邮箱','接收方邮箱','请登录你的相应邮箱，在邮箱设置中开启POP3/SMTP服务，将你生成并收到的授权码输入（无空格）','邮件标题','邮件内容']
s =t.multenterbox('输入信息：','mail',message)
mailFromAddress = s[0]
mailToAddress=s[1]
mailPassWord=s[2]


#mailUser ='1661705883@qq.com''wj1661705883@163.com'
#mailToAddress = '2033019629@qq.com'


clientSocket = socket(AF_INET, SOCK_STREAM)#创建tcp客户端套接字
clientSocket.connect((mailserver, 25))#与tcp服务器进行连接，目的地即为邮箱服务器，目的端口号为默认的25
 
recv = clientSocket.recv(1024).decode()#收到smtp状态码
print(recv)
if recv[:3] != '220':
    t.msgbox(msg='220 reply not received from server.', title='220', ok_button='ok')#必须收到220，指服务就绪
   
helo = 'HELO mailserver\r\n'#发送helo命令
clientSocket.send(helo.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '250':#必须收到250，指服务就绪所要求的邮件动作完成，可以继续邮件对话。通常在EHLO/HELO命令后会通过“250-”来描述服务器所支持的特性
    pass
 
login = 'auth login\r\n'#登录请求
clientSocket.send(login.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '334':#base64编码后
    pass
 
user = base64.b64encode(mailFromAddress.encode()) + b'\r\n'# 邮箱账号经过base64编码，\r\n表结束
clientSocket.send(user)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '334':pass#base64编码后的账号
else:
 t.msgbox(msg='你的邮箱错误', title='fail', ok_button='ok')
 
psw =base64.b64encode(mailPassWord.encode()) + b'\r\n'# 授权码经过base64编码，\r\n表结束
clientSocket.send(psw)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '235':#235 Authentication successful
    pass
else:
 t.msgbox(msg='授权码错误', title='fail', ok_button='ok')

MF = 'MAIL FROM: <'+ mailFromAddress + '>\r\n'#MAIL FROM命令
clientSocket.send(MF.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '250':#必须收到250，指服务就绪所要求的邮件动作完成，可以继续邮件对话。通常在EHLO/HELO命令后会通过“250-”来描述服务器所支持的特性
    pass
else:t.msgbox(msg='你的邮箱错误', title='fail', ok_button='ok')

RT = 'RCPT TO: <'+ mailToAddress + '>\r\n'#RCPT TO命令
clientSocket.send(RT.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == '250':#必须收到250，指服务就绪所要求的邮件动作完成，可以继续邮件对话。通常在EHLO/HELO命令后会通过“250-”来描述服务器所支持的特性
    pass
else:t.msgbox(msg='接收方邮箱错误', title='fail', ok_button='ok')
 
DATA = 'DATA\r\n'#DATA 命令
while True:
    clientSocket.send(DATA.encode())
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    print(recv)
    if recv[:3] == '354':#必须收到354，开始接收邮件内容输入，以<CRLF>.<CRLF>(即单行一个点)结束输入
        break
 
msg = 'FROM: ' + mailFromAddress + '\r\n'
msg += 'TO: ' + mailToAddress +  '\r\n'
msg += 'Subject: ' + s[3] +  '\r\n'
msg += s[4]
endmsg = "\r\n.\r\n"
clientSocket.send(msg.encode())
 
while True:
    clientSocket.send(endmsg.encode())#发送一个点表示邮件结束
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] == '250':#必须收到250，指服务就绪所要求的邮件动作完成，可以继续邮件对话。通常在EHLO/HELO命令后会通过“250-”来描述服务器所支持的特性
        break

QUIT = 'QUIT\r\n'#QUIT命令
while True:
    clientSocket.send(QUIT.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] == '221':#必须收到221，指服务关闭了传输通道
        break


t.msgbox(msg='成功投递邮件', title='success', ok_button='ok')



