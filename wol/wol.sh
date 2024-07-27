#!/bin/bash
echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nCustom-Header: Value\r\n\r\n完成!"
wakeonlan -i 192.168.3.3 2C:F0:5D:85:2E:D8 > /dev/null
# 用来检测任务是否执行的通知
#curl https://bark.s6.design/ZdrWZumT8QnPGUsmVjmg9k/开机完成