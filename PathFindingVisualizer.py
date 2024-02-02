import pygame
import math
import pickle
import os
from queue import PriorityQueue
pygame.init()


WIDTH = 600
WIDTH_whole = 890
HEIGHT = 610

ROWS = 40

WINDOW = pygame.display.set_mode((WIDTH_whole, HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")

#ALL FONT INITIALIZATIONS
font_box = pygame.font.SysFont('ocraextended', 20)
font_button = pygame.font.SysFont('ocraextended', 18, bold = 1)
font_screen = pygame.font.SysFont('ocraextended', 13)
font_screen_1 = pygame.font.SysFont('ocraextended', 13, bold = 1)
font_screen_2 = pygame.font.SysFont('ocraextended', 20)
font_screen_list = pygame.font.SysFont('ocraextended', 17)
error_heading_font = pygame.font.SysFont('ocraextended', 14, bold = 1)
error_sign_font = pygame.font.SysFont('calibri', 16, bold = 1)
error_text_font = pygame.font.SysFont('ocraextended', 13)

#ALL COLORS
DARKRED = (220, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 90, 90)
GREEN = (0, 255, 0)
LIGHTGREEN = (51, 255, 51)
LIGHTERGREEN = (102, 255, 102)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (90, 90, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
PINK = (255, 210, 255)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
LIGHTGREY = (180, 180, 180)
LIGHTERGREY = (250, 250, 250)
DARKGREY = (40,40,40)
CYAN = (64, 224, 250)	  #CUSTOM COLOR

#ALL TEXTS
controls_text1 = 'LEFT MOUSE CLICK: Place Start/End/Barrier'
controls_text2 = 'RIGHT MOUSE CLICK: Remove Start/End/Barrier'
controls_text3 = 'SPACEBAR: Start algorithm'
controls_text4 = 'R: Reset Grid'
list_heading = 'SAVED GRIDS'

d1 = 'Path Finding is finding the'
d2 = 'shortest possible path between two'
d3 = 'given points.'
d4 = 'This Path Finding Visualizer'
d5 = 'presents it\'s working on a 2D grid'
d6 = '(40x40) in an attractive manner.'
d7 = 'It let\'s the user create their own'
d8 = 'simple or complex grids and allows'
d9 = 'the user to save any grid instead'
d10 = 'of losing it after the program is'
d11 = 'shut down.'
d12 = 'CONTROLS'
d13 = 'Left Mouse Click:'
d14 = 'Left-clicking any grid box (node)'
d15 = 'will make it the START NODE (  )'
d16 = 'Left-clicking another node will'
d17 = 'make that node the END NODE (  )'
d18 = 'Any nodes clicked after will'
d19 = 'become BARRIERS (  )'
d20 = 'The algorithm will find the'
d21 = 'shortest possible path from the'
d22 = 'START NODE to the END NODE while'
d23 = 'avoiding the BARRIERS.'
d24 = 'Right Mouse Click:'
d25 = 'Right-clicking any node will'
d26 = 'revert it back to an EMPTY NODE.'
d27 = 'Spacebar:'
d28 = 'Pressing the Spacebar key after'
d29 = 'creating a grid will run the'
d30 = 'algorithm.'
d31 = 'Reset (R):'
d32 = 'Pressing the R key will clear the'
d33 = 'grid.'
d34 = 'TIP:'
d35 = 'Save your grid before starting'
d36 = 'the algorithm.'
d_last = 'Press the button again to close'
d_last1 = 'this window.'

redsign = '?'
greensign = '>'
ortext = 'OR'
closew = 'Close this window to continue'

#Grid doesn't exist/incorrect TEXT
errorheading1 = 'INVALID GRID NAME'
error11 = ' Could not find requested grid'
error12 = ' Make sure the grid you are trying to load is in'
error13 = ' the \'SAVED GRIDS\' list'
error14 = ' Spell check and capitalization check before'
error15 = ' hitting ENTER because every entry is case'
error16 = ' sensitive'

#Grid exists with same name TEXT
errorheading2 = 'DUPLICATE GRID NAME'
error21 = ' Found another grid with same name'
error22 = ' Delete existing grid'
error23 = ' Give current grid another name'

#When PATH does not exist
errorheading3 = 'PATH VALIDATION FAILED'
error31 = ' Path does not exist'
error32 = ' Make sure the START NODE and the END NODE are'
error33 = ' not completely isolated'
error34 = ' This algorithm does not find path through'
error35 = ' diagonal nodes'

#When user tries to save a grid after running the algorithm
errorheading4 = 'ILLEGAL SAVE ATTEMPT'
error41 = 'Saving a grid after running the algorithm is'
error42 = 'forbidden because it corrupts the node'
error43 = 'addresses and their attributes'
error44 = 'Definitely not because the developer was'
error45 = 'too lazy to figure out why it did not work'

#When the user has used every grid slot available
errorheading5 = 'SAVED GRIDS LIMIT REACHED'
error51 = ' Maximum number of grids saved'
error52 = ' Delete existing grids'
error53 = ' Lose the current grid'

#When any entry has no alphanumeric text
errorheading6 = 'EMPTY ENTRY'
error61 = ' The entry was either empty or only had spaces'
error62 = ' Don\'t do that'


saved_list = []

#EXTRACTING SAVED GRIDS' NAMES FROM FOLDER
for file in os.listdir("."):
	if "." in file or os.path.isdir(file):
		continue
	saved_list.append(file)


class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col
	
	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == CYAN

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = YELLOW

	def make_barrier(self):
		self.color = BLACK
	
	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = CYAN

	def make_path(self):
		self.color = GREEN


	def draw(self, window):
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

	def update_nieghbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():	  #DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():						#UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():	  #RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():						#LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

	
def h(p1, p2):			 #Heuristic function
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1- x2) + abs(y1 - y2)

def recreate_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

					
		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			recreate_path(came_from, current, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))

					open_set_hash.add(neighbor)
					neighbor.make_open()
		
		draw()

		if current != start:
			current.make_closed()
		

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

def draw_gridlines(window, rows, width):
	gap = width // rows
	for i in range(rows + 1):
		pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows + 1):
			pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface, error, GridNotExist, NameCopy, PathNotExist, IllegalSave, SaveLimit, EmptyEntry):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_gridlines(window, rows, width)

	redrawbutton()

	if error == True:
		errorbox(window, GridNotExist, NameCopy, PathNotExist, IllegalSave, SaveLimit, EmptyEntry)

	pygame.draw.rect(WINDOW, loadboxcolor, load_box, 2)
	pygame.draw.rect(WINDOW, saveboxcolor, save_box, 2)
	pygame.draw.rect(WINDOW, deleteboxcolor, delete_box, 2)
	WINDOW.blit(load_txt_surface, (load_box.x+7, load_box.y+6))
	WINDOW.blit(save_txt_surface, (save_box.x+7, save_box.y+6))
	WINDOW.blit(delete_txt_surface, (delete_box.x+7, delete_box.y+6))

	message(d1, PURPLE, 897, 3)
	message(d2, PURPLE, 897, 16)
	message(d3, PURPLE, 897, 29)
	message(d4, BLACK, 897, 55)
	message(d5, BLACK, 897, 68)
	message(d6, BLACK, 897, 81)
	message(d7, BLACK, 897, 94)
	message(d8, BLACK, 897, 107)
	message(d9, BLACK, 897, 120)
	message(d10, BLACK, 897, 133)
	message(d11, BLACK, 897, 146)
	message(d12, PURPLE, 897, 172)
	message(d13, PURPLE, 897, 198)
	message(d14, BLACK, 897, 211)
	message(d15, BLACK, 897, 224)
	message(d16, BLACK, 897, 237)
	message(d17, BLACK, 897, 250)
	message(d18, BLACK, 897, 263)
	message(d19, BLACK, 897, 276)
	message(d20, PURPLE, 897, 302)
	message(d21, PURPLE, 897, 315)
	message(d22, PURPLE, 897, 328)
	message(d23, PURPLE, 897, 341)
	message(d24, PURPLE, 897, 367)
	message(d25, BLACK, 897, 380)
	message(d26, BLACK, 897, 393)
	message(d27, PURPLE, 897, 419)
	message(d28, BLACK, 897, 432)
	message(d29, BLACK, 897, 445)
	message(d30, BLACK, 897, 458)
	message(d31, PURPLE, 897, 484)
	message(d32, BLACK, 897, 497)
	message(d33, BLACK, 897, 510)
	messagelast(d34, RED, 895, 536)
	message(d35, DARKRED, 933, 536)
	message(d36, DARKRED, 933, 549)
	messagelast(d_last, PURPLE, 895, 570)
	messagelast(d_last1, PURPLE, 895, 583)

	pygame.draw.rect(window, ORANGE, (1132, 227, 10, 10))
	pygame.draw.rect(window, CYAN, (1132, 253, 10, 10))
	pygame.draw.rect(window, BLACK, (1036, 279, 10, 10))

	message2(list_heading, BLACK, 680, 138)

	messagelist(str(saved_list), PURPLE, 616, 168)


	pygame.draw.line(window, GREY, (610, 135), (880, 135), 1)	  #top first
	pygame.draw.line(window, GREY, (610, 163), (880, 163), 1)	  #top second
	pygame.draw.line(window, GREY, (610, 555), (880, 555), 1)     #bottom
	pygame.draw.line(window, GREY, (610, 135), (610, 555), 1)	  #left
	pygame.draw.line(window, GREY, (880, 135), (880, 555), 1)	  #right
	pygame.draw.line(window, GREY, (890, 0), (1180, 0), 1)        #extra top
	pygame.draw.line(window, GREY, (890, 600), (1180, 600), 1)    #extra bottom
	pygame.draw.line(window, GREY, (890, 0), (890, 600), 1)       #extra left
	pygame.draw.line(window, GREY, (1180, 0), (1180, 600), 1)     #extra right


	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos

	row = x // gap
	col = y // gap

	return row, col

#BUTTON


class Button():
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw_button(self,WINDOW,outline=GREY):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(WINDOW, outline, (self.x-1,self.y-1,self.width+2,self.height+2),0)
			
		pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width,self.height),0)
		
		if self.text != '':
			text = font_button.render(self.text, 1, BLACK)
			WINDOW.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))
	
	def er_button(self,WINDOW,outline=PURPLE):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(WINDOW, outline, (self.x-1,self.y-1,self.width+3,self.height+3),0)
			
		pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width,self.height),0)
	
	def close_button(self,WINDOW,outline=PURPLE):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(WINDOW, outline, (self.x-1,self.y-1,self.width+2,self.height+2),0)
			
		pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width,self.height),0)

		if self.text != '':
			text = font_button.render(self.text, 1, WHITE)
			WINDOW.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2) - 1))


	def isOver(self, pos):
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
			
		return False


ins_button = Button(BLACK, 611, 565, 269, 35, 'DETAILS / CONTROLS')
error_button = Button(LIGHTERGREY, 100, 220, 400, 160, '')
x_button = Button(RED, 470, 220, 30, 19, 'x')

def redrawbutton():
	ins_button.draw_button(WINDOW)

def errorbox(window, GridNotExist, NameCopy, PathNotExist, IllegalSave, SaveLimit, EmptyEntry):
	error_button.er_button(WINDOW)
	x_button.close_button(WINDOW)
	pygame.draw.line(window, PURPLE, (100, 240), (500, 240), 1)
	messagelast(closew, PURPLE, 105, 362)

	if GridNotExist:
		GridNotExist_text()
	elif NameCopy:
		NameCopy_text()
	elif PathNotExist:
		PathNotExist_text()
	elif IllegalSave:
		IllegalSave_text()
	elif SaveLimit:
		SaveLimit_text()
	elif EmptyEntry:
		EmptyEntry_text()


def message(msg, color, x, y): 
	screen_text = font_screen.render(msg, 1, color)
	WINDOW.blit(screen_text, (x, y))

def messagelast(msg, color, x, y): 
	screen_text_1 = font_screen_1.render(msg, 1, color)
	WINDOW.blit(screen_text_1, (x, y))

def message2(msg, color, x, y): 
	screen_text_2 = font_screen_2.render(msg, 1, color)
	WINDOW.blit(screen_text_2, (x, y))

def messagelist(msg, color, x, y):
	for word in saved_list:
		screen_text_list = font_screen_list.render(word, 1, color)
		WINDOW.blit(screen_text_list, (x, y))
		y += 18

def errheading(msg, color, x, y): 
	error_heading = error_heading_font.render(msg, 1, color)
	WINDOW.blit(error_heading, (x, y))

def errtext(msg, color, x, y): 
	error_text = error_text_font.render(msg, 1, color)
	WINDOW.blit(error_text, (x, y))

def errsign(msg, color, x, y):
	error_sign = error_sign_font.render(msg, 1, color)
	WINDOW.blit(error_sign, (x, y))

load_box = pygame.Rect(610, 45, 270, 35)
save_box = pygame.Rect(610, 0, 270, 35)
delete_box = pygame.Rect(610, 90, 270, 35)

#All error text functions

def GridNotExist_text():
	errheading(errorheading1, RED, 104, 222)
	errsign(redsign, RED, 104, 247)
	errtext(error11, BLACK, 105, 246)
	messagelast(greensign, DARKGREEN, 102, 274)
	errtext(error12, BLACK, 105, 274)
	errtext(error13, BLACK, 105, 288)
	messagelast(greensign, DARKGREEN, 102, 302)
	errtext(error14, BLACK, 105, 302)
	errtext(error15, BLACK, 105, 316)
	errtext(error16, BLACK, 105, 330)

def NameCopy_text():
	errheading(errorheading2, RED, 104, 222)
	errsign(redsign, RED, 104, 247)
	errtext(error21, BLACK, 105, 246)
	messagelast(greensign, DARKGREEN, 102, 274)
	errtext(error22, BLACK, 105, 274)
	errtext(ortext, PURPLE, 102, 288)
	messagelast(greensign, DARKGREEN, 102, 302)
	errtext(error23, BLACK, 105, 302)

def PathNotExist_text():
	errheading(errorheading3, RED, 104, 222)
	errsign(redsign, RED, 104, 247)
	errtext(error31, BLACK, 105, 246)
	messagelast(greensign, DARKGREEN, 102, 274)
	errtext(error32, BLACK, 105, 274)
	errtext(error33, BLACK, 105, 288)
	messagelast(greensign, DARKGREEN, 102, 302)
	errtext(error34, BLACK, 105, 302)
	errtext(error35, BLACK, 105, 316)

def IllegalSave_text():
	errheading(errorheading4, RED, 104, 222)
	errtext(error41, PURPLE, 105, 246)
	errtext(error42, PURPLE, 105, 260)
	errtext(error43, PURPLE, 105, 274)
	errtext(error44, PURPLE, 105, 302)
	errtext(error45, PURPLE, 105, 316)

def SaveLimit_text():
	errheading(errorheading5, RED, 104, 222)
	errsign(redsign, RED, 104, 247)
	errtext(error51, BLACK, 105, 246)
	messagelast(greensign, DARKGREEN, 102, 274)
	errtext(error52, BLACK, 105, 274)
	errtext(ortext, PURPLE, 102, 288)
	messagelast(greensign, DARKGREEN, 102, 302)
	errtext(error53, BLACK, 105, 302)

def EmptyEntry_text():
	errheading(errorheading6, RED, 104, 222)
	errsign(redsign, RED, 104, 247)
	errtext(error61, BLACK, 105, 246)
	messagelast(greensign, DARKGREEN, 102, 274)
	errtext(error62, BLACK, 105, 274)


def main(window, width):
	#(pygame.font.get_fonts())
	#(os.listdir("."))
	# (saved_list)
	loadboxcolor = pygame.Color('lightgreen')
	saveboxcolor = pygame.Color('lightskyblue')
	deleteboxcolor = pygame.Color(255, 125, 125)
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	loadactive = False
	saveactive = False
	deleteactive = False
	clicked = False
	instructions = False
	error = False
	
	GridNotExist = False
	NameCopy = False
	PathNotExist = False
	IllegalSave = False
	SaveLimit = False
	EmptyEntry = False

	load_text = 'Enter to load grid'
	save_text = 'Enter to save grid'
	delete_text = 'Enter to delete grid'
	load_txt_surface = font_box.render(load_text, True, BLACK)
	save_txt_surface = font_box.render(save_text, True, BLACK)
	delete_txt_surface = font_box.render(delete_text, True, BLACK)
	while run:
		draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface, error, GridNotExist, NameCopy, PathNotExist, IllegalSave, SaveLimit, EmptyEntry)
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.MOUSEMOTION and clicked == False:
				if ins_button.isOver(pos):
					ins_button.color = LIGHTERGREEN
				else:
					ins_button.color = LIGHTGREEN

				if x_button.isOver(pos):
					x_button.color = LIGHTRED
				else:
					x_button.color = RED

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
				if ins_button.isOver(pos):
					ins_button.color = DARKGREEN

				if x_button.isOver(pos):
					x_button.color = DARKRED

			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False
				if ins_button.isOver(pos):
					ins_button.color = LIGHTERGREEN
					#("Pressed ins button")
					if instructions == False:
						instructions = True
						pygame.display.set_mode((1190, HEIGHT))
					else:
						instructions = False
						pygame.display.set_mode((WIDTH_whole, HEIGHT))

				if x_button.isOver(pos):
					error = False
					if GridNotExist:
						GridNotExist = False
					elif NameCopy:
						NameCopy = False
					elif PathNotExist:
						PathNotExist = False
					elif IllegalSave:
						IllegalSave = False
						os.remove(save_text)
					elif SaveLimit:
						SaveLimit = False
					elif EmptyEntry:
						EmptyEntry = False
					

			if error == False:

				if event.type == pygame.MOUSEBUTTONDOWN:
					if load_box.collidepoint(event.pos):
						loadactive = True
						if load_text == 'Enter to load grid':
							load_text = ''
					else:
						loadactive = False
						if load_text == '':
							load_text = 'Enter to load grid'

					if save_box.collidepoint(event.pos):
						saveactive = True
						if save_text == 'Enter to save grid':
							save_text = ''
					else:
						saveactive = False
						if save_text == '':
							save_text = 'Enter to save grid'

					if delete_box.collidepoint(event.pos):
						deleteactive = True
						if delete_text == 'Enter to delete grid':
							delete_text = ''
					else:
						deleteactive = False
						if delete_text == '':
							delete_text = 'Enter to delete grid'


				if pygame.mouse.get_pressed()[0]:	 #LEFT MOUSE BUTTON
					pos1 = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos1, ROWS, width)
					try:
						node = grid[row][col]
					except:
						continue
					if not start and node != end:
						start = node
						start.make_start()
					elif not end and node != start:
						end = node
						end.make_end()
					elif node != start and node != end:
						node.make_barrier()


				elif pygame.mouse.get_pressed()[2]:   #RIGHT MOUSE BUTTON
					pos1 = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos1, ROWS, width)
					try:
						node = grid[row][col]
					except:
						continue
					node.reset()
					if node == start:
						start = None
					if node == end:
						end = None
				
				if event.type == pygame.KEYDOWN:
					if loadactive:
						if event.key == pygame.K_RETURN:
							if load_text == '' or load_text.isspace():
								error = True
								EmptyEntry = True
								break
							#(load_text)
							try:
								with open(load_text, 'rb') as filehandle:	# read the data as binary data stream
									grid = pickle.load(filehandle)
							except:
								error = True
								GridNotExist = True
								break
							for row in grid:
								for node in row:
									if node.color == ORANGE:
										start = node
										start.make_start()
									elif node.color == CYAN:
										end = node
										end.make_end()
									elif node.color == BLACK:
										node.make_barrier()
									elif node.color == YELLOW or node.color == RED or node.color == GREEN:
										node.reset()
							load_text = ''
						elif event.key == pygame.K_BACKSPACE:
							load_text = load_text[:-1]
						else:
							if len(load_text) < 21:
								load_text += event.unicode
							else:
								continue

					if saveactive:
						if event.key == pygame.K_RETURN:
							if save_text == '' or save_text.isspace():
								error = True
								EmptyEntry = True
								break

							if len(saved_list) < 21:
								if save_text in saved_list:
									error = True
									NameCopy = True
									break
								try:
									with open(save_text, 'wb') as filehandle:	# store the data as binary data stream
										pickle.dump(grid, filehandle)
								except:
									error = True
									IllegalSave = True
									break
								saved_list.append(save_text)
								#(saved_list)
							else:
								error = True
								SaveLimit = True
								break
						elif event.key == pygame.K_BACKSPACE:
							save_text = save_text[:-1]
						else:
							if len(save_text) < 21:
								save_text += event.unicode
							else:
								continue

					if deleteactive:
						if event.key == pygame.K_RETURN:
							if delete_text == '' or delete_text.isspace():
								error = True
								EmptyEntry = True
								break
							#(delete_text)
							try:
								os.remove(delete_text)
								saved_list.remove(delete_text)
							except:
								error = True
								GridNotExist = True
								break
							#(saved_list)
							delete_text = ''
						elif event.key == pygame.K_BACKSPACE:
							delete_text = delete_text[:-1]
						else:
							if len(delete_text) < 21:
								delete_text += event.unicode
							else:
								continue

					if not loadactive and not saveactive and not deleteactive:
						if event.key == pygame.K_SPACE and start and end:	 #SPACEBAR
							for row in grid:
								for node in row:
									if node.color == YELLOW or node.color == RED or node.color == GREEN:
										node.reset()
							for row in grid:
								for node in row:
									node.update_nieghbors(grid)

							if not algorithm(lambda: draw(window, grid, ROWS, width, loadboxcolor, saveboxcolor, deleteboxcolor, load_txt_surface, save_txt_surface, delete_txt_surface, error, GridNotExist, NameCopy, PathNotExist, IllegalSave, SaveLimit, EmptyEntry), grid, start, end):
								error = True
								PathNotExist = True


						if event.key == pygame.K_r:		 #KEY 'r'
							start = None
							end = None
							grid = make_grid(ROWS, width)

		if loadactive:
			loadboxcolor = pygame.Color(0, 220, 0)
			load_txt_surface = font_box.render(load_text, True, BLACK)
		else:
			loadboxcolor = pygame.Color('lightgreen')
			load_txt_surface = font_box.render(load_text, True, GREY)


		if saveactive:
			saveboxcolor = pygame.Color('dodgerblue')
			save_txt_surface = font_box.render(save_text, True, BLACK)
		else:
			saveboxcolor = pygame.Color('lightskyblue')
			save_txt_surface = font_box.render(save_text, True, GREY)


		if deleteactive:
			deleteboxcolor = pygame.Color(255, 40, 40)
			delete_txt_surface = font_box.render(delete_text, True, (255, 40, 40))
		else:
			deleteboxcolor = pygame.Color(255, 125, 125)
			delete_txt_surface = font_box.render(delete_text, True, (255, 125, 125))



	pygame.quit()

main(WINDOW, WIDTH)