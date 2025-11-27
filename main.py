from sistema import SistemaComunicacao

if __name__ == '__main__':
    fonte = 'Um texto qualquer'
    voltagem = 1.0
    snr_db = 15.0
    
    sistema_comunicacao = SistemaComunicacao(fonte, voltagem, snr_db)
    texto_final, taxa_ber = sistema_comunicacao.executar()
    print(f"Texto Final: {texto_final}")
    print(f"Taxa de Erro de Bit: {taxa_ber}")