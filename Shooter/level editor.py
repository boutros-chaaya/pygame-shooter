import pygame
import csv


#button class
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


pygame.init()


# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# Define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 10

FPS = 60
clock = pygame.time.Clock()

# Define Colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
text_color = (73, 92, 62)

# define font
font = pygame.font.SysFont('Futura', 30)


# create empty tile list
world_data = []
for i in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


# Load images
pine1_img = pygame.image.load('images/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('images/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('images/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('images/background/sky_cloud.png').convert_alpha()
save_img = pygame.image.load('images/tile/save_btn.png').convert_alpha()
load_img = pygame.image.load('images/tile/load_btn.png').convert_alpha()

# store tiles in list 
image_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'images/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	image_list.append(img)


def draw_text(text, text_color, x, y):
	text_surface = font.render(text, True, text_color)
	text_rectangle = text_surface.get_rect(midleft=(x, y))
	screen.blit(text_surface, text_rectangle)
	



def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for i in range(4):
		screen.blit(sky_img, ((i * width)- scroll * 0.5, 0))
		screen.blit(mountain_img, ((i * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((i * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((i * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))


def draw_grid():
	# vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

	# horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


# funciton for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(image_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
				
				

# create buttons
save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
button_list = []
button_col = 0
button_row = 0 
for i in range(len(image_list)):
	tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, image_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0


run = True
while run:
	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()


	# save and load data
	if save_button.draw(screen):
		# save level
		with open (f'level{level}_data', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for row in world_data:
				writer.writerow(row)

	if load_button.draw(screen):
		# load level
		# reset scroll
		scroll = 0
		with open (f'level{level}_data', 'r', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					pass
				


	if scroll_left and scroll > 0:
		scroll -= scroll_speed
	if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += scroll_speed


	# add new tiles to the map 
	# get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE
	
	# check that the coordinates are within the tiles area
	if pos[0] < SCREEN_WIDTH and pos [1] < SCREEN_HEIGHT:
		# update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x	] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				run = False

	#for event in pygame.event.get():
		# scrolling
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				scroll_speed = 20

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				scroll_speed = 10

			# changing levels
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level != 0:
				level -= 1


	# draw tile pannel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
	
	# choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count
	
	# highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	# show level number
	draw_text(f'Level: {level}', text_color, 25, 665)
	draw_text('Press UP or DOWN to change level', text_color, 25, 700)

	pygame.display.update()


pygame.quit()
