import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from simulador import Simulador


class InterfaceRotas(tk.Tk):
    """Exibe a interface gráfica e conecta os controles às regras do simulador."""

    def __init__(self, arquivoInstancia):
        """Inicializa o simulador e monta os componentes visuais da janela."""
        super().__init__()
        self.simulador = Simulador(arquivoInstancia)
        self.cidades = self.simulador.cidades
        self.grafo = self.simulador.grafo
        self.title("Simulador de Gerenciamento de Rotas")
        self.geometry("960x680")
        self.minsize(800, 560)

        self._criarInterface()
        self._atualizarDados()

    def _criarInterface(self):
        """Cria o cabeçalho, as abas e as tabelas da janela."""
        cabecalho = ttk.Frame(self, padding=(12, 12, 12, 4))
        cabecalho.pack(fill="x")

        ttk.Label(
            cabecalho,
            text="Simulador de Gerenciamento de Rotas",
            font=("", 16, "bold"),
        ).pack(side="left")
        ttk.Button(
            cabecalho,
            text="Carregar instância",
            command=self._selecionarInstancia,
        ).pack(side="right")

        self.estatisticas = tk.StringVar()
        ttk.Label(
            self,
            textvariable=self.estatisticas,
            padding=(12, 4, 12, 10),
        ).pack(fill="x")

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        cidades = ttk.Frame(abas, padding=10)
        distancias = ttk.Frame(abas, padding=10)
        rotas = ttk.Frame(abas, padding=10)
        abas.add(cidades, text="Cidades")
        abas.add(distancias, text="Distâncias")
        abas.add(rotas, text="Conexões e rotas")

        self.tabelaCidades = self._criarTabela(
            cidades,
            (("id", "ID", 80), ("x", "Coordenada X", 180), ("y", "Coordenada Y", 180)),
        )
        self.tabelaDistancias = self._criarTabela(
            distancias,
            (
                ("origem", "Cidade", 150),
                ("destino", "Outra cidade", 150),
                ("distancia", "Distância euclidiana", 220),
            ),
        )

        self._criarAbaRotas(rotas)

    def _criarTabela(self, pai, colunas):
        """Cria e configura uma tabela com barras de rolagem."""
        tabela = ttk.Treeview(
            pai,
            columns=tuple(coluna[0] for coluna in colunas),
            show="headings",
        )
        for identificador, titulo, largura in colunas:
            tabela.heading(identificador, text=titulo)
            tabela.column(identificador, width=largura, anchor="center")

        barra = ttk.Scrollbar(pai, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabela

    def _criarAbaRotas(self, pai):
        """Monta os controles para conexões, busca e exibição de rotas."""
        conexao = ttk.LabelFrame(pai, text="Criar conexão entre cidades", padding=10)
        conexao.pack(fill="x")

        ttk.Label(conexao, text="Cidade A:").pack(side="left")
        self.cidadeA = ttk.Combobox(conexao, state="readonly", width=10)
        self.cidadeA.pack(side="left", padx=(6, 14))

        ttk.Label(conexao, text="Cidade B:").pack(side="left")
        self.cidadeB = ttk.Combobox(conexao, state="readonly", width=10)
        self.cidadeB.pack(side="left", padx=(6, 14))

        ttk.Button(
            conexao,
            text="Adicionar conexão",
            command=self._adicionarConexao,
        ).pack(side="left")

        conexoes = ttk.LabelFrame(pai, text="Conexões cadastradas", padding=8)
        conexoes.pack(fill="x", pady=(10, 0))
        self.tabelaConexoes = self._criarTabela(
            conexoes,
            (
                ("cidadeA", "Cidade A", 130),
                ("cidadeB", "Cidade B", 130),
                ("distancia", "Distância", 160),
            ),
        )
        self.tabelaConexoes.configure(height=5)

        busca = ttk.LabelFrame(pai, text="Encontrar rotas", padding=10)
        busca.pack(fill="x", pady=(10, 0))

        ttk.Label(busca, text="Partida:").pack(side="left")
        self.partida = ttk.Combobox(busca, state="readonly", width=10)
        self.partida.pack(side="left", padx=(6, 14))

        ttk.Label(busca, text="Chegada:").pack(side="left")
        self.chegada = ttk.Combobox(busca, state="readonly", width=10)
        self.chegada.pack(side="left", padx=(6, 14))

        ttk.Button(
            busca,
            text="Buscar rotas",
            command=self._buscarRotas,
        ).pack(side="left")

        resultados = ttk.LabelFrame(pai, text="Rotas encontradas", padding=8)
        resultados.pack(fill="both", expand=True, pady=(10, 0))
        self.resultados = tk.Text(resultados, height=8, wrap="word", state="disabled")
        barra = ttk.Scrollbar(resultados, orient="vertical", command=self.resultados.yview)
        self.resultados.configure(yscrollcommand=barra.set)
        self.resultados.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    def _atualizarDados(self):
        """Atualiza estatísticas, listas de cidades, distâncias e conexões."""
        ids = [str(cidade) for cidade in sorted(self.cidades.pontosInteresse)]
        for seletor in (self.cidadeA, self.cidadeB, self.partida, self.chegada):
            seletor["values"] = ids
            if ids and seletor.get() not in ids:
                seletor.set(ids[0])

        self.estatisticas.set(
            f"Cidades: {self.cidades.quantidadeCidades}    |    "
            f"Permutações (n!): {self.cidades.calcularPermutacoes()}    |    "
            f"Combinações C(n, 2): {self.cidades.calcularCombinacoes()}    |    "
            f"Rotas com partida fixa ((n-1)!): "
            f"{self.cidades.calcularRotasPossiveis()}"
        )

        self._limparTabela(self.tabelaCidades)
        for cidade in self.cidades.listaCidades:
            self.tabelaCidades.insert(
                "",
                "end",
                values=(
                    cidade["cidadeID"],
                    f'{cidade["posicaoX"]:g}',
                    f'{cidade["posicaoY"]:g}',
                ),
            )

        self._limparTabela(self.tabelaDistancias)
        for indiceA, cidadeA in enumerate(self.cidades.listaCidades):
            for cidadeB in self.cidades.listaCidades[indiceA + 1:]:
                distancia = self.cidades.calcularDistancia(cidadeA, cidadeB)
                self.tabelaDistancias.insert(
                    "",
                    "end",
                    values=(
                        cidadeA["cidadeID"],
                        cidadeB["cidadeID"],
                        f"{distancia:.2f}",
                    ),
                )

        self._atualizarConexoes()
        self._definirResultados("")

    @staticmethod
    def _limparTabela(tabela):
        """Remove todas as linhas atualmente exibidas em uma tabela."""
        tabela.delete(*tabela.get_children())

    def _atualizarConexoes(self):
        """Atualiza a tabela com as conexões cadastradas no grafo."""
        self._limparTabela(self.tabelaConexoes)
        for indiceA in range(self.cidades.quantidadeCidades):
            for indiceB in range(indiceA + 1, self.cidades.quantidadeCidades):
                if self.grafo.matrizAdjacencia[indiceA][indiceB]:
                    cidadeA = self.cidades.listaCidades[indiceA]
                    cidadeB = self.cidades.listaCidades[indiceB]
                    distancia = self.cidades.calcularDistancia(cidadeA, cidadeB)
                    self.tabelaConexoes.insert(
                        "",
                        "end",
                        values=(indiceA + 1, indiceB + 1, f"{distancia:.2f}"),
                    )

    def _adicionarConexao(self):
        """Lê as cidades selecionadas e tenta cadastrar uma conexão."""
        try:
            cidadeA = int(self.cidadeA.get())
            cidadeB = int(self.cidadeB.get())
            if self.grafo.matrizAdjacencia[cidadeA - 1][cidadeB - 1]:
                messagebox.showinfo("Conexão existente", "Essas cidades já estão conectadas.")
                return
            self.grafo.adicionarConexao(cidadeA, cidadeB)
        except (ValueError, IndexError) as erro:
            messagebox.showwarning("Conexão inválida", str(erro))
            return

        self._atualizarConexoes()
        self._definirResultados("")

    def _buscarRotas(self):
        """Obtém a partida e a chegada e mostra as rotas encontradas."""
        try:
            partida = int(self.partida.get())
            chegada = int(self.chegada.get())
            rotas = self.grafo.buscarRotas(partida, chegada)
        except (ValueError, IndexError) as erro:
            messagebox.showwarning("Entrada inválida", str(erro))
            return

        if not rotas:
            self._definirResultados(f"Nenhuma rota encontrada de {partida} até {chegada}.")
            return

        linhas = [f"Rotas de {partida} até {chegada}:\n"]
        for rota, distancia in rotas:
            caminho = " -> ".join(str(cidade) for cidade in rota)
            linhas.append(f"{caminho}  (distância: {distancia:.2f})")
        linhas.append(f"\nTotal de rotas encontradas: {len(rotas)}")
        self._definirResultados("\n".join(linhas))

    def _definirResultados(self, texto):
        """Atualiza o texto da área de resultados da interface."""
        self.resultados.configure(state="normal")
        self.resultados.delete("1.0", "end")
        self.resultados.insert("1.0", texto)
        self.resultados.configure(state="disabled")

    def _selecionarInstancia(self):
        """Abre o seletor de arquivo e recarrega uma nova instância."""
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo de instâncias",
            filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")),
        )
        if not caminho:
            return

        try:
            novoSimulador = Simulador(caminho)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Erro ao carregar instância", str(erro))
            return

        self.simulador = novoSimulador
        self.cidades = novoSimulador.cidades
        self.grafo = novoSimulador.grafo
        self._atualizarDados()


def main():
    """Cria a interface padrão ou mostra um erro caso ela não possa iniciar."""
    arquivoInstancia = Path(__file__).with_name("instancia.txt")
    try:
        interface = InterfaceRotas(arquivoInstancia)
    except (OSError, ValueError) as erro:
        janela = tk.Tk()
        janela.withdraw()
        messagebox.showerror("Erro ao iniciar", str(erro))
        janela.destroy()
        return

    interface.mainloop()


if __name__ == "__main__":
    main()
