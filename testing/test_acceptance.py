import subprocess

DATA = b"\x00" * 1000


def do(cmd):
    print("do", cmd, flush=True)
    subprocess.check_call(cmd, shell=isinstance(cmd, str), stderr=subprocess.STDOUT)


def test_basic_flow(tmpdir):
    tmpdir.chdir()
    borg_repo = tmpdir.join("borg")
    tmpdir.ensure("data/initial.bin").write_binary(DATA)
    do(f"BORG_PASSPHRASE=example borg init {borg_repo} -e authenticated")
    do(f"BORG_PASSPHRASE=example borg create {borg_repo}::data data")
    do("git init annex")
    tmpdir.join("annex").chdir()
    do("git annex init")
    do(
        f"git annex initremote foo type=external externaltype=borg "
        f"encryption=none repo={borg_repo} passphrase=example "
        f"exporttree=no"
    )
    output = subprocess.getoutput("git annex info foo")
    print(output)
    # todo - get infos
    # assert f"repo: {borg_repo}" in output
