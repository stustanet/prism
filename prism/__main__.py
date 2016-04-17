import argparse
import importlib

from os import listdir

from pathlib import Path

from .prism import Prism


def main():
    cmd = argparse.ArgumentParser()
    cmd.add_argument("-c", "--config", default="/etc/prism/config.py")

    args = cmd.parse_args()

    loader = importlib.machinery.SourceFileLoader("config", args.config)
    config = loader.load_module("config")

    prism = Prism(config.JID, config.PASSWORD, config.NICK)
    for room in config.ROOMS:
        prism.join_muc(room)

    prism.config = config

    # loading plugins
    plugin_path = Path(__file__).resolve().parent / "plugins"

    for filename in plugin_path.glob("*.py"):
        if (plugin_path / filename).exists():

            modname = 'plugins.%s' % filename.stem
            loader = importlib.machinery.SourceFileLoader(
                modname, str(filename))

            module = loader.load_module(modname)
            module.register_to(prism)


    prism.start((config.HOST, config.PORT))


if __name__ == "__main__":
    main()
