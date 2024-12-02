import os
from utils import Utils

# Caminhos para os arquivos de dados
caminho_veiculos = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'veiculosTransporte.json')
caminho_cidades = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'cidades.json')
caminho_siglas = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'estadosSiglas.json')

# Carregar dados
veiculosTransporte = Utils.carregarDadosVeiculos(caminho_veiculos)
cidades = Utils.carregarCidades(caminho_cidades)
siglas = Utils.carregarSiglas(caminho_siglas)


def escolherCidadeEstado():
    """Permite ao usuário escolher uma cidade e estado de saída entre as opções fixas."""
    opcoes = [
        ("Belém", "PA"),
        ("Recife", "PE"),
        ("São Paulo", "SP"),
        ("Curitiba", "PR")
    ]

    while True:
        Utils.limparTela()
        print("Escolha uma cidade e estado para saída:")
        for i, (cidade, estado) in enumerate(opcoes, start=1):
            print(f"{i}. {cidade} - {estado}")
        print("0. Voltar ao menu anterior")
        print("9. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "0":
            return None, None  # Voltar ao menu anterior
        elif escolha == "9":
            Utils.limparTela()
            exit()

        try:
            escolha = int(escolha)
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Tente novamente.")


def menuVenda():
    while True:
        Utils.limparTela()
        print("\nEscolha um estado (ou sigla): ")
        print("0. Voltar ao menu principal")
        print("9. Sair")

        estado_destino = input("Informe o estado: ")
        if estado_destino == "0":
            return  # Voltar ao menu principal
        elif estado_destino == "9":
            Utils.limparTela()
            exit()

        estado_valido = Utils.validarEstado(estado_destino, siglas)
        while estado_valido is None:
            print("Estado inválido! Tente novamente.")
            estado_destino = input("Informe o estado: ")
            if estado_destino == "0":
                return
            elif estado_destino == "9":
                Utils.limparTela()
                exit()
            estado_valido = Utils.validarEstado(estado_destino, siglas)

        while True:
            print("\nInforme o nome da cidade:")
            print("0. Voltar para informar outro estado")
            print("9. Sair")

            cidade_Destino = input("Digite o nome da cidade: ")
            if cidade_Destino == "0":
                break
            elif cidade_Destino == "9":
                Utils.limparTela()
                exit()

            cidade_Destino = Utils.removerAcento(cidade_Destino)
            cidades_do_estado = Utils.listarCidadesPorEstado(estado_valido, cidades)

            if cidade_Destino.upper() not in cidades_do_estado:
                print("Cidade inválida! Tente novamente.")
            else:
                while True:
                    try:
                        print("\nInforme o peso da mercadoria (em kg):")
                        print("0. Voltar para informar outra cidade")
                        print("9. Sair")
                        peso = input("Digite o peso: ")

                        if peso == "0":
                            break
                        elif peso == "9":
                            Utils.limparTela()
                            exit()

                        peso = int(peso)
                        if peso <= 0:
                            raise ValueError("O peso deve ser um valor positivo.")
                        menuCategorias(peso, cidade_Destino, estado_valido)
                        return
                    except ValueError as e:
                        print(f"Entrada inválida: {e}. Tente novamente.")


def menuAdministrador():
    while True:
        Utils.limparTela()
        print("\n=== Área do Administrador ===")
        print("Digite a senha para acessar:")
        print("0. Voltar ao menu principal")
        print("9. Sair")

        senha = input("Senha: ")
        if senha == "0":
            return
        elif senha == "9":
            Utils.limparTela()
            exit()

        if Utils.autenticarAdmin(senha):
            while True:
                Utils.limparTela()
                print("=== Opções do Administrador ===")
                print("1. Ver veículos indisponíveis")
                print("2. Marcar veículo como disponível")
                print("0. Voltar")
                print("9. Sair")

                escolha = input("Escolha uma opção: ")
                if escolha == "1":
                    Utils.listarVeiculos(veiculosTransporte, "Nao")
                elif escolha == "2":
                    Utils.marcarVeiculoComoDisponivel(veiculosTransporte, caminho_veiculos)
                elif escolha == "0":
                    return
                elif escolha == "9":
                    Utils.limparTela()
                    exit()
                else:
                    print("Opção inválida! Tente novamente.")
                Utils.pausaParaContinuar()
        else:
            print("Senha incorreta! Tente novamente.")
            Utils.pausaParaContinuar()


def menuCategorias(peso, cidade_Destino, estado_destino):
    Cidade_Saida, Estado_Saida = escolherCidadeEstado()
    if Cidade_Saida is None or Estado_Saida is None:
        return  # Voltar ao menu anterior

    while True:
        Utils.limparTela()
        print("\nEscolha a categoria do veículo de transporte:")
        print("1. Utilitários")
        print("2. Caminhão Leve")
        print("3. Caminhão Pesado")
        print("4. Caminhão Extra Pesado")
        print("0. Voltar ao menu anterior")
        print("9. Sair")

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

                try:
                    veiculo_escolhido = int(input("Escolha um veículo para reservar (número): ")) - 1
                    if 0 <= veiculo_escolhido < len(veiculos_disponiveis):
                        Utils.reservarVeiculo(
                            veiculos_disponiveis[veiculo_escolhido],
                            caminho_veiculos,
                            veiculosTransporte,
                            cidade_Destino,
                            estado_destino
                        )
                        print("A melhor rota para o destino da sua mercadoria está disponível no link abaixo, boa viagem!")
                        print(f"{Utils.montaMelhorRota(Cidade_Saida, Estado_Saida, cidade_Destino, estado_destino)}")
                        Utils.pausaParaContinuar()
                        return
                    else:
                        print("Opção inválida! Tente novamente.")
                except ValueError:
                    print("Entrada inválida! Tente novamente.")
            else:
                print("Nenhum veículo disponível para as especificações fornecidas.")
                Utils.pausaParaContinuar()
        elif escolha == "0":
            return
        elif escolha == "9":
            Utils.limparTela()
            exit()
        else:
            print("Opção inválida! Tente novamente.")
            Utils.pausaParaContinuar()


def menuPrincipal():
    while True:
        Utils.limparTela()
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
            Utils.limparTela()
            exit()
        else:
            print("Opção inválida. Tente novamente.")


def main():
    if veiculosTransporte is None or cidades is None or siglas is None:
        print("Erro ao carregar os dados. O programa será encerrado.")
        return
    menuPrincipal()


if __name__ == '__main__':
    main()