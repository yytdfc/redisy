#!/usr/bin/env python
# encoding: utf-8
from redisy import Redisy
from redisy import Converter

r = Redisy(host='localhost', port=6379, db=0)


def test_converter():
    c = Converter('json')
    assert (c.from_value(1) == '1')
    assert (c.from_value(0.44) == '0.44')
    assert (c.from_value('hello') == '"hello"')
    assert (c.from_value('123') == '"123"')

    assert (c.to_value('1') == 1)
    assert (c.to_value('0.44') == 0.44)
    assert (c.to_value('"hello"') == 'hello')
    assert (c.to_value('"123"') == '123')


def test_connect():
    assert (r.ping())


def test_keyvalue():
    def set_get(key, value):
        r[key] = value
        assert (r[key] == value)

    set_get(1, 2)
    set_get(2, '123')
    set_get(3, '[234]')
    assert (r['none_key'] is None)


def test_list():
    list_raw = [1, '2', '333', [1, 2, 'abc'], (123)]
    r['1'] = list_raw
    l = r['1']
    assert (len(list_raw) == len(l))
    for i, j in zip(list_raw, l):
        assert (i == j)
    for i in range(len(l)):
        assert (l[i] == list_raw[i])
    assert (l.pop() == list_raw[-1])
    assert (l.pop(0) == list_raw[0])
    for i, j in zip(list_raw[1:-1], l):
        assert (i == j)
    l[0] = 1234
    assert (l[0] == 1234)
    try:
        l[999]
    except IndexError:
        assert (True)
    else:
        assert (False)
    l.append(4321)
    assert (l[-1] == 4321)
    l.extend(['f', 'i', 'f', 'a'])
    assert (l[-4:] == ['f', 'i', 'f', 'a'])
    print(l)
    print(repr(l))


def test_set():
    se = {1, 2, 'a'}
    r['1'] = se
    s = r['1']
    assert (len(s) == 3)
    assert (s() == se)
    assert (1 in s)
    assert (10 not in s)
    s.add(10)
    assert (10 in s)
    p = s.pop()
    assert (p not in s)
    print(s)
    print(repr(s))


def test_hash():
    dic = {1: 'a', '2': 'b', 'c': 3}
    r['1'] = dic
    d = r['1']
    print(d)
    assert (len(d) == 3)
    assert (d() == dic)
    assert (1 in d)
    assert (10 not in d)
    d[10] = 'ten'
    assert (10 in d)
    assert ('10' not in d)
    assert (d[10] == 'ten')
    assert (d.pop(10) == 'ten')
    del d[1]
    try:
        d[10]
    except KeyError:
        assert (True)
    else:
        assert (False)
    print(d)
    print(repr(d))
    print(d.keys())
    print(d.values())
