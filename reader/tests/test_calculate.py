import txtcompiler

def test_isnumber():
    assert txtcompiler.isnumber(-243.43)
    assert not txtcompiler.isnumber("wasd34.21")
    assert txtcompiler.isnumber("23.1")

def test_calculate_simple_1():
    assert txtcompiler.calculate("1+4-2") == 2

def test_calculate_simple_2():
    assert txtcompiler.calculate("2*4-4") == 4