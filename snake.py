import pygame, sys

pygame.init()

screen = pygame.display.set_mode((400, 500))

clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill((0, 0, 255))

# Rect allows us to control more points rather than just the top left point
test_rect = pygame.Rect(100, 200, 100, 101)  # Rect(x, y, w, h) where (x,y) is coordinates of top left point

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.fill(pygame.Color('gold'))
    screen.fill((175, 215, 70))
    pygame.draw.rect(screen, pygame.Color('Red'), test_rect)  # pygame.draw.rect(surface, color, rect)
    # we could also use it to draw other shapes like pygame.draw.ellipse() etc

    # specifies where the top left corner of our test_surface will be placed
    screen.blit(test_surface, (200, 250))  # block image transformer

    pygame.display.update()
    clock.tick(60)



