import select
import socket
import traceback


EOF = chr(4)
QUIT = 'quit()'


class REPLHandler(object):

    @staticmethod
    def set_log(func):
        REPLHandler.log_message = func

    @staticmethod
    def set_message(func):
        REPLHandler.show_message = func

    @staticmethod
    def release_attributes():
        REPLHandler.log_message = None
        REPLHandler.show_message = None

    _in_error = False

    def __init__(self, host, port, env):

        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.setblocking(0)

        self.read_list = [self._server_sock]
        self.env = env.copy()
        self.prompt = '>>> '

        self._local_addr = (host, port)

        try:
            self._server_sock.bind(self._local_addr)
            self._server_sock.listen(5)
            self.log_message('Starting on: {}'.format(
                self._local_addr))
        except:
            self._in_error = True
            msg = 'ERROR: Cannot bind to {}, port in use'.format(
                self._local_addr)
            self.show_message(msg)
            self.log_message(msg)

    def error(self):
        return self._in_error

    def send(self, sock, msg):
        sock.send(msg.encode('utf-8'))

    def close_session(self, sock):
        if sock in self.read_list:
            self.read_list.remove(sock)
        try:
            sock.close()
        except socket.error:
            pass

    def send_prompt(self, sock):
        self.send(sock, self.prompt)

    def process(self):
        readable, _writable, _errored = select.select(
            self.read_list, [], [], 0)

        for sock in readable:
            if sock is self._server_sock:
                self._accept_client()
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        self._process_data(data, sock)
                    else:
                        self.close_session(sock)
                    self.send_prompt(sock)
                except socket.error:
                    self.close_session(sock)
                except Exception:
                    error = traceback.format_exc()
                    self.log_message(error)
                    self.send(sock, error)
                    self.send_prompt(sock)

    def _accept_client(self):
        client_socket, address = self._server_sock.accept()
        self.read_list.append(client_socket)
        self.send_prompt(client_socket)
        self.log_message("Connection from {}".format(
            address))

    def _process_data(self, data, sock):
        expr = data.rstrip()

        if expr == EOF:
            return

        expr = expr.decode('utf-8')

        if expr == QUIT:
            self.close_session(sock)
            return

        try:
            value = eval(expr, globals(), self.env)  # nosec
            out = format(value) + '\n'
            self.send(sock, out)
        except Exception:
            exec(expr, self.env)  # nosec

    def shutdown(self):
        self._server_sock.close()
