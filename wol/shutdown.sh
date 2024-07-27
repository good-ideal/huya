#!/bin/bash
echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nCustom-Header: Value\r\n\r\n完成!"
net rpc shutdown -I 192.168.3.3 address -U Administrator% > /dev/null
