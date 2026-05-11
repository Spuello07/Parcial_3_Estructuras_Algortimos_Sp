"""
Deteccion de Objetos en Imagenes Binarias
Parcial #3 - Estructuras de Datos y Algoritmos
"""
import sys
import os
from collections import deque


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        for attr in dir(Color):
            if not attr.startswith("_"):
                setattr(Color, attr, "")


def pausar(mensaje="Presione ENTER para continuar..."):
    input(f"\n{Color.OKCYAN}{mensaje}{Color.ENDC}")


def print_titulo(texto):
    print(f"\n{Color.BOLD}{texto}{Color.ENDC}\n")


def print_seccion(texto):
    print(f"\n{Color.BOLD}{texto}{Color.ENDC}")


def leer_imagen(ruta):
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    imagen = []
    for num, linea in enumerate(lineas, 1):
        linea = linea.strip()
        if not linea:
            continue
        try:
            fila = [int(x) for x in linea.split()]
        except ValueError:
            raise ValueError(f"Linea {num}: solo 0 y 1 separados por espacios.")
        if not all(x in (0, 1) for x in fila):
            raise ValueError(f"Linea {num}: valores invalidos (solo 0 o 1).")
        if fila:
            imagen.append(fila)

    if not imagen:
        raise ValueError("Archivo vacio.")

    n_cols = len(imagen[0])
    for i, fila in enumerate(imagen):
        if len(fila) != n_cols:
            raise ValueError(f"Fila {i+1} tiene {len(fila)} cols, esperado {n_cols}.")
    return imagen


def visualizar_imagen(imagen):
    filas, cols = len(imagen), len(imagen[0])
    lineas = ["     " + " ".join(str(i % 10) for i in range(cols))]
    lineas.append("   " + "─" * (cols * 2 + 1))
    for i, fila in enumerate(imagen):
        lineas.append(f"{i:2d} │ " + " ".join("█" if x else "░" for x in fila))
    return "\n".join(lineas)


def tiene_marco(imagen):
    filas, cols = len(imagen), len(imagen[0])
    if filas == 1 and cols == 1:
        return imagen[0][0] == 0
    for j in range(cols):
        if imagen[0][j] or imagen[filas - 1][j]:
            return False
    for i in range(filas):
        if imagen[i][0] or imagen[i][cols - 1]:
            return False
    return True


def obtener_bordes_anomalos(imagen):
    anomalos = []
    filas, cols = len(imagen), len(imagen[0])
    for j in range(cols):
        if imagen[0][j]:
            anomalos.append((0, j))
        if imagen[filas - 1][j]:
            anomalos.append((filas - 1, j))
    for i in range(filas):
        if imagen[i][0]:
            anomalos.append((i, 0))
        if imagen[i][cols - 1]:
            anomalos.append((i, cols - 1))
    return list(set(anomalos))


def contar_objetos_y_stats(imagen):
    filas, cols = len(imagen), len(imagen[0])
    visitado = [[False] * cols for _ in range(filas)]
    etiquetas = [[0] * cols for _ in range(filas)]
    objetos_stats = []
    vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    contador = 0

    for i in range(filas):
        for j in range(cols):
            if imagen[i][j] and not visitado[i][j]:
                contador += 1
                cola = deque([(i, j)])
                visitado[i][j] = True
                etiquetas[i][j] = contador
                pixeles = []

                while cola:
                    x, y = cola.popleft()
                    pixeles.append((x, y))
                    for dx, dy in vecinos:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < filas and 0 <= ny < cols:
                            if imagen[nx][ny] and not visitado[nx][ny]:
                                visitado[nx][ny] = True
                                etiquetas[nx][ny] = contador
                                cola.append((nx, ny))

                area = len(pixeles)
                xs = [p[0] for p in pixeles]
                ys = [p[1] for p in pixeles]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                perimetro = 0
                for x, y in pixeles:
                    for dx, dy in vecinos:
                        nx, ny = x + dx, y + dy
                        if nx < 0 or nx >= filas or ny < 0 or ny >= cols or not imagen[nx][ny]:
                            perimetro += 1
                objetos_stats.append({
                    "id": contador,
                    "area": area,
                    "perimetro": perimetro,
                    "bbox": (min_x, min_y, max_x, max_y),
                    "alto": max_x - min_x + 1,
                    "ancho": max_y - min_y + 1,
                    "centroide": (sum(xs) / area, sum(ys) / area)
                })

    return contador, objetos_stats, etiquetas


def visualizar_etiquetas(etiquetas):
    filas, cols = len(etiquetas), len(etiquetas[0])
    max_e = max(max(f) for f in etiquetas)
    d = len(str(max_e)) if max_e else 1
    lineas = ["     " + " ".join(str(i % 10).center(d) for i in range(cols))]
    lineas.append("   " + "─" * (cols * (d + 1) + 1))
    for i, fila in enumerate(etiquetas):
        lineas.append(f"{i:2d} │ " + " ".join(str(x).center(d) if x else "░".center(d) for x in fila))
    return "\n".join(lineas)


def exportar_reporte(ruta_entrada, stats_img, hay_marco, objetos, filas, cols):
    nombre = os.path.splitext(os.path.basename(ruta_entrada))[0]
    ruta_out = os.path.join(os.path.dirname(ruta_entrada), f"RESULTADO_{nombre}.txt")
    reporte = (
        f"DETECCION DE OBJETOS - REPORTE\n"
        f"\n"
        f"Archivo: {os.path.basename(ruta_entrada)}\n"
        f"Dimensiones: {filas}x{cols}\n"
        f"Marco: {'SI' if hay_marco else 'NO'}\n"
        f"Objetos detectados: {len(objetos)}\n\n"
        f"Estadisticas:\n"
        f"  Pixeles blancos: {stats_img['blancos']}\n"
        f"  Pixeles negros:  {stats_img['negros']}\n\n"
        f"Detalle de objetos:\n"
    )
    for obj in objetos:
        reporte += (
            f"\nObjeto #{obj['id']}:\n"
            f"  Area:      {obj['area']} pixeles\n"
            f"  Perimetro: {obj['perimetro']}\n"
            f"  BBox:      filas [{obj['bbox'][0]}-{obj['bbox'][2]}], cols [{obj['bbox'][1]}-{obj['bbox'][3]}]\n"
            f"  Dimension: {obj['alto']}x{obj['ancho']}\n"
            f"  Centroide: ({obj['centroide'][0]:.2f}, {obj['centroide'][1]:.2f})\n"
        )
    with open(ruta_out, 'w', encoding='utf-8') as f:
        f.write(reporte)
    return ruta_out


def crear_prueba():
    datos = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,1,0,0],
        [0,1,1,1,1,0,0,1,0,0],
        [0,1,1,1,0,0,0,1,0,0],
        [0,0,1,1,0,0,1,1,0,0],
        [0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,1,1,0,0],
        [0,0,0,0,0,1,0,0,0,0]
    ]
    with open("imagen_prueba.txt", 'w') as f:
        for fila in datos:
            f.write(" ".join(map(str, fila)) + "\n")
    print(f"{Color.OKGREEN}Archivo de prueba creado: {os.path.abspath('imagen_prueba.txt')}{Color.ENDC}")
    return "imagen_prueba.txt"


def limpiar_pantalla():
    os.system("cls" if sys.platform == "win32" else "clear")


def menu():
    limpiar_pantalla()
    print_titulo("DETECCION DE OBJETOS EN IMAGENES BINARIAS")
    print(f"{Color.BOLD}Parcial #3 - Estructuras de Datos y Algoritmos{Color.ENDC}")
    print(f"{Color.OKCYAN}By: Santiago Jose Puello Berrocal{Color.ENDC}\n")
    print(f"  {Color.OKGREEN}[1]{Color.ENDC} Procesar imagen desde archivo")
    print(f"  {Color.OKGREEN}[2]{Color.ENDC} Crear imagen de prueba (10x10)")
    print(f"  {Color.OKGREEN}[0]{Color.ENDC} Salir\n")
    return input(f"{Color.BOLD}Opcion: {Color.ENDC}").strip()


def procesar(ruta, exportar=False):
    limpiar_pantalla()
    print_titulo("PROCESANDO IMAGEN")

    print_seccion("1. Carga del archivo")
    try:
        imagen = leer_imagen(ruta)
        filas, cols = len(imagen), len(imagen[0])
        print(f"{Color.OKGREEN}Cargado: {filas}x{cols} pixeles{Color.ENDC}")
    except Exception as e:
        print(f"{Color.FAIL}Error: {e}{Color.ENDC}")
        pausar()
        return False

    print_seccion("2. Visualizacion")
    print(f"{Color.OKCYAN}Leyenda: █ = Blanco (1)  |  ░ = Negro (0){Color.ENDC}")
    print(visualizar_imagen(imagen))
    pausar()

    print_seccion("3. Analisis de borde")
    hay_marco = tiene_marco(imagen)
    if hay_marco:
        print(f"{Color.OKGREEN}La imagen SI tiene marco.{Color.ENDC}")
    else:
        print(f"{Color.FAIL}La imagen NO tiene marco.{Color.ENDC}")
        anom = obtener_bordes_anomalos(imagen)
        print(f"{Color.OKCYAN}Pixeles blancos en borde: {len(anom)}{Color.ENDC}")
        for x, y in anom[:5]:
            print(f"   - ({x},{y})")
        if len(anom) > 5:
            print(f"   ... y {len(anom)-5} mas.")
    pausar()

    print_seccion("4. Deteccion de objetos (BFS 4-vecinos)")
    n_objetos, stats_objetos, etiquetas = contar_objetos_y_stats(imagen)
    print(f"{Color.OKGREEN}Objetos detectados: {n_objetos}{Color.ENDC}")

    if n_objetos:
        print_seccion("5. Mapa de objetos etiquetados")
        print(visualizar_etiquetas(etiquetas))
        pausar()

    print_seccion("6. Estadisticas de objetos")
    total = filas * cols
    blancos = sum(sum(f) for f in imagen)
    negros = total - blancos
    print(f"  Dimensiones imagen: {filas} x {cols}")
    print(f"  Total pixeles:      {total}")
    print(f"  Blancos:            {blancos} ({100*blancos/total:.1f}%)")
    print(f"  Negros:             {negros} ({100*negros/total:.1f}%)")
    print(f"  Objetos:            {n_objetos}\n")

    if stats_objetos:
        header = f"  {'ID':<6} {'Area':<8} {'Perimetro':<10} {'Dimension':<10} {'Centroide':<18}"
        print(f"{Color.BOLD}{header}{Color.ENDC}")
        print(f"  {'─'*6} {'─'*8} {'─'*10} {'─'*10} {'─'*18}")
        for obj in stats_objetos:
            linea = (
                f"  #{obj['id']:<5}"
                f" {obj['area']:<8}"
                f" {obj['perimetro']:<10}"
                f" {obj['alto']}x{obj['ancho']:<7}"
                f" ({obj['centroide'][0]:.2f}, {obj['centroide'][1]:.2f})"
            )
            print(linea)
    pausar()

    print_seccion("7. Resumen")
    print(f"  Archivo:  {os.path.basename(ruta)}")
    print(f"  Marco:    {'SI' if hay_marco else 'NO'}")
    print(f"  Objetos:  {n_objetos}")

    if exportar:
        stats_img = {"blancos": blancos, "negros": negros}
        r_out = exportar_reporte(ruta, stats_img, hay_marco, stats_objetos, filas, cols)
        print(f"{Color.OKGREEN}Reporte exportado: {r_out}{Color.ENDC}")

    print(f"\n{Color.BOLD}PROCESO COMPLETADO{Color.ENDC}")
    pausar("Presione ENTER para volver al menu...")
    return True


def main():
    while True:
        op = menu()
        if op == "1":
            ruta = input(f"\n{Color.BOLD}Ruta del archivo .txt: {Color.ENDC}").strip().strip('"\'')
            if not ruta:
                print(f"{Color.FAIL}Ruta vacia.{Color.ENDC}")
                pausar()
                continue
            exp = input(f"{Color.OKCYAN}Exportar reporte? (s/n): {Color.ENDC}").strip().lower() == "s"
            procesar(ruta, exportar=exp)
        elif op == "2":
            ruta = crear_prueba()
            pausar("ENTER para procesar...")
            procesar(ruta, exportar=False)
        elif op == "0":
            limpiar_pantalla()
            print(f"\n{Color.OKGREEN}Hasta pronto.{Color.ENDC}\n")
            pausar("Presione ENTER para cerrar...")
            break
        else:
            print(f"{Color.FAIL}Opcion invalida.{Color.ENDC}")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.WARNING}Interrumpido.{Color.ENDC}")
        pausar("Presione ENTER para cerrar...")