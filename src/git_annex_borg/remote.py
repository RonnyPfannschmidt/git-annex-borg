import sys
from . import protocol as p

# rom .state import AnnexBorgState
import logging

log = logging.getLogger(__name__)


def reply(msg):
    print(msg, flush=True)


def main(stream=sys.stdin):
    logging.basicConfig(level=logging.INFO)
    try:
        return run(map(p.Msg.from_line, stream))
    except Exception:
        log.exception("main failed")


def run(messages):
    log.info("starting remote")
    reply(p.Version())
    for msg in messages:
        if isinstance(msg, p.Prepare):
            prepare(messages)
            break
        elif isinstance(msg, p.Exportsupported):
            reply(msg.reply())
        elif isinstance(msg, p.Initremote):
            reply("FAULT")
        else:
            assert False, msg


def prepare(messages):
    pass
