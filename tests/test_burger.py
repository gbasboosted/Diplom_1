from unittest.mock import Mock, call

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger


class TestBurger:
    def test_new_burger_has_no_bun(self, burger):
        assert burger.bun is None

    def test_new_burger_has_no_ingredients(self, burger):
        assert burger.ingredients == []

    def test_burgers_have_independent_ingredients(self, burger, ingredient_factory):
        another_burger = Burger()
        burger.add_ingredient(ingredient_factory())

        assert another_burger.ingredients == []

    def test_set_buns_sets_selected_bun(self, burger, bun):
        burger.set_buns(bun)

        assert burger.bun is bun

    def test_set_buns_replaces_bun(
        self, burger, bun, ingredient_factory
    ):
        ingredient = ingredient_factory()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        replacement = Mock(spec=Bun)
        burger.set_buns(replacement)

        assert burger.bun is replacement

    def test_set_buns_preserves_ingredients_when_replacing_bun(
        self, burger, bun, ingredient_factory
    ):
        ingredient = ingredient_factory()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        burger.set_buns(Mock(spec=Bun))

        assert burger.ingredients == [ingredient]

    @pytest.mark.parametrize("count", [1, 3], ids=["one", "several"])
    def test_add_ingredient_preserves_order(self, burger, ingredient_factory, count):
        ingredients = [ingredient_factory(name=f"ingredient {i}") for i in range(count)]

        for ingredient in ingredients:
            burger.add_ingredient(ingredient)

        assert burger.ingredients == ingredients

    def test_add_same_ingredient_twice(self, burger, ingredient_factory):
        ingredient = ingredient_factory()
        burger.add_ingredient(ingredient)
        burger.add_ingredient(ingredient)

        assert burger.ingredients == [ingredient, ingredient]

    @pytest.mark.parametrize(
        "index, remaining",
        [(0, [1, 2]), (1, [0, 2]), (2, [0, 1])],
        ids=["first", "middle", "last"],
    )
    def test_remove_ingredient_at_index(
        self, burger, ingredient_factory, index, remaining
    ):
        ingredients = [ingredient_factory(name=f"ingredient {i}") for i in range(3)]
        burger.ingredients = ingredients.copy()

        burger.remove_ingredient(index)

        assert burger.ingredients == [ingredients[i] for i in remaining]

    def test_remove_only_ingredient(self, burger, ingredient_factory):
        burger.ingredients = [ingredient_factory()]

        burger.remove_ingredient(0)

        assert burger.ingredients == []

    @pytest.mark.parametrize(
        "index, new_index, expected_order",
        [
            (0, 2, [1, 2, 0]),
            (2, 0, [2, 0, 1]),
            (0, 1, [1, 0, 2]),
            (2, 1, [0, 2, 1]),
            (1, 1, [0, 1, 2]),
        ],
        ids=["first-to-last", "last-to-first", "forward", "backward", "same-index"],
    )
    def test_move_ingredient_preserves_all_ingredients_in_expected_order(
        self, burger, ingredient_factory, index, new_index, expected_order
    ):
        ingredients = [ingredient_factory(name=f"ingredient {i}") for i in range(3)]
        burger.ingredients = ingredients.copy()

        burger.move_ingredient(index, new_index)

        assert burger.ingredients == [ingredients[i] for i in expected_order]

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_price",
        [
            (100, [], 200),
            (100, [50], 250),
            (100, [50, 20, 30], 300),
            (0, [], 0),
            (0, [0, 0], 0),
            (0, [50], 50),
            (100, [0], 200),
            (10.25, [1.25, 2.5], 24.25),
        ],
        ids=[
            "buns-only", "one-ingredient", "several-ingredients", "free-buns",
            "all-free", "free-buns-paid-filling", "free-filling", "fractional-prices",
        ],
    )
    def test_get_price_counts_two_buns_and_each_ingredient(
        self, burger, bun, ingredient_factory,
        bun_price, ingredient_prices, expected_price,
    ):
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)
        burger.ingredients = [ingredient_factory(price=price) for price in ingredient_prices]

        actual_price = burger.get_price()

        assert actual_price == pytest.approx(expected_price)

    def test_get_price_requests_bun_price_once(self, burger, bun):
        burger.set_buns(bun)

        burger.get_price()

        assert bun.get_price.call_args_list == [call()]

    @pytest.mark.parametrize("ingredient_index", [0, 1, 2], ids=["first", "middle", "last"])
    def test_get_price_requests_ingredient_price_once(
        self, burger, bun, ingredient_factory, ingredient_index
    ):
        burger.set_buns(bun)
        burger.ingredients = [ingredient_factory(price=price) for price in [50, 20, 30]]

        burger.get_price()

        assert burger.ingredients[ingredient_index].get_price.call_args_list == [call()]

    def test_get_price_counts_repeated_ingredient(self, burger, bun, ingredient_factory):
        ingredient = ingredient_factory(price=50)
        burger.set_buns(bun)
        burger.ingredients = [ingredient, ingredient]

        assert burger.get_price() == 300

    @pytest.mark.parametrize(
        "ingredient_type, expected_line",
        [("SAUCE", "= sauce ketchup ="), ("FILLING", "= filling ketchup =")],
        ids=["sauce", "filling"],
    )
    def test_get_receipt_uses_lowercase_type(
        self, burger, bun, ingredient_factory, ingredient_type, expected_line
    ):
        burger.set_buns(bun)
        burger.ingredients = [ingredient_factory("ketchup", 25, ingredient_type)]

        assert burger.get_receipt() == (
            "(==== black bun ====)\n"
            f"{expected_line}\n"
            "(==== black bun ====)\n\n"
            "Price: 225"
        )

    def test_get_receipt_without_ingredients(self, burger, bun):
        burger.set_buns(bun)

        assert burger.get_receipt() == (
            "(==== black bun ====)\n"
            "(==== black bun ====)\n\n"
            "Price: 200"
        )

    def test_get_receipt_shows_current_order_and_total_after_changes(
        self, burger, bun, ingredient_factory
    ):
        bun.get_name.return_value = "Космическая булочка"
        bun.get_price.return_value = 10.25
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_factory("Котлета", 2.5, "FILLING"))
        burger.add_ingredient(ingredient_factory("Соус", 1.25, "SAUCE"))
        burger.add_ingredient(ingredient_factory("Лишний", 100, "FILLING"))
        burger.move_ingredient(1, 0)
        burger.remove_ingredient(2)

        assert burger.get_receipt() == (
            "(==== Космическая булочка ====)\n"
            "= sauce Соус =\n"
            "= filling Котлета =\n"
            "(==== Космическая булочка ====)\n\n"
            "Price: 24.25"
        )
