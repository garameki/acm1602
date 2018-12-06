#!/user/bin/env python3

class A:
	AA = 5

	class B():
		BB = 50
		def __init__(self):
			pass
		def print(self,num):
			A.print(num)

	def __init__(self):
		self.b = self.B()

	@classmethod
	def print(self,num):
		print(self.AA,num)


if __name__ == '__main__':
	a1 = A()
	a2 = Qa.b.print(a.b.BB)
