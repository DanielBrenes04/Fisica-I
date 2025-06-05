# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import math

def calcularVector(i):
    print(f"\nVector #{i+1}")
    magnitud = float(input("Ingrese la magnitud: "))
    direccion = float(input("Ingrese la direccion en grados: "))
    rad = math.radians(direccion)
    x= magnitud*math.cos(rad)
    y= magnitud*math.sin(rad)
    return x, y

def main():
    N = int(input("Cuantos vectores desea ingresar? "))
    sumx = 0.0
    sumy = 0.0

    for i in range(N):
        x, y = calcularVector(i)
        sumx += x
        sumy += y

    ResMagnitud = math.sqrt(sumx**2 + sumy**2)
    ResDireccion = math.degrees(math.atan2(sumy, sumx))

    print("\nVector resultante:")
    print(f"Magnitud: {ResMagnitud:.2f}")
    print(f"Direccion: {ResDireccion:.2f} grados")

if __name__ == "__main__":
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


