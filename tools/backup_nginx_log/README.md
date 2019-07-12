# 功能

对nginx的日志进行定期切割和备份，备份失败时可以通过本地短信接口通知

# 用法

一般情况都是在单机上增加crontab进行，建议的crontab为：
```
# 每天10:10对日志进行切割
10 10 * * * cd /root/opbin/backup_log/nginx/bin && bash backup_nginx_log.sh >/dev/null 2>&1
```

