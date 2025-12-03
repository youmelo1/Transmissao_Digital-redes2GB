import componentes as comp

class SistemaComunicacao:
    def __init__(self, fonte, voltagem, snr_db, modulacao):
        self.fonte = fonte
        self.voltagem = voltagem
        self.snr_db = snr_db
        self.modulacao = modulacao

    def executar(self):
        # Transforma o texto em binario
        bits_dados = comp.ascii_binario(self.fonte)

        # --- ETAPA DE TRANSMISSÃO ---
        if self.modulacao == 'ASK':
            # Rota 1: Codifica os bits usando AMI (Ideal para ASK)
            simbolos = comp.codificacao_AMI(bits_dados)
            # Modula o sinal usando ASK
            sinal_transmitido = comp.modulacao_ASK(simbolos, self.voltagem)

        elif self.modulacao == 'BPSK':
            # Rota 2: Codifica os bits usando NRZ (Ideal para BPSK)
            simbolos = comp.codificacao_NRZ(bits_dados)
            # Modula o sinal usando BPSK
            sinal_transmitido = comp.modulacao_BPSK(simbolos, self.voltagem)

        else:
            raise ValueError('Modulação inválida. Escolha ASK ou BPSK.')

        # --- ETAPA DE CANAL ---
        # Adiciona o ruido
        sinal_recebido = comp.canal_com_ruido_AWGN(sinal_transmitido, self.snr_db)

        # --- ETAPA DE RECEPÇÃO ---
        if self.modulacao == 'ASK':
            # Demodula o sinal ASK
            simbolos_recuperados = comp.demodulacao_ASK(sinal_recebido, self.voltagem)
            # Decodifica os simbolos AMI
            bits_decodificados = comp.decodificacao_AMI(simbolos_recuperados)

        elif self.modulacao == 'BPSK':
            # Demodula o sinal BPSK
            simbolos_recuperados = comp.demodulacao_BPSK(sinal_recebido, self.voltagem)
            # Decodifica os simbolos NRZ
            bits_decodificados = comp.decodificacao_NRZ(simbolos_recuperados)

        #Transforma os bits decodificados em uma string
        texto_final = comp.binario_ascii(bits_decodificados)

        # Calcula a taxa de erro de bit
        taxa_ber = comp.calcular_ber(bits_dados, bits_decodificados)

        return texto_final, taxa_ber