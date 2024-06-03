import pygame, sys

pygame.init()

screen = pygame.display.set_mode((400, 500))

clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill((0, 0, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.fill(pygame.Color('gold'))
    screen.fill((175, 215, 70))

    # specifies where the top left corner of our test_surface will be placed
    screen.blit(test_surface, (200, 250))  # block image transformer


    pygame.display.update()


