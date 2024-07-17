import pygame
import random
import sys
import time
import math

pygame.init()

def main():
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Double Shot Trainer")

    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

    target_radius = 30
    num_targets = 2
    target_life_time = 1500  
    start_time = 0
    max_lives = 3
    gray_bar_height = 40

    heart_img = pygame.image.load('data/heart.png')
    heart_img = pygame.transform.scale(heart_img, (30, 30))

    game_over = False
    score = 0
    lives = max_lives

    clock = pygame.time.Clock()

    class Target:

        def __init__(self):
            self.x = random.randint(target_radius, screen_width - target_radius)
            self.y = random.randint(gray_bar_height + target_radius, screen_height - target_radius)
            self.radius = target_radius
            self.creation_time = time.time()

        def draw(self, surface):
            steps = 4
            colors = [red, white]
            for i in range(steps, 0, -1):
                color = colors[i % 2]
                pygame.draw.circle(surface, color, (self.x, self.y), int(self.radius * (i / steps)))

    def draw_text(surface, text, font, color, position):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def create_button(surface, text, font, color, rect_color, rect_position):
        rect = pygame.Rect(rect_position)
        pygame.draw.rect(surface, rect_color, rect)
        draw_text(surface, text, font, color, (rect.x + 10, rect.y + 10))
        return rect

    def reset_game():
        nonlocal score, lives, targets, game_over, start_time, hit_countdown
        score = 0
        lives = max_lives
        targets = [Target() for _ in range(num_targets)]
        game_over = False
        start_time = time.time()
        hit_countdown = time.time()

    reset_game()

    running = True

    while running:
        delta_time = clock.tick(60)
        screen.fill(orange)

        pygame.draw.rect(screen, gray, [0, 0, screen_width, gray_bar_height])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_over:
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        reset_game()
                    elif main_menu_button.collidepoint(mouse_x, mouse_y):
                        import main
                        main.main()  
                        return
                else:
                    for target in targets:
                        distance = math.hypot(mouse_x - target.x, mouse_y - target.y)
                        if distance < target.radius:
                            targets.remove(target)
                            break
                    if len(targets) == 0:
                        score += 1
                        targets = [Target() for _ in range(num_targets)]
                        hit_countdown = time.time()

        if not game_over:
            if time.time() - hit_countdown > target_life_time / 1000:
                lives -= 1
                targets = [Target() for _ in range(num_targets)]
                hit_countdown = time.time()
                if lives <= 0:
                    game_over = True

            for target in targets:
                target.draw(screen)

        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 5))

        for i in range(lives):
            screen.blit(heart_img, (screen_width - 40 - i * 40, 5))

        if game_over:
            font = pygame.font.SysFont(None, 36)
            end_text = font.render("GAME OVER", True, red)
            screen.blit(end_text, (screen_width / 2 - end_text.get_width() / 2, screen_height / 2 - end_text.get_height() / 2))
            play_again_button = create_button(screen, "PLAY AGAIN", font, white, black, (screen_width / 2 - 85, screen_height / 2 + 40, 170, 48))
            main_menu_button = create_button(screen, "MAIN MENU", font, white, black, (screen_width / 2 - 85, screen_height / 2 + 100, 170, 48))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
