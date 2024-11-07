import json
import os
import unicodedata

class Utils:
    @staticmethod
    def carregarDadosVeiculos(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                veiculosTransporte = json.load(arquivo)
                print("Dados dos veículos carregados com sucesso!")
                return veiculosTransporte
        except FileNotFoundError:
            print("Erro: O arquivo JSON de veículos não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: O JSON dos veículos está mal formatado.")
        except Exception as e:
            print(f"Erro inesperado ao carregar veículos: {e}")
        return None

    @staticmethod
    def carregarCidades(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                cidades = json.load(arquivo)
                print("Cidades carregadas com sucesso!")
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
                print("Siglas dos estados carregadas com sucesso!")
                return siglas
        except FileNotFoundError:
            print("Erro: O arquivo de siglas não foi encontrado.")
        except json.JSONDecodeError:
            print("Erro: O JSON das siglas está mal formatado.")
        except Exception as e:
            print(f"Erro inesperado ao carregar siglas: {e}")
        return None

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
    def salvarDadosVeiculos(caminho, veiculosTransporte):
        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                json.dump(veiculosTransporte, arquivo, ensure_ascii=False, indent=4)
                print("Dados dos veículos salvos com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar dados dos veículos: {e}")

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
    
