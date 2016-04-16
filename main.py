import re

from os import listdir, getpid
from os.path import isfile, join
import psutil

import importlib

from prism import Prism

def ensure_uniqueness():
    import os
    import psutil

    my_process = psutil.Process(os.getpid())

    procs = [p for p in psutil.process_iter()]

    for p in procs:
        try: # ignore zombie processes and the ones we can't access
            if my_process.exe() == p.exe() and my_process.pid != p.pid:
                print('there can be only one prism! killing', p.pid)
                p.terminate()
        except (psutil.ZombieProcess, psutil.AccessDenied):
            pass


def auto_update(prism):
    def restart(msg):
        import os
        import sys

        python_exe = sys.executable

        import subprocess
        process = subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode != 0:
            print('problems when pulling newest version')

        os.execl(python_exe, python_exe, *sys.argv)

    prism._xmpp.add_event_handler('session_end', restart)

if __name__ == "__main__":

    import config

    # kill older prisms
    ensure_uniqueness()

    prism = Prism(config.JID, config.PASSWORD, config.NICK)
    for room in config.ROOMS:
        prism.join_muc(room)

    prism.config = config

    # loading plugins

    plugin_path = './plugins'
    python_matcher = re.compile('([^\.]+)\.py', re.I)
    plugin_files = [python_matcher.match(f).group(1)
                        for f in listdir(plugin_path)
                            if isfile(join(plugin_path, f))
                                and python_matcher.match(f)]

    for plugin in plugin_files:
        module = importlib.import_module('plugins.%s' % plugin)
        module.register(prism)

    # starting
    auto_update(prism)

    prism.start((config.HOST, config.PORT))
