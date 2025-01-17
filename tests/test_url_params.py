import pytest

from juniorguru import url_params


@pytest.mark.parametrize('url,param_names,expected', [
    ('https://example.com', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&b=2', ['a', 'b'], 'https://example.com'),
    ('https://example.com?a=1&c=3&b=2', ['a', 'b'], 'https://example.com?c=3'),
    ('https://example.com', [], 'https://example.com'),
    ('https://example.com?a=1&b=2', [], 'https://example.com?a=1&b=2'),
])
def test_strip_params(url, param_names, expected):
    assert url_params.strip_params(url, param_names) == expected


@pytest.mark.parametrize('url,param_name,expected', [
    ('https://example.com', 'b', 'https://example.com?b=1'),
    ('https://example.com?a=1&b=2&c=3', 'b', 'https://example.com?a=1&b=3&c=3'),
])
def test_increment_param(url, param_name, expected):
    assert url_params.increment_param(url, param_name) == expected


@pytest.mark.parametrize('url,param_name,inc,expected', [
    ('https://example.com', 'b', 25, 'https://example.com?b=25'),
    ('https://example.com?a=1&b=2&c=3', 'b', 25, 'https://example.com?a=1&b=27&c=3'),
])
def test_increment_param_inc(url, param_name, inc, expected):
    assert url_params.increment_param(url, param_name, inc) == expected
