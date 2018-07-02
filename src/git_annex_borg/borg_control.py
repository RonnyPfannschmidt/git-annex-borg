import logging
import attr
import subprocess
import json

log = logging.getLogger(__name__)


@attr.s
class BorgControl:
    path = attr.ib()
    passphrase = attr.ib(repr=False)

    def get_unindexed_archives(self):
        log.debug(self)
        d = subprocess.getoutput(f"borg list --json {self.path}")
        log.debug(d)
        d = json.loads(d)
        log.debug("%r", d)
        return [BorgArchive(name=i["archive"]) for i in d["archives"]]


@attr.s
class BorgArchive:
    name = attr.ib()
