import os

def asset_path(*paths):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "assets", *paths)
