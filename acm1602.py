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

	def returnHome(self):
			self._set(2)

	class EntryModeSet(Base):
		MOJIWOUTTARA_CURSOR_MIGI   = 0x6
		MOJIWOUTTARA_CURSOR_HIDARI = 0x4
		MOJIWOUTTARA_GAMEN_MIGI     = 0x7
		MOJIWOUTTARA_GAMEN_HIDARI   = 0x5
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
		CURSOR_MIGI = 0x18
		CURSOR_HIDARI = 0x1C
		SCREEN_MIGI = 0x10
		SCREEN_HIDARI =0x14
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
	
	def setDDRAMAddress(self,gyou,retsu):
		if gyou < 1:gyou = 1
		if gyou > 2:gyou = 2
		if retsu < 1:retsu = 1
		if retsu > 16:retsu = 16
		addr = (gyou - 1) * 0x40 + retsu -1;	
		addr = addr | 0x80
		self._set(addr)

	def sendMessage(self,strs):
		strs = strs + "                    "
		for ii in range(15):
			self._put(strs[ii])

	def _set(self,num):
		if self.lcd is not None:
			self.lcd.write_byte_data(self.SLAVE_ADDR,self.CONTROL_SET,num)
			time.sleep(0.01)
		else:
			self._message_not_open(self)#クラスメソッドの中からインスタンスメソッドを呼ぶときにはselfを渡す。

	def _put(self,str):
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
				self.lcd.write_byte_data(self.SLAVE_ADDR,self.CONTROL_WRITE,int(byte))
				time.sleep(sp)
				sp = self.sleeptime
		else:
			self._message_not_open()

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
		self.setDDRAMAddress(1,1)
	def line2(self):
		self.setDDRAMAddress(2,1)
		

if __name__ == '__main__':

	a = ACM1602()
	a.cls()
	a.speed(0.5)
	a.sendMessage("コンニチハ")
	a.line2()
	a.sendMessage("キョウハイイテンキデスネ")

