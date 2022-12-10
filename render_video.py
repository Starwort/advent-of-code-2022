from io import TextIOWrapper
from itertools import count
from sys import argv

from colorama import Cursor, init

from computer import Computer

init()


def render_cell_group(cells: list[list[bool]], x: int, y: int):
    """Update the screen based on the current state of the cells, by overwriting
    the old braille character representing the group containing (x, y)
    """
    screen_x = x // 2
    screen_y = y // 4
    group_x = screen_x * 2
    group_y = screen_y * 4
    # Braille characters are represented as U+2800 + 8-bit binary number
    # representing the 8 pixels in the character. The pixels are ordered as
    # follows:
    # 1 4
    # 2 5
    # 3 6
    # 7 8
    group_value = 0
    for i, (x, y) in enumerate(
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3)]
    ):
        group_value |= cells[group_y + y][group_x + x] << i
    print(Cursor.POS(screen_x, screen_y) + chr(0x2800 + group_value), end="")


class UnbufferedTape:
    """A tape that reads from a file-like object, but doesn't buffer the input
    (so that the file can be read while the program is running)
    """

    file: TextIOWrapper

    def __init__(self, file):
        self.file = file

    def __getitem__(self, index):
        return self.file.readline().split()

    def __len__(self):
        return 190533030


if __name__ == "__main__":
    match argv:
        case [_, input_file, video_width, video_height]:
            with open(input_file) as f:
                computer = Computer("")
                computer.tape = UnbufferedTape(f)  # type: ignore
                video_width = int(video_width)
                video_height = int(video_height)
                frame_length = video_width * video_height
                cells = [
                    [False for _ in range(video_width)] for _ in range(video_height)
                ]
                frame_total = next(2**i for i in count() if 2**i >= frame_length)
                frame_blank = frame_total - frame_length
                frames = 0
                for cycle, state in enumerate(computer.run()):
                    # blanking at the start of the frame avoid an artifact where the
                    # first frame will always have two pixels shown at the top left
                    frame_cycle = cycle % frame_total - frame_blank
                    if frame_cycle < 0:
                        continue
                    elif frame_cycle == 0:
                        print(Cursor.POS(0, 0) + str(frames), end="")
                        frames += 1
                    y, x = divmod(frame_cycle, video_width)
                    old = cells[y][x]
                    cells[y][x] = abs(state.x - x) <= 1
                    if old != cells[y][x]:
                        render_cell_group(cells, x, y)
        case _:
            print("Usage: render_video.py <input_file> <video_width> <video_height>")
