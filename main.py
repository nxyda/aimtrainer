import pygame
import random
import sys

from pygame.constants import USEREVENT

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Aim Trainer")

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

target_radius = 20
target_time = 2000

clock = pygame.time.Clock()
target_timer = pygame.USEREVENT + 1
pygame.time.set_timer(target_timer, target_time)

score = 0

def draw_target():
  x = random.randint(target_radius, screen_width - target_radius)
  y = random.randint(target_radius, screen_height - target_radius)
  pygame.draw.circle(screen, red, (x, y), target_radius)
  return x, y

running = True
target_position = draw_target()

while running:
  screen.fill(white)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      distance = ((mouse_x - target_position[0]) ** 2 + (mouse_y - target_position[1]) ** 2) ** 0.5
      if distance < target_radius:
        score += 1
        target_position = draw_target()
    elif event.type == target_timer:
      target_position = draw_target()

  pygame.draw.circle(screen, red, target_position, target_radius)
  
  font = pygame.font.SysFont(None, 36)
  score_text = font.render(f"Score: {score}", True, black)
  screen.blit(score_text, (10, 10))
  
  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()

      
