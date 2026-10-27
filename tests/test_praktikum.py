import runpy

import pytest


@pytest.mark.parametrize("run_name", ["praktikum.praktikum", "__main__"])
def test_main_prints_receipt(capsys, run_name):
    namespace = runpy.run_module("praktikum.praktikum", run_name=run_name)
    if run_name != "__main__":
        namespace["main"]()

    assert capsys.readouterr().out == (
        "(==== black bun ====)\n"
        "= sauce sour cream =\n"
        "= filling cutlet =\n"
        "= filling dinosaur =\n"
        "(==== black bun ====)\n\n"
        "Price: 700\n"
    )
