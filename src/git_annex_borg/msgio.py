import sys
import attr
import logging
from .protocol import Msg, Value

log = logging.getLogger(__name__)


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
        msg = Msg.from_line(self._input.readline())
        log.debug("in %r", msg)
        return msg

    def send(self, msg: Msg):
        log.debug("out %r", msg)
        self._output.write(str(msg))
        self._output.write("\n")
        self._output.flush()

    def request(self, msg, expected=Msg):
        self.send(msg)
        reply = next(self)
        assert isinstance(reply, expected)
        return reply

    def request_value(self, msg):
        return self.request(msg, Value).value
