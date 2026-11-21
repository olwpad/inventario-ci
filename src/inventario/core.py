"""Lógica de negocio mínima: un inventario de productos en memoria."""


class StockInsuficiente(Exception):
    """Se intenta retirar más unidades de las disponibles."""


class Inventario:
    def __init__(self):
        self._productos = {}  # nombre -> {"cantidad": int, "precio": float}

    def agregar(self, nombre: str, cantidad: int, precio: float) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        producto = self._productos.setdefault(nombre, {"cantidad": 0, "precio": precio})
        producto["cantidad"] += cantidad
        producto["precio"] = precio

    def retirar(self, nombre: str, cantidad: int) -> None:
        disponible = self.cantidad(nombre)
        if cantidad > disponible:
            raise StockInsuficiente(f"Solo hay {disponible} unidades de {nombre}")
        self._productos[nombre]["cantidad"] -= cantidad

    def cantidad(self, nombre: str) -> int:
        return self._productos.get(nombre, {"cantidad": 0})["cantidad"]

    def valor_total(self) -> float:
        return round(sum(p["cantidad"] * p["precio"] for p in self._productos.values()), 2)

    def como_dict(self) -> dict:
        return {nombre: dict(datos) for nombre, datos in self._productos.items()}
