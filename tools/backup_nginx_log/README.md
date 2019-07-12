# 功能

对nginx的日志进行定期切割和备份，备份失败时可以通过本地短信接口通知

# 用法

一般情况都是在单机上增加crontab进行，建议的crontab为：
```
# 每天10:10对日志进行切割
10 10 * * * cd /root/opbin/backup_log/nginx/bin && bash backup_nginx_log.sh >/dev/null 2>&1
```

# 配置

使用前，需要根据实际情况修改脚本中的配置信息:
```
# config
# 日志文件所在路径
log_path="/data1/shuangyi/www/logs/shuangyi/"

# 需要备份的文件名，多个文件用空格分隔
log_filenames="access.log nginx_error.log"

# 目标的备份路径
dest_path="/data1/shuangyi/www/logs/shuangyi/backup"

# nginx所在路径
nginx_bin="/usr/bin/nginx "

# 切割备份后的文件保留的天数
delay_delete=365

# 异常告警的手机号，多个手机号用逗号分隔
phone_list="13088888888"

# 本地发短信的接口,如果没有这一项设置为空即可
GSMSEND="/root/opbin/sms/gsmsend "

# config end

```
