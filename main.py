import pygame
import random
import sys
import math


pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Aim Trainer")


white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (128, 128, 128)


target_min_radius = 10
target_max_radius = 30
target_life_time = 2000  
num_targets = 5


clock = pygame.time.Clock()


score = 0


class Target:
    def __init__(self):
        self.x = random.randint(target_max_radius, screen_width - target_max_radius)
        self.y = random.randint(target_max_radius, screen_height - target_max_radius)
        self.life_time = target_life_time
        self.radius = target_min_radius
        self.growing = True

    def update(self, delta_time):
        if self.growing:
            self.radius += (target_max_radius - target_min_radius) * (delta_time / (self.life_time / 2))
            if self.radius >= target_max_radius:
                self.radius = target_max_radius
                self.growing = False
        else:
            self.radius -= (target_max_radius - target_min_radius) * (delta_time / (self.life_time / 2))
            if self.radius <= target_min_radius:
                self.radius = target_min_radius
                return False  
        return True

    def draw(self, surface):
        steps = 4
        colors = [red, white]
        for i in range(steps, 0, -1):
            color = colors[i % 2]
            pygame.draw.circle(surface, color, (self.x, self.y), int(self.radius * (i / steps)))


targets = [Target() for _ in range(num_targets)]


running = True
while running:
    delta_time = clock.tick(60)
    screen.fill(gray)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for target in targets:
                distance = math.hypot(mouse_x - target.x, mouse_y - target.y)
                if distance < target.radius:
                    score += 1
                    targets.remove(target)
                    targets.append(Target())
                    break

    for target in targets:
        if not target.update(delta_time):
            targets.remove(target)
            targets.append(Target())
        target.draw(screen)


    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
