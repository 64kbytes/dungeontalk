import tty, termios, sys
from DM import DM

class Terminal:
	def __init__(self, filename=None):
		self.interp = DM()

		"""
		self.source = None
		
		if filename is not None:
			with open(filename, 'r') as source:
				self.source = source.read()
				self.interp.read(self.source)
		"""

	def test(self):

		self.interp.test()

	def begin(self):

		"""
		if not self.source:
			self.interp.load();
		"""

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
T.test()


"""
import readline
readline.parse_and_bind("tab: complete")

class SFACompleter:
	def __init__(self,transfile):
		fin = open(transfile,"r")
		self.rules = {}
		self.start = []
		for line in fin:
			assert('->' in line)
			line = line.strip()
			first,second = line.split('->')
			if first == '$':
				self.start.append(second)
				if second not in self.rules:
					self.rules[second] = []
			else:
				if first not in self.rules:
					self.rules[first] = []
				if second not in self.rules:
					self.rules[second] = []
				self.rules[first].append(second)
		fin.close()

		print self.rules

	def process(self,tokens):
		if len(tokens) == 0:
			return []
		elif len(tokens) == 1:
			return [x+" " for x in self.start if x.startswith(tokens[-1])]
		else:
			 ret = [x+" " for x in self.rules[tokens[-2]] if x.startswith(tokens[-1])]
		return ret

	def complete(self,text,state):
		try:
			tokens = readline.get_line_buffer().split()
			if not tokens or readline.get_line_buffer()[-1] == " ":
				tokens.append(text)
			results = self.process(tokens)+[None]
			return results[state]
		except Exception,e:
			print
			print e
			print
		return None

completer = SFACompleter("rules5.txt")
readline.set_completer(completer.complete)

line = raw_input('prompt> ')
"""
