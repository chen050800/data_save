#create_connection(address, timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None)
# modify the SSLSocket of ssl.py 
import urllib2, urllib
from ssl_socket import get_ssl_socket
url = 'https://172.31.1.20:443/ssl/user/auth/password?username=1&password=1'
r = urllib2.urlopen(url)
#print r.read()
info = r.info()
#print info
session_str = info.getheader('Set-Cookie').split(';')[0]

xml_req = urllib2.Request('https://172.31.1.20/ssl/user/portal/intergration.xml')
xml_req.add_header('Cookie', session_str)
xml_r = urllib2.urlopen(xml_req)
#print xml_r.read()

print 'ssl_socket connect'

ssl_sock = get_ssl_socket(('172.31.1.20', 443), ('172.31.1.194',80), '743ec785', session_str, ('172.31.1.197', 0))[0]
#import socket, ssl, pprint

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ssl_sock = ssl.wrap_socket(s, None, None)
#ssl_sock.connect(('172.31.1.20', 443))


#ssl_sock.send('CONNECT 172.31.1.194:80 HTTP/1.1\r\nHost: 172.31.1.20\r\nAccept: */*\r\nCookie: MapID=743ec785;%s\r\n\r\n'%(session_str))
#print ssl_sock.read()

ssl_sock.send('GET / HTTP/1.1\r\nHost: 172.31.1.194\r\n\r\n')
print ssl_sock.read()
