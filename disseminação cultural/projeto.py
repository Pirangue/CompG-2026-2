"""
Simulador de disseminação cultural em uma matriz 9x9.

Cada indivíduo possui seis genes:
família, sexo, período, curso, religião e origem.

A população evolui por seleção, cruzamento e mutação.
A função de aptidão favorece indivíduos com características
menos frequentes, especialmente período e curso.
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk
from typing import ClassVar


# ============================================================
# Configurações gerais
# ============================================================

TAMANHO_MATRIZ = 9
TAMANHO_POPULACAO = TAMANHO_MATRIZ * TAMANHO_MATRIZ

SEXOS = (
    "Feminino",
    "Masculino",
    "Não binário",
)

PERIODOS = (
    "1º período",
    "2º período",
    "3º período",
    "4º período",
    "5º período",
)

CURSOS = (
    "Computação",
    "Administração",
    "Direito",
    "Engenharia",
    "Psicologia",
)

RELIGIOES = (
    "Católica",
    "Evangélica",
    "Espírita",
    "Umbanda",
    "Sem religião",
)

ORIGENS = (
    "Norte",
    "Nordeste",
    "Centro-Oeste",
    "Sudeste",
    "Sul",
)

CORES_CURSOS = {
    "Computação": "#3b82f6",
    "Administração": "#10b981",
    "Direito": "#f97316",
    "Engenharia": "#8b5cf6",
    "Psicologia": "#ec4899",
}

TEMAS = {
    "Claro": {
        "fundo": "#f1f5f9",
        "cartao": "#ffffff",
        "texto": "#172033",
        "secundario": "#64748b",
        "borda": "#dbe3ec",
        "canvas": "#f8fafc",
        "sombra": "#cbd5e1",
        "selecionado": "#111827",
    },
    "Escuro": {
        "fundo": "#111827",
        "cartao": "#1f2937",
        "texto": "#f8fafc",
        "secundario": "#cbd5e1",
        "borda": "#374151",
        "canvas": "#172033",
        "sombra": "#0f172a",
        "selecionado": "#ffffff",
    },
}


# ============================================================
# Modelo de dados
# ============================================================

@dataclass
class Individuo:
    """Representa um indivíduo e seus genes culturais."""

    numero: int
    familia: str
    sexo: str
    periodo: str
    curso: str
    religiao: str
    origem: str
    lider: bool = False

    def genes(self) -> tuple[str, ...]:
        return (
            self.familia,
            self.sexo,
            self.periodo,
            self.curso,
            self.religiao,
            self.origem,
        )


# ============================================================
# Algoritmo genético
# ============================================================

class AlgoritmoGenetico:
    """Gerencia a criação e a evolução da população."""

    _numero_global: ClassVar[int] = 0

    def __init__(
        self,
        quantidade_familias: int = 5,
        taxa_mutacao: float = 0.12,
        taxa_influencia: float = 0.45,
    ) -> None:
        self.quantidade_familias = quantidade_familias
        self.taxa_mutacao = taxa_mutacao
        self.taxa_influencia = taxa_influencia
        self.familias = tuple(
            f"Família {numero}"
            for numero in range(1, quantidade_familias + 1)
        )
        self.geracao = 0
        self.posicao_lider = random.randrange(TAMANHO_POPULACAO)
        self.populacao = self.criar_populacao()

    @classmethod
    def novo_numero(cls) -> int:
        cls._numero_global += 1
        return cls._numero_global

    def novo_individuo(self) -> Individuo:
        return Individuo(
            numero=self.novo_numero(),
            familia=random.choice(self.familias),
            sexo=random.choice(SEXOS),
            periodo=random.choice(PERIODOS),
            curso=random.choice(CURSOS),
            religiao=random.choice(RELIGIOES),
            origem=random.choice(ORIGENS),
        )

    def criar_populacao(self) -> list[Individuo]:
        self.geracao = 0
        populacao = [
            self.novo_individuo()
            for _ in range(TAMANHO_POPULACAO)
        ]
        populacao[self.posicao_lider].lider = True
        return populacao

    @staticmethod
    def contagem(
        populacao: list[Individuo],
        atributo: str,
    ) -> dict[str, int]:
        resultado: dict[str, int] = {}
        for individuo in populacao:
            valor = getattr(individuo, atributo)
            resultado[valor] = resultado.get(valor, 0) + 1
        return resultado

    def aptidao(self, individuo: Individuo) -> float:
        """Favorece genes raros; período e curso têm maior peso."""
        pesos = {
            "familia": 1.0,
            "sexo": 0.5,
            "periodo": 4.0,
            "curso": 4.0,
            "religiao": 0.5,
            "origem": 0.5,
        }
        pontuacao = 0.0
        for atributo, peso in pesos.items():
            frequencias = self.contagem(self.populacao, atributo)
            valor = getattr(individuo, atributo)
            pontuacao += peso / frequencias.get(valor, 1)
        return pontuacao

    def cruzar(self, primeiro: Individuo, segundo: Individuo) -> Individuo:
        genes_a = primeiro.genes()
        genes_b = segundo.genes()
        genes = [
            random.choice((genes_a[i], genes_b[i]))
            for i in range(len(genes_a))
        ]
        filho = Individuo(
            numero=self.novo_numero(),
            familia=genes[0],
            sexo=genes[1],
            periodo=genes[2],
            curso=genes[3],
            religiao=genes[4],
            origem=genes[5],
        )
        return self.mutar(filho)

    def mutar(self, individuo: Individuo) -> Individuo:
        """Aplica mutação independente em cada gene."""
        possibilidades = {
            "familia": self.familias,
            "sexo": SEXOS,
            "periodo": PERIODOS,
            "curso": CURSOS,
            "religiao": RELIGIOES,
            "origem": ORIGENS,
        }
        for atributo, opcoes in possibilidades.items():
            if random.random() < self.taxa_mutacao:
                setattr(individuo, atributo, random.choice(opcoes))
        return individuo

    def vizinhos_do_lider(self) -> list[int]:
        """Posições vizinhas ao líder (laterais, acima, abaixo e diagonais)."""
        linha_lider, coluna_lider = divmod(self.posicao_lider, TAMANHO_MATRIZ)
        vizinhos = []
        for d_linha in (-1, 0, 1):
            for d_coluna in (-1, 0, 1):
                if d_linha == 0 and d_coluna == 0:
                    continue
                linha = linha_lider + d_linha
                coluna = coluna_lider + d_coluna
                if 0 <= linha < TAMANHO_MATRIZ and 0 <= coluna < TAMANHO_MATRIZ:
                    vizinhos.append(linha * TAMANHO_MATRIZ + coluna)
        return vizinhos

    def influenciar_vizinhos(self) -> None:
        """Cada gene do vizinho pode ser substituído pelo gene do líder."""
        lider = self.populacao[self.posicao_lider]
        atributos = ("familia", "sexo", "periodo", "curso", "religiao", "origem")
        for posicao in self.vizinhos_do_lider():
            vizinho = self.populacao[posicao]
            for atributo in atributos:
                if random.random() < self.taxa_influencia:
                    setattr(vizinho, atributo, getattr(lider, atributo))

    def evoluir(self) -> None:
        """Aplica a influência do líder e cria uma nova geração."""
        self.influenciar_vizinhos()

        lider_atual = self.populacao[self.posicao_lider]

        ordenados = sorted(self.populacao, key=self.aptidao, reverse=True)
        elite = ordenados[: max(2, TAMANHO_POPULACAO // 5)]

        # Preserva os melhores indivíduos que não sejam o líder.
        nova_populacao = [p for p in elite if not p.lider][:2]

        # Reserva uma vaga para o líder.
        while len(nova_populacao) < TAMANHO_POPULACAO - 1:
            primeiro, segundo = random.sample(elite, 2)
            nova_populacao.append(self.cruzar(primeiro, segundo))

        # O líder volta exatamente à sua posição original.
        nova_populacao.insert(self.posicao_lider, lider_atual)

        self.populacao = nova_populacao
        self.geracao += 1

    def diversidade(self, atributo: str) -> int:
        return len({getattr(i, atributo) for i in self.populacao})

    def aptidao_media(self) -> float:
        if not self.populacao:
            return 0.0
        return sum(self.aptidao(i) for i in self.populacao) / len(self.populacao)


# ============================================================
# Interface gráfica
# ============================================================

class Aplicacao:
    """Interface gráfica principal do simulador."""

    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.raiz.title("Disseminação cultural")
        self.raiz.geometry("1280x820")
        self.raiz.minsize(980, 680)

        self.tema = "Claro"
        self.estilo = ttk.Style(self.raiz)

        self.familias_var = tk.IntVar(value=5)
        self.geracoes_var = tk.IntVar(value=10)
        self.mutacao_var = tk.DoubleVar(value=12)
        self.tema_var = tk.StringVar(value=self.tema)
        self.influencia_var = tk.DoubleVar(value=45)

        self.geracao_var = tk.StringVar()
        self.populacao_var = tk.StringVar()
        self.aptidao_var = tk.StringVar()
        self.diversidade_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.algoritmo = AlgoritmoGenetico(
            quantidade_familias=self.familias_var.get(),
            taxa_mutacao=self.mutacao_var.get() / 100,
            taxa_influencia=self.influencia_var.get() / 100,
        )

        self.individuo_selecionado: Individuo | None = None
        self.automacao_id: str | None = None
        self.alvo_automacao: int | None = None
        self.itens_matriz: list[int] = []

        self._configurar_estilo()
        self._montar_interface()
        self._aplicar_tema()
        self._atualizar_interface()

        self.raiz.protocol(
            "WM_DELETE_WINDOW",
            self._encerrar,
        )

    # --------------------------------------------------------
    # Configuração visual
    # --------------------------------------------------------

    def _configurar_estilo(self) -> None:
        self.estilo.theme_use("clam")

        self.estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 22, "bold"),
        )

        self.estilo.configure(
            "Subtitulo.TLabel",
            font=("Segoe UI", 10),
        )

        self.estilo.configure(
            "Card.TLabelframe",
            padding=12,
        )

        self.estilo.configure(
            "Card.TLabelframe.Label",
            font=("Segoe UI", 10, "bold"),
        )

        self.estilo.configure(
            "Acao.TButton",
            padding=(12, 7),
            font=("Segoe UI", 9, "bold"),
        )

    def _montar_interface(self) -> None:
        principal = ttk.Frame(self.raiz, padding=20)
        principal.pack(fill="both", expand=True)

        principal.columnconfigure(0, weight=1)
        principal.rowconfigure(2, weight=1)

        cabecalho = ttk.Frame(principal)
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        ttk.Label(
            cabecalho,
            text="Disseminação cultural",
            style="Titulo.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            cabecalho,
            text=(
                "Observe a distribuição dos indivíduos, explore seus genes "
                "e acompanhe a evolução da população."
            ),
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        self._montar_configuracoes(principal)

        conteudo = ttk.PanedWindow(
            principal,
            orient="horizontal",
        )
        conteudo.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        area_matriz = ttk.Frame(conteudo)
        area_painel = ttk.Frame(conteudo)

        conteudo.add(area_matriz, weight=4)
        conteudo.add(area_painel, weight=1)

        self._montar_matriz(area_matriz)
        self._montar_painel(area_painel)

        self._montar_controles(principal)
        self._montar_legenda(principal)

    def _montar_configuracoes(
        self,
        parent: ttk.Frame,
    ) -> None:
        configuracoes = ttk.LabelFrame(
            parent,
            text="Configurações da simulação",
            style="Card.TLabelframe",
        )
        configuracoes.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 16),
        )

        for coluna in range(8):
            configuracoes.columnconfigure(coluna, weight=0)

        ttk.Label(
            configuracoes,
            text="Famílias",
        ).grid(row=0, column=0, sticky="w")

        ttk.Spinbox(
            configuracoes,
            from_=1,
            to=20,
            width=6,
            textvariable=self.familias_var,
        ).grid(row=0, column=1, padx=(6, 18))

        ttk.Label(
            configuracoes,
            text="Gerações",
        ).grid(row=0, column=2, sticky="w")

        ttk.Spinbox(
            configuracoes,
            from_=1,
            to=10000,
            width=7,
            textvariable=self.geracoes_var,
        ).grid(row=0, column=3, padx=(6, 18))

        ttk.Label(
            configuracoes,
            text="Mutação (%)",
        ).grid(row=0, column=4, sticky="w")

        ttk.Spinbox(
            configuracoes,
            from_=0,
            to=100,
            increment=1,
            width=7,
            textvariable=self.mutacao_var,
        ).grid(row=0, column=5, padx=(6, 18))

        ttk.Label(
            configuracoes,
            text="Tema",
        ).grid(row=0, column=6, sticky="w")

        ttk.Combobox(
            configuracoes,
            textvariable=self.tema_var,
            values=tuple(TEMAS),
            state="readonly",
            width=10,
        ).grid(row=0, column=7, padx=(6, 12))

        ttk.Button(
            configuracoes,
            text="Aplicar",
            style="Acao.TButton",
            command=self.aplicar_configuracoes,
        ).grid(row=0, column=8)

        ttk.Label(
            configuracoes,
            text="Influência (%)",
        ).grid(row=1, column=0, sticky="w", pady=(10, 0))

        ttk.Spinbox(
            configuracoes,
            from_=0,
            to=100,
            increment=1,
            width=7,
            textvariable=self.influencia_var,
        ).grid(row=1, column=1, padx=(6, 18), pady=(10, 0))

    def _montar_matriz(self, parent: ttk.Frame) -> None:
        moldura = ttk.LabelFrame(
            parent,
            text="População",
            style="Card.TLabelframe",
        )
        moldura.pack(fill="both", expand=True)

        moldura.rowconfigure(0, weight=1)
        moldura.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            moldura,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        barra_vertical = ttk.Scrollbar(
            moldura,
            orient="vertical",
            command=self.canvas.yview,
        )
        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        barra_horizontal = ttk.Scrollbar(
            moldura,
            orient="horizontal",
            command=self.canvas.xview,
        )
        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.canvas.configure(
            xscrollcommand=barra_horizontal.set,
            yscrollcommand=barra_vertical.set,
        )

        self.canvas.bind(
            "<Configure>",
            lambda _evento: self._desenhar_matriz(),
        )

    def _montar_painel(self, parent: ttk.Frame) -> None:
        painel = ttk.LabelFrame(
            parent,
            text="Informações",
            style="Card.TLabelframe",
        )
        painel.pack(fill="both", expand=True, padx=(16, 0))

        painel.rowconfigure(1, weight=1)
        painel.columnconfigure(0, weight=1)

        indicadores = ttk.Frame(painel)
        indicadores.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 14),
        )

        ttk.Label(
            indicadores,
            textvariable=self.geracao_var,
        ).pack(anchor="w", pady=2)

        ttk.Label(
            indicadores,
            textvariable=self.populacao_var,
        ).pack(anchor="w", pady=2)

        ttk.Label(
            indicadores,
            textvariable=self.aptidao_var,
        ).pack(anchor="w", pady=2)

        ttk.Label(
            indicadores,
            textvariable=self.diversidade_var,
            wraplength=260,
        ).pack(anchor="w", pady=2)

        self.info = tk.Text(
            painel,
            width=31,
            height=18,
            wrap="word",
            relief="flat",
            borderwidth=0,
            state="disabled",
            font=("Segoe UI", 10),
        )
        self.info.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self._escrever_info(
            "Clique em uma célula da matriz para visualizar os genes "
            "do indivíduo."
        )

    def _montar_controles(self, parent: ttk.Frame) -> None:
        controles = ttk.Frame(parent)
        controles.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(16, 0),
        )

        ttk.Button(
            controles,
            text="Nova população",
            style="Acao.TButton",
            command=self.nova_populacao,
        ).pack(side="left")

        ttk.Button(
            controles,
            text="Próxima geração",
            style="Acao.TButton",
            command=self.proxima_geracao,
        ).pack(side="left", padx=8)

        ttk.Button(
            controles,
            text="Executar gerações",
            style="Acao.TButton",
            command=self.executar_geracoes,
        ).pack(side="left")

        self.botao_automatico = ttk.Button(
            controles,
            text="Evolução automática",
            style="Acao.TButton",
            command=self.alternar_automacao,
        )
        self.botao_automatico.pack(side="left", padx=8)

        ttk.Label(
            controles,
            textvariable=self.status_var,
            anchor="e",
        ).pack(side="right")

    def _montar_legenda(self, parent: ttk.Frame) -> None:
        legenda = ttk.Frame(parent)
        legenda.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(14, 0),
        )

        ttk.Label(
            legenda,
            text="Curso:",
        ).pack(side="left", padx=(0, 8))

        for curso, cor in CORES_CURSOS.items():
            etiqueta = tk.Label(
                legenda,
                text=curso,
                bg=cor,
                fg="white",
                padx=8,
                pady=4,
                font=("Segoe UI", 8, "bold"),
            )
            etiqueta.pack(side="left", padx=3)

    # --------------------------------------------------------
    # Desenho e informações
    # --------------------------------------------------------

    def _desenhar_matriz(self) -> None:
        self.canvas.delete("all")
        self.itens_matriz.clear()

        if not self.algoritmo.populacao:
            return

        largura_disponivel = max(
            self.canvas.winfo_width(),
            600,
        )

        altura_disponivel = max(
            self.canvas.winfo_height(),
            500,
        )

        espacamento = 10
        margem = 18

        largura_celula = max(
            58,
            min(
                98,
                (
                    largura_disponivel
                    - (2 * margem)
                    - ((TAMANHO_MATRIZ - 1) * espacamento)
                ) / TAMANHO_MATRIZ,
            ),
        )

        altura_celula = max(
            54,
            min(
                82,
                (
                    altura_disponivel
                    - (2 * margem)
                    - ((TAMANHO_MATRIZ - 1) * espacamento)
                ) / TAMANHO_MATRIZ,
            ),
        )

        tema = TEMAS[self.tema]

        for linha in range(TAMANHO_MATRIZ):
            for coluna in range(TAMANHO_MATRIZ):
                indice = linha * TAMANHO_MATRIZ + coluna
                individuo = self.algoritmo.populacao[indice]

                x1 = margem + coluna * (
                    largura_celula + espacamento
                )
                y1 = margem + linha * (
                    altura_celula + espacamento
                )
                x2 = x1 + largura_celula
                y2 = y1 + altura_celula

                cor_curso = CORES_CURSOS[individuo.curso]
                selecionado = (
                    self.individuo_selecionado is not None
                    and individuo.numero
                    == self.individuo_selecionado.numero
                )

                eh_lider = individuo.lider

                sombra = self._retangulo_arredondado(
                    x1 + 3,
                    y1 + 4,
                    x2 + 3,
                    y2 + 4,
                    raio=14,
                    fill=tema["sombra"],
                    outline="",
                )

                celula = self._retangulo_arredondado(
                    x1,
                    y1,
                    x2,
                    y2,
                    raio=14,
                    fill=cor_curso,
                    outline=(
                        "#facc15"
                        if eh_lider
                        else tema["selecionado"]
                        if selecionado
                        else cor_curso
                    ),
                    width=5 if eh_lider else 4 if selecionado else 2,
                )

                texto = self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=(
                        f"★ LÍDER\n"
                        if individuo.lider
                        else ""
                    ) + (
                        f"{individuo.familia.replace('Família ', 'F')}\n"
                        f"{individuo.periodo.split('º')[0]}º período"
                    ),
                    fill="white",
                    font=("Segoe UI", 9, "bold"),
                    justify="center",
                )

                tag = f"individuo_{individuo.numero}"

                for item in (celula, texto):
                    self.canvas.addtag_withtag(tag, item)

                self.canvas.tag_bind(
                    tag,
                    "<Button-1>",
                    lambda _evento, pessoa=individuo:
                    self.mostrar_individuo(pessoa),
                )

                self.canvas.tag_bind(
                    tag,
                    "<Enter>",
                    lambda _evento, item=celula:
                    self._destacar_celula(item, True),
                )

                self.canvas.tag_bind(
                    tag,
                    "<Leave>",
                    lambda _evento, item=celula,
                    pessoa=individuo:
                    self._destacar_celula(
                        item,
                        False,
                        pessoa,
                    ),
                )

                self.itens_matriz.extend(
                    [sombra, celula, texto]
                )

        largura_total = (
            2 * margem
            + TAMANHO_MATRIZ * largura_celula
            + (TAMANHO_MATRIZ - 1) * espacamento
        )

        altura_total = (
            2 * margem
            + TAMANHO_MATRIZ * altura_celula
            + (TAMANHO_MATRIZ - 1) * espacamento
        )

        self.canvas.configure(
            scrollregion=(0, 0, largura_total, altura_total),
        )

    def _retangulo_arredondado(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        raio: float,
        **opcoes: object,
    ) -> int:
        raio = min(
            raio,
            (x2 - x1) / 2,
            (y2 - y1) / 2,
        )

        pontos = (
            x1 + raio, y1,
            x2 - raio, y1,
            x2, y1 + raio,
            x2, y2 - raio,
            x2 - raio, y2,
            x1 + raio, y2,
            x1, y2 - raio,
            x1, y1 + raio,
        )

        return self.canvas.create_polygon(
            pontos,
            smooth=True,
            splinesteps=16,
            **opcoes,
        )

    def _destacar_celula(
        self,
        item: int,
        ativo: bool,
        individuo: Individuo | None = None,
    ) -> None:
        if ativo:
            self.canvas.itemconfigure(
                item,
                width=4,
                outline="#ffffff",
            )
            return

        tema = TEMAS[self.tema]

        selecionado = (
            individuo is not None
            and self.individuo_selecionado is not None
            and individuo.numero
            == self.individuo_selecionado.numero
        )

        self.canvas.itemconfigure(
            item,
            width=4 if selecionado else 2,
            outline=(
                tema["selecionado"]
                if selecionado
                else self.canvas.itemcget(item, "fill")
            ),
        )

    def mostrar_individuo(self, individuo: Individuo) -> None:
        self.individuo_selecionado = individuo

        papel = (
            "LÍDER DA POPULAÇÃO"
            if individuo.lider
            else "Membro da população"
        )

        texto = (   
            f"INDIVÍDUO #{individuo.numero}\n"
            f"{'─' * 25}\n"
            f"{papel}\n\n"
            f"Família: {individuo.familia}\n"
            f"Sexo: {individuo.sexo}\n"
            f"Período: {individuo.periodo}\n"
            f"Curso: {individuo.curso}\n"
            f"Religião: {individuo.religiao}\n"
            f"Origem: {individuo.origem}\n\n"
        )

        if individuo.lider:
            texto += (
                "Este indivíduo influencia seus vizinhos "
                "diretos e diagonais."
            )
        else:
            texto += (
                "O indivíduo pode receber genes do líder quando "
                "está em uma posição vizinha."
            )

        self._escrever_info(texto)
        self._desenhar_matriz()

    def _escrever_info(self, texto: str) -> None:
        self.info.configure(state="normal")
        self.info.delete("1.0", "end")
        self.info.insert("1.0", texto)
        self.info.configure(state="disabled")

    # --------------------------------------------------------
    # Atualização da interface
    # --------------------------------------------------------

    def _atualizar_interface(self) -> None:
        self._desenhar_matriz()

        diversidade_periodo = self.algoritmo.diversidade(
            "periodo"
        )
        diversidade_curso = self.algoritmo.diversidade(
            "curso"
        )

        self.geracao_var.set(
            f"Geração atual: {self.algoritmo.geracao}"
        )

        self.populacao_var.set(
            f"Indivíduos: {len(self.algoritmo.populacao)}"
        )

        self.aptidao_var.set(
            f"Aptidão média: {self.algoritmo.aptidao_media():.3f}"
        )

        self.diversidade_var.set(
            "Diversidade: "
            f"{diversidade_periodo} períodos e "
            f"{diversidade_curso} cursos"
        )

        self.status_var.set(
            f"Geração {self.algoritmo.geracao}  •  "
            f"{len(self.algoritmo.populacao)} indivíduos  •  "
            f"{self.algoritmo.quantidade_familias} famílias"
        )

    # --------------------------------------------------------
    # Ações da aplicação
    # --------------------------------------------------------

    def nova_populacao(self) -> None:
        self.parar_automacao()

        self.algoritmo = AlgoritmoGenetico(
            quantidade_familias=self.familias_var.get(),
            taxa_mutacao=self.mutacao_var.get() / 100,
            taxa_influencia=self.influencia_var.get() / 100,
        )

        self.individuo_selecionado = None

        self._escrever_info(
            "Clique em uma célula da matriz para visualizar "
            "os genes do indivíduo."
        )

        self._atualizar_interface()

    def proxima_geracao(self) -> None:
        self.algoritmo.evoluir()
        self._atualizar_interface()

    def executar_geracoes(self) -> None:
        try:
            quantidade = self._ler_geracoes()
        except ValueError as erro:
            messagebox.showerror(
                "Valor inválido",
                str(erro),
            )
            return

        self.parar_automacao()

        for _ in range(quantidade):
            self.algoritmo.evoluir()

        self._atualizar_interface()

    def aplicar_configuracoes(self) -> None:
        try:
            familias = self._ler_familias()
            mutacao = self._ler_mutacao()
        except ValueError as erro:
            messagebox.showerror(
                "Configuração inválida",
                str(erro),
            )
            return

        self.familias_var.set(familias)
        self.mutacao_var.set(mutacao)
        self.tema = self.tema_var.get()

        self._aplicar_tema()
        self.nova_populacao()

    def alternar_automacao(self) -> None:
        if self.automacao_id is not None:
            self.parar_automacao()
            return

        try:
            quantidade = self._ler_geracoes()
        except ValueError as erro:
            messagebox.showerror(
                "Valor inválido",
                str(erro),
            )
            return

        self.alvo_automacao = (
            self.algoritmo.geracao + quantidade
        )

        self.botao_automatico.configure(
            text="Parar evolução",
        )

        self.automacao_id = self.raiz.after(
            50,
            self._evoluir_automaticamente,
        )

    def _evoluir_automaticamente(self) -> None:
        self.automacao_id = None

        if self.alvo_automacao is None:
            return

        if self.algoritmo.geracao >= self.alvo_automacao:
            self.parar_automacao()
            return

        self.proxima_geracao()

        self.automacao_id = self.raiz.after(
            450,
            self._evoluir_automaticamente,
        )

    def parar_automacao(self) -> None:
        if self.automacao_id is not None:
            self.raiz.after_cancel(self.automacao_id)

        self.automacao_id = None
        self.alvo_automacao = None

        if hasattr(self, "botao_automatico"):
            self.botao_automatico.configure(
                text="Evolução automática",
            )

    # --------------------------------------------------------
    # Validação
    # --------------------------------------------------------

    def _ler_familias(self) -> int:
        try:
            valor = int(self.familias_var.get())
        except (TypeError, ValueError, tk.TclError):
            raise ValueError(
                "A quantidade de famílias deve ser um número inteiro."
            )

        if not 1 <= valor <= 20:
            raise ValueError(
                "A quantidade de famílias deve estar entre 1 e 20."
            )

        return valor

    def _ler_geracoes(self) -> int:
        try:
            valor = int(self.geracoes_var.get())
        except (TypeError, ValueError, tk.TclError):
            raise ValueError(
                "A quantidade de gerações deve ser um número inteiro."
            )

        if not 1 <= valor <= 10000:
            raise ValueError(
                "A quantidade de gerações deve estar entre 1 e 10.000."
            )

        return valor

    def _ler_mutacao(self) -> float:
        try:
            valor = float(self.mutacao_var.get())
        except (TypeError, ValueError, tk.TclError):
            raise ValueError(
                "A taxa de mutação deve ser um número."
            )

        if not 0 <= valor <= 100:
            raise ValueError(
                "A taxa de mutação deve estar entre 0% e 100%."
            )

        return valor

    # --------------------------------------------------------
    # Tema e encerramento
    # --------------------------------------------------------

    def _aplicar_tema(self) -> None:
        cores = TEMAS[self.tema]

        self.raiz.configure(
            bg=cores["fundo"],
        )

        self.estilo.configure(
            "TFrame",
            background=cores["fundo"],
        )

        self.estilo.configure(
            "TLabelframe",
            background=cores["fundo"],
            bordercolor=cores["borda"],
        )

        self.estilo.configure(
            "TLabelframe.Label",
            background=cores["fundo"],
            foreground=cores["texto"],
        )

        self.estilo.configure(
            "TLabel",
            background=cores["fundo"],
            foreground=cores["texto"],
        )

        self.estilo.configure(
            "Titulo.TLabel",
            background=cores["fundo"],
            foreground=cores["texto"],
        )

        self.estilo.configure(
            "Subtitulo.TLabel",
            background=cores["fundo"],
            foreground=cores["secundario"],
        )

        self.estilo.configure(
            "TButton",
            background=cores["cartao"],
            foreground=cores["texto"],
        )

        self.estilo.map(
            "TButton",
            background=[
                ("active", cores["borda"]),
            ],
        )

        self.canvas.configure(
            bg=cores["canvas"],
        )

        self.info.configure(
            bg=cores["cartao"],
            fg=cores["texto"],
            insertbackground=cores["texto"],
            selectbackground=cores["borda"],
        )

        self._desenhar_matriz()

    def _encerrar(self) -> None:
        self.parar_automacao()
        self.raiz.destroy()


# ============================================================
# Inicialização
# ============================================================

def executar() -> None:
    raiz = tk.Tk()
    Aplicacao(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    executar()