import fire

from koobai.cli import CLI


if __name__ == "__main__":
    with CLI() as instance:
        fire.Fire(instance)
