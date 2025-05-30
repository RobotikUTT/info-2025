import pygame

def show_score(score):
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('Score')
    font = pygame.font.Font(None, 200)
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Rendre le texte sur une surface
        text_surface = font.render(str(score), True, (255, 255, 255))
        # Rotation à 90 degrés
        rotated_surface = pygame.transform.rotate(text_surface, 270)  # angle en degrés, sens horaire

        # Position pour centrer le texte tourné sur l'écran
        rect = rotated_surface.get_rect(center=(150, 100))  # centre écran 300x200

        screen.blit(rotated_surface, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()