

import time

OPEN = 0
CLOSED = 1
HALF_OPEN = 2


class circuitbreak(object):
    def __init__(self, allowed_fails=3, retry_time=10, validation_func=None, allowed_exceptions=None,
                 failure_exceptions=None):


        self.allowed_fails = allowed_fails
        self.retry_time = retry_time

        self.failure_count = 0
        self.state = OPEN
        self.halfstate_load_time = 0

        self.validation_func = validation_func

        if allowed_exceptions is not None:
            self.allowed_exceptions = tuple(allowed_exceptions)
        else:
            self.allowed_exceptions = ()

        if failure_exceptions is not None:
            self.failure_exceptions = tuple(failure_exceptions)
        else:
            self.failure_exceptions = ()

    def set_open_state(self):

        self.state = OPEN
        self.open_time = time.time()
        self.halfstate_load_time = self.open_time + self.retry_time

    def set_close_state(self):

        self.state = CLOSED
        self.failure_count = 0

    def set_half_open_state(self):

        self.state = HALF_OPEN

    def check_state(self):
        try:
            if self.state == OPEN:
                now = time.time()
                if now >= self.halfstate_load_time:
                    self.set_half_open_state()
                    raise cirbreakexceptions('circuit in half open state')
            return self.state
        except cirbreakexceptions, cx:
            print cx.msg

    def handle_failure(self):

        try:
            self.failure_count += 1
            if self.failure_count >= self.allowed_fails:
                self.set_open_state()
                raise cirbreakexceptions('circuit open')
        except cirbreakexceptions, cx:
            print cx.msg

    def handle_success(self):

        self.failure_count = 0
        self.set_close_state()

    def getState(self):
        return self.state
class cirbreakexceptions(Exception):
    def __init__(self, msg):
        self.msg = msg











