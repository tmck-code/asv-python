from dataclasses import dataclass
from typing import NamedTuple, List, Iterator
import io


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

    def ensure_string(coll: list) -> list:
        return list(map(str, coll))

    def __enter__(self):
        self.stream: io.TextIOWrapper = open(self.fpath, "w")
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.stream.close()

@dataclass
class ASVReader(ASVIO):
    def __iter__(self) -> Iterator[List[str]]:
        buff = ""
        for line in self.stream:
            buff += line
            if line.endswith(self.fmt.EOL):
                yield buff.removesuffix(self.fmt.EOL).split(self.fmt.DELIMITER)
                buff = ""


@dataclass
class ASVWriter(ASVIO):
    def writerow(self, row: List[str]):
        print(self.fmt.DELIMITER.join(row), file=self.stream, end=self.fmt.EOL)
