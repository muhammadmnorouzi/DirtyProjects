import pygame
import sys
from random import randint , choice
from time import sleep
from datetime import datetime

class Enemy(object):
    """
    enemy generator
    """
    
    def __init__(self , size = (20 , 20) , pos = (0 , 0) , health = 3 , screen_size = (320 , 600)):
        """
        args:
        	size:tup:size of a rectangle
        	pos: tup:posision
        	health:int
        	screen_size:tup:generate enemies optimized
        """
        self.screen_size = screen_size
        self.position = pos
        self.size = size
        self.health = health
    
    def render(self , screen):
        """
        args:
        	screen:Pygame display
        drawing the instance of enemy
        """
        x , y = self.position
        w , h = self.size
        health_3_color =(0 , 255 , 255)
        health_2_color =(127 , 255 , 0)
        health_1_color =(255 , 0 , 0)
        
        
        if self.health == 3:
            color = health_3_color
        if self.health == 2:
            color = health_2_color
        if self.health == 1:
            color = health_1_color
            
        rect_object = pygame.Rect((x , y , w , h))
        pygame.draw.rect(screen , color , rect_object , 5)
    
    def next(self):
        """
        changes the position of enemy instance to x , y + h
        """
        x , y = self.position
        w , h = self.size
        
        self.position = (x , y + h)
        
        
class Shoots(object):
    """
    """
    
    shoots = []

    def __init__(self , pos = (160 , 1000)  , step = 5 , radius = 5 , shooter_id="fighter" , screen_size = (320 , 600)):
        """
        args:
        	pos:tup:starting position of shoot
        	step:int:controls speed of shoot
        	radius:int:radius of circle(the shoot)
        	shooter_id:["fighter" ,"enemy"]:choose direction of shoot
        	screen_size:tup:correction and some other uses
        """
        self.screen_size = screen_size
        self.shooter_id = shooter_id
        self.position = pos
        self.step = step
        self.radius = radius
        self.shoots.append(self)

    def render(self , screen):
        """
        args:
        	screen:pygame display set_mode
        """

        green = (0,255,0)
        red = (255,0,0)
        #print on screen all enemies
        for shoot in Shoots.shoots:
            if shoot.shooter_id == "fighter":
                pygame.draw.circle(screen , green , shoot.position , self.radius)
            if shoot.shooter_id == "enemy" :
                pygame.draw.circle(screen , red , shoot.position , self.radius)

        #move shoots
        for index in range(len(self.shoots)):
            if self.shoots[index].shooter_id == "fighter":
                x , y = self.shoots[index].position
                self.shoots[index].position = (x , y - self.step)
            if self.shoots[index].shooter_id == "enemy":
                x , y = self.shoots[index].position
                self.shoots[index].position = (x , y + self.step)


        #delete out of screen shoots
        for shoot in self.shoots:
            x , y = shoot.position
            if shoot.shooter_id == "fighter":
                if y <= 0:
                    self.shoots.remove(shoot)
            elif shoot.shooter_id == "enemy":
                if y >= self.screen_size[1]:
                    self.shoots.remove(shoot)


class Star(object):
    """
    Background generator
    """
    
    def __init__(self , number_of_stars = 10 , screen_size = (320 , 600) ):
        """
        args:
        	number_of_stars:int:the count of starts will apear 
        	screen_size:tup:generate stars inside the screen
        """
        self.number_of_stars = number_of_stars
        self.screen_size = screen_size
        #stars:list of tuples :: position of each star
        self.stars = []
        
        #create random positions for stars
        for _ in range(self.number_of_stars):
            x , y = (randint(0 , self.screen_size[0]) , randint(0 , self.screen_size[1]))
            self.stars.append((x , y))
            
    def render(self , screen):
        """
        args:
        	screen:pygame display

        prints stars to the screen
        """
        for pos in self.stars:
            radius = randint(0 , 2)
            white   = (255 , 255 , 255)
            pygame.draw.circle(screen , white , pos , radius)
            
    def next(self):
        """
        moves the stars forward :: animates
        """
        for index in range(len(self.stars)):
            x , y = self.stars[index]
            speed = randint(1 , 4)
            
            if y + speed >= self.screen_size[1] + 10:
                new_y = -10
            else:
                new_y = y + speed
            
            self.stars[index] = (x , new_y)
        

class Fighter(object):
    """
    Fighter class
    give access to fighter
    """
    
    def __init__(self ,screen_size = (320 , 600) , size = (20 , 20) , pos = (150 , 550) , health = 3 , step = 5 , standard_height_percentage = 25):
        """
        """
        self.health =   health
        self.step   =   step
        self.position = pos
        self.size = size
        self.screen_size = screen_size
        self.standard_height_percentage =   standard_height_percentage / 100.
    
    def collision(self):
        """
        """
        self.health -= 1
        if self.health >= 0:
            return True
        else:
            return False
        
        
    def to_left(self):
        """
        """
        x , y = self.position
        if x - self.step <= 0:
            x = 0
        else:
            x = x - self.step
            
        self.position = (x , y)

        
    def to_right(self):
        """
        """
        
        x , y = self.position
        screen_width , screen_height = self.screen_size
        fighter_width , fighter_height = self.size
        
        if x + self.step + fighter_width >= screen_width:
            x = screen_width - fighter_width
        else:
            x = x + self.step
            
        self.position = (x , y)
            
        
    def to_up(self):
        """
        """
        
        x , y = self.position
        screen_width , screen_height = self.screen_size
        fighter_width , fighter_height = self.size
        
        if y - self.step <= int(screen_height * self.standard_height_percentage):
            y = int(screen_height * self.standard_height_percentage)
        else:
            y = y - self.step
            
        self.position = (x , y)
        
        
    def to_down(self):
        """
        """
        
        x , y = self.position
        screen_width , screen_height = self.screen_size
        fighter_width , fighter_height = self.size
        
        if y + self.step + fighter_height >= screen_height:
            y = screen_height - fighter_height
        else:
            y = y + self.step
            
        self.position = (x , y)
        
    def shoot(self):
        """
        """
        Shoots(self.position)
        
    def render(self , screen):
        """
        """
        x , y = self.position
        w , h = self.size
        
        green = (0 , 0 , 255)
        pygame.draw.rect(screen , green , (x , y , w , h))

    def change_position(self , new_pos):
        """
        """
        self.position = new_pos
        
class Game(object):
    """
    main game class
    """
    
    def __init__(self , SCREEN_SIZE = (320 , 600) , fighter_size = (20 , 40) , enemy_size = (20 , 20) ):
        """
        SCREEN_SIZE vals % 20 == 0
        """
        self.screen_size = SCREEN_SIZE
        
        self.enemies = []
        self.shoots  = []
        self.shoots_should_be_deleted = []
        self.enemies_should_be_deleted = []
        self.enemies_who_can_shoot = []
        
        self.score = 0
        self.star = Star(100)
        self.fighter = Fighter(step = 25 , size = fighter_size)
        self.shoot = Shoots(pos = (0 , 0) , step = 8)
        self.fighter_condition = True
    
        self.enemy_size = enemy_size
        self.count_of_enemies_in_row = int(SCREEN_SIZE[0] / self.enemy_size[0])
    
    def star_simulator(self , screen):
        self.star.render(screen)
        self.star.next()

            
    def add_new_row_of_enemies(self , row = 1 , randomly = True):
        """
        """
        #move last enemies forward
        for times in range(row):
            for index in range(len(self.enemies)):
                self.enemies[index].next()
                
        for y_coordinate in range(0 , self.enemy_size[1] * row , self.enemy_size[1]):
            for x_coordinate in range(0 , self.screen_size[0]  , self.enemy_size[0]):
                if randomly == True:
                    if randint(0 , 10) == 0:
                        self.enemies.append(Enemy(self.enemy_size , (x_coordinate , y_coordinate)))
                else:
                    self.enemies.append(Enemy(self.enemy_size , (x_coordinate , y_coordinate)))         

    def delete_enemies_and_shoots(self):
        """
        """
        
        #delete all enemies beside shoots
        for item in self.enemies_should_be_deleted:
            self.enemies.remove(item)
        
        #delete all shoots beside enemies
        for item in self.shoots_should_be_deleted:
            Shoots.shoots.remove(item)
        
        self.enemies_should_be_deleted  =   []
        self.shoots_should_be_deleted   =   []


    def check_collision(self):
        """
        check collision of shoots with enemies
        enemies with figter
        
        delete collided enemies and shoots
        decrease fighter health if neccessary
        """
        #enemy and shoot collision chcker
        for shoot in Shoots.shoots:
            if shoot.shooter_id == "fighter":
                for enemy in self.enemies:
                    x_shoot , y_shoot = shoot.position
                    r_shoot = shoot.radius
                    x_enemy , y_enemy = enemy.position
                    w_enemy , h_enemy = enemy.size
                    
                    #collision condition of enemy and shoot
                    if x_shoot >= x_enemy and x_shoot <= (x_enemy + w_enemy):
                        if y_shoot >= y_enemy and y_shoot <= (y_enemy + h_enemy):
                            
                            if enemy.health <= 1:
                                self.score += 1
                                self.enemies_should_be_deleted.append(enemy)
                            else:
                                enemy.health -= 1
                            
                            if shoot not in self.shoots_should_be_deleted:
                                self.shoots_should_be_deleted.append(shoot)

            elif shoot.shooter_id == "enemy":
                x_shoot , y_shoot = shoot.position
                r_shoot = shoot.radius
                x_fighter , y_fighter = self.fighter.position
                w_fighter , h_fighter = self.fighter.size

                if y_shoot + r_shoot >= y_fighter:
                	if (x_shoot >= x_fighter and x_shoot <= x_fighter + w_fighter) or (x_shoot + r_shoot >= x_fighter and x_shoot + r_shoot <= x_fighter + w_fighter):
                		self.fighter.health -= 1
                		if self.fighter.health == 0:
                			self.fighter_condition = False
                		self.shoots_should_be_deleted.append(shoot)
                
                    
        #check collision of enemy and fighter
        x_fighter , y_fighter = self.fighter.position
        w_fighter , h_fighter = self.fighter.size
        for enemy in self.enemies:
            x_enemy , y_enemy = enemy.position
            w_enemy , h_enemy = enemy.size
            
            if (x_enemy <= (x_fighter + w_fighter) and x_enemy >= x_fighter ) or ((x_enemy + w_enemy) <= (x_fighter + w_fighter) and (x_enemy + w_enemy) >= (x_fighter)):
                if (y_enemy + h_enemy) >= (y_fighter):
                    
                    self.fighter_condition = self.fighter.collision()
                    
                    if enemy not in self.enemies_should_be_deleted:
                        self.enemies_should_be_deleted.append(enemy)

        #delete similer shoots and enemies
        self.shoots_should_be_deleted = set(self.shoots_should_be_deleted)
        self.enemies_should_be_deleted = set(self.enemies_should_be_deleted)
            
        #delete all collided enemies and shoots
        self.delete_enemies_and_shoots()
    
    def check_enemies_position(self):
        """
        """
        width_screen , height_screen = self.screen_size
        for enemy in self.enemies:
            x_enemy , y_enemy = enemy.position
            w_enemy , h_enemy = enemy.size
            
            if y_enemy + h_enemy >= height_screen:
                self.enemies_should_be_deleted.append(enemy)
                
                self.score -= 10
                
                if self.score < 0:
                    self.fighter_condition = False
            
    def enemy_shoots(self):
    	"""
    	"""
    	x_fighter , y_fighter = self.fighter.position
    	w_fighter , h_fighter = self.fighter.size
    	for enemy in self.enemies:
    		x_enemy , y_enemy  = enemy.position
    		w_enemy , h_enemy = enemy.size

    		absolute_distance = abs(abs(x_enemy + w_enemy) - abs(x_fighter + w_fighter))

    		#find close enemies
    		if absolute_distance <= 20:
    			self.enemies_who_can_shoot.append(enemy)

    	for shooter_enemy in self.enemies_who_can_shoot:
    		if randint(0 , 100) == 0:
	    		x_enemy , y_enemy  = enemy.position
    			w_enemy , h_enemy = enemy.size
    			#extract shoots position
    			x = x_enemy + int(w_enemy/2)
    			y = y_enemy + h_enemy
    			self.shoots.append(Shoots(pos = (x,y) , shooter_id = "enemy"))

    	self.enemies_who_can_shoot = []





    def start(self , screen):
        """
        """
        started_at = datetime.now()
        
        black = (0,0,0)
        
        #create first group of enemies
        self.add_new_row_of_enemies(row = 3)
        
        game_font = pygame.font.Font("font.ttf" , 20)
        clock = pygame.time.Clock()
        
        while True:
            
            #get current time
            now = datetime.now()
            diff = now - started_at
            
            #fill the screen with black
            screen.fill(black)
            
            #star simulation
            self.star_simulator(screen)
            
            #check if fighter condition is ok
            if self.fighter_condition == False:
                text = f"You Lost!Your score is {self.score}."
                text = game_font.render(text , True , (255 , 0 , 0))
                x , y = self.screen_size
                screen.blit(text , ( 10 , int(y/2)))
                pygame.display.update()
                sleep(5)
                pygame.quit()
                sys.exit()
            elif self.fighter_condition == True:
                text = f"Your score is {self.score}"
                text = game_font.render(text , True , (255 , 0 , 255))
                screen.blit(text , ( 10 , 10))
                text = f"Your health is {self.fighter.health}"
                text = game_font.render(text , True , (255 , 0 , 255))
                screen.blit(text , (10 , 30))
                text = f"time left: {diff}"
                text = game_font.render(text , True , (255 , 0 , 255))
                screen.blit(text , (10 , 50))
            
            #create a new row of enemies randomly
            if randint(0 , 100) == 0:
                self.add_new_row_of_enemies()

            
            #catch user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        #move fighter up
                        self.fighter.to_up()
                        
                    elif event.key == pygame.K_s:
                        #move fighter down
                        self.fighter.to_down()

                    elif event.key == pygame.K_a:
                        #move fighter left
                        self.fighter.to_left()

                    elif event.key == pygame.K_d:
                        #move fighter right
                        self.fighter.to_right()
                        
                    elif event.key == pygame.K_x:
                        #shoot
                        x_shooter , y_shooter = self.fighter.position
                        w_fighter = self.fighter.size[0]
                        if self.score <= 20:
                            self.shoots.append(Shoots(pos = ((x_shooter + int(w_fighter / 2)) , y_shooter)))
                        elif self.score > 20 and self.score <= 100:
                            self.shoots.append(Shoots(pos = ((x_shooter + w_fighter) , y_shooter)))
                            self.shoots.append(Shoots(pos = (x_shooter  , y_shooter)))
                        else:
                            self.shoots.append(Shoots(pos = ((x_shooter - int(w_fighter / 2)) , y_shooter)))
                            self.shoots.append(Shoots(pos = ((x_shooter + int(w_fighter / 2)) , y_shooter)))
                            self.shoots.append(Shoots(pos = ((x_shooter +  w_fighter + int(w_fighter / 2)) , y_shooter)))
                            
                           
                            
            
            #render fighter
            self.fighter.render(screen)
            
            #render all the enemies in the screen
            for index in range(len(self.enemies)):
                self.enemies[index].render(screen)
                
            #render shoots
            self.shoot.render(screen)
            
            #enemies shoot
            self.enemy_shoots()
                        
            #check enemies position
            self.check_enemies_position()
            
            #find all collided shoots and enemies
            self.check_collision()
            clock.tick(50)
            
            #show the whole rendered things on screen
            pygame.display.update()
            


if __name__ == "__main__":
    try:
        #scoop of testing 
        SCREEN_SIZE = (320 , 600)

        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE , pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("MMN SPACE SHOOTER")

        GAME = Game(SCREEN_SIZE)
        STARTED_GAME = GAME.start(screen)
    except Exception as error:
        print(error)