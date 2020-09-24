import ray.tune as tune

def _convert(val: str) -> any:
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass


def apply_tune(config: dict):
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