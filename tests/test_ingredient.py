import pytest

from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestIngredient:
    @pytest.mark.parametrize("name", ["cutlet", "Космическая котлета"])
    def test_get_name_returns_ingredient_name(self, name):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, name, 100)

        assert ingredient.get_name() == name

    @pytest.mark.parametrize("price", [0, 100, 10.25])
    def test_get_price_returns_ingredient_price(self, price):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", price)

        assert ingredient.get_price() == price

    @pytest.mark.parametrize("ingredient_type", [INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING])
    def test_get_type_returns_ingredient_type(self, ingredient_type):
        ingredient = Ingredient(ingredient_type, "ingredient", 100)

        assert ingredient.get_type() == ingredient_type
