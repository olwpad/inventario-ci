import pytest

from inventario import Inventario, StockInsuficiente


@pytest.fixture
def inv():
    i = Inventario()
    i.agregar("led", 10, 500)
    return i


def test_agregar_suma_cantidades(inv):
    inv.agregar("led", 5, 500)
    assert inv.cantidad("led") == 15


def test_retirar_descuenta(inv):
    inv.retirar("led", 4)
    assert inv.cantidad("led") == 6


def test_retirar_mas_de_lo_disponible_falla(inv):
    with pytest.raises(StockInsuficiente):
        inv.retirar("led", 11)


def test_producto_inexistente_tiene_cero(inv):
    assert inv.cantidad("motor") == 0


def test_valor_total(inv):
    inv.agregar("resistencia", 100, 50)
    assert inv.valor_total() == 10 * 500 + 100 * 50


@pytest.mark.parametrize("cantidad", [0, -3])
def test_cantidad_invalida(inv, cantidad):
    with pytest.raises(ValueError):
        inv.agregar("led", cantidad, 500)
