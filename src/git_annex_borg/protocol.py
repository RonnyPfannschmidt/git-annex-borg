import attr
import re
import logging

log = logging.getLogger(__name__)

KNOWN_COMMANDS = {}
CLASS_TO_COMMAND = {}


def convert_class_to_command(cls):
    name = cls.__name__
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).upper()


def register(cls):
    cmd = convert_class_to_command(cls)
    KNOWN_COMMANDS[cmd] = cls
    CLASS_TO_COMMAND[cls] = cmd
    return cls


def msgclass(cls):
    return register(attr.s(str=False, frozen=True)(cls))


@attr.s(str=False, frozen=True)
class Msg:

    @classmethod
    def from_line(cls, line):
        line = line.rstrip("\n")
        if " " in line:
            cmd, part = line.split(" ", 1)
        else:
            cmd = line
            part = None
        inst = KNOWN_COMMANDS[cmd].from_part(part)
        log.debug(inst)
        return inst

    def __str__(self):
        part = self.to_part()
        if part:
            return f"{CLASS_TO_COMMAND[type(self)]} {part}"
        else:
            return CLASS_TO_COMMAND[type(self)]


class SimpleMsgMixin(object):

    @classmethod
    def from_part(cls, part):
        assert not part
        return cls()

    def to_part(self):
        return


@msgclass
class Version(Msg):
    number = attr.ib(default=1)

    def to_part(self):
        return "1"


@msgclass
class Initremote(SimpleMsgMixin, Msg):

    @classmethod
    def from_part(cls, part):
        return cls()


@msgclass
class Exportsupported(SimpleMsgMixin, Msg):

    def reply(self):
        return ExportsupportedFailure()


@msgclass
class ExportsupportedFailure(SimpleMsgMixin, Msg):
    pass


@msgclass
class Prepare(SimpleMsgMixin, Msg):
    pass
