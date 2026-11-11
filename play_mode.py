import random

from pico2d import *
import game_world
import game_framework
from bird import Bird, FRAMES_PER_ACTION
from boy import Boy
from grass import Grass

BIRD_COUNT = 10

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    # 새 10마리: 위치, 높이, 방향, 속도, 날갯짓 박자를 새마다 무작위로
    for _ in range(BIRD_COUNT):
        bird = Bird(x=random.uniform(100, get_canvas_width() - 100),
                    y=random.uniform(250, 560),
                    dir=random.choice((-1, 1)),
                    speed_kmph=random.uniform(20.0, 35.0),
                    frame=random.uniform(0, FRAMES_PER_ACTION))
        game_world.add_oject(bird)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()









