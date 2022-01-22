from pygame.locals import *
import pygame

player_width = 32
player_height = 32
wall_width = 64
wall_height = 64


class Player(pygame.sprite.Sprite):
    x = 50
    y = 50
    speed = 8

    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("player.png"), (player_width, player_height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 64
        self.rect.y = 64

   # def moveRight(self):
    #    self.x = self.x + self.speed

    #def moveLeft(self):
     #   self.x = self.x - self.speed

    #def moveUp(self):
     #   self.y = self.y - self.speed

    #def moveDown(self):
     #   self.y = self.y + self.speed


class Maze:
    def __init__(self):
        self.M = 10
        self.N = 8
        self.maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.pieces = self.Generate()

    def Generate(self):
        y = 0
        wall_pieces = []
        for row in self.maze:
            x = 0
            for column in row:
                if int(column):  # if 1:
                    new_wall_piece = Walls(x, y)
                    wall_pieces.append(new_wall_piece)
                x += wall_height
            y += wall_width
        return wall_pieces

    def draw(self, display_surf, image_surf):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                display_surf.blit(image_surf, (bx * 64, by * 64))

            bx = bx + 1
            if bx > self.M - 1:
                bx = 0
                by = by + 1


class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Walls, self).__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.transform.scale(
            pygame.image.load("black.png"), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0


    def __init__(self):
        self.sprite = pygame.sprite.Group()
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze()
        self._background_colour = (255, 255, 255)
        self.on_init()

        self.Run()

    def Run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))

        pygame.display.init()
        pygame.display.set_caption("The Maze Game")
        pygame.key.set_repeat(25)
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen.fill(self._background_colour)

        for piece in self.maze.pieces:
            self.sprite.add(piece)
        self.sprite.add(self.player)
        self.sprite.draw(self.screen)
        pygame.display.flip()

        while self._running:
            self.Events(pygame.event.get())
            pygame.display.flip()
            self.clock.tick(50)
        pygame.quit()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption("Maze Game")
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("black.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def Events(self, events):

        # Method manages events - keystrokes, quitting, movement, collision and drawing IF movement has occured

        prev_location = [self.player.rect.x, self.player.rect.y]
        possible_location_x = [self.player.rect.x, self.player.rect.y]
        possible_location_y = [self.player.rect.x, self.player.rect.y]
        next_position = [self.player.rect.x, self.player.rect.y]
        for e in events:
            if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
                self._running = 0
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            possible_location_x[0] -= self.player.speed if self.player.rect.x > 0 else 0
            print("a")
        if keys[K_RIGHT] or keys[K_d]:
            possible_location_x[0] += self.player.speed if self.player.rect.x < self.windowWidth - 32 else 0
            print("d")
        if keys[K_UP] or keys[K_w]:
            possible_location_y[1] -= self.player.speed if self.player.rect.y > 0 else 0
            print("w")
        if keys[K_DOWN] or keys[K_s]:
            possible_location_y[1] += self.player.speed if self.player.rect.y < self.windowHeight - 32 else 0
            print("s")

        self.player.rect.x, self.player.rect.y = possible_location_x
        if not any(piece.rect.colliderect(self.player.rect) for piece in self.maze.pieces):
            # if colliderect with any maze wall pieces and the player is True, player is returned to their
            # previous location before screen is updated

            next_position = (self.player.rect.x, next_position[1])
            #print('collision')

        self.player.rect.x, self.player.rect.y = possible_location_y

        if not any(piece.rect.colliderect(self.player.rect) for piece in self.maze.pieces):
            # if colliderect with any maze wall pieces and the player is True, player is returned to their
            # previous location before screen is updated

            next_position = (next_position[0], self.player.rect.y)
            # print('collision')

        self.player.rect.x, self.player.rect.y = next_position

        if prev_location != (self.player.rect.x, self.player.rect.y):

            # if player location does not match previous location, the background and sprites will need to be
            # drawn agains

            self.screen.fill(self._background_colour)
            self.sprite.draw(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    game = App()

