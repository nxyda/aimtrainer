import pygame
import sys
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_RADIUS = 50
TARGET_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (255, 165, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 36
GAME_DURATION = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Target Tracking")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, FONT_SIZE)
small_font = pygame.font.SysFont(None, 24)

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def draw_target(surface, position, radius):
    steps = 4
    colors = [TARGET_COLOR, WHITE]
    for i in range(steps, 0, -1):
        color = colors[i % 2]
        pygame.draw.circle(surface, color, position, int(radius * (i / steps)))

def draw_button(surface, text, font, color, button_color, rect):
    pygame.draw.rect(surface, button_color, rect)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (
        rect.x + (rect.width - text_surface.get_width()) // 2,
        rect.y + (rect.height - text_surface.get_height()) // 2
    ))

def reset_game():
    click_count = 0
    start_time = time.time()

    target_pos = [random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS),
                  random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)]
    target_velocity = [random.choice([-4, 4]), random.choice([-4, 4])]

    return click_count, start_time, target_pos, target_velocity

def game_loop():
    click_count, start_time, target_pos, target_velocity = reset_game()

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        draw_target(screen, target_pos, TARGET_RADIUS)

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

    return click_count

def main():
    while True:
        click_count = game_loop()

        screen.fill(BACKGROUND_COLOR)
        final_text = f"Final Clicks: {click_count}"
        draw_text(screen, final_text, font, TEXT_COLOR, 
                  (SCREEN_WIDTH // 2 - font.size(final_text)[0] // 2, SCREEN_HEIGHT // 2 - font.size(final_text)[1] // 2))

        play_again_button = pygame.Rect((SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 40, 170, 48))
        main_menu_button = pygame.Rect((SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 100, 170, 48))

        draw_button(screen, "PLAY AGAIN", small_font, WHITE, (0, 128, 0), play_again_button)
        draw_button(screen, "MAIN MENU", small_font, WHITE, (128, 0, 0), main_menu_button)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        waiting_for_input = False
                    elif main_menu_button.collidepoint(mouse_x, mouse_y):
                        import main
                        main.main()
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
