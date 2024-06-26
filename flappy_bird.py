import pygame
import neat
import time
import os 
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
gen = 0
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 10
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        # negative val is upwards (since downwards is postive y for pycharm coordinate system )
        self.vel = -10.5
        self.tick_count = 0
        self.height =  self.y
    
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5* self.tick_count**2
        # terminal velocity 
        if  d >= 16:
            d = 16
        # makes the bird jump higher
        if d < 0:
            d -= 2
        self.y = self.y + d
        
        # if the bird is going up just set the rotation to max 
        if d< 0 or self.y  < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
                
        # if the bird is going down, then nose pointing down 
        else:
            if  self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self,win):
        self.img_count += 1
        # wings flap  up
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        # wings levelled 
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        # wings down 
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        # wings level 
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        # wings flap up and reset  
        elif self.img_count < self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0 
        
        # if the bird is going down, set the image to the bird having wings levelled 
        # set the image count to animation time so it doesn't skip a frame 
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # rotate the image self.img with the angle self.tilt 
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # rotate the image around the center 
        new_rect = rotated_image.get_rect(center= self.img.get_rect(topleft= (self.x,self.y)).center)

        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom: 0
        # top piple is flipped upsdie down 
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50,450)
        # represents the y coordinate of the bottom edge of pipe so random number minus the height of pipe(320*2)
        # if minus then some part of it will go out the screen since decreasing in y coordinate 
        # in the pycharm coordinate system leads to the object going up  so if self.height = 300 and pipe
        # height is 640(320*2) the pipe will be shortened upwards by 340 (300-640=-340)
        self.top = self.height - self.PIPE_TOP.get_height()
        # represents the y coordinate of the top edge of the pipe so random number plus the gap between pipes
        # (300+ 200) = 500 - represents the y coordinate of the top edge 
        self.bottom = self.height + self.GAP 
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x , self.bottom))
     
     # pixel perfect collision 
     # mask looks at an image and looks at where the pixels are 
     # 2d list as many pixels going across and going down 
     # sees if any pixels in the list cross over with another 
     
    def collide(self, bird):
         bird_mask = bird.get_mask()
         top_mask = pygame.mask.from_surface(self.PIPE_TOP)
         bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
         
         # how far the bird is from the top pipe 
         top_offset = (self.x - bird.x , self.top - round(bird.y))
         # how far the bird is from the bottom pipe
         bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
         
         # if doesn't overlap then returns none (look at masking pygames documentation )
         b_point = bird_mask.overlap(bottom_mask, bottom_offset)
         t_point = bird_mask.overlap(top_mask, top_offset)
         
         if t_point or b_point:
             return True
         return False 
     

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self,y) :
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        # x1 moves first, then x2 moves, x2 (right edge) will move to the right-end of the window
        # as x1 moves from right-end of the window to left-end with the window wiht self.width length
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH 
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self,win):
        win.blit(self.IMG,(self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))    

# drawing everything         
def draw_window(win,birds,pipes, base, score, gen):
   
    
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
        
    text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
    win.blit(text,(WIN_WIDTH -10- text.get_width(),10))
    
    text = STAT_FONT.render("Gen: " + str(gen), 1,(255,255,255))
    win.blit(text,(10,10))
        
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes, config):
    global gen
    gen += 1
    nets = []
    ge = []
    birds = []
    # genomes () is actually a tuple (genome_id, genome_obj) 
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)
    
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    # intialize pygame window and bird 
    score = 0
    run = True
    while run:
        clock.tick(30)
        # event listener to quit pygame 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()
        #bird.move()
        pipe_ind = 0
        if len(birds)> 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind =1
        else:
            run = False 
            break 
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate((bird.y, abs(bird.y -pipes[pipe_ind].height), abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0] > 0.5: 
                bird.jump()
            
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                    
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                
            pipe.move()
        
        if add_pipe:
            score+= 1
            for g in ge:
                g.fitness += 5
                
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        for x,bird in enumerate(birds):
        # check if the bird hit the ground   
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        base.move()        
        draw_window(win, birds, pipes, base, score,gen)
   

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                        neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)
    
    
# import = pickle (pycharm lib) and save the winner object, save that as a file and use that neural netowrk associated wiht genome 
# a function that only uses one neural network  