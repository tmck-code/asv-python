from asv import asv
import os

def teardown_module():
    if os.path.exists:
        os.remove("test/data.asv")

def test_basic_row_generate():
    data = ["123", "Tom", "xxx", ""]
    result = asv.ASVWriter.generate(data)
    
    assert result == "lsdkjflsdkjf"

def test_basic_write():
    data = [
        ["id", "name", "value", "other"],
        ["123", "Tom", "xxx", ""],
        ["124", "Laura", "yyy", "some note here"],
    ]
    with asv.ASVWriter("test/data.asv") as writer:
        for row in data:
            writer.write_row(row)

    result = "\n".split(open("test/data.asv").read())

    assert result == "slkdfjlskjdflkj"