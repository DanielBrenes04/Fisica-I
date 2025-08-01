# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import math
import matplotlib.pyplot as plt

def calcularFuerza(i):
    print(f"\nFuerza #{i+1}")
    print("¿Cómo desea ingresar la fuerza?")
    print("1. Magnitud y dirección")
    print("2. Componentes (Fx, Fy)")
    opcion = input("Seleccione una opción (1 o 2): ")

    if opcion == "1":
        magnitud = float(input("Ingrese la magnitud (N): "))
        direccion = float(input("Ingrese la dirección en grados: "))
        rad = math.radians(direccion)
        fx = magnitud * math.cos(rad)
        fy = magnitud * math.sin(rad)
    elif opcion == "2":
        fx = float(input("Ingrese la componente Fx (N): "))
        fy = float(input("Ingrese la componente Fy (N): "))
    else:
        print("Opción no válida. Intente de nuevo.")
        return calcularFuerza(i)
    return fx, fy

def visualizar_fuerzas(fuerzas, fx_total, fy_total):
    plt.figure(figsize=(7,7))
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.scatter(0, 0, s=500, color='lightblue', edgecolor='black', label='Bloque')

    for i, (fx, fy) in enumerate(fuerzas):
        plt.arrow(0, 0, fx, fy, head_width=0.15, length_includes_head=True, color='C0', alpha=0.6)
        plt.text(fx*1.05, fy*1.05, f'F{i+1}', color='C0')

    plt.arrow(0, 0, fx_total, fy_total, head_width=0.2, length_includes_head=True, color='red', linewidth=2, label='Fuerza Neta')
    plt.text(fx_total*1.1, fy_total*1.1, 'F_neta', color='red', fontweight='bold')

    max_f = max([abs(fx) for fx,fy in fuerzas] + [abs(fy) for fx,fy in fuerzas] + [abs(fx_total), abs(fy_total), 5])
    plt.xlim(-max_f*1.5, max_f*1.5)
    plt.ylim(-max_f*1.5, max_f*1.5)
    plt.xlabel('Fx (N)')
    plt.ylabel('Fy (N)')
    plt.title('Visualización de fuerzas sobre el bloque')
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()

def main():
    masa = float(input("Ingrese la masa del bloque (en kilogramos): "))
    N = int(input("¿Cuántas fuerzas desea ingresar? "))
    fuerzas = []

    for i in range(N):
        fx, fy = calcularFuerza(i)
        fuerzas.append((fx, fy))

    fx_total = sum(fx for fx, fy in fuerzas)
    fy_total = sum(fy for fx, fy in fuerzas)
    magnitud_fuerza_neta = math.hypot(fx_total, fy_total)

    print("\n--- RESULTADOS ---")
    print(f" - Componentes de la Fuerza Neta: Fx = {fx_total:.2f} N, Fy = {fy_total:.2f} N")
    print(f" - La Magnitud de la Fuerza Neta es: {magnitud_fuerza_neta:.2f} N")

    if masa > 0: # Para evitar división por cero
        aceleracion = magnitud_fuerza_neta / masa
        ax = fx_total / masa
        ay = fy_total / masa
        print(f" - Componentes de la Aceleración: ax = {ax:.2f} m/s², ay = {ay:.2f} m/s²")
        print(f" - La Magnitud de la Aceleración del bloque es: {aceleracion:.2f} m/s²")
    else:
        print("\nLa masa debe ser mayor que cero para calcular la aceleración.")

    visualizar_fuerzas(fuerzas, fx_total, fy_total)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
