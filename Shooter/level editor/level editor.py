import pygame

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

# Load images
pine1_img = pygame.image.load('images/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('images/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('images/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('images/background/sky_cloud.png').convert_alpha()

# store tiles in list 
image_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'images/tile/{x}.png').convert_alpha()


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


run = True
while run:
	clock.tick(FPS)

	draw_bg()
	draw_grid()

	if scroll_left and scroll > 0:
		scroll -= scroll_speed
	if scroll_right:
		scroll += scroll_speed




	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				run = False

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


	pygame.display.update()


pygame.quit()
