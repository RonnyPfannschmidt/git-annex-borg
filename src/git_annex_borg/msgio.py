import sys
import attr
import logging
from .protocol import Msg, Value

log = logging.getLogger(__name__)
log_lines = log.getChild("lines")
log_messages = log.getChild("messages")


@attr.s
class MsgIO(object):
    _input = attr.ib()
    _output = attr.ib()

    @classmethod
    def from_stdio(cls) -> "MsgIO":
        return cls(input=sys.stdin, output=sys.stdout)

    def __iter__(self):
        return self

    def __next__(self) -> Msg:
        line = self._input.readline().rstrip("\n")
        if not line:
            log.debug("end of input")
            raise StopIteration()
        log_lines.debug("in %s", line)
        msg = Msg.from_line(line)
        log_messages.debug("in %r", msg)
        return msg

    def send(self, msg: Msg):
        log_messages.debug("out %r", msg)

        log_lines.debug("out %s", msg)
        self._output.write(f"{msg}\n")
        self._output.flush()

    def request(self, msg, expected=Msg):
        self.send(msg)
        reply = next(self)
        assert isinstance(reply, expected)
        return reply

    def request_value(self, msg):
        return self.request(msg, Value).value
