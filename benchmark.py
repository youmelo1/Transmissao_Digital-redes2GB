import matplotlib.pyplot as plt
import numpy as np
from sistema import SistemaComunicacao

class Benchmark:
    """
    Classe responsável por executar testes de validação e 
    benchmarks comparativos (geração de gráficos) para o sistema de comunicação.
    """
    
    @staticmethod
    def validar_sistema(mensagem, voltagem, snr_db, modulacao):
        """
        Executa uma simulação única para validar se a mensagem está chegando corretamente.
        """
        print("\n" + "="*60)
        print(f"--- 1. Verificação de Funcionamento ({modulacao}) ---")
        print("="*60)
        
        sistema = SistemaComunicacao(mensagem, voltagem, snr_db, modulacao)
        texto_final, taxa_ber = sistema.executar()
        
        print(f"Mensagem Original: {mensagem}")
        print(f"Mensagem Recebida: {texto_final}")
        print(f"SNR Utilizada:     {snr_db} dB")
        print(f"Taxa de Erro (BER): {taxa_ber:.5f}")
        print("-" * 60)

    @staticmethod
    def gerar_grafico_comparativo(
        mensagem="Simulacao de Redes de Computadores II - Comparacao de Modulacoes. " * 50,  
        voltagem=1.0,                                 
        intervalo_snr=None,
        titulo="Comparação de Modulações"                         
    ):
        """
        Executa a simulação em loop para ASK e BPSK variando o SNR 
        e plota o gráfico de BER vs SNR.
        
        Se intervalo_snr não for passado, usa de 0 a 18 dB com passo 2.
        """
        
        # Define o padrão caso o usuário não passe nada
        if intervalo_snr is None:
            intervalo_snr = np.arange(0, 19, 2)

        print("\n" + "="*60)
        print("--- 2. Iniciando Simulação Comparativa (ASK vs BPSK) ---")
        print(f"Voltagem: {voltagem}V | Tamanho da mensagem: {len(mensagem)*8} bits")
        print("="*60)

        ber_ask = []
        ber_bpsk = []

        for snr in intervalo_snr:
            # Simula ASK
            sis_ask = SistemaComunicacao(mensagem, voltagem, snr, modulacao='ASK')
            _, erro_ask = sis_ask.executar()
            ber_ask.append(erro_ask)

            # Simula BPSK
            sis_bpsk = SistemaComunicacao(mensagem, voltagem, snr, modulacao='BPSK')
            _, erro_bpsk = sis_bpsk.executar()
            ber_bpsk.append(erro_bpsk)

            print(f"SNR: {snr:.1f}dB -> BER ASK: {erro_ask:.4f} | BER BPSK: {erro_bpsk:.4f}")

        # --- GERAÇÃO DO GRÁFICO ---
        print("\nGerando gráfico de resultados...")
        plt.figure(figsize=(10, 6))

        # Eixo X 
        plt.semilogy(intervalo_snr, ber_ask, 'r-o', label='AMI + ASK')
        plt.semilogy(intervalo_snr, ber_bpsk, 'b-s', label='NRZ + BPSK')

        plt.title(f'{titulo} (Voltagem: {voltagem}V)')
        plt.xlabel('SNR (dB)')
        plt.ylabel('Taxa de Erro de Bit (BER)')
        plt.grid(True, which="both", linestyle='--', alpha=0.6)
        plt.legend()

        plt.savefig(f'images/{titulo}.png')
        plt.show()
        print("Concluído.")