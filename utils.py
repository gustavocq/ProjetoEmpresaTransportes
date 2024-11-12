import json
import os
import unicodedata

class Utils:
    @staticmethod
    def limparTela():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pausaParaContinuar():
        print("\nPressione Enter para continuar...")
        input()  

    @staticmethod
    def autenticarAdmin(senha_fornecida):
        senha_admin = "admin"  # Defina uma senha forte
        if senha_fornecida == senha_admin:
            print("Acesso concedido.")
            return True
        else:
            print("Senha incorreta. Acesso negado.")
            return False 

    @staticmethod
    def carregarDadosVeiculos(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                veiculosTransporte = json.load(arquivo)
                return veiculosTransporte
        except FileNotFoundError:
            print("Erro: O arquivo JSON de veículos não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: O JSON dos veículos está mal formatado.")
        except Exception as e:
            print(f"Erro inesperado ao carregar veículos: {e}")
        return None

    # Carrega os dados das cidades do arquivo JSON
    @staticmethod
    def carregarCidades(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                cidades = json.load(arquivo)
                return cidades
        except FileNotFoundError:
            print("Erro: O arquivo de cidades não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: O JSON das cidades está mal formatado.")
        except Exception as e:
            print(f"Erro inesperado ao carregar cidades: {e}")
        return None

    # Carrega as siglas dos estados
    @staticmethod
    def carregarSiglas(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                siglas = json.load(arquivo)
                return siglas
        except FileNotFoundError:
            print("Erro: O arquivo de siglas não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: O JSON das siglas está mal formatado.")
        except Exception as e:
            print(f"Erro inesperado ao carregar siglas: {e}")
        return None

    @staticmethod
    def salvarDadosVeiculos(caminho, veiculosTransporte):
        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                json.dump(veiculosTransporte, arquivo, ensure_ascii=False, indent=4)
                print("Dados dos veículos salvos com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar dados dos veículos: {e}")

    @staticmethod
    def validarEstado(estado, siglas):
        estado = estado.strip().lower()
        siglas_lower = {k.lower(): v for k, v in siglas.items()}
        if estado in siglas_lower:
            return siglas_lower[estado]
        elif estado in (v.lower() for v in siglas_lower.values()):
            return Utils.removerAcento(estado)
        return None

    @staticmethod
    def validarCidade(cidade, estado, cidades):
        estado_cidades = Utils.listarCidadesPorEstado(estado, cidades)
        if estado_cidades:
            if cidade in estado_cidades:
                return cidade
        return None

    @staticmethod
    def filtrarVeiculosPorCategoria(veiculosTransporte, categoria, peso):
        veiculos_disponiveis = []
        if categoria in veiculosTransporte:
            for veiculo in veiculosTransporte[categoria]:
                capacidade = veiculo['Capacidade']
                if capacidade >= peso and veiculo.get('Disponibilidade') == "Sim":
                    veiculos_disponiveis.append(veiculo)
        return veiculos_disponiveis

    @staticmethod
    def reservarVeiculo(veiculo, caminho, veiculosTransporte, cidade, estado):
        veiculo['Destino'] = f"{cidade} - {estado}"
        veiculo['Disponibilidade'] = "Nao"
        Utils.salvarDadosVeiculos(caminho, veiculosTransporte)
        print(f"Veículo {veiculo['Modelo']} reservado com sucesso! Destino: {veiculo['Destino']}")

    @staticmethod
    def listarCidadesPorEstado(estado, cidades):
        if estado in cidades:
            return cidades[estado]
        else:
            return None

    @staticmethod
    def removerAcento(texto):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

    @staticmethod
    def montaMelhorRota(cidadeSaida, estadoSaida, cidadeDestino, estadoDestino):
        cidadeSaida = cidadeSaida.replace(" ","+")
        estadoSaida = estadoSaida.replace(" ","+")
        cidadeDestino = cidadeDestino.replace(" ","+")
        estadoDestino = estadoDestino.replace(" ","+")
        return f"https://www.google.com/maps/dir/?api=1&origin={cidadeSaida},{estadoSaida}&destination={cidadeDestino},{estadoDestino}&travelmode=driving"

    @staticmethod
    def autenticarAdmin(senha_fornecida):
        senha_admin = "admin"
        if senha_fornecida == senha_admin:
            print("Acesso concedido.")
            return True
        else:
            print("Senha incorreta. Acesso negado.")
            return False    
    
    @staticmethod
    def marcarVeiculoComoDisponivel(self):
        veiculos_indisponiveis = [
            veiculo for categoria in self.veiculosTransporte.values()
            for veiculo in categoria if veiculo.get('Disponibilidade') == "Nao"
        ]

        if not veiculos_indisponiveis:
            print("Não há veículos indisponíveis para marcar como disponíveis.")
            return

        print("\nEscolha um veículo para marcar como disponível:")
        for i, veiculo in enumerate(veiculos_indisponiveis):
            print(f"{i + 1}. {veiculo['Modelo']} - Destino: {veiculo.get('Destino', 'N/A')}")

        try:
            escolha = int(input("Digite o número do veículo: ")) - 1
            if 0 <= escolha < len(veiculos_indisponiveis):
                veiculos_indisponiveis[escolha]['Disponibilidade'] = "Sim"
                veiculos_indisponiveis[escolha].pop('Destino', None)
                self.utils.salvarDadosVeiculos(self.CAMINHO_JSON_VEICULOS, self.veiculosTransporte)
                print("Veículo marcado como disponível com sucesso!")
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Tente novamente.")

    @staticmethod
    def marcarVeiculoComoIndisponivel(self):
        veiculos_disponiveis = [
            veiculo for categoria in self.veiculosTransporte.values()
            for veiculo in categoria if veiculo.get('Disponibilidade') == "Sim"
        ]

        if not veiculos_disponiveis:
            print("Não há veículos disponíveis para marcar como indisponíveis.")
            return

        print("\nEscolha um veículo para marcar como indisponível:")
        for i, veiculo in enumerate(veiculos_disponiveis):
            print(f"{i + 1}. {veiculo['Modelo']}")

        try:
            escolha = int(input("Digite o número do veículo: ")) - 1
            if 0 <= escolha < len(veiculos_disponiveis):
                destino = input("Informe o destino do veículo: ")
                veiculos_disponiveis[escolha]['Disponibilidade'] = "Nao"
                veiculos_disponiveis[escolha]['Destino'] = destino
                self.utils.salvarDadosVeiculos(self.CAMINHO_JSON_VEICULOS, self.veiculosTransporte)
                print("Veículo marcado como indisponível com sucesso!")
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Tente novamente.")

    def listarVeiculos(veiculosTransporte, disponibilidade):
        # Lista para armazenar veículos filtrados
        veiculosFiltrados = []

        # Itera sobre as categorias e veículos para filtrar pela disponibilidade
        for categoria in veiculosTransporte.values():
            for veiculo in categoria:
                # Verifica se a disponibilidade corresponde ao solicitado
                if veiculo.get('Disponibilidade', '').lower() == disponibilidade.lower():
                    veiculosFiltrados.append(veiculo)

        # Imprime os resultados conforme a disponibilidade
        if veiculosFiltrados:
            if disponibilidade.lower() == "sim":
                print("\nVeículos disponíveis:")
            else:
                print("\nVeículos indisponíveis:")

            # Exibe a lista dos veículos filtrados
            for i, veiculo in enumerate(veiculosFiltrados):
                destino = veiculo.get('Destino', 'Destino não especificado')
                print(f"{i + 1}. {veiculo['Modelo']} - Destino: {destino}")
        else:
            print("Não há veículos disponíveis no momento." if disponibilidade.lower() == "sim" else "Não há veículos indisponíveis no momento.")

    @staticmethod
    def marcarVeiculoComoDisponivel(veiculosTransporte, CAMINHO_JSON_VEICULOS):
        # Filtra os veículos indisponíveis
        veiculos_indisponiveis = [
            veiculo for categoria in veiculosTransporte.values()
            for veiculo in categoria if veiculo.get('Disponibilidade') == "Nao"
        ]

        # Verifica se há veículos indisponíveis
        if not veiculos_indisponiveis:
            print("Não há veículos indisponíveis para marcar como disponíveis.")
            return

        # Exibe a lista de veículos indisponíveis para o usuário escolher
        print("\nEscolha um veículo para marcar como disponível:")
        for i, veiculo in enumerate(veiculos_indisponiveis):
            destino = veiculo.get('Destino', 'Destino não especificado')
            print(f"{i + 1}. {veiculo['Modelo']} - Destino: {destino}")

        try:
            # Solicita que o usuário selecione um veículo
            escolha = int(input("Digite o número do veículo: ")) - 1

            # Valida a escolha do usuário e atualiza a disponibilidade
            if 0 <= escolha < len(veiculos_indisponiveis):
                veiculo_escolhido = veiculos_indisponiveis[escolha]
                veiculo_escolhido['Disponibilidade'] = "Sim"
                veiculo_escolhido.pop('Destino', None)  

                # Salva as alterações no JSON
                Utils.salvarDadosVeiculos(CAMINHO_JSON_VEICULOS, veiculosTransporte)
                print("Veículo marcado como disponível com sucesso!")
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Tente novamente.")

    @staticmethod
    def salvarDadosVeiculos(caminho_json, dados_veiculos):
        # Salva os dados dos veículos no arquivo JSON
        with open(caminho_json, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_veiculos, arquivo, ensure_ascii=False, indent=4)
        print("Dados dos veículos salvos com sucesso.")
    
    @staticmethod
    def setarVeiculoDisponivel(veiculo, veiculos):
        """
        Define o status de disponibilidade de um veículo como 'Sim'.
        """
        veiculo['Disponibilidade'] = "Sim"
        veiculo.pop('Destino', None) 
