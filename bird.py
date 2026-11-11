from pico2d import load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

# 새의 크기: 날개를 접은 그림의 꼬리 끝~부리 끝(146픽셀)을 몸길이 1.5m로 보고 모든 그림을 같은 비율로 줄인다
BIRD_LENGTH_M = 1.5
BIRD_LENGTH_IN_IMAGE = 146
SCALE = BIRD_LENGTH_M * PIXEL_PER_METER / BIRD_LENGTH_IN_IMAGE

# 날갯짓 속도 (임시): 1초에 3번
FRAMES_PER_ACTION = 14
FLAPS_PER_SECOND = 3.0

# tools/measure_bird_frames.py 로 잰 14장의 실제 영역과 눈 위치 (pico2d 좌표, 아래쪽 원점)
# 그림을 5x3 칸으로 똑같이 나누면 날개 끝이 잘리거나 옆 그림이 묻어 나오고, 눈 높이가 최대 9픽셀 튄다.
# (left, bottom, width, height, eye_x, eye_y)
FRAMES = (
    (34, 362, 146, 143, 123.7, 412.2),  # 0  날개를 머리 위로
    (216, 363, 146, 141, 305.7, 413.0),  # 1
    (398, 364, 146, 130, 488.1, 414.9),  # 2
    (555, 367, 171, 122, 670.1, 417.9),  # 3  앞으로 내리침
    (728, 370, 182, 88, 852.1, 420.9),  # 4
    (34, 171, 146, 118, 123.7, 251.2),  # 5  몸 아래로
    (216, 166, 146, 124, 306.1, 252.9),  # 6
    (398, 170, 146, 120, 487.7, 252.0),  # 7
    (580, 180, 146, 109, 670.1, 251.9),  # 8
    (762, 177, 146, 110, 852.1, 249.9),  # 9
    (34, 6, 146, 108, 124.1, 76.9),  # 10 뒤로 젖힘
    (216, 6, 146, 106, 305.7, 74.0),  # 11
    (376, 23, 168, 88, 487.7, 73.0),  # 12
    (546, 22, 180, 114, 669.7, 72.2),  # 13 다시 머리 위로
)


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y  # 새의 위치 = 눈의 위치
        self.frame = 0.0
        self.frames_per_second = FLAPS_PER_SECOND * FRAMES_PER_ACTION

    def update(self):
        self.frame = (self.frame + self.frames_per_second * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        left, bottom, width, height, eye_x, eye_y = FRAMES[int(self.frame)]
        # pico2d 는 지정한 자리를 그림의 가운데로 삼으므로, 잘라 낸 영역의 가운데가 눈에서 떨어진 만큼 옮겨 그린다
        offset_x = (left + width / 2 - eye_x) * SCALE
        offset_y = (bottom + height / 2 - eye_y) * SCALE
        Bird.image.clip_draw(left, bottom, width, height,
                             self.x + offset_x, self.y + offset_y,
                             width * SCALE, height * SCALE)
