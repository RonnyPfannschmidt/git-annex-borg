import attr
import re
import enum

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
class Extensions(Msg):
    extensions = attr.ib(converter=set)

    @classmethod
    def from_part(cls, part):
        return cls(part.split())

    def to_part(self):
        return " ".join(self.extensions)


@msgclass
class Value(Msg):
    value = attr.ib()

    @classmethod
    def from_part(cls, part):
        return cls(part)

    def to_part(self):
        return self.value


@msgclass
class UnsupportedRequest(SimpleMsgMixin, Msg):
    pass


@msgclass
class Initremote(SimpleMsgMixin, Msg):
    pass


@msgclass
class Getgitdir(SimpleMsgMixin, Msg):
    pass


@msgclass
class Getconfig(Msg):
    key = attr.ib()

    @classmethod
    def from_part(cls, part):
        return cls(part)

    def to_part(self):
        return self.key


@msgclass
class InitremoteSuccess(SimpleMsgMixin, Msg):
    pass


@msgclass
class Exportsupported(SimpleMsgMixin, Msg):
    def failure(self):
        return ExportsupportedFailure()

    def success(self):
        return ExportsupportedSuccess()


@msgclass
class ExportsupportedFailure(SimpleMsgMixin, Msg):
    pass


@msgclass
class ExportsupportedSuccess(SimpleMsgMixin, Msg):
    pass


@msgclass
class Prepare(SimpleMsgMixin, Msg):
    pass


@msgclass
class PrepareSuccess(SimpleMsgMixin, Msg):
    pass


@msgclass
class Getcost(SimpleMsgMixin, Msg):
    pass


@msgclass
class Cost(Msg):
    cost = attr.ib()

    @classmethod
    def from_part(cls, part):
        return cls(int(part))

    def to_part(self):
        return str(self.cost)


@msgclass
class Getavailability(SimpleMsgMixin, Msg):
    pass


class AvailabilityScope(enum.Enum):
    LOCAL = 1
    GLOBAL = 2


@msgclass
class Availability(Msg):
    scope = attr.ib()

    def to_part(self):
        return self.scope.name


@msgclass
class Setconfig(Msg):
    key = attr.ib()
    value = attr.ib()

    def to_part(self):
        return f"{self.key} {self.value}"


@msgclass
class Setcreds(Msg):
    key = attr.ib()
    user = attr.ib()
    password = attr.ib()

    def to_part(self):
        return f"{self.key} {self.user} {self.password}"


@msgclass
class Getcreds(Msg):
    key = attr.ib()

    def to_part(self):
        return self.key


@msgclass
class Getinfo(SimpleMsgMixin, Msg):
    pass


@msgclass
class Infoend(SimpleMsgMixin, Msg):
    pass


@msgclass
class Infofield(Msg):
    name = attr.ib()

    def to_part(self):
        return self.name


@msgclass
class Infovalue(Msg):
    value = attr.ib()

    def to_part(self):
        return self.value


@msgclass
class Creds(Msg):
    user = attr.ib()
    password = attr.ib()

    @classmethod
    def from_part(cls, part):
        return cls(*part.split(" ", 1))
