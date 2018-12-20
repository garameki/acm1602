import time
import smbus
from time import sleep

#Thanks.
#from https://github.com/yuma-m/raspi_lcd_acm1602ni
from character_table import INITIALIZE_CODES, LINEBREAK_CODE, CHAR_TABLE

class ACM1602:
	BUS_ADDR = 1
	SLAVE_ADDR = 0x50
	CONTROL_SET = 0x00
	CONTROL_WRITE = 0x80

	#default
	bCD = 1
	bRH = 2
	bEMS = 6
	bDOOC = 12
	bFS = 0x38
	bCDS = 0x1C

	def __init__(self):
		self.pos = [0,0,0]
		self.lcd = smbus.SMBus(self.BUS_ADDR)
		self.sleeptime = 0.01

		#make instance
		self.entryModeSet       = self.EntryModeSet()
		self.displayOnOffControl= self.DisplayOnOffControl()
		self.cursorDisplayShift = self.CursorDisplayShift()
		self.functionSet        = self.FunctionSet()

		#override Base class' property 'parent'
		self.entryModeSet.parent        = self
		self.displayOnOffControl.parent = self
		self.cursorDisplayShift.parent  = self
		self.functionSet.parent         = self

		#initialize
		self.functionSet.set(self.FunctionSet.DATA8_LINE2_YDOTS10)
		self.clearDisplay()
		self.entryModeSet.set(self.EntryModeSet.MOJIWOUTTARA_CURSOR_MIGI)
		self.displayOnOffControl.set(self.DisplayOnOffControl.DISPON_CURSORON_BLINKON)

	class Base:
		def __init__(self):
			self.parent = null #interface like Java This must be overrided when this class is inherited.
		def set(self,num):
			self.parent._set(num)
		def dict(self):
			for ele in self.__dict__:
				print(ele)

	def clearDisplay(self):
			self._set(1)
			self.pos[1] = 0
			self.pos[2] = 0

	def returnHome(self):
			self._set(2)


	class EntryModeSet(Base):
		MOJIWOUTTARA_CURSOR_MIGI   = 0x6
		MOJIWOUTTARA_CURSOR_HIDARI = 0x4
		MOJIWOUTTARA_GAMEN_MIGI     = 0x5
		MOJIWOUTTARA_GAMEN_HIDARI   = 0x7
		def __init__(self):
			pass
		
	class DisplayOnOffControl(Base):
		DISPON_CURSORON_BLINKON    = 0xF
		DISPON_CURSORON_BLINKOFF   = 0xE
		DISPON_CURSOROFF_BLINKON   = 0xD
		DISPON_CURSOROFF_BLINKOFF  = 0xC
		DISPOFF_CURSORON_BLINKON   = 0xB
		DISPOFF_CURSORON_BLINKOFF  = 0xA
		DISPOFF_CURSOROFF_BLINKON  = 0x9
		DISPOFF_CURSOROFF_BLINKOFF = 0x8
		def __init__(self):
			pass
	
	class CursorDisplayShift(Base):
		SCREEN_HIDARI = 0x18
		SCREEN_MIGI = 0x1C
		CURSOR_HIDARI = 0x10
		CURSOR_MIGI =0x14
		def __init__(self):
			pass

	class FunctionSet(Base):
		DATA8_LINE2_YDOTS8  = 0x3C
		DATA8_LINE2_YDOTS10 = 0x38
		DATA8_LINE1_YDOTS8  = 0x34
		DATA8_LINE1_YDOTS10 = 0x30
		DATA4_LINE2_YDOTS8  = 0x2C
		DATA4_LINE2_YDOTS10 = 0x28
		DATA4_LINE1_YDOTS8  = 0x24
		DATA4_LINE1_YDOTS10 = 0x20
		def __init__(self):
			pass
	
	def setCGRAMAddress(self,xx):
		xx = xx | 0x40
		self._set(xx)
	
#	def setDDRAMAddress(self,gyou,retsu):
#		if gyou < 1:gyou = 1
#		if gyou > 2:gyou = 2
#		if retsu < 1:retsu = 1
#		if retsu > 16:retsu = 16
#		addr = (gyou - 1) * 0x40 + retsu -1;	
#		addr = addr | 0x80
#		self._set(addr)

	def setDDRAMAddress(self,xx):
		xx = xx | 0x80
		self._set(xx)


	def sendMessage(self,strs,nLine):
		nByte = 0
		for ii in range(len(strs)):
			nByte += self._put1(strs[ii],nLine)
		return nByte

	def send2Messages(self,str1,str2):
		bytes1 = self.sendMessage(str1,1)
		bytes2 = self.sendMessage(str2,2)

		if bytes1 > bytes2:
			self.sendMessage(' ' * (bytes1 -bytes2),2)
		elif bytes2 > bytes1:
			self.sendMessage(' ' * (bytes2 -bytes1),1)

		return bytes1 if bytes1 > bytes2 else bytes2


	def _set(self,num):
		if self.lcd is not None:
			self.lcd.write_byte_data(self.SLAVE_ADDR,self.CONTROL_SET,num)
			time.sleep(0.01)
		else:
			self._message_not_open(self)#クラスメソッドの中からインスタンスメソッドを呼ぶときにはselfを渡す。
	def _put1(self,str,nLine):

		#nLine > 2 or nLine < 1 then エラー発生


		if self.lcd is not None:
			if str == " " or str == "　":
				sp = 0.01
			else:
				sp = self.sleeptime
			try:
				bytes = CHAR_TABLE[str]
			except KeyError:
				bytes = CHAR_TABLE["X"]
			if len(bytes) == 2:
				sp = 0.01
			for byte in bytes:
				if nLine == 1:
					self.setDDRAMAddress(self.pos[nLine])
				else:
					self.setDDRAMAddress(0x40 + self.pos[nLine])

				if self.pos[nLine] > 39:
					if nLine == 1:
						self.setDDRAMAddress(0)
					else:
						self.setDDRAMAddress(0x40)
					self.pos[nLine] = 0
				self.lcd.write_byte_data(self.SLAVE_ADDR,self.CONTROL_WRITE,int(byte))
				self.pos[nLine] += 1
				#time.sleep(sp)
				sp = self.sleeptime
		else:
			self._message_not_open()
		return len(bytes)


	def _message_not_open(self):
		print(self)
		print("self.lcd has been None yet.")

	def speed(self,sp):
		if sp < 0.01:sp = 0.01
		self.sleeptime = sp
	#sugars

	def cls(self):
		self.clearDisplay()
	def cls1(self):
		self.line1()
		self.sendMessage("                 ")
	def cls2(self):
		self.line2()
		self.sendMessage("                 ")
	def line1(self):
		self.setDDRAMAddress(0)
	def line2(self):
		self.setDDRAMAddress(0x40)
		

	def screenMigi(self,nn):
		for i in range(nn):
			self.cursorDisplayShift.set(self.CursorDisplayShift.SCREEN_MIGI)
	def screenHidari(self,nn):
		for i in range(nn):
			self.cursorDisplayShift.set(self.CursorDisplayShift.SCREEN_HIDARI)
	def cursorHidari(self,nn):
		for i in range(nn):
			self.cursorDisplayShift.set(self.CursorDisplayShift.CURSOR_HIDARI)
	def cursorMigi(self,nn):
		for i in range(nn):
			self.cursorDisplayShift.set(self.CursorDisplayShift.CURSOR_MIGI)
			



if __name__ == '__main__':

	a = ACM1602()

	print(a.pos)

	#画面に表示する
	if True:
		a.cls()
		a.speed(0.01)
		a.sendMessage("コンニチハ",1)
	#	a.line2()
	#	a.sendMessage("キョウハイイテンキデスネ",1)
	#push命令を作る
	#行を指定して文字列をpushすると、現在の表示がだんだんと左にずれて、pushした文字列が右側から現れるという機能
	if False:
		a.cls()
		a.entryModeSet.set(a.EntryModeSet.MOJIWOUTTARA_CURSOR_MIGI)
		#a.sendMessage('     o                             ')
		#a.entryModeSet.set(a.EntryModeSet.MOJIWOUTTARA_GAMEN_HIDARI)
		i=0
		for n in range(1,41):
			a.sendMessage(str(n%10))	
			i += 1
			print(i)
			if i > 16:
				a.screenHidari(1)
				pass
		a.setDDRAMAddress(0x40 + 39 )

		a.sendMessage("A")	
	if True:
		import threading

		class MyThread1(threading.Thread):
			def __init__(self):
				threading.Thread.__init__(self)

			def run(self):

				while True:
					a.screenHidari(1)
					a.pos[0] += 1
					time.sleep(0.1)

		class MyThread2(threading.Thread):
			def __init__(self):
				threading.Thread.__init__(self)

			def run(self):
				i=0	
				stringss1 = ["コンヤノテンキ","グンマケン","サイタマケン","トチギケン"]
				stringss2 = ["","ハレ","ハレ","クモリ"]
				while True:
					begin = a.pos[0]
					i += 1	
					bytes = a.send2Messages(stringss1[i%3],stringss2[i%3])
					bytes += a.send2Messages(" "," ")

					while a.pos[0] != begin + bytes:
						time.sleep(0.05)

		a.pos[1] = 20
		a.pos[2] = 20
		thread1 = MyThread1()
		thread2 = MyThread2()
		thread1.start()
		thread2.start()
		thread1.join()
		thread2.join()





