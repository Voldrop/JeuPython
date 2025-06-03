# Action-RPG 2D top-down skeleton using pygame
# Modern pixel art animations, procedural dungeons, loot system

import random
import pygame

# --- Asset Management ---
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, key, path):
        self.images[key] = pygame.image.load(path).convert_alpha()

    def load_sound(self, key, path):
        self.sounds[key] = pygame.mixer.Sound(path)

    def get_image(self, key):
        return self.images.get(key)

    def get_sound(self, key):
        return self.sounds.get(key)


# --- Entities ---
class Entity(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt, game):
        self.rect.center += self.velocity * dt

class Player(Entity):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.health = 100
        self.inventory = []

    def handle_input(self, keys):
        speed = 200
        self.velocity = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            self.velocity.y = -speed
        if keys[pygame.K_s]:
            self.velocity.y = speed
        if keys[pygame.K_a]:
            self.velocity.x = -speed
        if keys[pygame.K_d]:
            self.velocity.x = speed

class Enemy(Entity):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.health = 50

    def update(self, dt, game):
        # Basic AI: move toward player
        player_pos = pygame.Vector2(game.player.rect.center)
        direction = player_pos - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.velocity = direction * 100
        super().update(dt, game)

# --- Dungeon Generation ---
class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[0 for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.generate()

    def generate(self):
        # Very simplistic room generation
        for _ in range(5):
            w, h = random.randint(5, 10), random.randint(5, 10)
            x, y = random.randint(1, self.width - w - 1), random.randint(1, self.height - h - 1)
            self.rooms.append(pygame.Rect(x, y, w, h))
        # TODO: connect rooms with corridors

# --- HUD ---
class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont('Arial', 18)

    def draw(self, surface):
        health_text = self.font.render(f'HP: {self.player.health}', True, (255, 255, 255))
        surface.blit(health_text, (10, 10))

# --- Main Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        # Placeholder: load assets here
        self.player = Player(pygame.Surface((32, 32)), (400, 300))
        self.enemies = pygame.sprite.Group()
        self.dungeon = Dungeon(50, 50)
        self.hud = HUD(self.player)
        self.running = True

    def spawn_enemy(self, pos):
        enemy = Enemy(pygame.Surface((32, 32)), pos)
        self.enemies.add(enemy)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

            self.player.update(dt, self)
            self.enemies.update(dt, self)

            self.screen.fill((30, 30, 30))
            self.screen.blit(self.player.image, self.player.rect)
            for enemy in self.enemies:
                self.screen.blit(enemy.image, enemy.rect)
            self.hud.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.spawn_enemy((200, 200))
    game.run()
