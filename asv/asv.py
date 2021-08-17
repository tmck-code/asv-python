from typing import NamedTuple
import io

class Format(NamedTuple):
    EOL: str
    DELIMITER: str

ASV_FORMAT = Format(
    EOL       = chr(29) + '\n',
    DELIMITER = chr(30),
)
from dataclasses import dataclass

@dataclass
class ASVReader:
    istream: io.TextIOWrapper
    fmt: Format = ASV_FORMAT

    def __iter__(self):
        buff = ''
        for line in self.istream:
            buff += line
            if line.endswith(self.fmt.EOL):
                yield buff.removesuffix(self.fmt.EOL).split(self.fmt.DELIMITER)
                buff = ''

@dataclass
class ASVWriter:
    ostream: io.TextIOWrapper
    fmt: Format = ASV_FORMAT

    def writerow(self, row):
        print(
            self.fmt.DELIMITER.join(row),
            file=self.ostream,
            end=self.fmt.EOL
        )

