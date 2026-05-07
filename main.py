# Complete your game here
import random
import pygame

WIDTH = 640
HEIGHT = 500
WINDOW_HEIGHT = HEIGHT + 10

class CollectingGame:
    def __init__(self):
        pygame.init()
        
        self.load_images()
        self.highest_score = 0
        self.new_highest_score = False
        self.new_game()

        self.window = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.score_font = pygame.font.SysFont("Arial", 18)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("A collecting game")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["coin", "door", "monster", "robot"]:
            self.images.append(pygame.image.load(f"{name}.png"))

    def new_game(self):
        self.update_highest_score()
        self.game_finished = False
        self.new_highest_score = False
        self.door = self.images[1]
        self.door_x = WIDTH//2 - self.door.get_width()//2
        self.door_y = HEIGHT - self.door.get_height() - 40
        self.robot =  Robot(self.images[3])
        self.coin = Coin(self.images[0])        
        self.monster = Monster(self.images[2], self.door_x, self.door_y)
        self.monster_start_time = pygame.time.get_ticks() + 3000
        self.score = 0

    def update_highest_score(self):
        if hasattr(self, "score") and self.score > self.highest_score:
            self.highest_score = self.score
            self.new_highest_score = True

    def main_loop(self):
        while True:
            self.check_events()
            if not self.game_finished:
                if pygame.time.get_ticks() >= self.monster_start_time:
                    self.monster.move()
                self.robot.move()
                self.check_collisions()
                
            self.draw_window()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = True
                if event.key == pygame.K_UP:
                    self.robot.to_up = True
                if event.key == pygame.K_DOWN:
                    self.robot.to_down = True
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = False
                if event.key == pygame.K_UP:
                    self.robot.to_up = False
                if event.key == pygame.K_DOWN:
                    self.robot.to_down = False
            

    def check_collisions(self):
        if ( self.coin.x + self.coin.coin_img.get_width() > self.robot.x and 
            self.coin.y < self.robot.y + self.robot.robot_img.get_height() and 
            self.coin.y + self.coin.coin_img.get_height() > self.robot.y and
            self.coin.x < self.robot.x + self.robot.robot_img.get_width()):
            self.score += 1
            self.coin = Coin(self.images[0])

        robot_rect = pygame.Rect(
            self.robot.x,
            self.robot.y,
            self.robot.robot_img.get_width(),
            self.robot.robot_img.get_height()
        ).inflate(-20, -20)
        monster_rect = pygame.Rect(
            self.monster.x,
            self.monster.y,
            self.monster.monster_img.get_width(),
            self.monster.monster_img.get_height()
        ).inflate(-20, -20)

        if robot_rect.colliderect(monster_rect):
            self.game_finished = True
            self.update_highest_score()


    def draw_window(self):
        self.window.fill((230, 220, 250))

        self.window.blit(self.door, (self.door_x, self.door_y))

        self.window.blit(self.coin.coin_img, (self.coin.x, self.coin.y))
        self.window.blit(self.monster.monster_img, (self.monster.x, self.monster.y))
        self.window.blit(self.robot.robot_img, (self.robot.x, self.robot.y))
        
        newgame_text = self.score_font.render("F2 = new game", True, (255, 0, 0))
        self.window.blit(newgame_text, (320, HEIGHT - 30))

        exitgame_text = self.score_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(exitgame_text, (470, HEIGHT - 30))

        score_text = self.score_font.render(f"Score: {self.score}", True, (255, 0, 0))
        self.window.blit(score_text, (50, HEIGHT - 30))

        highest_score_text = self.score_font.render(f"Highest score: {self.highest_score}", True, (255, 0, 0))
        self.window.blit(highest_score_text, (150, HEIGHT - 30))

        if self.game_finished:

            if self.new_highest_score:
                game_text = self.game_font.render("Congratulations! New highest score!", True, (255, 255, 0))
                game_text_x = WIDTH / 2 - game_text.get_width() / 2
                game_text_y = HEIGHT / 2 - game_text.get_height() / 2 - 20
                pygame.draw.rect(self.window, (0, 0,0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
                self.window.blit(game_text, (game_text_x, game_text_y))
            else:
                game_text = self.game_font.render("Game over!", True, (255, 0, 0))
                game_text_x = WIDTH / 2 - game_text.get_width() / 2
                game_text_y = HEIGHT / 2 - game_text.get_height() / 2 - 20
                pygame.draw.rect(self.window, (0, 0,0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
                self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()
        


class Coin:
    def __init__(self,coin):
        self.coin_img = coin
        self.x = random.randint(0, WIDTH - coin.get_width())
        self.y = random.randint(0, HEIGHT - coin.get_height()-40)
       
class Robot:
    def __init__(self, robot):
        self.robot_img = robot
        self.x = 0
        self.y = 0
        self.speed = 5
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False
    
    def move(self):
        if self.to_right:
            self.x += self.speed
        if self.to_left:
            self.x -= self.speed
        if self.to_up:
            self.y -= self.speed
        if self.to_down:
            self.y += self.speed

      # keep robot inside window
        if self.x < 0:
            self.x = 0
        if self.x + self.robot_img.get_width() > WIDTH:
            self.x = WIDTH - self.robot_img.get_width()
        if self.y < 0:
            self.y = 0
        if self.y + self.robot_img.get_height() > HEIGHT:
            self.y = HEIGHT - self.robot_img.get_height()

class Monster:
    def __init__(self,monster, door_x, door_y):
        self.monster_img = monster
        self.x = door_x
        self.y = door_y
        self.speed = random.randint(3, 15)
        self.direction = "up"
    
    def move(self):
        if random.randint(1, 60) == 1:
            self.direction = random.choice(["left", "right", "up", "down"])
            self.speed = random.randint(1, 7)
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

      # keep monster inside window
        if self.x < 0:
            self.x = 0
            self.direction = random.choice(["right", "up", "down"])
        if self.x + self.monster_img.get_width() > WIDTH:
            self.x = WIDTH - self.monster_img.get_width()
            self.direction = random.choice(["left", "up", "down"])
        if self.y < 0:
            self.y = 0
            self.direction = random.choice(["left", "right", "down"])
        if self.y + self.monster_img.get_height() > HEIGHT:
            self.y = HEIGHT - self.monster_img.get_height()
            self.direction = random.choice(["left", "right", "up"])
        

if __name__ == "__main__":
    CollectingGame()
