import pygame
import sys
import random

# Константи
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ініціалізація Pygame
pygame.init()

# Екран і шрифт
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dinosaur")
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(50, HEIGHT - 100, 50, 50)
        self.jump_speed = -15
        self.gravity = 1
        self.dy = 0

    def jump(self):
        if self.rect.bottom >= HEIGHT - 50:
            self.dy = self.jump_speed

    def update(self):
        self.dy += self.gravity
        self.rect.y += self.dy
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH, HEIGHT - 80, 20, 20)

    def update(self):
        self.rect.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Game:
    def __init__(self):
        self.running = True
        self.start_menu = True
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.score = 0
        self.lives = 3
        self.clock = pygame.time.Clock()
        self.start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50, "Start/Restart")

    def reset(self):
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.score = 0
        self.lives = 3

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.start_menu:
                if self.start_button.is_clicked(event.pos):
                    self.start_menu = False
                    self.reset()
            if event.type == pygame.KEYDOWN and not self.start_menu:
                if event.key == pygame.K_SPACE:
                    self.dinosaur.jump()

    def update(self):
        if not self.start_menu:
            self.dinosaur.update()

            if random.randint(1, 100) > 98:
                self.obstacles.append(Obstacle())

            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.rect.colliderect(self.dinosaur.rect):
                    self.lives -= 1
                    self.obstacles.remove(obstacle)
                elif obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1

            if self.lives <= 0:
                self.start_menu = True

    def draw(self):
        screen.fill(WHITE)

        if self.start_menu:
            self.start_button.draw(screen)
        else:
            self.dinosaur.draw(screen)
            for obstacle in self.obstacles:
                obstacle.draw(screen)

            score_text = font.render(f"Score: {self.score}", True, BLACK)
            lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 40))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()