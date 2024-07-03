#!/bin/bash
#echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nCustom-Header: Value\r\n\r\nok!" | nc -e wol.sh -l -k -p 9999
#echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nCustom-Header: Value\r\n\r\nHello, client!" | nc -l -e "sleep 1" -p 9999
#net rpc shutdown -I 192.168.3.3 address -U Administrator%
nc -l -e wol.sh -p 10222