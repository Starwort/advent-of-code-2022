import json
from pathlib import Path
from random import randrange

import requests

from day_07 import Folder, data

fs_dir = Path("./day_07_fs").absolute()


def get_lipsum(size: int) -> str:
    resp = requests.post(
        "https://www.lipsum.com/feed/json",
        data={
            "amount": size - 1,
            "what": "bytes",
            "start": "yes",
            "generate": "Generate Lorem Ipsum",
        },
    )
    lipsum = json.loads(resp.text)["feed"]["lipsum"] + "\n"
    while len(lipsum) > size:
        to_delete = randrange(len(lipsum))
        # try to avoid making the text look janky
        if lipsum[to_delete] not in "\n .,'ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            lipsum = lipsum[:to_delete] + lipsum[to_delete + 1 :]
    return lipsum


def make_files(path: Path, files: Folder):
    path.mkdir(exist_ok=True)
    for name, contents in files.items():
        # Pylance won't let me use the Folder alias here :(
        if isinstance(contents, dict):
            make_files(path / name, contents)
        else:
            # `contents` is `int`
            lipsum = get_lipsum(contents)
            (path / name).write_text(lipsum)
            pass


make_files(fs_dir, data)
