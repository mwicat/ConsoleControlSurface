from _Framework.ControlSurface import ControlSurface

from .util import spawn_console


class ConsoleControlSurface(ControlSurface):

    def __init__(self, c_instance):
        super(ConsoleControlSurface, self).__init__(c_instance)
        self.log_message('Initializing ConsoleControlSurface...')

        with self.component_guard():
            pass

        namespace = {
            'remote_script': c_instance,
            'control_surface': self,
            'song': c_instance.song(),
        }

        spawn_console(namespace)

        self.log_message('Initialized ConsoleControlSurface.')
