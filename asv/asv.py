from dataclasses import dataclass
from typing import NamedTuple, List, Iterator
import io


class Format(NamedTuple):
    EOL: str
    DELIMITER: str


ASV_FORMAT = Format(
    EOL=chr(29) + "\n",
    DELIMITER=chr(30),
)


@dataclass
class ASVIO:
    stream: io.TextIOWrapper
    fmt: Format = ASV_FORMAT


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
