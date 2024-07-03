#!/bin/bash
echo $(date +%Y-%m-%d\ %H:%M:%S)
echo "开始执行清理工作！"

chromePid=$(ps -ef | grep chrome | grep -v grep | awk '{print $2}')
pythonPid=$(ps aux | grep main.py | grep -v grep | awk '{print $2}')
#ps aux | grep main.py | awk '{print $2}' | xargs kill -15
#ps -ef | grep chrome | grep -v grep | awk '{print $2}' | xargs kill -15


# 检查是否找到了进程
if [ -n "$chromePid" ]; then
    # 进程存在，执行终止命令（可以选择使用kill -15或kill -9）
    for pid in $chromePid; do
	echo "停止chrome进程 $pid"
    	kill -9 "$pid"  # 或者 kill -15 "$pid"
    done
else
    echo "没有找到chrome进程"
fi

if [ -n "$pythonPid" ]; then
    # 进程存在，执行终止命令（可以选择使用kill -15或kill -9）
   for pid in $pythonPid; do
        echo "停止python进程 $pid"
        kill -9 "$pid"  # 或者 kill -15 "$pid"
    done
else
    echo "没有找到python进程"
fi

#ps aux | grep main.py | awk '{print $2}' | xargs kill -15
#ps -ef | grep chrome | grep -v grep | awk '{print $2}' | xargs kill -15
echo "执行清理工作完成！"
exit
