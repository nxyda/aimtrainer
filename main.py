import pygame
import sys
import aim_trainer
import double_shot
import reflex

pygame.init()


def main():
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Aim Trainer - Main Menu")

    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

    clock = pygame.time.Clock()

    # Load images
    aim_trainer_img = pygame.image.load('data/aim_trainer.png')
    double_shot_img = pygame.image.load('data/double_shot.png')
    reflex_img = pygame.image.load('data/reflex.png')
    target_tracking_img = pygame.image.load('data/target_tracking.png')

    def draw_text(surface, text, font, color, position):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, position)

    def create_image_button(surface, img, position):
        rect = img.get_rect(center=position)
        surface.blit(img, rect.topleft)
        return rect

    running = True
    while running:
        screen.fill(orange)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if aim_trainer_button.collidepoint(mouse_x, mouse_y):
                    aim_trainer.main()
                elif double_shot_button.collidepoint(mouse_x, mouse_y):
                    double_shot.main()
                elif reflex_button.collidepoint(mouse_x, mouse_y):
                    reflex.main()
                elif target_tracking_button.collidepoint(mouse_x, mouse_y):
                    pass

        font = pygame.font.SysFont(None, 48)
        title_text = font.render("Aim Trainer", True, black)
        screen.blit(title_text,
                    (screen_width / 2 - title_text.get_width() / 2, 20))

        aim_trainer_button = create_image_button(screen, aim_trainer_img,
                                                 (screen_width / 2, 200))
        double_shot_button = create_image_button(screen, double_shot_img,
                                                 (screen_width / 2, 300))
        reflex_button = create_image_button(screen, reflex_img,
                                            (screen_width / 2, 400))
        target_tracking_button = create_image_button(screen,
                                                     target_tracking_img,
                                                     (screen_width / 2, 500))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
