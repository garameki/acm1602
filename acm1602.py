import smbus
from time import sleep

#Thanks.
#from https://github.com/yuma-m/raspi_lcd_acm1602ni
from character_table import INITIALIZE_CODES, LINEBREAK_CODE, CHAR_TABLE

lcd = smbus.SMbus(1)
LCD_ADDR = 0x50

FUNCTION_SET_myLCD = 0x38


	

class ACM1602:
	lcd = None
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

	def __init__(self,BUS_ADDR):
		self.CD=self.ClearDisplay()
		self.RH=self.ReturnHome()
		self.EMS=self.EntryModeSet()
		self.DOOC=self.DisplayOnOffControl()
		self.CDS=CursorDisplayControl()
		self.FS=FunctionSet()

		self.lcd = smbus.SMbus(self.BUS_ADDR)

	class Base:
		def __init__(self):
			pass
		def set(self,num):
			ACM1602._set(num)
		def dict(self):
			for ele in self.__dict__:
				print(ele)

	class ClearDisplayi(Base):
		def __init__(self):
			pass
		def set(self):#Override
			ACM1602._set(num)

	class RturnHome(Base):
	
	
	
	
	
	
	
	def __init__(self):
			pass
		def set(self):#Override
			ACM1602._set(num)

	class EntryModeSet(Base):
		MOJIWOUTTARA_KA-SORU_MIGI   = 0x6
		MOJIWOUTTARA_KA-SORU_HIDARI = 0x4
		MOJIWOUTTARA_GAMEN_MIGI     = 0x7
		MOJIWOUTTARA_GAMEN_HIDARI   = 0x5
		def __init__(self):
			pass
		
	class DisplayOnOffControll(Base):
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

	def setOrdinary(self):
		self.FS.set(FS.
	
	def sendMessage(self,strs):
		for letter in strs:
			self._put(letter)

	@classmethod
	def _set(self,num):
		if self.lcd is not None:
			self.lcd.write_byte_data(SLAVE_ADDR,CONTROL_SET,num)
		else:
			self._message_not_open()

	def _put(self,str):
		if self.lcd is not None:
			try:
				byte = CHAR_TABLE[str]
			except KeyError:
				byte = CHAR_TABLE["X"]

			self.lcd.write_byte_data(SLAVE_ADDR,CONTROL_WRITE,byte)
		else
			self._message_not_open()

	def _message_not_open(self):
		print("self.lcd has been None yet.")


if __name__ == __main__:
