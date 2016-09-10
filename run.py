import tty, termios, sys
from DM import DM

class Terminal:

	KEY_ESC 	= 27
	KEY_RETURN 	= 13

	def getchar(self):
		#Returns a single character from standard input
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch
	
	def play(self):

		while True:

			try:

				brief = self.dm.get_brief()
				
				print brief.description

				instr = raw_input('%s $ >>> ' % (brief.ego.get_full_name()))

				if reply == 'quit':
					break

				reply = self.dm.submit(instr)

				print reply

			except KeyboardInterrupt:
				print 'EXIT'
				break

	def __init__(self):
		self.dm = DM()
		self.play()

tty = Terminal()

"""
class Terminal:
	def __init__(self, filename=None):
		self.interp = DM()

		
		#self.source = None
		
		#if filename is not None:
		#	with open(filename, 'r') as source:
		#		self.source = source.read()
		#		self.interp.read(self.source)
		

	def test(self):

		self.interp.test()

	def begin(self):

		
		#if not self.source:
		#	self.interp.load();
		

		self.interp.read('game_script.dtk', is_file=True)


		while True:
			ch = self.getchar()

			if ch == 'q':
				break
				
			instr = self.interp.exec_next()
			
			if instr is False:
				print 'EOF'
				break

			#print '-' * 80
		
	
	def getchar(self):
		#Returns a single character from standard input
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch
   
T = Terminal()
#T.begin()
#T.test()
"""
