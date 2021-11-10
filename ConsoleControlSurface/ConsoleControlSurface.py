from _Framework.ControlSurface import ControlSurface

from . import ingress

DEFAULT_ADDRESS = ('localhost', 8484)
INITIALIZED = False


class ConsoleControlSurface(ControlSurface):

    def __init__(self, c_instance):
        super(ConsoleControlSurface, self).__init__(c_instance)
        global INITIALIZED

        if INITIALIZED:
            return

        self.log_message('Initializing ConsoleControlSurface...')

        with self.component_guard():
            env = {
                'remote_script': c_instance,
                'control_surface': self,
                'song': c_instance.song(),
            }

            self.thread = ingress.install(address=DEFAULT_ADDRESS, env=env)

        self.log_message('Initialized ConsoleControlSurface mareczek.')
        INITIALIZED =  True
