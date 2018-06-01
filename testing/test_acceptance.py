import subprocess

DATA = b"\x00" * 1000


def do(cmd):
    print("do", cmd, flush=True)
    subprocess.check_call(cmd, shell=isinstance(cmd, str))


def test_basic_flow(tmpdir):
    tmpdir.chdir()
    tmpdir.ensure("data/initial.bin").write_binary(DATA)
    do("BORG_PASSPHRASE=example borg init borg_repo -e authenticated")
    do("BORG_PASSPHRASE=example borg create borg_repo::data data")
    do("git init annex")
    tmpdir.join("annex").chdir()
    do("git annex init")
    do("git annex initremote foo type=external externaltype=borg encryption=none")
