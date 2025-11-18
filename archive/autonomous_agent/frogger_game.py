import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRID_SIZE = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger Game")
clock = pygame.time.Clock()


class Frog:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - GRID_SIZE
        self.size = 40
        self.lives = 3
        self.score = 0

    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            self.x = new_x
            self.y = new_y
            if dy < 0:  # Moving forward
                self.score += 10

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), self.size // 2)
        # Eyes
        pygame.draw.circle(screen, WHITE, (self.x + 20, self.y + 15), 8)
        pygame.draw.circle(screen, WHITE, (self.x + 35, self.y + 15), 8)
        pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 15), 4)
        pygame.draw.circle(screen, BLACK, (self.x + 35, self.y + 15), 4)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - GRID_SIZE


class Vehicle:
    def __init__(self, y, speed, color, width):
        self.y = y
        self.speed = speed
        self.color = color
        self.width = width
        self.height = 40
        if speed > 0:
            self.x = -width
        else:
            self.x = WIDTH

    def update(self):
        self.x += self.speed
        if self.speed > 0 and self.x > WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = WIDTH

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height), 2)


class Log:
    def __init__(self, y, speed, width):
        self.y = y
        self.speed = speed
        self.width = width
        self.height = 40
        if speed > 0:
            self.x = -width
        else:
            self.x = WIDTH

    def update(self):
        self.x += self.speed
        if self.speed > 0 and self.x > WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = WIDTH

    def draw(self):
        pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (101, 67, 33), (self.x, self.y, self.width, self.height), 2)


def main():
    frog = Frog()

    # Create vehicles
    vehicles = [
        Vehicle(450, 3, RED, 80),
        Vehicle(400, -2, YELLOW, 60),
        Vehicle(350, 4, RED, 100),
        Vehicle(300, -3, YELLOW, 70),
        Vehicle(250, 2, RED, 90),
    ]

    # Create logs
    logs = [Log(200, 2, 150), Log(150, -1.5, 120), Log(100, 2.5, 180)]

    font = pygame.font.Font(None, 36)
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    frog.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    frog.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    frog.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    frog.move(1, 0)

        # Update
        for vehicle in vehicles:
            vehicle.update()
        for log in logs:
            log.update()

        # Check collisions with vehicles
        frog_rect = pygame.Rect(frog.x, frog.y, GRID_SIZE, GRID_SIZE)
        for vehicle in vehicles:
            vehicle_rect = pygame.Rect(vehicle.x, vehicle.y, vehicle.width, vehicle.height)
            if frog_rect.colliderect(vehicle_rect):
                frog.lives -= 1
                frog.reset()
                if frog.lives <= 0:
                    print(f"Game Over! Final Score: {frog.score}")
                    running = False

        # Check if on log in water
        if 100 <= frog.y <= 200:
            on_log = False
            for log in logs:
                log_rect = pygame.Rect(log.x, log.y, log.width, log.height)
                if frog_rect.colliderect(log_rect):
                    on_log = True
                    frog.x += log.speed  # Move with log
                    break
            if not on_log:
                frog.lives -= 1
                frog.reset()
                if frog.lives <= 0:
                    print(f"Game Over! Final Score: {frog.score}")
                    running = False

        # Check win condition
        if frog.y <= 50:
            frog.score += 100
            frog.reset()

        # Draw
        screen.fill(BLACK)

        # Draw safe zones
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE))  # Start
        pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, GRID_SIZE))  # Goal

        # Draw road
        pygame.draw.rect(screen, GRAY, (0, 250, WIDTH, 250))

        # Draw water
        pygame.draw.rect(screen, BLUE, (0, 100, WIDTH, 150))

        # Draw game objects
        for vehicle in vehicles:
            vehicle.draw()
        for log in logs:
            log.draw()
        frog.draw()

        # Draw UI
        score_text = font.render(f"Score: {frog.score}", True, WHITE)
        lives_text = font.render(f"Lives: {frog.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
