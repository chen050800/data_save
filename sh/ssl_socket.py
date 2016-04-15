#-*- coding = UTF-8 -*-

import socket, ssl


def get_ssl_socket(fw_address, server_address, mapid, session_str, source_address=None):

    fw_ip, fw_port = fw_address
    server_ip, server_port = server_address
    flag = False
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if source_address:
        s.bind(source_address)
    ssl_sock = ssl.wrap_socket(s, None, None)
    ssl_sock.connect(fw_address)
    
    connect_str = 'CONNECT %s:%s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nCookie: MapID=%s;%s\r\n\r\n'
    
    ssl_sock.send(connect_str%(server_ip, server_port, fw_ip, mapid, session_str))
    message =  ssl_sock.read()

    if '200 Connection established' in message:
        flag = True
        
    print message
    
    return [ssl_sock, flag, message] 

