import requests


def escolherDieta():
    ingredientes = []
    restricao_dieta = []

    dieta = input("Que tipo de dieta pretendes seguir? ")

    escolha_ingredientes = input("Desejas usar algum ingrediente especifio (sim/nao)? ").lower() #Lower para nao ter problema de capitalizacao
    while escolha_ingredientes == "sim":
        ingredientes.append(input("Que ingrediente pretendes utilizar: ").lower()) #Damos lower para nao ter problemas na query da api
        escolha_ingredientes = input("Desejas usar algum outro ingrediente (sim/nao)? ").lower()
    
    escolha_restricao = input("Tens alguma restricao dietetica (sim/nao)? ")
    while escolha_restricao == "sim":
        restricao_dieta.append(input("Que restricao dietetica tens? ").lower()) 
        escolha_restricao = input("Desejas adicionar alguma outra restricao (sim/nao)? ").lower()

    return dieta, ingredientes, restricao_dieta

def main():
    dieta, ingredientes, restricao_dieta = escolherDieta()

main()