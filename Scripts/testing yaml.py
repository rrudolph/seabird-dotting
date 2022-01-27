# Testing and/or experimental script, you can safely ignore this. 

import pathlib, yaml

def get_config():
    here = pathlib.Path(__file__).parent
    with open(here.joinpath("test.yaml")) as f:
        data = yaml.safe_load(f)
        return data

data = get_config()
print(data)

for name, data in data.items():
    print(name, data)