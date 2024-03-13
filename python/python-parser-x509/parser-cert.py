import ssl
import OpenSSL.crypto
import sys
import socket
from pyasn1.codec.der import decoder
from OpenSSL import crypto

#https://www.pyopenssl.org/en/latest/api/crypto.html#x509-objects

if (len(sys.argv) > 1):
	filename = sys.argv[1]

	with open(filename, "r") as fp:
		der_cert = fp.read()
	cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, der_cert)
else:
	context = ssl.create_default_context()
	hostname = 'www.aliyun.com'
	with socket.create_connection((hostname, 443)) as sock:
	    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
	        der_cert = ssock.getpeercert(binary_form=True)
	cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, der_cert)


	cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

	#der_bytes = cert.public_bytes(encoding=x509.Encoding.DER)
	with open(hostname+".cert", "wb") as fp:
		fp.write(cert_pem)
 
print('Subject:', cert.get_subject())
print('Issuer:', cert.get_issuer())
print('Start date:', cert.get_notBefore())
print('Expiration date:', cert.get_notAfter())
print('Pubkey:', cert.get_pubkey())
print('signature Algorithm:', cert.get_signature_algorithm())


print("====== subject ======")
for item in cert.get_subject().get_components():
	print(item)


print("======= issuer: =========")
for item in cert.get_issuer().get_components():
	print(item)


print("============ extension: ============")
ext_count = cert.get_extension_count()
print('ext_count:', ext_count)

domains = []
for i in range(ext_count):
	ext = cert.get_extension(i)
	print()
	print(ext.get_short_name())
	print(ext)
	if ext.get_short_name() == b'subjectAltName':
		content = "{}".format(ext)
		for name in str(content).split(','):
			if 'DNS:' in name:
				domain = name.split(":")[1]
				domains.append(domain.strip())
		print("/".join(domains))

