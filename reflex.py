import pygame
import sys
import time
import random

pygame.init()


def main():
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Reflex Trainer")

    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

    target_radius = 50
    num_trials = 5
    reaction_times = []

    clock = pygame.time.Clock()

    def draw_text(surface, text, font, color, position):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def show_target(surface, position, radius):
        steps = 4
        colors = [red, white]
        for i in range(steps, 0, -1):
            color = colors[i % 2]
            pygame.draw.circle(surface, color, position,
                               int(radius * (i / steps)))

    def create_button(surface, text, font, color, rect_color, rect_position):
        rect = pygame.Rect(rect_position)
        pygame.draw.rect(surface, rect_color, rect)
        draw_text(surface, text, font, color, (rect.x + 10, rect.y + 10))
        return rect

    def reset_game():
        nonlocal trial_count, target_visible, target_appear_time, trial_delay, last_reaction_time, reaction_times
        trial_count = 0
        target_visible = False
        target_appear_time = 0
        trial_delay = random.uniform(1, 4)
        last_reaction_time = None
        reaction_times = []
        pygame.time.set_timer(pygame.USEREVENT, int(trial_delay * 1000))

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    reset_game()

    running = True
    while running:
        screen.fill(orange)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if target_visible:
                    reaction_time = time.time() - target_appear_time
                    reaction_times.append(reaction_time * 1000)
                    last_reaction_time = reaction_time * 1000
                    target_visible = False
                    trial_count += 1
                    if trial_count < num_trials:
                        trial_delay = random.uniform(1, 4)
                        pygame.time.set_timer(pygame.USEREVENT,
                                              int(trial_delay * 1000))
                    else:
                        avg_reaction_time = sum(reaction_times) / len(
                            reaction_times)
                        screen.fill(orange)
                        result_text = f"Average Reaction Time: {avg_reaction_time:.2f} ms"
                        draw_text(
                            screen, result_text, font, black,
                            (screen_width / 2 - font.size(result_text)[0] / 2,
                             screen_height / 2 -
                             font.size(result_text)[1] / 2))

                        play_again_button = create_button(
                            screen, "PLAY AGAIN", small_font, white, black,
                            (screen_width / 2 - 85, screen_height / 2 + 40,
                             170, 48))
                        main_menu_button = create_button(
                            screen, "MAIN MENU", small_font, white, black,
                            (screen_width / 2 - 85, screen_height / 2 + 100,
                             170, 48))

                        pygame.display.flip()

                        waiting_for_input = True
                        while waiting_for_input:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = event.pos
                                    if play_again_button.collidepoint(
                                            mouse_x, mouse_y):
                                        reset_game()
                                        waiting_for_input = False
                                    elif main_menu_button.collidepoint(
                                            mouse_x, mouse_y):
                                        import main
                                        main.main()

                        continue

            elif event.type == pygame.USEREVENT and not target_visible and trial_count < num_trials:
                target_appear_time = time.time()
                target_visible = True

        if target_visible:
            show_target(screen, (screen_width // 2, screen_height // 2),
                        target_radius)

        if last_reaction_time is not None:
            reaction_text = f"Last Reaction Time: {last_reaction_time:.2f} ms"
            draw_text(screen, reaction_text, small_font, black, (10, 50))

        trial_text = f"Trial: {trial_count + 1}/{num_trials}"
        draw_text(screen, trial_text, small_font, black, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
