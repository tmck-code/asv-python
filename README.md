# asv-python
> *Reader &amp; Writer for "ASCII-Separated Value" file format*

The CSV format has one main advantage over other plain-text serialisations: **the size** that it produces.

JSON/XML have advantages around typing, however in many cases this is not actually very useful. e.g. any single json field is not actually guaranteed to be the same type between successive records

This advantage is entirely wasted due to the lax specification around fields containing newlines, and other characters that need to be escaped. This results in a smorgasbord of different formats that any CSV parser must implement.

---

## ASCII Separated Values

> See https://en.wikipedia.org/wiki/Delimiter#ASCII_delimited_text

The ASCII format, since the beginning of time, has defined **characters that are reserved for unit (cell) and record (row) separation**

- `30 == "record separator"`, signals the end of a record or row
- `31 == "unit separator"`, Between fields of a record, or members of a row. 

Using these mitigates every problem with value escaping that are encountered with the current format.

- When writing: No need to escape anything, or quote cells, and newlines are permitted
- When reading: Just detect the 2 characters, and split on them

---

## Example Usage

```python
from asv import asv

data = [
    ["id", "name", "value", "other"],
    ["123", "Tom", "xxx", ""],
    ["124", "Laura", "yyy", "some note here"],
]

with open("data.asv", "w") as ostream:
    writer = asv.ASVWriter(ostream)
    for row in data:
        writer.write_row(row)

open('test/data.asv').read()
# 'id\x1fname\x1fvalue\x1fother\x1e\n123\x1fTom\x1fxxx\x1f\x1e\n124\x1fLaura\x1fyyy\x1fsome note here\x1e\n'

with open("data.asv") as istream:
    reader = asv.ASVReader(istream)
    for row in reader:
        print(row)

# ['id', 'name', 'value', 'other']
# ['123', 'Tom', 'xxx', '']
# ['124', 'Laura', 'yyy', 'some note here']
```
