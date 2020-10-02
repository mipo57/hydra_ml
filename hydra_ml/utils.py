from typing import Type
import ray.tune as tune
from omegaconf import OmegaConf
from functools import partial
from importlib import import_module

def _convert(val: str) -> any:
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass

def as_class(target: str):
    module_name = ".".join(target.split(".")[:-1])
    module = import_module(module_name)

    classname = target.split(".")[-1]
    cls = getattr(module, classname)

    return cls

def apply_tune(config, max_recursion=0):
    cfg = OmegaConf.to_container(config, resolve=True)
    for _ in range(max_recursion):
        cfg = OmegaConf.create(cfg)
        cfg = OmegaConf.to_container(cfg, True)


    result = {}

    for key, value in config.items():
        if type(value) is dict:
            result[key] = apply_tune(value)
        elif type(value) is str:
            if value.startswith("#loguniform:"):
                _, values = value.split(":")
                values = values.split(",")[:2]

                result[key] = tune.loguniform(
                    float(values[0]), float(values[1]))
            elif value.startswith("#choice:"):
                _, values = value.split(":")
                values = values.split(",")
                values = map(_convert, values)
                values = list(values)

                result[key] = tune.choice(values)
            elif value.startswith("#grid:"):
                _, values = value.split(":")
                values = values.split(",")
                values = map(_convert, values)
                values = list(values)

                result[key] = tune.grid_search(values)
            else:
                result[key] = value
        else:
            result[key] = value


    return result

def file_interpolation(x, type):
    with open(x, 'r') as f:
        return type(f.read())

def json(x):
    with open(x, 'r') as f:
        return json.load(f)

def initialize():
    OmegaConf.register_resolver("json", json)
    OmegaConf.register_resolver("file_int", partial(file_interpolation, int))
    OmegaConf.register_resolver("file_float", partial(file_interpolation, float))