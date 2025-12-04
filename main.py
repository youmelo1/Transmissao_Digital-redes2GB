import matplotlib.pyplot as plt
import numpy as np
import time
from sistema import SistemaComunicacao
import componentes as comp

def demo_texto_simples():
    """Teste rápido para ver se o texto chega legível."""
    print("\n--- 1. Teste de Envio de Texto (BPSK @ 15dB) ---")
    mensagem = "Engenharia de Telecomunicacoes"
    
    # SNR de 15dB é razoavelmente limpo
    sis = SistemaComunicacao(mensagem, voltagem=1.0, snr_db=15.0, modulacao='BPSK')
    texto_rec, ber = sis.executar()
    
    print(f"Enviado:  {mensagem}")
    print(f"Recebido: {texto_rec}")
    print(f"Taxa de Erro (BER): {ber:.4f}")
    print("-" * 50)

def demo_grafico_ber():
    """Gera o gráfico comparativo clássico: Curva Waterfall."""
    print("\n--- 2. Gerando Curva de Desempenho (ASK vs BPSK) ---")
    print("Simulando várias intensidades de ruído...")
    
    texto_longo = "Simulacao de dados para estatistica de erro. " * 50
    snrs = np.arange(0, 19, 2) # De 0 a 18 dB
    
    ber_ask = []
    ber_bpsk = []

    for snr in snrs:
        # Teste ASK
        sis_ask = SistemaComunicacao(texto_longo, 1.0, snr, 'ASK')
        ber_ask.append(sis_ask.executar()[1])
        
        # Teste BPSK
        sis_bpsk = SistemaComunicacao(texto_longo, 1.0, snr, 'BPSK')
        ber_bpsk.append(sis_bpsk.executar()[1])
        print(f".", end="", flush=True) # Barra de progresso visual

    plt.figure(figsize=(10, 6))
    plt.semilogy(snrs, ber_ask, 'r-o', label='ASK (Amplitude)')
    plt.semilogy(snrs, ber_bpsk, 'b-s', label='BPSK (Fase)')
    plt.title('Comparação de Robustez: ASK vs BPSK')
    plt.xlabel('SNR (dB) - Relação Sinal-Ruído')
    plt.ylabel('BER (Taxa de Erro de Bit)')
    plt.grid(True, which="both", linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    print("\nGráfico gerado (feche a janela do gráfico para continuar).")
    plt.show()

def demo_visualizacao_ondas():
    """Mostra como o sinal elétrico se parece e o histograma do ruído."""
    print("\n--- 3. Visualização dos Sinais Elétricos ---")
    
    bits = [1, 0, 1, 1, 0, 0, 1, 0] # Sequência curta para visualizar
    voltagem = 1.0
    
    # Gerar sinais puros
    sinal_ask = comp.modulacao_ASK(comp.codificacao_AMI(bits), voltagem)
    sinal_bpsk = comp.modulacao_BPSK(comp.codificacao_NRZ(bits), voltagem)
    
    plt.figure(figsize=(12, 5))
    
    # Plot das Ondas
    plt.step(range(len(sinal_ask)), sinal_ask, where='mid', label='ASK (3 Níveis)', color='red', linewidth=2)
    plt.step(range(len(sinal_bpsk)), sinal_bpsk, where='mid', label='BPSK (2 Níveis)', color='blue', linestyle='--', linewidth=2)
    plt.title(f'Forma de Onda dos Bits: {bits}')
    plt.yticks([-1, 0, 1])
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print("Gráfico de ondas gerado.")
    plt.show()

if __name__ == "__main__":
    demo_texto_simples()
    demo_grafico_ber()
    demo_visualizacao_ondas()