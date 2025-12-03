import numpy as np
from benchmark import Benchmark

if __name__ == '__main__':

    # ==========================================================================
    # 1. PARTE DE VALIDAÇÃO (Teste Simples)
    # ==========================================================================
    # Objetivo: Verificar se uma mensagem curta chega corretamente com SNR alto.
    
    msg_teste = 'Teste de envio de mensagem'
    voltagem = 1.0
    snr_fixo = 20.0  # dB (alto para garantir pouco erro)
    modulacao = 'BPSK' # Tente trocar por 'ASK' para testar o outro

    # Chama o método estático da classe Benchmark
    Benchmark.validar_sistema(msg_teste, voltagem, snr_fixo, modulacao)


    # ==========================================================================
    # 2. PARTE DE SIMULAÇÃO (Gráfico Comparativo)
    # ==========================================================================
    # Objetivo: Gerar o gráfico de curvas BER vs SNR comparando ASK e BPSK.

    # Configurando o intervalo de SNR (ex: de 0 até 20, pulando de 2 em 2)
    # np.arange(inicio, fim_exclusivo, passo)
    meu_intervalo_snr = np.arange(0, 21, 2) 

    # Mensagem longa para garantir estatística de erro confiável no gráfico
    msg_longa = "Simulacao de Redes de Computadores - Teste de BER. " * 50
    
    # Nome para salvar o arquivo de imagem e usar no título
    nome_grafico = "Comparacao_Final_ASK_vs_BPSK"

    # Chama a função que gera o gráfico e salva na pasta /images
    Benchmark.gerar_grafico_comparativo(
        mensagem=msg_longa,
        voltagem=voltagem,
        intervalo_snr=meu_intervalo_snr,
        titulo=nome_grafico
    )