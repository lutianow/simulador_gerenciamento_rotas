import math


class InstanciaCidades:
    """Carrega as cidades de um arquivo e realiza cálculos relacionados a elas."""

    def __init__(self, nomeArquivo):
        """Valida o arquivo e inicializa a quantidade e as coordenadas das cidades."""
        with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        if not linhas:
            raise ValueError("O arquivo de instâncias está vazio.")

        try:
            self.quantidadeCidades = int(linhas[0].strip())
        except ValueError as erro:
            raise ValueError(
                "A primeira linha deve informar a quantidade de cidades."
            ) from erro

        if self.quantidadeCidades < 1:
            raise ValueError("A quantidade de cidades deve ser positiva.")
        if len(linhas[1:]) != self.quantidadeCidades:
            raise ValueError(
                f"O arquivo deve conter as coordenadas de exatamente "
                f"{self.quantidadeCidades} cidades."
            )

        self.listaCidades = self._prepararListaDicionario(linhas[1:])
        self.pontosInteresse = set(range(1, self.quantidadeCidades + 1))

    @staticmethod
    def _prepararListaDicionario(linhas):
        """Converte as linhas de coordenadas em registros com ID e posição."""
        cidades = []
        for identificador, linha in enumerate(linhas, start=1):
            posicoes = linha.split()
            if len(posicoes) != 2:
                raise ValueError(f"As coordenadas da cidade {identificador} são inválidas.")
            try:
                posicaoX, posicaoY = (float(valor) for valor in posicoes)
            except ValueError as erro:
                raise ValueError(
                    f"As coordenadas da cidade {identificador} devem ser numéricas."
                ) from erro

            cidades.append({
                "cidadeID": identificador,
                "posicaoX": posicaoX,
                "posicaoY": posicaoY,
            })
        return cidades

    @staticmethod
    def calcularDistancia(cidadeA, cidadeB):
        """Calcula a distância euclidiana entre duas cidades."""
        deltaX = cidadeA["posicaoX"] - cidadeB["posicaoX"]
        deltaY = cidadeA["posicaoY"] - cidadeB["posicaoY"]
        return math.hypot(deltaX, deltaY)

    def calcularPermutacoes(self):
        """Retorna o número de permutações possíveis das cidades."""
        return math.factorial(self.quantidadeCidades)

    def calcularCombinacoes(self):
        """Retorna o número de combinações de pares de cidades."""
        return math.comb(self.quantidadeCidades, 2)

    def calcularRotasPossiveis(self):
        """Retorna a quantidade teórica de rotas com uma partida fixa."""
        return math.factorial(self.quantidadeCidades - 1)


class GrafoRotas:
    """Representa as conexões entre cidades em uma matriz de adjacência."""

    def __init__(self, instancia):
        """Inicializa um grafo vazio com base na quantidade de cidades."""
        self.instancia = instancia
        quantidade = instancia.quantidadeCidades
        self.matrizAdjacencia = [
            [False for _ in range(quantidade)]
            for _ in range(quantidade)
        ]

    def adicionarConexao(self, cidadeA, cidadeB):
        """Adiciona uma conexão bidirecional entre duas cidades válidas."""
        pontos = self.instancia.pontosInteresse
        if cidadeA not in pontos or cidadeB not in pontos:
            raise ValueError(
                "Os IDs das cidades devem estar entre 1 e "
                f"{self.instancia.quantidadeCidades}."
            )
        if cidadeA == cidadeB:
            raise ValueError("Uma cidade não pode ser conectada a ela mesma.")

        self.matrizAdjacencia[cidadeA - 1][cidadeB - 1] = True
        self.matrizAdjacencia[cidadeB - 1][cidadeA - 1] = True

    def buscarRotas(self, partida, chegada):
        """Busca todas as rotas simples possíveis entre partida e chegada."""
        pontos = self.instancia.pontosInteresse
        if partida not in pontos or chegada not in pontos:
            raise ValueError(
                f"Partida e chegada devem estar entre 1 e "
                f"{self.instancia.quantidadeCidades}."
            )

        rotas = []

        def buscar(atual, rota, distanciaTotal):
            """Percorre recursivamente o grafo e acumula os caminhos encontrados."""
            if atual == chegada:
                rotas.append((rota.copy(), distanciaTotal))
                return

            for indice, conectado in enumerate(self.matrizAdjacencia[atual - 1]):
                proximaCidade = indice + 1
                if conectado and proximaCidade not in rota:
                    cidadeAtual = self.instancia.listaCidades[atual - 1]
                    cidadeSeguinte = self.instancia.listaCidades[proximaCidade - 1]
                    distanciaTrecho = self.instancia.calcularDistancia(
                        cidadeAtual, cidadeSeguinte
                    )
                    buscar(
                        proximaCidade,
                        rota + [proximaCidade],
                        distanciaTotal + distanciaTrecho,
                    )

        buscar(partida, [partida], 0.0)
        return rotas


class Simulador:
    """Reúne os dados das cidades e o grafo usado nas rotas."""

    def __init__(self, nomeArquivo):
        """Cria a instância das cidades e o grafo associado."""
        self.cidades = InstanciaCidades(nomeArquivo)
        self.grafo = GrafoRotas(self.cidades)
