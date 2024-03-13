# 说明

这个demo是用openssl库解析https的cert证书，并读取其中的关键字段内容

1. 在extension中读取subjectAltName字段，代表该证书签发的域名信息
2. 在cert中读取 cert.get\_notBefore 获取证书的开始时间
3. 在cert中读取 cert.get\_notAfter() 获取证书的失效时间
4. 在issuer中获取证书的签发机构
5. 在subject中获取证书的使用者信息,根据实际情况可能会有域名、公司等字段信息

# Usage

1. 从aliyun.com获取他的证书内容，并进行关键字段解析，同时将证书内容dump到本地文件 

python3 parser-cert.py

2. 解析指定的证书文件

 python3 parser-cert.py www.aliyun.com.cert
