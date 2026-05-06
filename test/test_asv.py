from asv import asv
import os

def teardown_module():
    if os.path.exists:
        os.remove('test/data.asv')

def test_basic_row_generate():
    data = ['123', 'Tom', 'xxx', '']
    result = asv.ASVWriter.generate(data)

    assert result == f'123\x1fTom\x1fxxx\x1f'

def test_basic_write():
    data = [
        ['id', 'name', 'value', 'other'],
        ['123', 'Tom', 'xxx', ''],
        ['124', 'Laura', 'yyy', 'some note here'],
    ]
    with asv.ASVWriter('test/data.asv') as writer:
        for row in data:
            writer.write_row(row)

    result = [l.split('\x1f') for l in open('test/data.asv').read().split('\x1e\n')]
    expected = data + [['']]
    assert result == expected
