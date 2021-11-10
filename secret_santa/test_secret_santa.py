from pathlib import Path

from secret_santa.secret_santa import SecretSantaSolver


def test_import() -> None:
    file = Path(__file__).with_name("example.json")
    ss = SecretSantaSolver(file)
    assert len(ss.config.rules) == 2
    assert len(ss.config.participants) == 12


def test_solve() -> None:
    file = Path(__file__).with_name("example.json")
    ss = SecretSantaSolver(file)
    res = ss.solve()
    assert len(res) == 12 // 2
    for rule in ss.config.rules:
        assert not any(map(lambda pair: pair[0] in rule and pair[1] in rule, res))
