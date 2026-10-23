import pytest

from praktikum.bun import Bun


class TestBun:
    @pytest.mark.parametrize("name", ["black bun", "Космическая булочка"])
    def test_get_name_returns_bun_name(self, name):
        assert Bun(name, 100).get_name() == name

    @pytest.mark.parametrize("price", [0, 100, 10.25])
    def test_get_price_returns_bun_price(self, price):
        assert Bun("black bun", price).get_price() == price
