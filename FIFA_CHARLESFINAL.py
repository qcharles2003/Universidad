##--Librerías necesarias--##
import json
import requests
import random
from typing import List, Optional
from datetime import datetime
import matplotlib.pyplot as plt
##--Fin de las librerías necesarias--##



##--Introducción a todas las clases del Programa--##
# Clase Equipo
class Equipo:
    def __init__(self, id: str, code: str, name: str, group: str):
        self.id = id
        self.code = code
        self.name = name
        self.group = group

# Clase Estadio
class Estadio:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

# Clase Partido
class Partido:
    def __init__(self, local: 'Equipo', visitante: 'Equipo', fecha_hora: str, estadio: 'Estadio'):
        self.local = local
        self.visitante = visitante
        self.fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
        self.estadio = estadio

# Clase Cliente
class Cliente:
    def __init__(self, nombre: str, cedula: str, edad: int):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

# Clase Entrada
class Entrada:
    def __init__(self, cliente: 'Cliente', partido: 'Partido', tipo: str, asiento: str, costo: float, codigo: str):
        self.cliente = cliente
        self.partido = partido
        self.tipo = tipo
        self.asiento = asiento
        self.costo = costo
        self.codigo = codigo

# Clase Producto
class Producto:
    def __init__(self, nombre: str, clasificacion: str, alcoholico: bool, empaque: bool, precio: float):
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.alcoholico = alcoholico
        self.empaque = empaque
        self.precio = precio

# Clase VentaRestaurante
class VentaRestaurante:
    def __init__(self, cliente: 'Cliente', productos: List['Producto'], total: float):
        self.cliente = cliente
        self.productos = productos
        self.total = total
##--Fin de la introducción a las clases del Programa--##


##--Generador de datos--##
def cargar_datos_desde_api(url: str):
    response = requests.get(url)
    return response.json()

def inicializar_datos():
    equipos_data = cargar_datos_desde_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json')
    estadios_data = cargar_datos_desde_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
    partidos_data = cargar_datos_desde_api('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json')

    equipos = [Equipo(e['id'], e['code'], e['name'], e['group']) for e in equipos_data]
    estadios = [Estadio(e['name'], e['city']) for e in estadios_data]

    equipos_dict = {equipo.id: equipo for equipo in equipos}
    estadios_dict = {estadio.name: estadio for estadio in estadios}

    partidos = []
    for partido in partidos_data:
        for equipo in equipos_dict:
            
            local = equipos_dict["away"]
            visitante = equipos_dict["home"]
            estadio = estadios_dict["stadium_id"]
        partidos.append(Partido(local, visitante, partido['date'], estadio))
    
    print(partidos)
    return equipos, estadios, partidos
##--Fin del generador de datos--##



##--Funciones para generar estadísticas--##
def generar_estadisticas(entradas: List[Entrada], ventas_restaurante: List[VentaRestaurante]):
    gasto_vip = [entrada.costo + sum(venta.total for venta in ventas_restaurante if venta.cliente == entrada.cliente) for entrada in entradas if entrada.tipo == 'VIP']
    promedio_gasto_vip = sum(gasto_vip) / len(gasto_vip) if gasto_vip else 0

    asistencia_partidos = {}
    for entrada in entradas:
        partido = entrada.partido
        if partido not in asistencia_partidos:
            asistencia_partidos[partido] = {'boletos_vendidos': 0, 'asistencia': 0}
        asistencia_partidos[partido]['boletos_vendidos'] += 1

    for venta in ventas_restaurante:
        for producto in venta.productos:
            if producto.nombre not in asistencia_partidos:
                asistencia_partidos[producto.nombre] = 0
            asistencia_partidos[producto.nombre] += 1

    return promedio_gasto_vip, asistencia_partidos
##--Fin de las funciones para generar estadísticas--##




##--Funciones para mostrar y graficar estadísticas--##
def mostrar_estadisticas(promedio_gasto_vip, asistencia_partidos):
    print(f"Promedio de gasto VIP: {promedio_gasto_vip:.2f}$")

    print("Asistencia a partidos (de mejor a peor):")
    for partido, data in sorted(asistencia_partidos.items(), key=lambda item: item[1]['asistencia'] / item[1]['boletos_vendidos'], reverse=True):
        print(f"{partido}: {data['boletos_vendidos']} boletos vendidos, {data['asistencia']} asistencia")

    partido_max_asistencia = max(asistencia_partidos.items(), key=lambda item: item[1]['asistencia'])[0]
    print(f"Partido con mayor asistencia: {partido_max_asistencia}")

    partido_max_boletos = max(asistencia_partidos.items(), key=lambda item: item[1]['boletos_vendidos'])[0]
    print(f"Partido con mayor boletos vendidos: {partido_max_boletos}")

    productos_mas_vendidos = sorted(asistencia_partidos.items(), key=lambda item: item[1], reverse=True)[:3]
    print("Top 3 productos más vendidos en el restaurante:")
    for producto, cantidad in productos_mas_vendidos:
        print(f"{producto}: {cantidad} vendidos")
##--Fin de las funciones para mostrar y graficar estadísticas--##




##--Funciones para generar y mostrar gráficos--##
def generar_graficos_estadisticas(promedio_gasto_vip, asistencia_partidos):
    plt.figure(figsize=(10, 6))
    partidos = list(asistencia_partidos.keys())
    ventas = [data['boletos_vendidos'] for data in asistencia_partidos.values()]
    asistencias = [data['asistencia'] for data in asistencia_partidos.values()]

    plt.bar(partidos, ventas, color='b', label='Boletos Vendidos')
    plt.bar(partidos, asistencias, color='r', label='Asistencia', alpha=0.7)
    plt.xlabel('Partidos')
    plt.ylabel('Número de Personas')
    plt.title('Boletos Vendidos y Asistencia por Partido')
    plt.legend()
    plt.show()
##--Fin de las funciones para generar y mostrar gráficos--##




##--Función principal--##
if __name__ == "__main__":
    equipos, estadios, partidos = inicializar_datos()

    #Registro clientes y ventas de entradas
    cliente1 = Cliente("Katherine Bautista", "14879255", 30)
    cliente2 = Cliente("Vianetth García", "6031235", 65)

    entrada1 = Entrada(cliente1, partidos[0], "VIP", "A1", 100.0, "ABC123")
    entrada2 = Entrada(cliente2, partidos[1], "General", "B2", 50.0, "DEF456")

    entradas = [entrada1, entrada2]

    #Registro de ventas en el restaurante
    producto1 = Producto("Cerveza", "bebida", True, False, 10)
    producto2 = Producto("Hamburguesa", "alimento", False, True, 8)

    venta_restaurante1 = VentaRestaurante(cliente1, [producto1, producto2], 50.0)
    venta_restaurante2 = VentaRestaurante(cliente2, [producto2], 20.0)

    ventas_restaurante = [venta_restaurante1, venta_restaurante2]

    #Generar y mostrar estadísticas
    promedio_gasto_vip, asistencia_partidos = generar_estadisticas(entradas, ventas_restaurante)
    mostrar_estadisticas(promedio_gasto_vip, asistencia_partidos)
    generar_graficos_estadisticas(promedio_gasto_vip, asistencia_partidos)
##--Fin de la función principal--##
