import os
from utils import Utils

caminho_veiculos = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'veiculosTransporte.json')
caminho_cidades  = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'cidades.json')
caminho_siglas   = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'estadosSiglas.json')

# Carregar dados
veiculosTransporte = Utils.carregarDadosVeiculos(caminho_veiculos)
cidades = Utils.carregarCidades(caminho_cidades)
siglas = Utils.carregarSiglas(caminho_siglas)        
        
def menuVenda():
    while True:
        Utils.limparTela()
        print("\nEscolha um estado (ou sigla): ")
        estado = input("Informe o estado: ")
        
        estado_valido = Utils.validarEstado(estado, siglas)
        while estado_valido is None:
            print("Estado inválido! Tente novamente.")
            print("\nEscolha um estado (ou sigla): ")
            estado = input("Informe o estado: ")
            estado_valido = Utils.validarEstado(estado, siglas)
        
        cidades_do_estado = Utils.listarCidadesPorEstado(estado_valido, cidades)
        while cidades_do_estado is None:
            print("Nenhuma cidade encontrada para o estado fornecido.")
            estado = input("Informe o estado: ")
            cidades_do_estado = Utils.listarCidadesPorEstado(estado_valido, cidades)                

        cidade_escolhida = input("Informe a cidade: ")
        cidade_escolhida = Utils.removerAcento(cidade_escolhida)

        while cidade_escolhida.upper() not in cidades_do_estado:                
            cidade_escolhida = input("Informe a cidade: ")

        # Solicita e valida o peso
        while True:
            try:
                peso = int(input("Informe o peso da mercadoria (em kg): "))
                if peso <= 0:
                    raise ValueError("O peso deve ser um valor positivo.")
                break
            except ValueError as e:
                print(f"Entrada inválida: {e}. Tente novamente.")

        # Menu de categorias
        menuCategorias(peso, cidade_escolhida, estado_valido)

def menuAdministrador():

    senha = input("Insira a senha do Administrador:")
    if Utils.autenticarAdmin(senha) == True:
        while True:
            Utils.limparTela()
            print("=== Área do Administrador ===")
            print("1. Ver veículos indisponíveis")
            print("2. Marcar veículo como disponível")
            print("0. Voltar")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                Utils.listarVeiculos(veiculosTransporte, "Nao")
            elif escolha == "2":
                Utils.marcarVeiculoComoDisponivel(veiculosTransporte, caminho_veiculos)
            elif escolha == "0":
                break
            else:
                print("Opção inválida! Tente novamente.")
            Utils.pausaParaContinuar() 
    else:
        menuAdministrador()

def menuCategorias(peso, cidade_escolhida, estado):
    print("\nEscolha a categoria do veículo de transporte:")
    print("1. Utilitários")
    print("2. Caminhão Leve")
    print("3. Caminhão Pesado")
    print("4. Caminhão Extra Pesado")
    print("0. Voltar ao menu anterior")

    escolha = input("Digite o número da opção desejada: ")
    categorias = {
        "1": "Utilitarios",
        "2": "Caminhao Leve",
        "3": "Caminhao Pesado",
        "4": "Caminhao Extra Pesado"
    }

    if escolha in categorias:
        categoria = categorias[escolha]
        veiculos_disponiveis = Utils.filtrarVeiculosPorCategoria(veiculosTransporte, categoria, peso)
        if veiculos_disponiveis:
            print("\nVeículos disponíveis:")
            for i, veiculo in enumerate(veiculos_disponiveis):
                print(f"{i + 1}. {veiculo['Modelo']} - Capacidade: {veiculo['Capacidade']}")

            # Solicita ao usuário escolher um veículo para reservar
            try:
                veiculo_escolhido = int(input("Escolha um veículo para reservar (número): ")) - 1
                if 0 <= veiculo_escolhido < len(veiculos_disponiveis):
                    Utils.reservarVeiculo(veiculos_disponiveis[veiculo_escolhido], caminho_veiculos, veiculosTransporte, cidade_escolhida, estado)
                    print("A melhor rota para o destino da sua mercadoria está disponível no link abaixo, boa viagem!")
                    print(f"{Utils.montaMelhorRota("Belo Horizonte", "MG", cidade_escolhida, estado)}")
                else:
                    print("Opção inválida! Tente novamente.")
            except ValueError:
                print("Entrada inválida! Tente novamente.")
        else:
            print("Nenhum veículo disponível para as especificações fornecidas.")
    elif escolha == "0":
        return
    else:
        print("Opção inválida! Tente novamente.")

    pausaParaContinuarPosVenda()
    
def menuPrincipal():

    Utils.limparTela()
    while True:
        print("\n*** Menu Principal ***")
        print("1. Menu de Venda")
        print("2. Menu de Administrador")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menuVenda()
        elif opcao == '2':
            menuAdministrador()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def pausaParaContinuarPosVenda():
    print("\nPressione Enter para continuar...")
    input()
    menuPrincipal()


def main():    

    if veiculosTransporte is None or cidades is None or siglas is None:
        print("Erro ao carregar os dados. O programa será encerrado.")
        return

    menuPrincipal()

if __name__ == '__main__':
    main()
