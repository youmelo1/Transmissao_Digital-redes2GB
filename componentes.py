import numpy as np

# ==============================================================================
# BLOCO 1: FONTE E CODIFICAÇÃO (Camada de Aplicação e Enlace)
# ==============================================================================

# --- PASSO 1: A Fonte ---
def ascii_binario(texto_original: str) -> list[int]:
    """
    Recebe: Um texto em ASCII.
    Faz: Converte o texto em binário.
    Retorna: Uma lista de 0s e 1s chamada 'bits_dados'.
    """
    string_binario = ''.join(format(ord(c), '08b') for c in texto_original)
    
    bits_dados = [int(bit) for bit in string_binario]
    
    return bits_dados


# --- PASSO 2: O Entregador Local (Codificação de Linha) ---
def codificacao_AMI(bits_dados: list[int]) -> list[int]:
    """
    Recebe: 'bits_dados' (0s e 1s vindos da fonte).
    Faz: Aplica AMI Bipolar (0 -> 0; 1 -> alterna +1/-1).
    Retorna: Lista de 'simbolos_ami' (ex: [0, +1, 0, -1]).
    """
    
    simbolos_ami = []
    occorrencias = 0
    
    for bit in bits_dados:
        if bit == 0:
            simbolos_ami.append(0)
        else:
            if occorrencias % 2 == 0:
                simbolos_ami.append(1)
            else:
                simbolos_ami.append(-1)
            occorrencias += 1
    
    return simbolos_ami

# ==============================================================================
# BLOCO 2: MODULAÇÃO (Camada Física - Transmissor)
# ==============================================================================

# --- PASSO 3A: O Pombo Correio (Técnica 1: ASK para AMI) ---
def modulacao_ASK(simbolos_ami: list[int], voltagem: float=1.0) -> np.ndarray:
    """
    Recebe: 'simbolos_ami', uma lista de inteiros discretos (-1, 0, 1).
    Faz: Mapeia os símbolos para amplitude de voltagem (Multiplicação escalar).
    Retorna: Um 'np.ndarray' de floats representando o sinal elétrico modulado.
    """
    
    # Garante que é array para permitir multiplicação vetorial
    sinal_entrada = np.array(simbolos_ami)
    
    # Modula a amplitude (Símbolo * Voltagem)
    sinal_transmitido = sinal_entrada * voltagem
    
    return sinal_transmitido


# ==============================================================================
# BLOCO 3: O MEIO (Canal com Ruído)
# ==============================================================================

# --- PASSO 4: O Nevoeiro ---
def canal_com_ruido_AWGN(sinal_transmitido: np.ndarray, snr_db: float) -> np.ndarray:
    """
    Recebe: 'sinal_transmitido' (array numpy de voltagens) e 'snr_db' (float em Decibéis).
    Faz: Calcula a potência do ruído baseada na SNR e soma ruído branco gaussiano ao sinal.
    Retorna: Um 'np.ndarray' contendo o sinal degradado (sinal + ruído).
    """
    
    # 1. Calcular a potência média do sinal transmitido
    potencia_sinal = np.mean(sinal_transmitido ** 2)
    
    # 2. Converter a SNR de dB para Linear
    snr_linear = 10 ** (snr_db / 10)
    
    # 3. Calcular a potência do ruído necessária
    potencia_ruido = potencia_sinal / snr_linear
    
    # 4. Gerar o ruído aleatório
    desvio_padrao = np.sqrt(potencia_ruido)
    ruido = np.random.normal(0, desvio_padrao, len(sinal_transmitido))
    
    # 5. Somar (Sinal + Ruído)
    sinal_recebido = sinal_transmitido + ruido
    
    return sinal_recebido

# ==============================================================================
# BLOCO 4: DEMODULAÇÃO E DECODIFICAÇÃO (Camada Física - Receptor)
# ==============================================================================

# --- PASSO 5A: O Receptor ASK ---
def demodulacao_ASK(sinal_recebido: np.ndarray, voltagem: float=1.0) -> np.ndarray:
    """
    Recebe: 'sinal_recebido' (array com ruído e voltagem variada).
    Faz: Normaliza o sinal e aplica limiares de decisão (>0.5, <-0.5) para recuperar inteiros.
    Retorna: Um 'np.ndarray' de inteiros com os símbolos estimados (-1, 0, 1).
    """
    
    # 1. Normaliza (tenta voltar para a escala de -1 a 1)
    sinal_normalizado = sinal_recebido / voltagem
    
    lista_recuperada = []
    
    for valor in sinal_normalizado:
        # Lógica de Decisão (Limiar em 0.5 e -0.5)
        if valor > 0.5:
            lista_recuperada.append(1)   # Estima que era +1
        elif valor < -0.5:
            lista_recuperada.append(-1)  # Estima que era -1
        else:
            lista_recuperada.append(0)   # Estima que era 0
            
    simbolos_ami_recuperados = np.array(lista_recuperada)
    
    return simbolos_ami_recuperados


# --- PASSO 6: O Tradutor do Entregador (Para AMI) ---
def decodificacao_AMI(simbolos_ami_recuperados: np.ndarray) -> list[int]:
    """
    Recebe: 'simbolos_ami_recuperados' (ex: [0, 1, 0, -1]).
    Faz: Transforma níveis AMI de volta em bits.
    Retorna: Lista 'bits_decodificados' (0s e 1s).
    """
    
    bits_decodificados = []
    
    for simbolo in simbolos_ami_recuperados:
        if simbolo == 0:
            bits_decodificados.append(0)
        else:
            # No AMI, tanto +1 quanto -1 representam o bit 1
            bits_decodificados.append(1)
    
    return bits_decodificados

# ==============================================================================
# BLOCO 5: DESTINO E ANÁLISE
# ==============================================================================

# --- PASSO 7: O Destino ---
def binario_ascii(bits_decodificados: list[int]) -> str:
    """
    Recebe: 'bits_decodificados' (lista final de bits).
    Faz: Agrupa em bytes e converte para texto.
    Retorna: String 'texto_final'.
    """
    
    texto_final = ""
    
    # Percorre de 8 em 8
    for i in range(0, len(bits_decodificados), 8):
        byte = bits_decodificados[i : i+8]
            
        byte_str = "".join(str(b) for b in byte)
        valor_ascii = int(byte_str, 2)
        texto_final += chr(valor_ascii)
        
    return texto_final


# --- PASSO 8: O Analista ---
def calcular_ber(bits_dados: list[int], bits_decodificados: list[int]) -> float:
    """
    Recebe: 'bits_dados' (original) e 'bits_decodificados' (final).
    Faz: Compara e calcula a taxa de erro.
    Retorna: Valor float (Taxa de Erro de Bit).
    """
    
    erros = 0
    for i in range(len(bits_dados)):
        if bits_dados[i] != bits_decodificados[i]:
            erros += 1
            
    
    if len(bits_dados) == 0:
        return 0.0
        
    taxa_ber = erros / len(bits_dados)
    return taxa_ber


