import os

from asv import asv


def teardown_module() -> None:
    if os.path.exists('test/data.asv'):
        os.remove('test/data.asv')

def test_basic_row_generate() -> None:
    data = ['123', 'Tom', 'xxx', '']
    result = asv.ASVWriter.generate(data)

    assert result == '123\x1fTom\x1fxxx\x1f'

def test_basic_write() -> None:
    data = [
        ['id', 'name', 'value', 'other'],
        ['123', 'Tom', 'xxx', ''],
        ['124', 'Laura', 'yyy', 'some note here'],
    ]
    with open('test/data.asv', 'w') as ostream:
        writer = asv.ASVWriter(ostream)
        for row in data:
            writer.write_row(row)

    result = []
    with open('test/data.asv') as istream:
        for line in istream.read().split('\x1e\n'):
            result.append(line.split('\x1f'))

    # TODO: fix this last empty line behaviour
    expected = data + [['']]

    assert result == expected
