import math


class InstanciaCidades:
    def __init__(self, nomeArquivo):
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
        deltaX = cidadeA["posicaoX"] - cidadeB["posicaoX"]
        deltaY = cidadeA["posicaoY"] - cidadeB["posicaoY"]
        return math.hypot(deltaX, deltaY)

    def calcularPermutacoes(self):
        return math.factorial(self.quantidadeCidades)

    def calcularCombinacoes(self):
        return math.comb(self.quantidadeCidades, 2)

    def calcularRotasPossiveis(self):
        return math.factorial(self.quantidadeCidades - 1)


class GrafoRotas:
    def __init__(self, instancia):
        self.instancia = instancia
        quantidade = instancia.quantidadeCidades
        self.matrizAdjacencia = [
            [False for _ in range(quantidade)]
            for _ in range(quantidade)
        ]

    def adicionarConexao(self, cidadeA, cidadeB):
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
        pontos = self.instancia.pontosInteresse
        if partida not in pontos or chegada not in pontos:
            raise ValueError(
                f"Partida e chegada devem estar entre 1 e "
                f"{self.instancia.quantidadeCidades}."
            )

        rotas = []

        def buscar(atual, rota, distanciaTotal):
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
    def __init__(self, nomeArquivo):
        self.cidades = InstanciaCidades(nomeArquivo)
        self.grafo = GrafoRotas(self.cidades)
