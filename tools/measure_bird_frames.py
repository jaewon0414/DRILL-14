# bird_animation.png 의 새 14장이 실제로 차지하는 영역과 눈 위치를 재는 도구
#
# 실행: 저장소 폴더에서  py -3.14 tools/measure_bird_frames.py
#
# 1) 투명하지 않은 픽셀을 이웃(8방향)한 것끼리 이어서 덩어리로 묶으면 새 한 마리가 덩어리 하나가 된다.
# 2) 덩어리마다 가장 왼쪽/오른쪽/위/아래 픽셀로 영역을 구한다.
# 3) 파란 눈동자 픽셀들의 평균 위치를 눈의 위치로 삼는다.
# 4) 그림 파일은 위쪽이 원점, pico2d 는 아래쪽이 원점이므로 아래쪽 기준으로 바꿔서 출력한다.
#    출력한 줄은 bird.py 의 FRAMES 표에 그대로 옮겨 쓴다.

import ctypes
import os
import warnings

warnings.filterwarnings('ignore')
from sdl2 import SDL_ConvertSurfaceFormat, SDL_PIXELFORMAT_RGBA32, SDL_FreeSurface
from sdl2.sdlimage import IMG_Load

IMAGE = os.path.join(os.path.dirname(__file__), '..', 'bird_animation.png')
ROWS = 3


def is_eye_blue(r, g, b):
    return b > 150 and r < 80 and g < 170 and b > r + 80


def main():
    loaded = IMG_Load(IMAGE.encode())
    surface = SDL_ConvertSurfaceFormat(loaded, SDL_PIXELFORMAT_RGBA32, 0)
    s = surface.contents
    w, h, pitch = s.w, s.h, s.pitch
    pixels = ctypes.string_at(s.pixels, pitch * h)

    def rgba(x, y):
        i = y * pitch + x * 4
        return pixels[i], pixels[i + 1], pixels[i + 2], pixels[i + 3]

    visited = bytearray(w * h)
    birds = []
    for sy in range(h):
        for sx in range(w):
            if visited[sy * w + sx] or rgba(sx, sy)[3] == 0:
                continue
            visited[sy * w + sx] = 1
            stack = [(sx, sy)]
            x0 = x1 = sx
            y0 = y1 = sy
            count = 0
            eye = []
            while stack:
                x, y = stack.pop()
                count += 1
                r, g, b, a = rgba(x, y)
                if is_eye_blue(r, g, b):
                    eye.append((x, y))
                x0, x1, y0, y1 = min(x0, x), max(x1, x), min(y0, y), max(y1, y)
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx] \
                                and rgba(nx, ny)[3] > 0:
                            visited[ny * w + nx] = 1
                            stack.append((nx, ny))
            if count < 500:  # 작은 티끌은 무시 (이 그림에는 없음)
                continue
            ex = sum(p[0] for p in eye) / len(eye) + 0.5  # 픽셀 가운데
            ey = sum(p[1] for p in eye) / len(eye) + 0.5
            birds.append((x0, y0, x1, y1, ex, ey))

    SDL_FreeSurface(surface)
    SDL_FreeSurface(loaded)

    # 눈 높이로 줄을 정하고, 줄 안에서는 왼쪽부터 → 날갯짓 순서
    birds.sort(key=lambda b: (int(b[5] // (h / ROWS)), b[0]))

    print(f'image {w}x{h}, birds {len(birds)}')
    print('# (left, bottom, width, height, eye_x, eye_y)  pico2d coords, origin = bottom-left')
    for i, (x0, y0, x1, y1, ex, ey) in enumerate(birds):
        left, width = x0, x1 - x0 + 1
        height = y1 - y0 + 1
        bottom = h - 1 - y1
        print(f'    ({left}, {bottom}, {width}, {height}, {ex:.1f}, {h - ey:.1f}),  # {i}')


if __name__ == '__main__':
    main()
