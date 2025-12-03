# Simulação de Sistemas de Comunicação Digital (ASK vs BPSK)

Este projeto implementa uma simulação completa de uma cadeia de transmissão digital, comparando duas técnicas de modulação clássicas sob a influência de ruído AWGN (Additive White Gaussian Noise):

1.  **AMI + ASK:** Codificação de Linha *Alternate Mark Inversion* com Modulação por Chaveamento de Amplitude.
2.  **NRZ + BPSK:** Codificação de Linha *Non-Return-to-Zero* com Modulação por Chaveamento de Fase Binária.

O objetivo é visualizar a **Taxa de Erro de Bit (BER)** em função da **Relação Sinal-Ruído (SNR)**.

---

## 📂 Estrutura do Projeto

O projeto é dividido em módulos para facilitar a manutenção e o entendimento:

### 1. `main.py` (Entrada)
É o painel de controle. Aqui você define os parâmetros da simulação (mensagem, voltagem, intervalo de SNR) e executa os testes. **É o único arquivo que você precisa editar para rodar testes diferentes.**

### 2. `benchmark.py` (Análise)
Contém a classe `Benchmark`, que automatiza os testes.
* `validar_sistema`: Roda uma transmissão única para verificar se a mensagem chega legível.
* `gerar_grafico_comparativo`: Roda um loop de simulações variando o ruído, calcula o BER para ASK e BPSK e gera um gráfico comparativo salvo na pasta `images/`.

### 3. `sistema.py` (Orquestrador)
Contém a classe `SistemaComunicacao`. Ela conecta as pontas: pega a mensagem, chama a codificação, modulação, adiciona ruído, demodula e decodifica. É a "placa mãe" da simulação.

### 4. `componentes.py` (Biblioteca)
Contém as funções matemáticas e lógicas de baixo nível:
* Conversão ASCII ↔ Binário.
* Codificadores de linha (AMI, NRZ).
* Moduladores e Demoduladores (ASK, BPSK).
* Canal com ruído AWGN.
* Cálculo de BER.

---

## 🚀 Como Executar

### Pré-requisitos
Você precisará do Python instalado e das bibliotecas `numpy` e `matplotlib`.

```bash
pip install numpy matplotlib
````

### Rodando a Simulação

Basta executar o arquivo principal:

```bash
python main.py
```

Ao executar, o script fará duas coisas automaticamente:

1.  Imprimirá no terminal o resultado de um envio de mensagem simples.
2.  Gerará uma simulação pesada variando o ruído e abrirá uma janela com o gráfico comparativo (além de salvar a imagem em `images/`).

-----

## 🧪 Como Personalizar os Testes

Para alterar os cenários de teste, você deve modificar as variáveis dentro do bloco `if __name__ == '__main__':` no arquivo **`main.py`**.

### Cenário 1: Testar uma mensagem curta e ver se chega correta

Se você quer apenas ver se o sistema está funcionando e decodificando o texto corretamente, altere a **Parte 1** da `main.py`.

**Exemplo:** Quero testar uma mensagem urgente com modulação ASK e Voltagem alta (5V).

```python
# Na main.py, altere as variáveis:
msg_teste = 'SOCORRO URGENTE'
voltagem = 5.0
snr_fixo = 30.0  # SNR alta para garantir que chegue limpo
modulacao = 'ASK' 

# O código executará a validação:
Benchmark.validar_sistema(msg_teste, voltagem, snr_fixo, modulacao)
```

### Cenário 2: Alterar o Gráfico (Intervalo de Teste)

Se você quiser ver como o sistema se comporta em situações de ruído extremo ou muito sutil, altere o `meu_intervalo_snr` na **Parte 2**.

**Exemplo:** Quero um gráfico mais detalhado, indo de 0dB até 10dB, testando de 1 em 1 dB.

```python
# np.arange(inicio, fim, passo)
meu_intervalo_snr = np.arange(0, 11, 1) 

# Nome do arquivo que será salvo
nome_grafico = "Teste_Detalhado_Baixo_SNR"

Benchmark.gerar_grafico_comparativo(
    mensagem=msg_longa,
    voltagem=voltagem,
    intervalo_snr=meu_intervalo_snr,
    titulo=nome_grafico
)
```

### Cenário 3: Testar o impacto da Voltagem

Você pode verificar como aumentar a voltagem melhora a resistência ao ruído.

**Exemplo:** Teste com voltagem baixa (0.5V). O erro deve aumentar consideravelmente.

```python
# Altere a voltagem passada para a função
voltagem_baixa = 0.5

Benchmark.gerar_grafico_comparativo(
    mensagem=msg_longa,
    voltagem=voltagem_baixa, # Passando a nova voltagem
    intervalo_snr=meu_intervalo_snr,
    titulo="Teste_Voltagem_Baixa"
)
```

-----

## 📊 Entendendo os Resultados

1.  **Terminal:** Você verá a mensagem original e a recebida. Se houver caracteres estranhos na mensagem recebida, significa que o ruído corrompeu alguns bits.
2.  **Gráfico (BER x SNR):**
      * **Eixo Y (BER):** É a taxa de erro. Quanto mais baixo, melhor. (Escala Logarítmica).
      * **Eixo X (SNR):** É a qualidade do sinal. Quanto mais alto (para a direita), menos ruído existe.
      * **Conclusão Esperada:** O BPSK (linha azul) geralmente apresenta desempenho melhor (menor erro) que o ASK (linha vermelha) para a mesma quantidade de energia/ruído, devido à maior distância euclidiana entre os símbolos na constelação.