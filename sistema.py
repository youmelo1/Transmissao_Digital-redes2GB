import componentes as comp


class SistemaComunicacao:
    def __init__(self, fonte,voltagem, snr_db):
        self.fonte = fonte
        self.voltagem = voltagem
        self.snr_db = snr_db
        
    def executar(self):
        # Transforma o texto em binario
        bits_dados = comp.ascii_binario(self.fonte)
        
        # Codifica os bits usando AMI
        simbolos_ami = comp.codificacao_AMI(bits_dados)
        
        # Modula o sinal
        sinal_transmitido = comp.modulacao_ASK(simbolos_ami, self.voltagem)
        
        # Adiciona o ruido
        sinal_recebido = comp.canal_com_ruido_AWGN(sinal_transmitido, self.snr_db)
        
        # Demodula o sinal
        simbolos_ami_recuperados = comp.demodulacao_ASK(sinal_recebido, self.voltagem)
        
        # Decodifica os simbolos
        bits_decodificados = comp.decodificacao_AMI(simbolos_ami_recuperados)
        
        #Transforma os bits decodificados em uma string
        texto_final = comp.binario_ascii(bits_decodificados)
        
        # Calcula a taxa de erro de bit
        taxa_ber = comp.calcular_ber(bits_dados, bits_decodificados)
        
        return texto_final, taxa_ber