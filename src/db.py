import json
import typing as t

from src import utils


class DatabaseStructure(t.TypedDict):
    all_links: set[str]
    links: set[str]
    corrupted_links: set[str]
    delayed_messages: dict[int, set[str]]


class Database(metaclass=utils.Singleton):
    DATABASE_PATH = utils.DATA_DIR / "db.json"

    def __init__(self) -> None:
        self.data: DatabaseStructure = self._read_data()

    @classmethod
    def _read_data(cls) -> DatabaseStructure:
        result: DatabaseStructure = {
            "all_links": set(),
            "links": set(),
            "corrupted_links": set(),
            "delayed_messages": {},
        }

        if not cls.DATABASE_PATH.exists():
            return result

        with cls.DATABASE_PATH.open("r") as f:
            result = cls._sanitize_json(json.load(f))
        return result

    @staticmethod
    def _sanitize_json(data: dict) -> DatabaseStructure:
        result: DatabaseStructure = {
            "all_links": set(data["all_links"]),
            "links": set(data["links"]),
            "corrupted_links": set(data["corrupted_links"]),
            "delayed_messages": {},
        }

        for key, value in data["delayed_messages"].items():
            result["delayed_messages"][key] = set(value)

        return result

    @staticmethod
    def _unsanitize_json(data: DatabaseStructure) -> dict:
        result = {
            "all_links": list(data["all_links"]),
            "links": list(data["links"]),
            "corrupted_links": list(data["corrupted_links"]),
            "delayed_messages": {},
        }

        for key, value in data["delayed_messages"].items():
            result["delayed_messages"][key] = list(value)

        return result

    def save(self) -> None:
        with self.DATABASE_PATH.open("w") as f:
            json.dump(self._unsanitize_json(self.data), f, indent=2, ensure_ascii=False)

    def add_links(self, links: set[str]) -> None:
        for link in links:
            if actual_link := utils.validate_link(link):
                if actual_link in self.data["all_links"]:
                    continue

                self.data["all_links"].add(actual_link)
                self.data["links"].add(actual_link)
            else:
                self.data["corrupted_links"].add(link)

        self.save()

    def add_delayed_messages(self, msg: set[str], *, to: int) -> None:
        self.data["delayed_messages"].setdefault(to, set())
        self.data["delayed_messages"][to].update(msg)
        self.save()

    def mark_link_as_joined(self, link: str) -> None:
        self.data["links"].remove(link)
        self.save()
