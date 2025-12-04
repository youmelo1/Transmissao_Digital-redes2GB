# Simulação de Sistemas de Comunicação Digital (ASK vs BPSK)

Este projeto implementa uma simulação completa de uma cadeia de transmissão digital, atendendo aos requisitos da disciplina de Redes de Computadores II. O sistema compara duas técnicas de modulação sob a influência de ruído AWGN (*Additive White Gaussian Noise*):

1.  **AMI + ASK:** Codificação de Linha *Alternate Mark Inversion* com Modulação por Chaveamento de Amplitude.
2.  **NRZ + BPSK:** Codificação de Linha *Non-Return-to-Zero* com Modulação por Chaveamento de Fase Binária.

O objetivo principal é visualizar a **Taxa de Erro de Bit (BER)** em função da **Relação Sinal-Ruído (SNR)** e entender graficamente o comportamento do sinal.

---

## 📂 Estrutura do Projeto

O projeto foi modularizado para garantir clareza e organização:

### 1. `main.py` (Demos Fixas)
Este arquivo contém uma suíte de demonstrações pré-configuradas. Ao ser executado, ele roda sequencialmente três cenários fixos para apresentar o funcionamento do trabalho (envio de texto, geração de gráficos e visualização de ondas).

### 2. `benchmark.py` (Ferramenta de Testes Personalizados)
Contém a classe `Benchmark`. Esta é a ferramenta que você deve utilizar caso queira realizar seus próprios testes com parâmetros personalizados.
* **`validar_sistema(...)`**: Para testar o envio de uma mensagem específica.
* **`gerar_grafico_comparativo(...)`**: Para gerar curvas de BER com intervalos de SNR definidos por você.

### 3. `sistema.py` (Orquestrador)
Contém a classe `SistemaComunicacao`, que conecta as pontas: fonte -> codificação -> modulação -> canal ruidoso -> demodulação -> decodificação.

### 4. `componentes.py` (Biblioteca Física e de Enlace)
Contém as funções matemáticas de baixo nível: conversão binária, codificadores AMI/NRZ, moduladores ASK/BPSK, canal AWGN e cálculo de BER.

---

## 🚀 Como Executar (Modo Demonstração)

Para ver o trabalho em funcionamento com as configurações padrão, basta executar o arquivo principal.

```bash
python main.py
````

Isso iniciará automaticamente as **Demos Fixas**:

1.  **Teste de Texto:** Envia a string *"Engenharia de Telecomunicacoes"* via BPSK a 15dB.
2.  **Curva de Desempenho:** Gera o gráfico BER vs SNR comparando ASK e BPSK (0 a 18 dB).
3.  **Osciloscópio:** Plota as formas de onda elétrica de uma sequência curta de bits.

-----

## 🛠 Como Criar Seus Próprios Testes (Modo Benchmark)

Se você deseja simular cenários específicos (ex: testar se uma mensagem chega com 5V de voltagem ou analisar um intervalo de ruído diferente), você deve utilizar a classe `Benchmark` dentro do seu código (no `main.py` ou em um novo script).

### 1\. Testar uma Mensagem Específica (Single Run)

Use o método `Benchmark.validar_sistema` para verificar se sua mensagem sobrevive a um nível específico de ruído.

```python
from benchmark import Benchmark

# Exemplo: Testando envio crítico com pouca energia (0.5V) e muito ruído (5dB)
Benchmark.validar_sistema(
    mensagem="Teste Personalizado 123", 
    voltagem=0.5, 
    snr_db=5.0, 
    modulacao='BPSK'
)
```

### 2\. Gerar Gráficos Personalizados

Use o método `Benchmark.gerar_grafico_comparativo` para estressar o sistema em um intervalo de SNR definido por você.

```python
import numpy as np
from benchmark import Benchmark

# Exemplo: Gerando gráfico de alta precisão (de 0 a 10dB, passo de 0.5)
meu_intervalo = np.arange(0, 10.5, 0.5)

Benchmark.gerar_grafico_comparativo(
    mensagem="Texto longo para estatistica...",
    voltagem=1.0,
    intervalo_snr=meu_intervalo,
    titulo="Meu_Teste_Personalizado"
)
```

-----

## 📊 Entendendo os Resultados

### 1\. Terminal (Log)

Nos testes de validação, você verá:

  * **Mensagem Original vs Recebida:** Permite ver visualmente se o texto foi corrompido.
  * **BER (Taxa de Erro):** 0.0 significa perfeição. Valores acima de 0 indicam erros.

### 2\. Gráfico BER x SNR (Curva Waterfall)

Este gráfico é gerado pelo Benchmark.

  * **Eixo Y (BER):** Taxa de erro (escala logarítmica).
  * **Eixo X (SNR):** Qualidade do sinal em dB.
  * **Interpretação:** O sistema **BPSK** (linha azul) tende a cair mais rápido (menos erros) do que o **ASK** (linha vermelha) conforme a qualidade do sinal melhora.

### 3\. Visualização de Ondas

Mostra a física do sinal:

  * **ASK:** Varia a amplitude (+V, 0, -V).
  * **BPSK:** Varia a fase (inverte a polaridade +V, -V).