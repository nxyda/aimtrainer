import pygame
import sys
import random
import time

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_RADIUS = 50
TARGET_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 36
GAME_DURATION = 30 


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Target Tracking")


clock = pygame.time.Clock()


font = pygame.font.SysFont(None, FONT_SIZE)

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def main():
    def reset_game():
        nonlocal click_count, start_time
        click_count = 0
        start_time = time.time()

        nonlocal target_pos, target_velocity
        target_pos = [random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS),
                      random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)]
        target_velocity = [random.choice([-5, 5]), random.choice([-5, 5])]

    target_pos = [random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS),
                  random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)]
    target_velocity = [random.choice([-5, 5]), random.choice([-5, 5])]

    click_count = 0
    start_time = time.time()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                distance = ((mouse_pos[0] - target_pos[0]) ** 2 + (mouse_pos[1] - target_pos[1]) ** 2) ** 0.5
                if distance < TARGET_RADIUS:
                    click_count += 1

        target_pos[0] += target_velocity[0]
        target_pos[1] += target_velocity[1]


        if target_pos[0] <= TARGET_RADIUS or target_pos[0] >= SCREEN_WIDTH - TARGET_RADIUS:
            target_velocity[0] = -target_velocity[0]
        if target_pos[1] <= TARGET_RADIUS or target_pos[1] >= SCREEN_HEIGHT - TARGET_RADIUS:
            target_velocity[1] = -target_velocity[1]


        pygame.draw.circle(screen, TARGET_COLOR, target_pos, TARGET_RADIUS)


        elapsed_time = time.time() - start_time
        time_left = max(GAME_DURATION - elapsed_time, 0)
        time_text = f"Time Left: {int(time_left)}s"
        draw_text(screen, time_text, font, TEXT_COLOR, (10, 10))

        click_text = f"Clicks: {click_count}"
        draw_text(screen, click_text, font, TEXT_COLOR, (10, 50))

        if time_left <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    screen.fill(BACKGROUND_COLOR)
    final_text = f"Final Clicks: {click_count}"
    draw_text(screen, final_text, font, TEXT_COLOR, (SCREEN_WIDTH // 2 - font.size(final_text)[0] // 2, SCREEN_HEIGHT // 2 - font.size(final_text)[1] // 2))
    pygame.display.flip()
    time.sleep(5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
