import subprocess
import pytest

DATA = b"\x00" * 1000


def do(cmd):
    print("do", cmd, flush=True)
    subprocess.check_call(cmd, shell=isinstance(cmd, str), stderr=subprocess.STDOUT)


@pytest.fixture(autouse=True)
def borg_env(monkeypatch):
    monkeypatch.setenv("BORG_PASSPHRASE", "example")
    monkeypatch.setenv("PYTHONUNBUFFERED", "yes")


def test_basic_flow(tmpdir):
    tmpdir.chdir()
    borg_repo = tmpdir.join("borg")
    tmpdir.ensure("data/initial.bin").write_binary(DATA)
    do(f"borg init {borg_repo} -e authenticated")
    do(f"borg create {borg_repo}::data data")
    do(f"borg create {borg_repo}::data2 data")
    do("git init annex")
    tmpdir.join("annex").chdir()
    do("git annex init")
    do(
        f"git annex initremote foo type=external externaltype=borg "
        f"encryption=none repo={borg_repo} "
        f"exporttree=no"
    )
    output = subprocess.getoutput("git annex info foo")
    print(output)
    # todo - get infos
    assert f"borg repo: {borg_repo}" in output
    assert "borg unindexed archive: data" in output
    assert "borg unindexed archive: data2" in output
