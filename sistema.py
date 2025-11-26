import numpy as np

def ascii_binario(texto: str):
    """
    Recebe: Um texto em ASCII.
    Faz: Converte o texto em binário.
    Retorna: Uma lista de 0s e 1s.
    """
    return list(''.join(format(ord(c), '08b') for c in texto))


# --- PASSO 2: O Entregador Local (Adiciona redundância/formato) ---
def codificacao_AMI(bits_entrada):
    """
    Recebe: Lista de bits originais (ex: [0, 1, 0, 1]).
    Faz: Aplica AMI Bipolar.
         - Bit 0 -> Vira nível 0.
         - Bit 1 -> Vira nível +1 ou -1 (alternando a cada ocorrência).
    Retorna: Lista de símbolos codificados (ex: [0, +1, 0, -1]).
             O tamanho da lista é IGUAL ao da original.
    """
    
    bits_codificados = []
    occorrencias = 0
    for bit in bits_entrada:
        if bit == 0:
            bits_codificados.append(0)
        else:
            if occorrencias % 2 == 0:
                bits_codificados.append(1)
            else:
                bits_codificados.append(-1)
            occorrencias += 1
    
    return bits_codificados

# --- PASSO 3: O Pombo Correio (Transforma bits em símbolos) ---
def modulacao_ask(bits_codificados, voltagem=1.0):
    """
    Recebe: Lista de bits codificados (do AMI) e a voltagem desejada.
    Faz: Implementa ASK (Amplitude Shift Keying).
         Multiplica o sinal de entrada pela voltagem (ex: 1 -> 5V, 0 -> 0V).
    Retorna: Array numpy de símbolos modulados em amplitude.
    """
    
    # Garante que é array para permitir multiplicação vetorial
    sinal = np.array(bits_codificados)
    
    # A "Mágica": Modula a amplitude (Símbolo * Amplitude)
    sinal_tx = sinal * voltagem
    
    return sinal_tx
    

# --- PASSO 4: O Nevoeiro (Adiciona Ruído AWGN) ---
def canal_com_ruido(sinal_tx, snr_db):
    """
    Recebe: Array de símbolos transmitidos e a SNR desejada em dB.
    Faz: Calcula a potência do sinal, converte SNR, gera ruído aleatório
         (np.random.normal) e soma ao sinal.
    Retorna: Array de símbolos com ruído (sinal_rx).
    """
    pass

# --- PASSO 5: O Receptor (Interpreta o símbolo sujo) ---
def demodulacao_ask(sinal_rx, voltagem=1.0):
    """
    Recebe: Array de símbolos ruidosos (ASK) e a voltagem utilizada.
    Faz: Recupera os dados ASK normalizando o sinal e aplicando limiares.
         Remove a voltagem para voltar aos níveis lógicos originais (-1, 0, 1).
    Retorna: Array numpy de bits recuperados/estimados.
    """
    
    # 1. Remove a amplificação (Normalização)
    sinal_normalizado = sinal_rx / voltagem
    
    bits_recuperados = []
    for valor in sinal_normalizado:
        # Lógica de Decisão (Limiar)
        # Como temos 0, 1 e -1, os "muros" ficam em 0.5 e -0.5
        
        if valor > 0.5:
            bits_recuperados.append(1)   # Era +1
        elif valor < -0.5:
            bits_recuperados.append(-1)  # Era -1
        else:
            bits_recuperados.append(0)   # Era 0 (está entre -0.5 e 0.5)
            
    return np.array(bits_recuperados)

# --- PASSO 6: Tradutor do Entregador (Remove a redundância) ---
def decodificacao_AMI(simbolos_demodulados):
    """
    Recebe: Lista de símbolos vindos do demodulador (ex: [0, 1, 0, -1]).
    Faz: Reverte o AMI.
         - Se o valor for 0 -> É bit 0.
         - Se o valor for diferente de 0 (independente do sinal) -> É bit 1.
    Retorna: Lista de bits de dados (0s e 1s).
    """
    pass

# --- PASSO 7: O Destino (Volta para Texto) ---
def binario_ascii(bits_dados):
    """
    Recebe: Lista de bits decodificados (0s e 1s).
    Faz: Agrupa de 8 em 8, converte para int, e depois para char (chr()).
    Retorna: String com a mensagem final (ex: 'Oi').
    """
    
    # 1. "Cola" a lista de bits numa string única ("01001...")
    bits_string = "".join(bits_dados)
    
    # 2. Converte tudo de uma vez (igual mostrei antes)
    return int(bits_string, 2).to_bytes(len(bits_string) // 8, 'big').decode('ascii')

# --- PASSO 8: O Analista (Cálculo de Erros) ---
def calcular_ber(bits_enviados, bits_recebidos):
    """
    Recebe: Lista original (da Fonte) e Lista final (do Destino).
    Faz: Compara posição por posição e conta quantos são diferentes.
         Fórmula: Erros / Total.
    Retorna: Valor float (ex: 0.005 para 0.5% de erro).
    """
    pass