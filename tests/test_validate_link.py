import pytest

from src.utils import validate_link


def gen_parametrize(hash: str) -> list[str]:
    return [
        f"https://t.me/{hash}",
        f"http://t.me/{hash}",
        f"ps://t.me/{hash}",
        f"://t.me/{hash}",
        f"t.me/{hash}",
        hash,
    ]


@pytest.mark.parametrize("link", gen_parametrize("+AAAbbb111cc-_000"))
def test_parse_link_valid(link: str) -> None:
    assert validate_link(link) == "+AAAbbb111cc-_000"


@pytest.mark.parametrize("link", gen_parametrize("+AAAbbb111cc-_00"))
def test_parse_link_invalid_not_enough_characters(link: str) -> None:
    assert validate_link(link) is False


@pytest.mark.parametrize("link", gen_parametrize("+AAAbbb111cc-_0000"))
def test_parse_link_invalid_too_many_characters(link: str) -> None:
    assert validate_link(link) is False


@pytest.mark.parametrize("link", gen_parametrize("+AAAbbb111cc-_00$"))
def test_parse_link_invalid_illegal_characters(link: str) -> None:
    assert validate_link(link) is False


@pytest.mark.parametrize(
    "link",
    [
        "https://casinot-tri-topora.com",
        "oefiejgirnivjgmioewjkfoprjgioerj",
        "http://google.com",
    ],
)
def test_parse_link_invalid_stupid_ass_link(link: str) -> None:
    assert validate_link(link) is False


@pytest.mark.parametrize(
    "link",
    [
        "https://t.me/rabotayvpolshe",
        "ps://t.me/robota_lviv_robota",
        "://t.me/undress_best_bot",
        "t.me/robota_ua_rabota",
    ],
)
def test_parse_link_normie_channels(link: str) -> None:
    assert validate_link(link) is False
