import pygame
import random
import sys
import math
import time

pygame.init()


def main():
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Aim Trainer")

    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

    target_min_radius = 10
    target_max_radius = 30
    target_life_time = 2000
    num_targets = 5
    max_missed_targets = 100
    gray_bar_height = 40

    global game_over, score, missed_targets, last_hit_time, reaction_times, targets, start_time, elapsed_time, play_again_button, go_to_main_button

    game_over = False
    score = 0
    missed_targets = 0
    last_hit_time = 0
    reaction_times = []

    clock = pygame.time.Clock()

    class Target:

        def __init__(self):
            self.x = random.randint(target_max_radius,
                                    screen_width - target_max_radius)
            self.y = random.randint(gray_bar_height + target_max_radius,
                                    screen_height - target_max_radius)
            self.life_time = target_life_time
            self.radius = target_min_radius
            self.growing = True

        def update(self, delta_time):
            if self.growing:
                self.radius += (target_max_radius -
                                target_min_radius) * (delta_time /
                                                      (self.life_time / 2))
                if self.radius >= target_max_radius:
                    self.radius = target_max_radius
                    self.growing = False
            else:
                self.radius -= (target_max_radius -
                                target_min_radius) * (delta_time /
                                                      (self.life_time / 2))
                if self.radius <= target_min_radius:
                    self.radius = target_min_radius
                    return False
            return True

        def draw(self, surface):
            steps = 4
            colors = [red, white]
            for i in range(steps, 0, -1):
                color = colors[i % 2]
                pygame.draw.circle(surface, color, (self.x, self.y),
                                   int(self.radius * (i / steps)))

    def draw_text(surface, text, font, color, position):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def create_button(surface, text, font, color, rect_color, rect_position):
        rect = pygame.Rect(rect_position)
        pygame.draw.rect(surface, rect_color, rect)
        draw_text(surface, text, font, color, (rect.x + 10, rect.y + 10))
        return rect

    def reset_game():
        global score, missed_targets, reaction_times, last_hit_time, targets, game_over, start_time, elapsed_time
        score = 0
        missed_targets = 0
        reaction_times = []
        last_hit_time = None
        targets = [Target() for _ in range(num_targets)]
        game_over = False
        start_time = time.time()
        elapsed_time = 0

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
                    elif go_to_main_button.collidepoint(mouse_x, mouse_y):
                        # Przejście do main.py
                        pygame.quit()
                        import main
                        main.main()
                        sys.exit()
                else:
                    for target in targets:
                        distance = math.hypot(mouse_x - target.x,
                                              mouse_y - target.y)
                        if distance < target.radius:
                            score += 1
                            reaction_times.append((time.time() -
                                                   last_hit_time) *
                                                  1000 if last_hit_time else 0)
                            last_hit_time = time.time()
                            targets.remove(target)
                            targets.append(Target())
                            break

        if not game_over:
            elapsed_time = time.time() - start_time
            for target in targets:
                if not target.update(delta_time):
                    targets.remove(target)
                    targets.append(Target())
                    missed_targets += 1
                    if missed_targets >= max_missed_targets:
                        game_over = True

                target.draw(screen)

        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {score}", True, black)
        missed_text = font.render(
            f"Missed: {missed_targets}/{max_missed_targets}", True, black)
        time_text = font.render(f"Time: {elapsed_time:.2f} s", True, black)

        screen.blit(score_text, (10, 5))
        screen.blit(missed_text, (200, 5))
        screen.blit(time_text, (400, 5))

        if reaction_times:
            avg_reaction_time = sum(reaction_times) / len(reaction_times)
            reaction_text = font.render(
                f"Avg Reaction Time: {avg_reaction_time:.2f} ms", True, black)
            screen.blit(reaction_text,
                        (screen_width - reaction_text.get_width() - 10, 5))

        if game_over:
            font = pygame.font.SysFont(None, 36)
            end_text = font.render("GAME OVER", True, red)
            screen.blit(end_text,
                        (screen_width / 2 - end_text.get_width() / 2,
                         screen_height / 2 - end_text.get_height() / 2))
            play_again_button = create_button(
                screen, "PLAY AGAIN", font, white, black,
                (screen_width / 2 - 85, screen_height / 2 + 40, 170, 48))
            go_to_main_button = create_button(
                screen, "GO TO MAIN", font, white, black,
                (screen_width / 2 - 85, screen_height / 2 + 100, 170, 48))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
