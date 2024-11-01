import json
import os
from utils import Utils  # Certifique-se de que o arquivo utils.py esteja no mesmo diretório

class main:
    # Define o caminho para a pasta BancoDeDados e os arquivos de veículos e cidades
    CAMINHO_JSON_VEICULOS = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'veiculosTransporte.json')
    CAMINHO_JSON_CIDADES = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'cidades.json')
    CAMINHO_JSON_SIGLAS = os.path.join(os.path.dirname(__file__), 'BancoDeDados', 'estadosSiglas.json')

    def __init__(self):
        # Instanciando a classe Utils
        self.utils = Utils()
        self.veiculosTransporte = self.utils.carregarDadosVeiculos(self.CAMINHO_JSON_VEICULOS)
        self.cidades = self.utils.carregarCidades(self.CAMINHO_JSON_CIDADES)
        self.siglas = self.utils.carregarSiglas(self.CAMINHO_JSON_SIGLAS)

        # Verificação após carregar os dados
        if not self.veiculosTransporte:
            print("Erro ao carregar dados dos veículos.")
            exit()
        if not self.cidades:
            print("Erro ao carregar dados das cidades.")
            exit()
        if not self.siglas:
            print("Erro ao carregar dados das siglas.")
            exit()

    # Limpa a tela do terminal
    @staticmethod
    def limparTela():
        os.system("cls" if os.name == "nt" else "clear")

    # Pausa para continuar
    @staticmethod
    def pausaParaContinuar():
        print("\nPressione Enter para continuar...")
        input()

    # Menu de categorias de veículos
    def menuCategorias(self, peso, cidade_escolhida, estado):
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
            veiculos_disponiveis = self.utils.filtrarVeiculosPorCategoria(self.veiculosTransporte, categoria, peso)
            if veiculos_disponiveis:
                print("\nVeículos disponíveis:")
                for i, veiculo in enumerate(veiculos_disponiveis):
                    print(f"{i + 1}. {veiculo['Modelo']} - Capacidade: {veiculo['Capacidade']}")

                # Solicita ao usuário escolher um veículo para reservar
                try:
                    veiculo_escolhido = int(input("Escolha um veículo para reservar (número): ")) - 1
                    if 0 <= veiculo_escolhido < len(veiculos_disponiveis):
                        self.utils.reservarVeiculo(veiculos_disponiveis[veiculo_escolhido], self.CAMINHO_JSON_VEICULOS, self.veiculosTransporte)
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
        
        self.pausaParaContinuar()

    # Menu principal
    def menuPrincipal(self):
        while True:
            self.limparTela()
            print("\nEscolha um estado (ou sigla): ")
            estado = input("Informe o estado: ")
            
            estado_valido = self.utils.validarEstado(estado, self.siglas)
            while estado_valido is None:
                print("Estado inválido! Tente novamente.")
                print("\nEscolha um estado (ou sigla): ")
                estado = input("Informe o estado: ")
                estado_valido = self.utils.validarEstado(estado, self.siglas)
            
            cidades_do_estado = self.utils.listarCidadesPorEstado(estado_valido, self.cidades)
            while cidades_do_estado is None:
                print("Nenhuma cidade encontrada para o estado fornecido.")
                estado = input("Informe o estado: ")
                cidades_do_estado = self.utils.listarCidadesPorEstado(estado_valido, self.cidades)                

            cidade_escolhida = input("Informe a cidade: ")
            cidade_escolhida = self.utils.removerAcento(cidade_escolhida)

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
            self.menuCategorias(peso, cidade_escolhida, estado_valido)

# Carregamento inicial e execução do menu principal
if __name__ == "__main__":
    main = main()
    main.menuPrincipal()
