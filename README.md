# Simulador de Gerenciamento de Rotas

Um pequeno painel para explorar cidades, criar conexões e descobrir caminhos entre elas.

## O que o programa faz

- Lê cidades e suas coordenadas de um arquivo de instância.
- Calcula as distâncias euclidianas entre cada par de cidades.
- Permite criar conexões entre cidades; cada conexão funciona nos dois sentidos.
- Encontra recursivamente todas as rotas simples entre uma partida e uma chegada. Uma rota simples não passa duas vezes pela mesma cidade.
- Mostra permutações, combinações de pares e o espaço amostral de rotas com partida fixa.

## Como as partes se organizam

- **`main.py` — ponto de partida:** inicia a interface gráfica.
- **`interface.py` — conversa com o usuário:** mostra as cidades, as distâncias e as conexões; permite carregar uma instância, cadastrar conexões e buscar rotas.
- **`simulador.py` — regras e cálculos:**
  - `InstanciaCidades` carrega as coordenadas e calcula distâncias e valores combinatórios.
  - `GrafoRotas` representa as conexões em uma matriz de adjacência e faz a busca recursiva.
  - `Simulador` reúne a instância de cidades e o grafo.
- **`instancia.txt` — dados de exemplo:** a primeira linha informa o número de cidades; as linhas seguintes contêm as coordenadas `x y` de cada uma.

As classes e funções do simulador possuem comentários breves que explicam sua responsabilidade e funcionamento.

> A interface gráfica foi desenvolvida com auxílio de inteligência artificial (IA).

## Para executar

Na pasta deste README, rode:

```bash
python3 main.py
```

Na janela:

1. Confira as cidades e suas distâncias nas abas correspondentes.
2. Em **Conexões e rotas**, selecione duas cidades e clique em **Adicionar conexão**.
3. Escolha a partida e a chegada e clique em **Buscar rotas**.

O programa carrega `instancia.txt` por padrão. Para usar outro arquivo, clique em **Carregar instância** na janela.
