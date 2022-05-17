import json

class ConfigBase:
    config = []

    def __init__(self, path: str = None) -> None:
        if path is not None:
            with open(path) as json_file:
                self.config = json.load(json_file)
        else:
            # TODO: Add error expectation handler
            pass