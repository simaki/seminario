import pytest


from seminario.utils.table import Table


class MyTable(Table):

    @property
    def attributes(self):
        return ('a', 'b', 'c', 'd')


def test_table_set():
    table = MyTable(a='value_a')
    print(table.attributes)
    table['b'] = 'value_b'
    table.c = 'value_c'

    assert dir(table) == ['a', 'b', 'c']

    assert table.a == 'value_a'
    assert table.b == 'value_b'
    assert table.c == 'value_c'
    assert table['a'] == 'value_a'
    assert table['b'] == 'value_b'
    assert table['c'] == 'value_c'

    assert table.d is None


def test_table_error0():
    with pytest.raises(AttributeError):
        table = MyTable()
        print(table.z)


def test_table_error1():
    with pytest.raises(AttributeError):
        table = MyTable(z='value_z')
        print(table)


def test_table_error2():
    with pytest.raises(AttributeError):
        table = MyTable()
        table.z = 'value_z'
