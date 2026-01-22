import streamlit as st
from datetime import date
import math
import io
import csv
import pandas as pd
import altair as alt

# ================================
# COPY PREMIUM (PT) — RumoCasa
# ================================
COPY = {
    "app_title": "RumoCasa 🏡 Planeador Habitacional",
    "app_tagline": "O planeador inteligente para a tua decisão de habitação.",

    "hero_title": "🏠 RumoCasa",
    "hero_subtitle": "O planeador inteligente para a tua decisão de habitação.",
    "hero_body": (
        "Decide com números — não com achismos. "
        "Compara Comprar, Construir ou Arrendar estrategicamente, percebe a entrada necessária, "
        "a prestação mensal e o impacto real dos juros antes de tomar decisões."
    ),

    "section_simular_title": "📊 O que queres simular?",
    "section_simular_body": (
        "Escolhe o cenário que estás a considerar e vê, de forma clara: "
        "quanto precisas à cabeça, quanto vais pagar todos os meses e o custo real ao longo do tempo. "
        "O RumoCasa ajuda-te a transformar uma decisão emocional numa decisão informada."
    ),

    "layout_label": "Disposição",
    "layout_opt_cols": "Colunas lado a lado",
    "layout_opt_tabs": "Abas separadas",

    "kpi_bar_hint": (
        "💡 Estes valores são estimativos e servem como apoio à decisão — "
        "não substituem propostas formais de instituições financeiras."
    ),

    "buy_title": "🏡 Comprar casa",
    "buy_body": (
        "Simula a compra de um imóvel já construído e percebe: "
        "o impacto do preço na entrada e na prestação, os custos associados à compra "
        "e a viabilidade do crédito no teu orçamento."
    ),
    "buy_link_label": "URL do anúncio (casa) (opcional)",
    "buy_link_help": "Podes colar o URL de um anúncio para facilitar a simulação.",

    "build_title": "🏗️ Construir casa",
    "build_body": (
        "Avalia um projeto de construção desde a base: custo do terreno, sistema construtivo, "
        "área útil e custo estimado por m². Percebe se construir é realmente mais vantajoso "
        "ou apenas parece à primeira vista."
    ),
    "build_link_label": "URL do anúncio (terreno) (opcional)",
    "build_link_help": "Opcional. Se tiveres o link do terreno, cola aqui para referência.",

    "rent_title": "🏘️ Arrendar como estratégia",
    "rent_body": (
        "Arrendar não é “deitar dinheiro fora” — pode ser uma fase estratégica. "
        "Aqui consegues comparar o custo do arrendamento, simular poupança mensal "
        "e perceber quanto tempo precisas para atingir a entrada ideal."
    ),

    "sens_title": "📈 Sensibilidade & cenários",
    "sens_body": "Testa variações de taxa, preço e prazo e vê como pequenas mudanças alteram o resultado final.",

    "save_title": "💰 Plano de poupança",
    "save_body": (
        "Simula quanto precisas de poupar por mês para atingir a entrada desejada, "
        "reduzir o valor do crédito e melhorar condições futuras."
    ),

    "partners_title": "🤝 Parceiros relevantes",
    "partners_body": "Versão demo. Aqui poderás ligar parceiros reais (crédito / construção / mediação) ao teu cenário.",

    "export_hint": "📥 Exporta e partilha o teu cenário (CSV) para discutir com bancos, parceiros ou família.",

    "disclaimer": (
        "⚠️ Nota: MVP educativo. Não constitui aconselhamento financeiro. "
        "Valores e taxas podem variar por banco, perfil e condições."
    ),

    "closing": (
        "🎯 Uma casa é uma decisão de vida. "
        "O RumoCasa ajuda-te a decidir com clareza, segurança e visão de longo prazo."
    ),
}

TIPS = {
    # ====================
    # Comprar
    # ====================
    "url_casa": "Cola aqui o link do anúncio (Idealista/Imovirtual, etc.). Serve para referência (e para automatismos futuros).",
    "preco_casa": "Preço do imóvel (valor do anúncio). É a base para entrada, IMT e cálculo da prestação.",
    "tipo_imovel": "HPP = Habitação Própria Permanente (IMT geralmente mais baixo). Secundária = férias/investimento (IMT mais alto).",
    "novo": "Marca se é imóvel novo (contexto). No MVP não altera o IMT, mas pode ser útil para custos/IVA noutras contas.",
    "entrada_pct": "Percentagem do preço paga com capitais próprios. Mais entrada = menos crédito e (em regra) prestação mais baixa.",
    "taeg": "TAEG inclui juros + comissões + seguros. É o indicador mais útil para comparar propostas de bancos.",
    "prazo": "Prazo do crédito. Mais prazo baixa a prestação, mas aumenta o total pago em juros.",
    "poup_atual": "Quanto tens disponível para a entrada. (Sugestão: não misturar com fundo de emergência.)",
    "condo": "Custos fixos mensais (condomínio/manutenção). Pequenos valores acumulam e mexem no orçamento.",
    "seguros": "Seguros associados ao crédito (vida/habitação). Podem variar muito e alterar a mensalidade real.",

    # ====================
    # Construir (chaves a bater com o teu código novo)
    # ====================
    "url_terreno": "Link do anúncio do terreno (opcional). Serve só para referência.",
    "preco_terreno": "Preço de compra do terreno. Muitas vezes é pago antes da obra ou no início do processo.",
    "estrutura": "Convencional, LSF ou Modular/3E. Muda custo, tempo e risco. Este simulador é estimativo.",
    "area_m2": "Área útil estimada da casa (m²). Quanto maior, maior tende a ser o custo total.",
    "custo_m2": "Estimativa do custo base por m². Varia por acabamentos, zona, mão de obra e projeto.",
    "iva_reduzido": "Aplica IVA reduzido (ex.: 6%) apenas quando o teu caso se enquadra. Confirma com técnico/contabilista.",
    "imprevistos_pct": "Margem para derrapagens (recomendado 10–20%). Construção raramente fecha a 100% do orçamento inicial.",
    "projetos_lic": "Arquitetura/engenharias/licenças/termos. Depende do município e complexidade do projeto.",
    "fiscalizacao": "Fiscalização/coordenação. Ajuda a evitar erros caros e derrapagens na obra.",
    "entrada_pct_build": "Percentagem do total do projeto paga com capitais próprios. (Bancos podem libertar em tranches.)",
    "cond_man_build": "Custos mensais (seguros/manutenção). Se não fizer sentido, podes pôr 0 no teu caso.",
    "prazo_obra": "Duração estimada da obra. Prazos maiores tendem a aumentar risco e custos indiretos.",

    # ====================
    # Arrendar
    # ====================
    "renda": "Valor da renda mensal. Serve para perceber quanto sobra para poupar rumo à entrada.",
    "infl_renda": "Estimativa de subida anual da renda. Se não quiseres complicar, usa 0–3%.",

    # ====================
    # Comparação
    # ====================
    "comparacao": "No RumoCasa, a comparação prioriza a mensalidade — porque é ela que acompanha a tua vida todos os meses, não só no primeiro dia.",
}

# -------------------------------------------------
# CONFIG DA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title=COPY["app_title"],
    page_icon="🏡",
    layout="centered",
)

st.markdown("""
<style>

/* ===== FORÇAR TEMA CLARO (ignorar dark mode do sistema) ===== */

html, body, .stApp {
    background-color: #f5f5f7 !important;
    color: #111827 !important;
}

/* Cards principais */
.section-card {
    background: #ffffff !important;
    color: #111827 !important;
}

/* Títulos */
h1, h2, h3, h4, h5 {
    color: #0f172a !important;
}

/* Texto secundário / descrições */
p, span, label {
    color: #374151 !important;
}

/* Captions do Streamlit */
[data-testid="stCaptionContainer"] p {
    color: #4b5563 !important;
}

/* Inputs */
input, textarea, select {
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Métricas */
[data-testid="metric-container"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 14px;
}

/* Remover influência do dark mode do SO */
@media (prefers-color-scheme: dark) {
    html, body, .stApp {
        background-color: #f5f5f7 !important;
        color: #111827 !important;
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# ESTILO GLOBAL RUMOCASA
# -------------------------------------------------
st.markdown(
    """
<style>
:root {
    --rc-green:        #0f5132;
    --rc-green-dark:   #0b3b25;
    --rc-green-soft:   rgba(15, 81, 50, 0.12);
    --rc-green-track:  rgba(15, 81, 50, 0.45);

    --rc-gray-900:     #111827;
    --rc-gray-800:     #1f2937;
    --rc-gray-700:     #374151;
    --rc-gray-500:     #6B7280;
    --rc-gray-200:     #e5e7eb;
    --rc-gray-100:     #f3f4f6;

    --rc-bg:           #f5f5f7;
}

html, body, .stApp {
    background-color: var(--rc-bg) !important;
    color: var(--rc-gray-900) !important;
}

.stApp { background-color: var(--rc-bg); }

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

@keyframes rc-fade-in-up {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.rc-fade-in { animation: rc-fade-in-up 0.55s ease-out both; }

.rc-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 2rem;
    animation: rc-fade-in-up 0.45s ease-out both;
}

.rc-logo {
    font-size: 3.1rem;
    font-weight: 900;
    color: var(--rc-gray-900);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.55rem;
}
.rc-logo .emoji { font-size: 3.1rem; }

.rc-logo-text {
    background: linear-gradient(90deg, #0f5132, #16a34a);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.rc-tagline {
    font-size: 1rem;
    color: var(--rc-gray-700);
    background: #ffffff;
    padding: 6px 14px;
    border-radius: 999px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

.rc-header-line {
    width: 90px;
    height: 3px;
    border-radius: 999px;
    margin-top: 0.35rem;
    background: linear-gradient(90deg, #10b981, #0f5132);
}

.section-card {
    background: #FFFFFF !important;
    color: var(--rc-gray-900) !important;
    border-radius: 18px;
    padding: 1.75rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 18px 40px rgba(15,23,42,0.08);
    margin: 0.6rem 0 1.4rem 0;
    animation: rc-fade-in-up 0.55s ease-out both;
}

.rc-main-card {
    background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.96) 100%);
    box-shadow: 0 26px 70px rgba(15,23,42,0.14);
    border-top: 3px solid rgba(16, 185, 129, 0.75);
}
.rc-main-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 30px 78px rgba(15,23,42,0.18);
}

.rc-main-section-title {
    font-size: 1.65rem;
    font-weight: 850;
    color: var(--rc-gray-900);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.subtitle {
    color: var(--rc-gray-700);
    font-size: 0.98rem;
    line-height: 1.45;
    margin: 0.1rem 0 0 0;
}

.main h3 {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--rc-gray-900);
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.85rem;
}
.main h3::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--rc-gray-200);
    margin-left: 0.75rem;
}

.stTextInput > div > div > input,
.stNumberInput input,
.stSelectbox > div > div > select,
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #d1d5db;
    padding: 6px 10px;
    font-size: 0.95rem;
    background: #ffffff !important;
    color: var(--rc-gray-900) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput input:focus,
.stSelectbox > div > div > select:focus,
.stTextArea textarea:focus {
    border-color: var(--rc-green);
    box-shadow: 0 0 0 2px var(--rc-green-soft);
    outline: none;
}

.stButton>button, .stDownloadButton>button {
    background-color: var(--rc-green);
    color: #ffffff;
    border-radius: 999px;
    border: none;
    padding: 0.45rem 1.2rem;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.15s ease-in-out;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: var(--rc-green-dark);
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(15, 81, 50, 0.35);
}

[data-testid="metric-container"] {
    background: #FFFFFF !important;
    color: var(--rc-gray-900) !important;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

.rc-sticky-summary { margin-bottom: 1rem; }
.rc-sticky-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.55rem 1.1rem;
    border-radius: 999px;
    background: rgba(15, 81, 50, 0.96);
    box-shadow: 0 10px 30px rgba(15,23,42,0.45);
    color: #ecfdf5;
    backdrop-filter: blur(10px);
}
.rc-sticky-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.85;
}
.rc-sticky-value {
    font-size: 0.98rem;
    font-weight: 700;
}

[data-testid="stCaptionContainer"] p {
    color: var(--rc-gray-900) !important;
    font-size: 0.95rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# HEADER + CARTÃO INICIAL (copy premium)
# -------------------------------------------------
st.markdown(
    """
    <div class="rc-header rc-fade-in">
      <div class="rc-logo">
        <span class="emoji">🏡</span>
        <span class="rc-logo-text">RumoCasa</span>
      </div>

      <div class="rc-tagline">
        O planeador inteligente para a tua decisão de casa.
      </div>

      <div class="rc-header-line"></div>
    </div>

    <div class="section-card rc-main-card rc-fade-in">
      <h2 class="rc-main-section-title">📊 O que queres simular?</h2>
      <p class="subtitle">
        Decide com números, não com “achismos”.
        Compara <b>Comprar</b> e <b>Construir</b>, percebe a <b>entrada</b>, a <b>mensalidade</b> e o impacto dos <b>juros</b>.
        E se estás a arrendar, usa isso como fase estratégica enquanto juntas (e fazes o dinheiro trabalhar).
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# placeholder da sticky bar
sticky_placeholder = st.empty()

# -------------------------------------------------
# Helpers / utilitários
# -------------------------------------------------
def K(ns: str, name: str) -> str:
    return f"{ns}::{name}"

def ss_get(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def euro0(x):
    try:
        return (f"{float(x):,.0f} €").replace(",", " ").replace(".", ",")
    except Exception:
        return "—"

def calc_prestacao(pv, taxa_anual, anos):
    r = float(taxa_anual) / 12.0
    n = int(anos * 12)
    if n <= 0:
        return 0.0
    if r == 0:
        return pv / n
    return (pv * r) / (1 - (1 + r) ** (-n))

def guess_price_from_url(url: str):
    # stub (para futuro)
    return None

def calc_imt_2025(valor: float, hab_pp: bool = True) -> float:
    v = float(valor)
    if v <= 0:
        return 0.0

    if not hab_pp:
        return v * 0.065  # simplificação para não-HPP

    if v <= 97064:
        return 0.0
    if v <= 132774:
        taxa, parcela = 0.02, 1941.28
    elif v <= 181034:
        taxa, parcela = 0.05, 5708.21
    elif v <= 301688:
        taxa, parcela = 0.07, 9087.19
    elif v <= 603289:
        taxa, parcela = 0.08, 11959.32
    else:
        return v * 0.06

    return v * taxa - parcela

# -------------------------------------------------
# Sticky Summary (mini-header)
# -------------------------------------------------
def ui_sticky_summary(container):
    upfront_buy   = float(st.session_state.get("upfront_buy", 0.0))
    entrada_build = float(st.session_state.get("entrada_build", 0.0))
    entrada = upfront_buy or entrada_build

    mensal_compra = float(st.session_state.get("mensal_compra", 0.0))
    mensal_build  = float(st.session_state.get("mensal_build", 0.0))
    mensal = mensal_compra or mensal_build

    if entrada <= 0 and mensal <= 0:
        return

    html = f"""
    <div class="rc-sticky-summary">
      <div class="rc-sticky-inner">
        <div>
          <div class="rc-sticky-label">Entrada estimada</div>
          <div class="rc-sticky-value">{euro0(entrada)}</div>
        </div>
        <div>
          <div class="rc-sticky-label">Prestação mensal</div>
          <div class="rc-sticky-value">{euro0(mensal)}</div>
        </div>
      </div>
    </div>
    """
    container.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------
# Toggle UI
# -------------------------------------------------
st.markdown("<div class='section-card' style='padding: 1rem 1.25rem; margin-top: -0.75rem;'>", unsafe_allow_html=True)
modo_ui = st.radio(
    COPY["layout_label"],
    [COPY["layout_opt_cols"], COPY["layout_opt_tabs"]],
    horizontal=True,
)

# ================================
# Secção COMPRAR
# ================================
def ui_comprar():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.markdown(f"### {COPY['buy_title']}")
    st.caption(COPY["buy_body"])

    colL, colR = st.columns(2)

    with colL:
        # URL do anúncio (opcional)
        url_casa = st.text_input(
            COPY["buy_link_label"],
            help=TIPS["url_casa"],  # ✅ tooltip mais forte e objetiva
            key=K("comprar", "url_casa"),
        )

        preco_guess = guess_price_from_url(url_casa) if url_casa else None

        preco_casa = st.number_input(
            "Preço da casa (€)",
            step=1000,
            min_value=10000,
            value=int(preco_guess or ss_get(K("comprar", "preco_casa"), 200_000)),
            help=TIPS["preco_casa"],
            key=K("comprar", "preco_casa_input"),
        )

        # (opcional) espelho sem key (não cria conflito)
        st.session_state[K("comprar", "preco_casa")] = preco_casa

    with colR:
        st.caption("Perfil do imóvel")
        tipo_imovel = st.selectbox(
            "Tipo de imóvel",
            ["Habitação Própria Permanente", "Secundária"],
            help=TIPS["tipo_imovel"],
            key=K("comprar", "tipo_imovel"),
            index=0
        )
        _ = st.checkbox(
            "Imóvel novo (IVA incluído)",
            help=TIPS["novo"],
            key=K("comprar", "novo")
        )

    st.divider()

    colA, colB, colC = st.columns(3)

    with colA:
        entrada_pct = st.number_input(
            "% Entrada",
            min_value=0.0,
            max_value=100.0,
            value=float(ss_get(K("comprar", "entrada_pct"), 10.0)),
            step=1.0,
            help=TIPS["entrada_pct"],
            key=K("comprar", "entrada_pct_input"),
        ) / 100.0

        poup_atual = st.number_input(
            "Poupança atual (€)",
            min_value=0,
            value=int(ss_get(K("comprar", "poup_atual"), 20_000)),
            step=500,
            help=TIPS["poup_atual"],
            key=K("comprar", "poup_atual_input"),
        )
        st.session_state["poup_atual"] = float(poup_atual)

    with colB:
        taeg_anual = st.number_input(
            "Taxa anual (TAEG %)",
            min_value=0.0,
            value=float(ss_get(K("comprar", "taeg"), 4.0)),
            step=0.1,
            help=TIPS["taeg"],
            key=K("comprar", "taeg_input"),
        ) / 100.0
        st.session_state["taeg_anual"] = float(taeg_anual)

    with colC:
        prazo_anos = st.number_input(
            "Prazo (anos)",
            min_value=1,
            max_value=50,
            value=int(ss_get(K("comprar", "prazo"), 30)),
            step=1,
            help=TIPS["prazo"],
            key=K("comprar", "prazo_input"),
        )
        st.session_state["prazo_anos"] = int(prazo_anos)

    is_hpp = (tipo_imovel == "Habitação Própria Permanente")
    imt = calc_imt_2025(preco_casa, hab_pp=is_hpp)
    selo = 0.008 * float(preco_casa)
    outros_custos = 1000.0
    custos_compra = imt + selo + outros_custos

    entrada = float(preco_casa) * float(entrada_pct)
    financiado = max(0.0, float(preco_casa) - entrada)
    prestacao = calc_prestacao(financiado, taeg_anual, prazo_anos)

    colX, colY = st.columns(2)

    with colX:
        condo = st.number_input(
            "Condomínio / Manutenção (€/mês)",
            min_value=0.0,
            value=float(ss_get(K("comprar", "condo"), 0.0)),
            step=5.0,
            help=TIPS["condo"],
            key=K("comprar", "condo_input"),
        )
        seguros = st.number_input(
            "Seguros (€/mês)",
            min_value=0.0,
            value=float(ss_get(K("comprar", "seguros"), 0.0)),
            step=5.0,
            help=TIPS["seguros"],
            key=K("comprar", "seguros_input"),
        )

    with colY:
        st.caption("💡 Dica: custos mensais “pequenos” (condomínio/seguros) mudam a realidade do orçamento.")

    mensal_compra = float(prestacao) + float(condo) + float(seguros)
    upfront_buy = float(entrada) + float(custos_compra)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Entrada necessária (entrada + impostos/custos)", euro0(upfront_buy))
        st.caption(
            f"IMT 2025: {euro0(imt)} | Selo: {euro0(selo)} | Escritura/registos (est.): {euro0(outros_custos)}"
        )

    with col2:
        st.metric("Prestação (crédito)", euro0(prestacao))
        st.metric("Mensal total (com custos)", euro0(mensal_compra))

    st.session_state["upfront_buy"] = float(upfront_buy)
    st.session_state["mensal_compra"] = float(mensal_compra)
    st.session_state["financiado"] = float(financiado)
    st.session_state["condo"] = float(condo)
    st.session_state["seguros"] = float(seguros)
    st.session_state["imt_2025"] = float(imt)

    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Secção CONSTRUIR
# ================================
def ui_construir():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### {COPY['build_title']}")
    st.caption(COPY["build_body"])

    colL, colR = st.columns(2)

    with colL:
        url_terreno = st.text_input(
            COPY["build_link_label"],
            help=TIPS["url_terreno"],
            key=K("construir", "url_terreno"),
        )

        preco_terreno = st.number_input(
            "Preço do terreno (€)",
            step=1000,
            min_value=0,
            value=int(ss_get(K("construir", "preco_terreno"), 50_000)),
            help=TIPS["preco_terreno"],
            key=K("construir", "preco_terreno_input"),
        )
        st.session_state[K("construir", "preco_terreno")] = preco_terreno


    with colR:
        estrutura = st.selectbox(
            "Sistema construtivo",
            ["Convencional", "LSF (aço leve)", "Modular / 3E"],
            help=TIPS["estrutura"],
            key=K("construir", "estrutura"),
            index=0,
        )

        area_m2 = st.number_input(
            "Área útil (m²)",
            min_value=40,
            value=int(ss_get(K("construir", "area_m2"), 120)),
            step=5,
            help=TIPS["area_m2"],
            key=K("construir", "area_m2_input"),
        )

        custo_m2 = st.number_input(
            "Custo base construção (€/m²)",
            min_value=600,
            value=int(ss_get(K("construir", "custo_m2"), 1100)),
            step=50,
            help=TIPS["custo_m2"],
            key=K("construir", "custo_m2_input"),
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        iva_reduzido = st.checkbox(
            "IVA reduzido (ex.: 6%)",
            value=bool(ss_get(K("construir", "iva_red"), True)),
            help=TIPS["iva_reduzido"],
            key=K("construir", "iva_reduzido"),
        )

        imprevistos_pct = st.slider(
            "Imprevistos (%)",
            0,
            20,
            value=int(ss_get(K("construir", "imp_pct"), 10)),
            help=TIPS["imprevistos_pct"],
            key=K("construir", "imp_prev"),
        )

    with col2:
        projetos_lic = st.number_input(
            "Projetos & Licenças (€)",
            value=float(ss_get(K("construir", "proj"), 8000.0)),
            step=1000.0,
            min_value=0.0,
            help=TIPS["projetos_lic"],
            key=K("construir", "proj_input"),
        )

    with col3:
        fiscalizacao = st.number_input(
            "Fiscalização/Coordenação (€)",
            value=float(ss_get(K("construir", "fisc"), 3000.0)),
            step=500.0,
            min_value=0.0,
            help=TIPS["fiscalizacao"],
            key=K("construir", "fisc_input"),
        )

    st.divider()

    colM, colN = st.columns(2)

    with colM:
        entrada_pct_build = st.slider(
            "% Entrada (construção)",
            0.0,
            50.0,
            value=float(ss_get(K("construir", "entrada_pct_build"), 10.0)),
            step=1.0,
            help=TIPS["entrada_pct_build"],
            key=K("construir", "entrada_constr"),
        ) / 100.0

        cond_man_build = st.number_input(
            "Seguros + Manutenção (€/mês)",
            value=float(ss_get(K("construir", "cond_build"), 40.0)),
            step=5.0,
            min_value=0.0,
            help=TIPS["cond_man_build"],
            key=K("construir", "cond_build_input"),
        )

    with colN:
        _ = st.slider(
            "Prazo de obra (meses)",
            6,
            24,
            value=int(ss_get(K("construir", "obra_meses"), 12)),
            help=TIPS["prazo_obra"],
            key=K("construir", "prazo_obra"),
        )

    # --- Ajuste simples por sistema construtivo (MVP) ---
    fator = 1.00
    if estrutura == "LSF (aço leve)":
        fator = 0.95
    elif estrutura == "Modular / 3E":
        fator = 0.90

    custo_construcao_base = float(area_m2) * float(custo_m2) * fator
    iva_pct = 0.06 if iva_reduzido else 0.23
    imprevistos = custo_construcao_base * (float(imprevistos_pct) / 100.0)
    iva_construcao = custo_construcao_base * float(iva_pct)

    total_construcao = (
        float(preco_terreno)
        + custo_construcao_base
        + imprevistos
        + iva_construcao
        + float(projetos_lic)
        + float(fiscalizacao)
    )

    # Usa taxa/prazo da secção Comprar (para comparar com a mesma base)
    taeg_anual = float(st.session_state.get("taeg_anual", 0.04))
    prazo_anos = int(st.session_state.get("prazo_anos", 30))

    entrada_build = total_construcao * float(entrada_pct_build)
    financiado_build = max(0.0, total_construcao - float(entrada_build))
    prest_build = calc_prestacao(financiado_build, taeg_anual, prazo_anos)
    mensal_build = float(prest_build) + float(cond_man_build)

    colX, colY = st.columns(2)

    with colX:
        st.metric("Total do projeto (estimado)", euro0(total_construcao))
        st.caption(
            f"Base: {euro0(custo_construcao_base)} | IVA: {euro0(iva_construcao)} | Imprevistos: {euro0(imprevistos)}"
        )

    with colY:
        st.metric("Entrada necessária", euro0(entrada_build))
        st.metric("Prestação estimada (crédito)", euro0(prest_build))
        st.caption(f"Mensal total (com seguros/manut.): {euro0(mensal_build)}")

    st.session_state["entrada_build"] = float(entrada_build)
    st.session_state["mensal_build"] = float(mensal_build)

    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Secção ARRENDAR
# ================================
def ui_arrendar():
    st.markdown(f"### {COPY['rent_title']}")
    st.markdown(
    f"<p style='color: var(--rc-gray-900); font-size: 0.95rem; line-height: 1.5; margin-top: -6px;'>"
    f"{COPY['rent_body']}</p>",
    unsafe_allow_html=True
)

    colL, colR = st.columns(2)
    with colL:
        renda = st.number_input("Renda (€/mês)", value=float(ss_get(K("arrendar", "renda"), 900.0)), step=10.0, min_value=0.0, key=K("arrendar", "renda_input"))
    with colR:
        inflacao_renda = st.number_input("Inflação anual da renda (%)", value=float(ss_get(K("arrendar", "infl_renda"), 3.0)), step=0.5, min_value=0.0, key=K("arrendar", "inflacao_input")) / 100.0

    st.session_state["renda"] = float(renda)
    st.session_state["inflacao_renda"] = float(inflacao_renda)

    st.caption("📌 No RumoCasa, arrendar não compete com comprar/construir — entra como fase de preparação e flexibilidade.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Arrendar como fase estratégica (copy premium)
# ================================
import textwrap

def ui_arrendar_estrategia():
    renda = float(st.session_state.get("renda", 0.0))
    poup_mensal = float(st.session_state.get("poupanca_mensal", 0.0))
    anos = int(st.session_state.get("anos_meta", 3))
    saldo_final = st.session_state.get("saldo_final_estimado", None)

    if renda <= 0 or poup_mensal <= 0:
        return

    if saldo_final is None:
        saldo_final = poup_mensal * anos * 12

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🧭 Arrendar como fase estratégica</h3>", unsafe_allow_html=True)

    html = f"""
<p style="margin:.65rem 0 .35rem 0; font-weight:600; color: var(--rc-gray-900);">
  Arrendar é uma fase estratégica — não um erro.
</p>

<p style="margin:.15rem 0 .65rem 0; color: var(--rc-gray-800);">
  <b>Arrendar não entra no “mais vantajoso”</b> porque não é aquisição.
  O que interessa aqui é: <b>quanto consegues preparar para a entrada</b> enquanto manténs flexibilidade.
</p>

<p style="margin:.65rem 0 .35rem 0; color: var(--rc-gray-800);">
  <span style="font-weight:700;">Cenário:</span>
  renda <b>{euro0(renda)}/mês</b> + poupança <b>{euro0(poup_mensal)}/mês</b> durante <b>{anos} anos</b>
  → podes acumular cerca de <b>{euro0(saldo_final)}</b> para a entrada.
</p>

<p style="margin:.35rem 0 0 0; color: #6B7280; font-size: 0.92rem;">
  Nota: ajusta a poupança mensal à tua realidade. O objetivo é transformar “arrendar” num plano com direção.
</p>
"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Comparar (apenas aquisição)
# ================================
def ui_comparar():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 Comparar aquisição</h3>", unsafe_allow_html=True)

    st.caption(
        "💡 No RumoCasa, a comparação prioriza a mensalidade — "
        "porque é ela que acompanha a tua vida todos os meses, não só no primeiro dia."
    )

    upfront_buy   = float(st.session_state.get("upfront_buy", 0.0))
    upfront_build = float(st.session_state.get("entrada_build", 0.0))
    mensal_buy    = float(st.session_state.get("mensal_compra", 0.0))
    mensal_build  = float(st.session_state.get("mensal_build", 0.0))

    if mensal_buy <= 0 and mensal_build <= 0:
        st.info("Preenche **Comprar** e/ou **Construir** para veres a comparação.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # --- KPIs ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("À cabeça (comprar)", euro0(upfront_buy))
        st.metric("Mensal (comprar)", euro0(mensal_buy))
    with col2:
        st.metric("À cabeça (construir)", euro0(upfront_build))
        st.metric("Mensal (construir)", euro0(mensal_build))

    # --- Determinar vencedor pela mensalidade ---
    winner = None
    diff = None
    if mensal_buy > 0 and mensal_build > 0:
        if mensal_buy < mensal_build:
            winner = "Comprar"
            diff = mensal_build - mensal_buy
        else:
            winner = "Construir"
            diff = mensal_buy - mensal_build

        # intensidade (0 a 1) baseada na diferença relativa
        # exemplo: diferença de 10% = 0.10 → começa a “pintar” mais
        base = max(mensal_buy, mensal_build)
        rel = (diff / base) if base > 0 else 0.0
        intensity = min(max(rel, 0.15), 0.85)  # clamp p/ ficar bonito

        st.markdown("#### 🏆 Resultado (mensalidade)")
        st.success(
            f"Mais leve no orçamento mensal: **{winner}**  "
            f"(diferença ~ {euro0(diff)}/mês)"
        )
    else:
        # se só existe 1 opção preenchida, mantém neutro
        intensity = 0.35

    # --- Dados para o gráfico ---
    data = []
    if mensal_buy > 0:
        data.append({"Opção": "Comprar", "Mensal (€)": mensal_buy})
    if mensal_build > 0:
        data.append({"Opção": "Construir", "Mensal (€)": mensal_build})

    df = pd.DataFrame(data)

    # Cor dinâmica: vencedor verde, perdedor cinza
    # Intensidade ajusta a opacidade do verde (quanto mais “compensa”, mais forte)
    green = f"rgba(15, 81, 50, {intensity:.2f})"
    gray  = "rgba(107, 114, 128, 0.35)"

    if winner:
        df["Cor"] = df["Opção"].apply(lambda x: green if x == winner else gray)
    else:
        df["Cor"] = "rgba(15, 81, 50, 0.35)"  # neutro quando só há uma opção

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Opção:N", sort=None),
            y=alt.Y("Mensal (€):Q"),
            color=alt.Color("Cor:N", scale=None, legend=None),
            tooltip=[
                alt.Tooltip("Opção:N"),
                alt.Tooltip("Mensal (€):Q", format=",.0f"),
            ],
        )
        .properties(height=260)
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Sensibilidade de juros (compra)
# ================================
def ui_sensibilidade():
    st.markdown(f"### {COPY['sens_title']}")
    st.caption(COPY["sens_body"])

    financiado = float(st.session_state.get("financiado", 0.0))
    taeg_base = float(st.session_state.get("taeg_anual", 0.04))
    prazo_anos = int(st.session_state.get("prazo_anos", 30))

    if financiado <= 0:
        st.info("Define primeiro um cenário em **Comprar** para veres a sensibilidade.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    taeg_low = max(0.0, taeg_base - 0.01)
    taeg_high = taeg_base + 0.01

    prest_low = calc_prestacao(financiado, taeg_low, prazo_anos)
    prest_base = calc_prestacao(financiado, taeg_base, prazo_anos)
    prest_high = calc_prestacao(financiado, taeg_high, prazo_anos)

    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("TAEG −1pp", euro0(prest_low))
    with colB:
        st.metric("TAEG base", euro0(prest_base))
    with colC:
        st.metric("TAEG +1pp", euro0(prest_high))

    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Formulário de leads (deploy-friendly)
# ================================
def ui_leads():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📩 Receber propostas reais</h3>", unsafe_allow_html=True)
    st.caption("Deixa os teus dados e o teu objetivo. O RumoCasa organiza o cenário e ajuda a encaminhar para parceiros (crédito / construção / mediação).")

    if "leads" not in st.session_state:
        st.session_state["leads"] = []

    with st.form("lead_form"):
        colA, colB = st.columns(2)
        with colA:
            lead_nome = st.text_input("Nome")
            lead_email = st.text_input("Email")
            lead_tel = st.text_input("Telefone (opcional)")
        with colB:
            lead_local = st.text_input("Localização / Concelho")
            lead_tipo = st.selectbox(
                "Interesse principal",
                ["Crédito Habitação", "Construção (LSF/Modular/3E)", "Arrendamento (fase estratégica)"],
            )
            lead_msg = st.text_area("Mensagem (opcional)", placeholder="Objetivo, orçamento e contexto…")

        submitted = st.form_submit_button("Quero ser contactado")
        if submitted:
            row = {
                "ts": date.today().isoformat(),
                "nome": lead_nome.strip(),
                "email": lead_email.strip(),
                "telefone": lead_tel.strip(),
                "local": lead_local.strip(),
                "tipo": lead_tipo,
                "upfront_compra": float(st.session_state.get("upfront_buy", 0.0)),
                "mensal_compra": float(st.session_state.get("mensal_compra", 0.0)),
                "entrada_constr": float(st.session_state.get("entrada_build", 0.0)),
                "mensal_constr": float(st.session_state.get("mensal_build", 0.0)),
                "renda_m1": float(st.session_state.get("renda", 0.0)),
                "msg": lead_msg.strip(),
            }
            st.session_state["leads"].append(row)
            st.success("✅ Recebido! Obrigado — vamos encaminhar o teu pedido para o parceiro mais adequado.")

    # Export (bom para demos)
    if st.session_state["leads"]:
        df_leads = pd.DataFrame(st.session_state["leads"])
        buf = io.StringIO()
        df_leads.to_csv(buf, index=False)
        st.download_button(
            "📥 Exportar pedidos (.csv)",
            data=buf.getvalue().encode("utf-8"),
            file_name="rumocasa_leads.csv",
            mime="text/csv",
            key=K("leads", "download"),
        )

    st.caption("Nota: MVP educativo. Não é aconselhamento financeiro. Valores e taxas podem variar por banco, perfil e condições.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Poupança & progresso para a entrada
# ================================
def payment_to_goal(goal, a0, months, annual_rate):
    if months <= 0:
        return 0.0
    r = annual_rate / 12.0
    if r == 0:
        return max(0.0, (goal - a0) / months)
    A = (1 + r) ** months
    return max(0.0, (goal - a0 * A) * r / (A - 1))

def ui_poupanca():
    st.markdown(f"### {COPY['save_title']}")
    st.caption(COPY["save_body"])

    goal_buy = float(st.session_state.get("upfront_buy", 0.0))
    goal_build = float(st.session_state.get("entrada_build", 0.0))
    goal = goal_buy or goal_build
    a0 = float(st.session_state.get("poup_atual", 0.0))

    c = st.number_input(
        "Poupança mensal (€)",
        min_value=0.0,
        max_value=10000.0,
        value=float(ss_get(K("poup", "mensal"), 300.0) or 300.0),
        step=50.0,
        key=K("poup", "mensal_input"),
    )

    prazo_alvo_anos = st.slider("Quero atingir a entrada em (anos)", 1, 10, value=3, key=K("poup", "anos_meta_slider"))
    prazo_alvo_meses = int(prazo_alvo_anos * 12)

    if goal <= 0:
        st.info("Define primeiro um cenário em **Comprar** ou **Construir** para calcular a meta de entrada.")
        st.session_state["poupanca_mensal"] = float(c)
        st.session_state["anos_meta"] = int(prazo_alvo_anos)
        st.session_state["saldo_final_estimado"] = float(a0 + c * prazo_alvo_meses)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    perc_atual = max(0.0, min(1.0, a0 / goal))
    pct_txt = f"{perc_atual*100:.1f}%".replace(".", ",")

    if perc_atual < 0.40:
        color, msg = "#dc3545", "🔴 Início. Um pequeno aumento mensal pode ter impacto grande no prazo."
    elif perc_atual < 0.80:
        color, msg = "#ffc107", "🟡 Bom caminho. Consistência > intensidade."
    else:
        color, msg = "#28a745", "🟢 Estás perto. Agora é evitar perder ritmo."

    st.markdown(
        f"""
        <div style="font-size:14px;margin-bottom:6px;">Já tens <b>{pct_txt}</b> da meta.</div>
        <div style="width:100%;background:#e9ecef;border-radius:10px;overflow:hidden;height:12px;">
          <div style="width:{perc_atual*100:.2f}%;height:12px;background:{color};"></div>
        </div>
        <div style="margin-top:8px;color:#495057;">{msg}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### ⏱️ Plano realista (quanto preciso por mês?)")
    need_0 = payment_to_goal(goal, a0, prazo_alvo_meses, 0.00)
    need_3 = payment_to_goal(goal, a0, prazo_alvo_meses, 0.03)
    need_6 = payment_to_goal(goal, a0, prazo_alvo_meses, 0.06)

    colx, coly, colz = st.columns(3)
    with colx:
        st.metric("Necessário/mês (0%)", euro0(need_0))
    with coly:
        st.metric("Necessário/mês (3%)", euro0(need_3))
    with colz:
        st.metric("Necessário/mês (6%)", euro0(need_6))

    if need_3 > c:
        st.caption(f"⚠️ Para cumprir em {prazo_alvo_anos} anos, falta cerca de **{euro0(need_3 - c)}/mês** (cenário 3%).")

    st.markdown("#### 💰 Simulação simples (poupança + juros)")
    taxa_opcoes = {
        "Conservador — 1,5%/ano": 0.015,
        "Segurança — 3%/ano": 0.03,
        "Crescimento — 5%/ano": 0.05,
        "Ambicioso — 7%/ano": 0.07,
    }

    taxa_sel = st.selectbox("Tipo de investimento (taxa anual)", list(taxa_opcoes.keys()), index=1, key=K("poup", "taxa_sel"))
    taxa_ano = float(taxa_opcoes.get(taxa_sel, 0.03))
    meses_sim = st.slider("Meses a simular", 6, 120, value=36, step=6, key=K("poup", "meses_sim"))

    r = taxa_ano / 12.0
    rows = []
    saldo = a0
    for m in range(1, int(meses_sim) + 1):
        juros = saldo * r
        saldo_final = saldo + juros + float(c)
        rows.append(
            {
                "Mês": m,
                "Saldo início (€)": round(saldo, 2),
                "Juros do mês (€)": round(juros, 2),
                "Poupança do mês (€)": round(float(c), 2),
                "Saldo fim (€)": round(saldo_final, 2),
            }
        )
        saldo = saldo_final

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    total_poup = float(df["Poupança do mês (€)"].sum())
    total_juros = float(df["Juros do mês (€)"].sum())
    saldo_final = float(df["Saldo fim (€)"].iloc[-1])

    st.session_state["poupanca_mensal"] = float(c)
    st.session_state["anos_meta"] = int(prazo_alvo_anos)
    st.session_state["saldo_final_estimado"] = float(saldo_final)

    falta = float(goal) - float(saldo_final)
    if falta <= 0:
        st.success("🎯 Com este plano, o valor estimado já cobre a entrada definida.")
    else:
        st.info(f"Ainda ficas a cerca de **{euro0(falta)}** da entrada. Ajusta prazo ou poupança mensal.")

    st.markdown(
        (
            f"**Total poupado (sem juros):** €{total_poup:,.0f}  |  "
            f"**Juros acumulados:** €{total_juros:,.0f}  |  "
            f"**Saldo final estimado:** €{saldo_final:,.0f}"
        ).replace(",", " ").replace(".", ",")
    )

    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        "📥 Descarregar simulação (.csv)",
        data=buf.getvalue().encode("utf-8"),
        file_name="simulacao_investimento_mes_a_mes.csv",
        mime="text/csv",
        key=K("poup", "download_csv"),
    )

    st.caption("Simulação educativa. Taxas são exemplos, não garantias. Serve para planeamento e literacia.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Parceiros
# ================================
def parceiros(perfil: dict, horiz: int = 36) -> list[dict]:
    quer_comprar = bool(perfil.get("comprar", False))
    quer_construir = bool(perfil.get("construir", False))
    quer_arrendar = bool(perfil.get("arrendar", False))
    tem_poupanca = bool(perfil.get("tem_poupanca", False))
    entrada_need = float(perfil.get("entrada_necessaria", 0.0))

    cards = []
    if quer_comprar or (tem_poupanca and entrada_need > 0):
        cards.append({"nome":"Corretor de Crédito","tag":"Banco","desc":"Comparação de condições e apoio na negociação.","url":"#","score":95})
    if quer_construir:
        cards.append({"nome":"Construtora Modular/LSF","tag":"Construtora","desc":"Orçamento rápido + apoio técnico por fases.","url":"#","score":90})
    if quer_arrendar:
        cards.append({"nome":"Portal de Arrendamento","tag":"Marketplace","desc":"Explorar zonas e preços para fase de transição.","url":"#","score":70})

    cards.sort(key=lambda c: c["score"], reverse=True)
    return cards

def ui_parceiros():
    st.markdown(f"### {COPY['partners_title']}")
    st.caption(COPY["partners_body"])

    perfil = {
        "comprar": True,
        "construir": True,
        "arrendar": True,
        "entrada_necessaria": float(st.session_state.get("upfront_buy", 0.0)) or float(st.session_state.get("entrada_build", 0.0)),
        "tem_poupanca": float(st.session_state.get("poup_atual", 0.0)) > 0,
    }

    cards = parceiros(perfil, horiz=36)
    if not cards:
        st.info("Nenhum parceiro disponível neste cenário ainda. 👀")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    cols = st.columns(min(3, len(cards)))
    for i, c in enumerate(cards):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div style="border:1px solid #e9eef5;border-radius:12px;padding:14px;">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <span style="background:#eef5ff;color:#2b6cb0;padding:2px 8px;border-radius:999px;font-size:12px;">{c['tag']}</span>
                    <div style="font-weight:700;">{c['nome']}</div>
                  </div>
                  <div style="font-size:13px;color:#495057;margin-bottom:10px;">{c['desc']}</div>
                  <a href="{c['url']}" target="_blank" style="
                      display:inline-block;background:#3b82f6;color:#fff;
                      padding:8px 12px;border-radius:8px;text-decoration:none;font-weight:600;">
                      Saber mais
                  </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# RENDER (ordem lógica)
# -------------------------------------------------
if modo_ui == COPY["layout_opt_cols"]:
    col_comp, col_constr = st.columns(2)
    with col_comp:
        ui_comprar()
    with col_constr:
        ui_construir()
else:
    tab_comp, tab_const = st.tabs(["🏠 Comprar", "🏗️ Construir"])
    with tab_comp:
        ui_comprar()
    with tab_const:
        ui_construir()

ui_arrendar()
ui_arrendar_estrategia()

ui_comparar()
ui_sensibilidade()

ui_poupanca()
ui_leads()
ui_parceiros()

ui_sticky_summary(sticky_placeholder)

st.markdown("---")
st.caption(COPY["disclaimer"])
st.markdown(f"**{COPY['closing']}**")





