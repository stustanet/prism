import re

from os import listdir
from os.path import isfile, join, dirname, realpath

import importlib

from prism import Prism


def main():
    import config

    prism = Prism(config.JID, config.PASSWORD, config.NICK)
    for room in config.ROOMS:
        prism.join_muc(room)

    prism.config = config

    # loading plugins

    plugin_path = join(dirname(realpath(__file__)), 'plugins')
    python_matcher = re.compile(r'([^\.]+)\.py', re.I)
    plugin_files = [python_matcher.match(f).group(1)
                    for f in listdir(plugin_path)
                    if isfile(join(plugin_path, f)) and
                    python_matcher.match(f)]

    for plugin in plugin_files:
        module = importlib.import_module('plugins.%s' % plugin)
        module.register(prism)

    # starting

    prism.start((config.HOST, config.PORT))


if __name__ == "__main__":
    main()
