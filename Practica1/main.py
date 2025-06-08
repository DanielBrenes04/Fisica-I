# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import math

def calcularVector(i):
    print(f"\nVector #{i+1}")
    print("¿Cómo desea ingresar el vector?")
    print("1. Magnitud y dirección")
    print("2. Componentes (x, y)")
    opcion = input("Seleccione una opción (1 o 2): ")

    if opcion == "1":
        magnitud = float(input("Ingrese la magnitud: "))
        direccion = float(input("Ingrese la dirección en grados: "))
        rad = math.radians(direccion)
        x = magnitud * math.cos(rad)
        y = magnitud * math.sin(rad)
    elif opcion == "2":
        x = float(input("Ingrese la componente x: "))
        y = float(input("Ingrese la componente y: "))
    else:
        print("Opción no válida. Intente de nuevo.")
        return calcularVector(i)
    return x, y

def main():
    N = int(input("¿Cuántos vectores desea ingresar? "))
    componentes_x = []
    componentes_y = []

    for i in range(N):
        x, y = calcularVector(i)
        componentes_x.append(x)
        componentes_y.append(y)

    suma_x = sum(componentes_x)
    suma_y = sum(componentes_y)

    print("\nVector resultante en componentes:")
    print(f"Componente x: {suma_x:.2f}")
    print(f"Componente y: {suma_y:.2f}")

if __name__ == "_main_":
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


