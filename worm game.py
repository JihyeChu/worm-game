import pygame
import sys  #창 닫는 시스템
import time
import random

#모듈 내 함수를 호출 할 때 사용(modulename 생략)
from pygame.locals import *

#창 사이즈
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
#픽셀 단위로 하기엔 작음, 그리드로 사용
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE


WHITE = (255, 255, 255)
GREEN = (27, 94, 32)
ORANGE = (250, 165, 0)
GRAY = (100, 100, 100)


up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)
stop = (0, 0)

FPS = 10

#파이썬이라는 뱀이 먹이를 먹는다.(객체 2개(뱀, 먹이))
class Python(object):
    #객체를 생성 할 때 자동으로 호출되는 특수한 메소드, 반드시 첫 번째 인자는 self
    #메소드 내에 클래스 변수 생성 가능
    def __init__(self):
        self.create()
        self.color = GREEN #뱀 색깔

    def create(self):
        self.length = 2 #뱀 초기 길이
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        self.direction = random.choice([up, down, left, right]) #방향 랜덤

    def control(self, xy):
        #뱀이 반대 방향으로 동작 X, ?
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy
            
    def stop(self):
        speed = 0
        
    def move(self):
        #위치들(s)중 [0] == 머리
        cur = self.positions[0]
        x, y = self.direction

            
        #뱀이 창을 넘어가면 반대 쪽으로 나오게끔        
        #new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT)
        new = ((cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE)))

        #뱀의 위치 위에 new(뱀 이동)가 있으면 죽음
        if (cur[0] < 0) or (cur[0] > WINDOW_WIDTH) or ( cur[1] < 0) or (cur[1] > WINDOW_HEIGHT):
            self.create()
        elif new in self.positions[2:]:
            if (x,y) == stop:
                return
            self.create()
        else:
            #위치에 new를 입력
            self.positions.insert(0, new)
            #연달아 움직이는 과정, 위치가 실제 길이보다 클 경우 하나 꺼냄
            if len(self.positions) > self.length:
               self.positions.pop()

    def eat(self):
        self.length += 1

    #뱀이 실제 화면에 표현 될 수 있게 그려야 함
    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)
            
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        #먹이 위치 random ???
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)
    
def draw_object(surface, color, pos):
    #rect(직사각형 영역)의 각 모양 그리기
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)       

#먹이를 먹었을 때
def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()

def show_info(length, speed, surface):
    #파일로부터 새로운 Font 객체를 생성(파일 이름(객체), 크기)
    font = pygame.font.Font(None, 34)
    #새로운 표면에 텍스트 그리기
    text = font.render("Length: " + str(length)+ "  Speed: " + str(round(speed, 2)),1, GRAY)
    #렌더링 된 텍스트의 크기와 오프셋을 반환
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)

if __name__ == '__main__':  #name에는 'pygame1'이라는 pygame1.py의 모듈이름 값이 저장
    python = Python()
    feed = Feed()

    pygame.init()   #초기화
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32) #pygame을 돌릴 창 초기화(해상도(0,0), 플래그, 깊이)
    pygame.display.set_caption('Python Game') #창 제목 변경  
    surface = pygame.Surface(window.get_size()) #이미지를 나타내는 파이 게임 객체
    surface = surface.convert() #이미지의 픽셀 형식을 변경(깊이, 플래그 = 0) -> 서페이스
    surface.fill(WHITE) #단면 색
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 40) #키보드 반복이 활성화 되면, 누르고 있는 키는 이벤트 생성(지연, 간격)
    window.blit(surface, (0, 0)) #하나의 이미지를 다른 이미지 위에 그린다. 지정한 좌표가 표면 정 가운데?에 위치 하도록

    
    while True:
        #event 가져오기
        for event in pygame.event.get():
            #QUIT을 통해 게임, 창 끄기
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #DOWN을 눌렀을때 키조작
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(up)
                elif event.key == K_DOWN:
                    python.control(down)
                elif event.key == K_LEFT:
                    python.control(left)
                elif event.key == K_RIGHT:
                    python.control(right)
                elif event.key == K_s:
                    python.control(stop)


        surface.fill(WHITE)
        python.move()
        check_eat(python, feed)
        speed = (FPS + python.length) / 2
        show_info(python.length, speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface, (0, 0))
        #전체 화면 화면을 화면으로 업데이트
        pygame.display.flip()
        #화면 일부만 업데이트
        pygame.display.update()
        #컴퓨터는 tick단위
        clock.tick(speed)
        
        
               


