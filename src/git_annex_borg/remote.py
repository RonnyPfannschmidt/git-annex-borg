from typing import Optional
from . import protocol as p

from .msgio import MsgIO
from .borg_control import BorgControl
import logging

log = logging.getLogger(__name__)


def main(msgio: Optional[MsgIO] = None):
    logging.basicConfig(level=logging.DEBUG)
    if msgio is None:
        msgio = MsgIO.from_stdio()
    try:
        return run(msgio)
    except Exception:
        log.exception("main failed")


def run(io: MsgIO):
    log.info("starting remote")
    io.send(p.Version())
    for msg in io:
        if isinstance(msg, p.Extensions):
            log.warning(msg)
            io.send(p.Extensions({"INFO"}))
            continue
        elif isinstance(msg, p.Prepare):
            remote = prepare(io)
            break
        elif isinstance(msg, p.Exportsupported):
            io.send(msg.success())
            return  # exit here due to annex issue
        elif isinstance(msg, p.Initremote):
            remote = initremote(io)
            break
        else:
            assert False, msg

    runremote(remote, io)


def prepare(io: MsgIO):
    log.info("Preparing borg annex")
    gitdir = io.request_value(p.Getgitdir())
    borg_repo = io.request_value(p.Getconfig("repo"))
    control = BorgControl(path=borg_repo, passphrase="")
    log.debug("git: %s, borg: %s", gitdir, control)
    io.send(p.PrepareSuccess())
    return control


def initremote(io: MsgIO):
    gitdir = io.request_value(p.Getgitdir())
    borg_repo = io.request_value(p.Getconfig("repo"))
    io.send(p.Setconfig("repo", borg_repo))
    control = BorgControl(path=borg_repo, passphrase="")
    log.debug("git: %s, borg: %s", gitdir, control)
    io.send(p.InitremoteSuccess())
    return control


def runremote(remote, io: MsgIO):
    log.info("running remote")
    for msg in io:
        if isinstance(msg, p.Getcost):
            io.send(p.Cost(50))
        elif isinstance(msg, p.Getavailability):
            io.send(p.Availability(p.AvailabilityScope.LOCAL))
        elif isinstance(msg, p.Exportsupported):
            io.send(msg.success())
        elif isinstance(msg, p.Getinfo):
            io.send(p.Infofield("borg repo"))
            io.send(p.Infovalue(remote.path))
            for archive in remote.get_unindexed_archives():
                io.send(p.Infofield("borg unindexed archive"))
                io.send(p.Infovalue(archive.name))
            io.send(p.Infoend())
        else:
            log.debug("unknown %", msg)
            return
