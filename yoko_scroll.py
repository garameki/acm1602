import time
import smbus
from time import sleep
from acm1602 import ACM1602
import threading
import subprocess

a = ACM1602()
a.cls()
a.speed(0.01)
a.sendMessage("コンニチハ",1)
a.pos[1] = 20 #カーソルの位置
a.pos[2] = 20 #カーソルの位置
a.stop = False #Trueでthread終了


messages1 = [" "]
messages2 = [" "]

class MyThread1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):

		while True:
			a.screenHidari(1)
			a.pos[0] += 1
			time.sleep(0.1)
			if a.stop: break

class MyThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		i=0	
		while True:
			if a.stop: break
			length = len(messages1)
			begin = a.pos[0]
			i += 1	
			bytes = a.send2Messages(messages1[i%length],messages2[i%length])
			bytes += a.send2Messages(" "," ")

			if i > 2*length:
				a.stop = True
				break

			while a.pos[0] != begin + bytes:
				time.sleep(0.05)



class MyThread3(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			if a.stop: break
			nickname = "apache2"
			name = nickname
			check_service("NTP","ntp")
			check_service("APACHE2","apache2")
			check_service("WMAX31856","websocket-client-max31856-9801")
			check_service("sys_kama","sys_kama")
			check_usbmemory("USBメモリ","TOSHIBA")
			check_cputemp("CPUオンド")
			check_cpuvolt("CPUデンアツ")
			time.sleep(5)
			
def check_service(nickname,name):
	cmd = ("systemctl status {}".format(name))
	tmp = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).stdout.readlines()
	aa=""
	for ele in tmp:
		aa += ele.decode('utf-8')
	import re
	try:
		status = re.search("(?<=Active:\s)[^\s]+",aa).group(0)
	except AttributeError:
		status = "None"
	try:
		n = messages1.index(nickname)
		messages2[n] = status
	except ValueError:
		messages1.append(nickname)
		messages2.append(status)

def check_usbmemory(nickname,name):
	cmd = ("mount -l | grep {}".format(name))
	tmp = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).stdout.readlines()
	aa=""
	for ele in tmp:
		aa += ele.decode('utf-8')
	import re
	if aa:
		status = "OK"
	else:
		status = "BAD"

	try:
		n = messages1.index(nickname)
		messages2[n] = status
	except ValueError:
		messages1.append(nickname)
		messages2.append(status)

def check_cputemp(nickname):
	cmd = ("vcgencmd measure_temp")
	tmp = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).stdout.readlines()
	aa=""
	for ele in tmp:
		aa += ele.decode('utf-8')
	import re
	try:
		temp=re.search("(?<=temp=)[^\s]+",aa).group(0)
	except AttributeError:
		temp = "BAD"
	try:
		n = messages1.index(nickname)
		messages2[n] = temp
	except ValueError:
		messages1.append(nickname)
		messages2.append(temp)

def check_cpuvolt(nickname):
	cmd = ("vcgencmd measure_volts")
	tmp = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).stdout.readlines()
	aa=""
	for ele in tmp:
		aa += ele.decode('utf-8')
	import re
	try:
		temp=re.search("(?<=volt=)[^\s]+",aa).group(0)
	except AttributeError:
		temp = "BAD"
	try:
		n = messages1.index(nickname)
		messages2[n] = temp
	except ValueError:
		messages1.append(nickname)
		messages2.append(temp)


thread1 = MyThread1()
thread2 = MyThread2()
thread3 = MyThread3()
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()





