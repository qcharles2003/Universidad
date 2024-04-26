#SUBRUTINAS
def calcular_masa_arepas(num1,num2,num3):
    return num1+num2+num3


#CÓDIGO PRINCIPAL
input1=True
while(input1 == True):
    try:
        num1string = input("ingrese cantidad 1: ")
        num1float = float(num1string)
        input1 = False
    except:
        print("La cantida ingresada es incorrecta: ")


input2=True
while(input2 == True):
    try:
        num2string = input("ingrese cantidad 2: ")
        num2float = float(num2string)
        input2 = False
    except:
        print("La cantida ingresada es incorrecta: ")


input3=True
while(input3 == True):
    try:
        num3string = input("ingrese cantidad 3: ")
        num3float = float(num3string)
        input3 = False
    except:
        print("La cantida ingresada es incorrecta: ")


print("La cantidad total de masa de las arepas es:", calcular_masa_arepas(num1float,num2float,num3float), "gramos")