from __future__ import annotations
import io
from collections.abc import Iterator
from dataclasses import dataclass
from typing import NamedTuple, Self


class Format(NamedTuple):
    EOL: str
    DELIMITER: str

# See https://en.wikipedia.org/wiki/Delimiter#ASCII_delimited_text
# 30 == "record separator", signals the end of a record or row
# 31 == "unit separator", Between fields of a record, or members of a row.
ASV_FORMAT = Format(
    EOL=chr(30) + "\n",
    DELIMITER=chr(31),
)


@dataclass
class ASVIO:
    fpath: str
    fmt: Format = ASV_FORMAT

    @staticmethod
    def ensure_string(coll: list) -> list:
        return list(map(str, coll))

    def __enter__(self) -> Self:
        self.stream: io.TextIOWrapper = open(self.fpath, "w")
        return self

    def __exit__(self, _exc_type: type, _exc_value: Exception, _traceback: object) -> None:
        self.stream.close()

@dataclass
class ASVReader(ASVIO):
    def __iter__(self) -> Iterator[list[str]]:
        buff = ""
        for line in self.stream:
            buff += line
            if line.endswith(self.fmt.EOL):
                yield buff.removesuffix(self.fmt.EOL).split(self.fmt.DELIMITER)
                buff = ""


@dataclass
class ASVWriter(ASVIO):

    @staticmethod
    def generate(row: list[str], delimiter: str = ASV_FORMAT.DELIMITER) -> str:
        return delimiter.join(row)

    def write_row(self, row: list[str]) -> None:
        print(self.generate(row), file=self.stream, end=self.fmt.EOL)
