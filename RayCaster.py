import pygame
from math import cos, sin, pi

BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)
GREEN = (152,251,152)

textures = {
    '1' : pygame.image.load('./images/diamond.png'),
    '2' : pygame.image.load('./images/stone.png'),
    '3' : pygame.image.load('./images/emerald.png')
    }

class Raycaster(object):
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.blocksize = 25
        self.wallHeight = 25

        self.stepSize = 5

        self.player = {
            "x" : 65,
            "y" : 50,
            "angle" : 90,
            "fov" : 40
            }

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize))
        rect = tex.get_rect()
        rect = rect.move( (x,y) )
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self,color):

        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize

                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY

                tx = maxHit / self.blocksize

                return dist, self.map[j][i], tx

            self.screen.set_at((x,y), WHITE)

            dist += 5

    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, wallType, tx = self.castRay(angle)

            x = halfWidth + i 

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

            start = int( halfHeight - h/2)
            end = int( halfHeight + h/2)

            img = textures[wallType]
            tx = int(tx * img.get_width())

            for y in range(start, end):
                ty = (y - start) / (end - start)
                ty = int(ty * img.get_height())
                texColor = img.get_at((tx, ty))
                self.screen.set_at((x, y), texColor)

        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)

    def message_to_screen(self, msg, color, x, y, size = 35, font = 0):
        font0 = pygame.font.SysFont('Corbel', size)
        font1 = pygame.font.SysFont('Arial', size)
        fonts = [font0, font1]
        screen_text = fonts[font].render(msg, True, color)
        screen.blit(screen_text, (x,y))

    def pause(self):

        paused = True
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width/2-55 <= mouse[0] <= width/2+85 and height/2-5 <= mouse[1] <= height/2+35:
                        paused = False
                
                    elif width/2-25 <= mouse[0] <= width/2+55 and height/2+45 <= mouse[1] <= height/2+95:
                        pygame.quit()
                        quit()

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_p:
                        paused = False

            pause_text = 'Pausa'
            pause2_text = 'Presione CONTINUE para continuar o QUIT para salir.'
            continue_text = 'Continue'
            quit_text = 'Quit'

            self.message_to_screen(pause_text, WHITE, width/2 - 45, height/4, 50)
            self.message_to_screen(pause2_text, WHITE, width/2 -250, height/4 + 60, 25)
            self.message_to_screen(continue_text, WHITE, width/2 - 50, height/2)
            self.message_to_screen(quit_text, WHITE, width/2 - 20, height/2 + 50)
            
            pygame.display.update()

            screen.fill((50,50,100))

            # Mouse position
            mouse = pygame.mouse.get_pos()

            # Continue button
            if width/2-55 <= mouse[0] <= width/2+85 and height/2-5 <= mouse[1] <= height/2+35:  
                pygame.draw.rect(screen,(80,80,140),[width/2-55,height/2-5,140,40])  
            else:
                pygame.draw.rect(screen,(40,40,60),[width/2-55,height/2-5,140,40])
            
            # Quit button
            if width/2-25 <= mouse[0] <= width/2+55 and height/2+45 <= mouse[1] <= height/2+95:
                pygame.draw.rect(screen,(80,80,140),[width/2-25,height/2+45,80,40])
            else:
                pygame.draw.rect(screen,(40,40,60),[width/2-25,height/2+45,80,40])

            clock.tick(30)


pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
clock = pygame.time.Clock()

width = screen.get_width()
height = screen.get_height()

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = pygame.font.SysFont('Corbel', 35).render(fps, 1, pygame.Color("white"))
    return fps

r = Raycaster(screen)
r.load_map('map.txt')

isRunning = True
def gameLoop():
    isRunning = True
    MainMenu = True
    while isRunning:

        while MainMenu == True:
            menu_text = 'MineGame'
            menu_text2 = 'Presione START para iniciar o QUIT para salir.'
            start_text = 'Start'
            quit_text = 'Quit'
            r.message_to_screen(menu_text, WHITE, width/2-40, height/2-100)
            r.message_to_screen(menu_text2, WHITE, width/2 - 200, height/2 - 50, 25)
            r.message_to_screen(start_text, WHITE, width/2, height/2)
            r.message_to_screen(quit_text, WHITE, width/2, height/2+50)

            pygame.display.update()
            
            screen.fill(BLACK)
            back_image = pygame.image.load('./images/mine.jpg')
            back_image = pygame.transform.scale( back_image, (1000,500))
            screen.blit(back_image, (0,0))

            pygame.draw.rect(screen,(50,50,50),[width/2-45,height/2-105,170,40])
            pygame.draw.rect(screen,(50,50,50),[width/2-205,height/2-55,470,35])

            # Mouse position
            mouse = pygame.mouse.get_pos()
            if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:  
                pygame.draw.rect(screen,(200,200,200),[width/2-5,height/2-10,80,50])  
            else:
                pygame.draw.rect(screen,(50,50,50),[width/2-5,height/2-10,80,50])

            if width/2-5 <= mouse[0] <= width/2+80 and height/2+40 <= mouse[1] <= height/2+90:
                pygame.draw.rect(screen,(200,200,200),[width/2-5,height/2+45,80,50])
            else:
                pygame.draw.rect(screen,(50,50,50),[width/2-5,height/2+45,80,50])

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:
                        MainMenu = False
                    if width/2-5 <= mouse[0] <= width/2+80 and height/2+40 <= mouse[1] <= height/2+90:
                        pygame.quit()
                        quit()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if width/2-5 <= mouse[0] <= width/2+80 and height/2-10 <= mouse[1] <= height/2+40:
                    break
            
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e:
                    r.player['angle'] += 5
                elif ev.key == pygame.K_p:
                    r.pause()

                i = int(newX / r.blocksize)
                j = int(newY / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY

        screen.fill(pygame.Color("dimgray")) #Fondo
        r.render()
        
        # FPS
        screen.fill(pygame.Color("black"), (0,0,35,40))
        screen.blit(updateFPS(), (0,0))

        # Main menu pause
        screen.fill(pygame.Color("black"), (880,0,120,30))
        r.message_to_screen('p to pause',WHITE,880,0,25)

        clock.tick(30)  
        pygame.display.update()

gameLoop()
