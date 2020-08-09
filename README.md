# mysite
git 演示文件

## 说明

个人博客
#### 在服务器部署后产生了BUG
在邮件发送位置使用的端口号，由于阿里云无法使用25号端口
所以需要settings中的邮件发送更改端口号
全部配置:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.qq.com'#阿里云的邮件端口屏蔽了25号

EMAIL_PORT =587  
#使用465号端口进行发送邮件需要设置EMAIL_USE_SSL=True
#使用587端口发送需设置EMAIL_USE_TLS = True
#上面两者不能并用
#且在阿里云上开放587端口号
EMAIL_HOST_USER = '*************' #

EMAIL_HOST_PASSWORD = '*******' #授权码

EMAIL_SUBJECT_PREFIX ='[/************/]'

EMAIL_USE_TLS = True #与SMTP服务器通信时，是否启动TLS链接(安全链接)
