import pygame

def draw_button(screen, text, x, y, w, h, color):
   
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
 
    font = pygame.font.SysFont("Arial", 30, bold=True)
    text_render = font.render(text, True, (255, 255, 255))
    
    text_rect = text_render.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_render, text_rect)


def get_user_name(screen):
    name = ""
    font = pygame.font.SysFont("Arial", 40)
    clock = pygame.time.Clock()
    input_active = True

    while input_active:
        screen.fill((30, 30, 30)) 
        
       
        prompt_font = pygame.font.SysFont("Arial", 25)
        prompt = prompt_font.render("Type your name and press ENTER:", True, (200, 200, 200))
        screen.blit(prompt, (50, 200))
        
       
        name_surf = font.render(name + "|", True, (255, 255, 0))
        screen.blit(name_surf, (50, 250))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name != "":
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
               
                    if len(name) < 15:
                        name += event.unicode
        
        clock.tick(30)
    return name
