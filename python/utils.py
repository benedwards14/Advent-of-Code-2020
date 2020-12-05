import os


__all__ = ("get_data",)


DATA_DIR = os.path.normpath(
    os.path.join(os.path.abspath(__file__), "../../data")
)


def get_data(day: int) -> str:
    with open(os.path.join(DATA_DIR, f"day_{day}.txt")) as f:
        return f.read()