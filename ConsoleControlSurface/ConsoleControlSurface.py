try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser
import os

import Live
from _Framework.ControlSurface import ControlSurface

from .REPLHandler import REPLHandler


CONFIG_PATH = os.path.expanduser('~/.ccsurface.ini')

PROCESS_INTERVAL = 1

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8484


class ConsoleControlSurface(ControlSurface):


    def __init__(self, c_instance):
        super(ConsoleControlSurface, self).__init__(c_instance)
        
        with self.component_guard():
            REPLHandler.set_log(self.log_message)
            REPLHandler.set_message(self.show_message)

            env = {
                'control_surface': self,
                'remote_script': c_instance,
                'live_app': Live.Application.get_application(),
                'live_set': c_instance.song(),
            }

            env['song'] = env['live_set']
            env['cs'] = env['control_surface']

            if os.path.exists(CONFIG_PATH):
                parser = SafeConfigParser()
                parser.read(CONFIG_PATH)
                host = parser.get('network', 'host')
                port = int(parser.get('network', 'port'))
            else:
                host = DEFAULT_HOST
                port = DEFAULT_PORT

            self.repl_handler = REPLHandler(host, port, env)

            self.parse()

            if not self.repl_handler.error():
                self.show_message('Ready')


    def disconnect(self):
        self.repl_handler.shutdown()

    def parse(self):
        self.repl_handler.process()
        self.schedule_message(
            PROCESS_INTERVAL, self.parse)
