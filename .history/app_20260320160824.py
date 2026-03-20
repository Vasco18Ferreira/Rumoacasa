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
    "app_title": "RumoCasa 🏡",

    "app_tagline": "Compara cenários e decide a tua casa com mais clareza.",

    "layout_label": "Como preferes ver a simulação?",
    "layout_opt_cols": "Comparação lado a lado",
    "layout_opt_tabs": "Ver por separadores",

    "hero_title": "Comprar ou construir casa? Decide com números reais.",

    "hero_subtitle": (
        "Compara cenários, estima a entrada necessária, a prestação mensal e o impacto real da tua decisão "
        "antes de avançar."
    ),

    "section_simular_title": "📊 O que queres simular?",

    "section_simular_body": (
        "Escolhe o cenário que estás a considerar e percebe, de forma clara, "
        "quanto precisas de entrada, quanto poderás pagar por mês e qual o impacto total da decisão. "
        "O RumoCasa ajuda-te a comparar com mais clareza e menos dúvida."
    ),

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




# ================================
# TIPS
# ================================
TIPS = {

    "preco_casa": "Preço do imóvel (valor do anúncio). É a base para calcular entrada, IMT e prestação.",
    "preco_hint": "Dica: usa o preço do anúncio. Se for um empreendimento novo, confirma se o valor inclui lugar de garagem/arrecadação e extras.",
    "tipo_imovel": "HPP = Habitação Própria Permanente (IMT geralmente mais baixo). Secundária = férias/investimento (IMT mais alto).",
    "novo": "Imóvel novo (contexto). No MVP não altera o IMT, mas pode ajudar em contas futuras (ex.: IVA/obras/acabamentos).",
    "entrada_pct": "Percentagem do preço paga com capitais próprios. Mais entrada = menos crédito e, em regra, prestação mais baixa.",
    "taeg": "TAEG inclui juros + comissões + seguros. É o indicador mais útil para comparar propostas de bancos.",
    "prazo": "Prazo do crédito. Mais prazo baixa a prestação, mas aumenta o total pago em juros.",
    "poup_atual": "Quanto tens disponível para a entrada. Sugestão: não misturar com fundo de emergência.",
    "condo": "Custos mensais fixos do imóvel (condomínio/manutenção). Pequenos valores acumulam e mexem no orçamento.",
    "seguros": "Seguros associados ao crédito (vida/habitação). Podem variar muito e alterar a mensalidade real.",


    "custo_avaliacao": "Custos típicos do início do processo: avaliação bancária, comissões iniciais, certidões, etc. (depende do banco).",
    "obras_mob": "Obras e/ou mobiliário inicial. Se a casa estiver pronta a habitar, pode ser 0.",
    "outros_custos": "Qualquer custo extra que queiras considerar (mudança, eletrodomésticos, pequenas reparações, etc.).",


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


    "renda": "Valor da renda mensal. Serve para perceber quanto sobra para poupar rumo à entrada.",
    "infl_renda": "Estimativa de subida anual da renda. Se não quiseres complicar, usa 0–3%.",


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

# -------------------------------------------------
# BOOT RESET — garante app limpa ao abrir
# -------------------------------------------------
if "boot_done" not in st.session_state:
    st.session_state["boot_done"] = True

    # estado UI
    st.session_state["has_results"] = False
    st.session_state["active_mode"] = None  # "comprar" | "construir"

    # resultados
    st.session_state["upfront_buy"] = 0.0
    st.session_state["mensal_compra"] = 0.0
    st.session_state["financiado"] = 0.0

    st.session_state["entrada_build"] = 0.0
    st.session_state["mensal_build"] = 0.0

    st.session_state["imt_2025"] = 0.0


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

def calc_imt_2025(valor: float, hab_pp: bool = True) -> float:
    v = float(valor)
    if v <= 0:
        return 0.0

    if not hab_pp:
        return v * 0.065  # simplificação (não-HPP)

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

def ui_wow_result(compra_entrada, compra_mensal, construir_entrada, construir_mensal):
    try:
        compra_entrada = float(compra_entrada or 0)
        compra_mensal = float(compra_mensal or 0)
        construir_entrada = float(construir_entrada or 0)
        construir_mensal = float(construir_mensal or 0)
    except Exception:
        return

    if compra_mensal <= 0 or construir_mensal <= 0:
        return

    if construir_mensal < compra_mensal:
        best_name = "Construir"
        best_monthly = construir_mensal
        best_entry = construir_entrada
        alt_name = "Comprar"
        alt_monthly = compra_mensal
        alt_entry = compra_entrada
        diff = compra_mensal - construir_mensal
        note = f"Neste cenário, construir reduz a prestação mensal em cerca de {euro0(diff)}."
    elif compra_mensal < construir_mensal:
        best_name = "Comprar"
        best_monthly = compra_mensal
        best_entry = compra_entrada
        alt_name = "Construir"
        alt_monthly = construir_mensal
        alt_entry = construir_entrada
        diff = construir_mensal - compra_mensal
        note = f"Neste cenário, comprar reduz a prestação mensal em cerca de {euro0(diff)}."
    else:
        best_name = "Empate técnico"
        best_monthly = compra_mensal
        best_entry = compra_entrada
        alt_name = "Construir"
        alt_monthly = construir_mensal
        alt_entry = construir_entrada
        diff = 0
        note = "Neste cenário, a prestação mensal estimada é muito semelhante nas duas opções."

    html = f"""
    <div class="rc-wow-wrap">
      <div class="rc-wow-title">✨ Comparação rápida do cenário</div>

      <div class="rc-wow-grid">
        <div class="rc-wow-card best">
          <div class="rc-wow-badge best">Melhor opção neste cenário</div>
          <h4>{best_name}</h4>
          <div class="rc-wow-main">{euro0(best_monthly)}</div>
          <div class="rc-wow-main-label">prestação mensal estimada</div>

          <div class="rc-wow-list">
            <div class="rc-wow-item">
              <span>Entrada estimada</span>
              <strong>{euro0(best_entry)}</strong>
            </div>
            <div class="rc-wow-item">
              <span>Mensalidade</span>
              <strong>{euro0(best_monthly)}</strong>
            </div>
          </div>
        </div>

        <div class="rc-wow-card">
          <div class="rc-wow-badge alt">Alternativa</div>
          <h4>{alt_name}</h4>
          <div class="rc-wow-main">{euro0(alt_monthly)}</div>
          <div class="rc-wow-main-label">prestação mensal estimada</div>

          <div class="rc-wow-list">
            <div class="rc-wow-item">
              <span>Entrada estimada</span>
              <strong>{euro0(alt_entry)}</strong>
            </div>
            <div class="rc-wow-item">
              <span>Mensalidade</span>
              <strong>{euro0(alt_monthly)}</strong>
            </div>
          </div>
        </div>
      </div>

      <div class="rc-wow-diff">
        <div class="rc-wow-diff-top">Diferença mensal estimada</div>
        <div class="rc-wow-diff-value">{euro0(diff)}</div>
        <div class="rc-wow-note">{note}</div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------
# ESTILO GLOBAL RUMOCASA (FORÇAR CLARO)
# -------------------------------------------------
st.markdown(
    """
<style>
:root {
    --rc-green:        #0f5132;
    --rc-green-dark:   #0b3b25;
    --rc-green-soft:   rgba(15, 81, 50, 0.12);


    --rc-gray-900:     #111827;
    --rc-gray-800:     #1f2937;
    --rc-gray-700:     #374151;
    --rc-gray-500:     #6B7280;
    --rc-gray-200:     #e5e7eb;
    --rc-bg:           #f5f5f7;
}

html, body, .stApp {
    background-color: var(--rc-bg) !important;
    color: var(--rc-gray-900) !important;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* animação suave */
@keyframes rc-fade-in-up {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.rc-fade-in { animation: rc-fade-in-up 0.55s ease-out both; }

/* header */
.rc-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 1.4rem;
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

/* cards */
.section-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.75rem;
    border: 1px solid var(--rc-gray-200);
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

/* títulos */
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

/* inputs */
.stTextInput > div > div > input,
.stNumberInput input,
.stSelectbox > div > div > select,
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
    padding: 6px 10px !important;
    font-size: 0.95rem !important;
    background: #ffffff !important;
    color: var(--rc-gray-900) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput input:focus,
.stSelectbox > div > div > select:focus,
.stTextArea textarea:focus {
    border-color: var(--rc-green) !important;
    box-shadow: 0 0 0 2px var(--rc-green-soft) !important;
    outline: none !important;
}

/* botões */
.stButton>button, .stDownloadButton>button {
    background-color: var(--rc-green) !important;
    color: #ffffff !important;
    border-radius: 999px !important;
    border: none !important;
    padding: 0.45rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    cursor: pointer !important;
    transition: all 0.15s ease-in-out !important;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: var(--rc-green-dark) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 18px rgba(15, 81, 50, 0.35) !important;
}

/* métricas */
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    padding: 12px !important;
    border-radius: 12px !important;
    border: 1px solid var(--rc-gray-200) !important;
}

/* sticky bar */
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

/* ===========================
   HERO SECTION (PREMIUM)
=========================== */

.rc-hero{
  background:
    radial-gradient(circle at top left, rgba(34,197,94,0.12), transparent 35%),
    linear-gradient(180deg, rgba(255,255,255,1), rgba(249,250,251,0.96));
  padding: 3.2rem 1.4rem 2.6rem 1.4rem;
  border-radius: 24px;
  text-align: center;
  margin-bottom: 2rem;
  border: 1px solid rgba(229,231,235,0.9);
  box-shadow: 0 18px 50px rgba(15,23,42,0.08);
}

.rc-hero-inner{
  max-width: 760px;
  margin: 0 auto;
}

.rc-hero-badge{
  display: inline-block;
  background: #ffffff;
  color: #0f5132;
  border: 1px solid rgba(16,185,129,0.25);
  padding: 0.45rem 0.85rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 1rem;
  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

.rc-hero-inner h1{
  font-size: 2.7rem;
  line-height: 1.15;
  font-weight: 850;
  margin: 0 0 0.75rem 0;
  color: #111827;
  letter-spacing: -0.02em;
}

.rc-hero-sub{
  font-size: 1.08rem;
  color: #4b5563;
  line-height: 1.7;
  margin: 0 auto;
  max-width: 700px;
}

.rc-hero-points{
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.rc-hero-points span{
  background: #ffffff;
  border: 1px solid #e5e7eb;
  padding: 0.55rem 0.85rem;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}

/* ===========================
   RESULTADO WOW
=========================== */

.rc-wow-wrap{
  margin: 1.1rem 0 1.6rem 0;
  animation: rc-fade-in-up 0.5s ease-out both;
}

.rc-wow-title{
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--rc-gray-900);
  margin-bottom: 0.9rem;
}

.rc-wow-grid{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.rc-wow-card{
  background: #ffffff;
  border: 1px solid var(--rc-gray-200);
  border-radius: 20px;
  padding: 1.2rem 1.2rem 1rem 1.2rem;
  box-shadow: 0 16px 35px rgba(15,23,42,0.06);
}

.rc-wow-card.best{
  border: 2px solid rgba(34,197,94,0.55);
  background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%);
  box-shadow: 0 20px 40px rgba(34,197,94,0.12);
}

.rc-wow-badge{
  display: inline-block;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
  margin-bottom: 0.7rem;
}

.rc-wow-badge.best{
  background: rgba(34,197,94,0.14);
  color: #166534;
}

.rc-wow-badge.alt{
  background: #f3f4f6;
  color: #374151;
}

.rc-wow-card h4{
  margin: 0 0 0.6rem 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #111827;
}

.rc-wow-main{
  font-size: 1.9rem;
  font-weight: 850;
  color: #111827;
  line-height: 1.1;
  margin-bottom: 0.2rem;
}

.rc-wow-main-label{
  font-size: 0.88rem;
  color: #6b7280;
  margin-bottom: 0.9rem;
}

.rc-wow-list{
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.rc-wow-item{
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.95rem;
  color: #374151;
}

.rc-wow-item strong{
  color: #111827;
}

.rc-wow-diff{
  margin-top: 1rem;
  background: linear-gradient(90deg, rgba(15,81,50,0.08), rgba(255,255,255,1));
  border: 1px solid rgba(15,81,50,0.12);
  border-radius: 18px;
  padding: 0.95rem 1rem;
}

.rc-wow-diff-top{
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.rc-wow-diff-value{
  font-size: 1.2rem;
  font-weight: 800;
  color: #0f5132;
}

.rc-wow-note{
  margin-top: 0.45rem;
  font-size: 0.93rem;
  color: #374151;
}

@media (max-width: 900px){
  .rc-wow-grid{
    grid-template-columns: 1fr;
  }
}

</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="rc-hero rc-fade-in">
      <div class="rc-hero-inner">

        <div class="rc-hero-badge">
          Planeador habitacional inteligente
        </div>

        <h1>{COPY["hero_title"]}</h1>

        <p class="rc-hero-sub">
          {COPY["hero_subtitle"]}
        </p>

        <div class="rc-hero-points">
          <span>📊 Comparação simples</span>
          <span>💰 Estimativas claras</span>
          <span>🧠 Decisão mais segura</span>
        </div>

      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Estado UI (uma vez)
# -------------------------------------------------
if "active_mode" not in st.session_state:
    st.session_state["active_mode"] = None

if "buy_done" not in st.session_state:
    st.session_state["buy_done"] = False

if "build_done" not in st.session_state:
    st.session_state["build_done"] = False


# -------------------------------------------------
# Reset manual (Nova simulação)
# -------------------------------------------------
colR1, colR2 = st.columns([1, 3])

with colR1:
    if st.button("🔄 Nova simulação", use_container_width=True):

        # 1) limpar resultados (pôr a 0)
        keys_to_zero = [
            "upfront_buy", "mensal_compra", "financiado", "imt_2025",
            "entrada_build", "mensal_build",
        ]
        for k in keys_to_zero:
            st.session_state[k] = 0.0

        # 2) estado da UI
        st.session_state["buy_done"] = False
        st.session_state["build_done"] = False
        st.session_state["active_mode"] = None

        # 3) limpar inputs (para não ficarem valores antigos nos campos)
        keys_to_pop = [
            # comprar
            K("comprar", "preco_casa_input"),
            K("comprar", "entrada_pct_input"),
            K("comprar", "taeg_input"),
            K("comprar", "prazo_input"),
            K("comprar", "condo_input"),
            K("comprar", "seguros_input"),
            K("comprar", "custo_avaliacao_input"),
            K("comprar", "obras_mob_input"),
            K("comprar", "outros_extra_input"),

            # construir
            K("construir", "preco_terreno_input"),
            K("construir", "estrutura"),
            K("construir", "area_m2_input"),
            K("construir", "custo_m2_input"),
            K("construir", "proj_input"),
            K("construir", "fisc_input"),
            K("construir", "cond_build_input"),
            K("construir", "prazo_obra"),
            K("construir", "iva_reduzido"),
            K("construir", "imp_prev"),
        ]
        for k in keys_to_pop:
            st.session_state.pop(k, None)

        st.rerun()


# -------------------------------------------------
# Sticky Summary — último calculado
# -------------------------------------------------
def ui_sticky_summary(container):

    mode = st.session_state.get("active_mode")

    if mode == "comprar" and st.session_state.get("buy_done", False):
        entrada = float(st.session_state.get("upfront_buy", 0.0) or 0.0)
        mensal  = float(st.session_state.get("mensal_compra", 0.0) or 0.0)

    elif mode == "construir" and st.session_state.get("build_done", False):
        entrada = float(st.session_state.get("entrada_build", 0.0) or 0.0)
        mensal  = float(st.session_state.get("mensal_build", 0.0) or 0.0)

    else:
        return

    if entrada <= 0 or mensal <= 0:
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


# placeholder + render (tem de vir DEPOIS da função)
sticky_placeholder = st.empty()
ui_sticky_summary(sticky_placeholder)


# -------------------------------------------------
# Toggle UI
# -------------------------------------------------
st.markdown("<div class='section-card' style='padding: 1rem 1.25rem; margin-top: -0.75rem;'>", unsafe_allow_html=True)
modo_ui = st.radio(
    COPY["layout_label"],
    [COPY["layout_opt_cols"], COPY["layout_opt_tabs"]],
    horizontal=True,
)
st.markdown("</div>", unsafe_allow_html=True)


# ================================
# Secção COMPRAR
# ================================

def ui_comprar():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### {COPY['buy_title']}")
    st.caption(COPY["buy_body"])

    # ----------------------------
    # FORM (inputs)
    # ----------------------------
    with st.form("form_comprar", clear_on_submit=False):

        colL, colR = st.columns(2)

        with colL:
            preco_casa = st.number_input(
                "Preço da casa (€)",
                step=1000,
                min_value=10000,
                value=int(ss_get(K("comprar", "preco_casa"), 200_000)),
                help=TIPS["preco_casa"],
                key=K("comprar", "preco_casa_input"),
            )
            st.caption("💡 " + TIPS["preco_hint"])

        with colR:
            tipo_imovel = st.selectbox(
                "Tipo de imóvel",
                ["Habitação Própria Permanente", "Secundária"],
                help=TIPS["tipo_imovel"],
                key=K("comprar", "tipo_imovel"),
                index=0,
            )

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

        with colB:
            taeg_anual = st.number_input(
                "Taxa anual (TAEG %)",
                min_value=0.0,
                value=float(ss_get(K("comprar", "taeg"), 4.0)),
                step=0.1,
                help=TIPS["taeg"],
                key=K("comprar", "taeg_input"),
            ) / 100.0

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

        with st.expander("➕ Custos adicionais (opcional, mas recomendado)", expanded=False):
            custo_avaliacao = st.number_input(
                "Avaliação + despesas iniciais (€)",
                min_value=0,
                step=50,
                value=int(ss_get(K("comprar", "custo_avaliacao"), 1000)),
                help=TIPS["custo_avaliacao"],
                key=K("comprar", "custo_avaliacao_input"),
            )
            obras_mob = st.number_input(
                "Obras / mobiliário inicial (€)",
                min_value=0,
                step=250,
                value=int(ss_get(K("comprar", "obras_mob"), 0)),
                help=TIPS["obras_mob"],
                key=K("comprar", "obras_mob_input"),
            )
            outros_extra = st.number_input(
                "Outros custos (€)",
                min_value=0,
                step=100,
                value=int(ss_get(K("comprar", "outros_extra"), 0)),
                help=TIPS["outros_custos"],
                key=K("comprar", "outros_extra_input"),
            )

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

        submitted = st.form_submit_button("✅ Calcular compra", use_container_width=True)

    # ----------------------------
    # CÁLCULOS (só quando clica)
    # ----------------------------
    if not submitted:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    is_hpp = (tipo_imovel == "Habitação Própria Permanente")
    imt = calc_imt_2025(preco_casa, hab_pp=is_hpp)
    selo = 0.008 * float(preco_casa)

    escritura_regs = 1000.0

    custos_extra = float(custo_avaliacao) + float(obras_mob) + float(outros_extra)
    custos_compra = float(imt) + float(selo) + float(escritura_regs) + float(custos_extra)

    entrada = float(preco_casa) * float(entrada_pct)
    financiado = max(0.0, float(preco_casa) - entrada)
    prestacao = calc_prestacao(financiado, taeg_anual, prazo_anos)

    mensal_compra = float(prestacao) + float(condo) + float(seguros)
    upfront_buy = float(entrada) + float(custos_compra)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Entrada necessária (entrada + impostos/custos)", euro0(upfront_buy))
        st.caption(
            f"IMT 2025: {euro0(imt)} | Selo: {euro0(selo)} | Escritura/registos: {euro0(escritura_regs)} | Extras: {euro0(custos_extra)}"
        )
    
    with col2:
        st.metric("Prestação (crédito)", euro0(prestacao))
        st.metric("Mensal total (com custos)", euro0(mensal_compra))

# ----------------------------
    # Guardar resultados (para sticky/comparar)
    # ----------------------------
    st.session_state["upfront_buy"]   = float(upfront_buy)
    st.session_state["mensal_compra"] = float(mensal_compra)
    st.session_state["financiado"]    = float(financiado)
    st.session_state["imt_2025"]      = float(imt)

    # Para o construir usar a mesma base (TAEG/prazo)
    st.session_state["taeg_anual"]  = float(taeg_anual)
    st.session_state["prazo_anos"]  = int(prazo_anos)

    # Estado UI (sticky + último calculado)
    st.session_state["has_results"] = True
    st.session_state["active_mode"] = "comprar"

    st.success("Cenário de compra calculado ✅")
    st.markdown("</div>", unsafe_allow_html=True)


# ================================
# Secção CONSTRUIR (v3) — dinâmico + sem URL
# ================================
def ui_construir():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### {COPY['build_title']}")
    st.caption(COPY["build_body"])

    # ----------------------------
    # Sistemas (defaults 2026 - editáveis)
    # Nota: defaults são ponto de partida (mercado varia).
    # ----------------------------

    SYSTEMS = {
        "Convencional": {
            "custo_m2_default": 1200,
            "fator": 1.00,
            "prazo_meses_default": 14,
            "pros": [
                "Mais comum e fácil de comparar orçamentos",
                "Boa aceitação bancária/seguradoras",
                "Flexível em projeto e alterações",
            ],
            "cons": [
                "Normalmente mais lento",
                "Maior risco de derrapagens (mão de obra/atrasos)",
                "Dependente de equipas e disponibilidade local",
            ],
        },
        "LSF (aço leve)": {
            "custo_m2_default": 1100,
            "fator": 0.95,
            "prazo_meses_default": 10,
            "pros": [
                "Construção mais rápida e previsível",
                "Obra mais “seca” (menos tempos de cura)",
                "Boa eficiência térmica (depende do detalhe do sistema)",
            ],
            "cons": [
                "Qualidade depende MUITO do fabricante/montagem",
                "Menos fornecedores (comparação pode ser difícil)",
                "Detalhes (pontes térmicas/isolamentos) são críticos",
            ],
        },
        "Modular / 3E": {
            "custo_m2_default": 1050,
            "fator": 0.92,
            "prazo_meses_default": 8,
            "pros": [
                "Prazo geralmente mais curto",
                "Maior controlo industrial (consistência)",
                "Menos variáveis em obra (depende do modelo)",
            ],
            "cons": [
                "Logística/transportes podem pesar (acessos)",
                "Limitações de personalização (alguns fornecedores)",
                "Prazos dependem da fila de produção",
            ],
        },
        "Madeira / CLT": {
            "custo_m2_default": 1350,
            "fator": 1.03,
            "prazo_meses_default": 9,
            "pros": [
                "Rápida (sistemas industrializados)",
                "Conforto térmico/acústico excelente (bem executado)",
                "Pegada carbónica potencialmente menor",
            ],
            "cons": [
                "Pode ser mais caro (material + detalhe + acabamentos)",
                "Exige bom projeto de humidades/ventilação",
                "Nem todos os bancos/seguros tratam igual (varia)",
            ],
        },
    }

    # ----------------------------
    # 1) Escolha do sistema FORA do form (para ser dinâmico)
    # ----------------------------
    colA, colB = st.columns([1.2, 1.0])
    with colA:
        estrutura = st.selectbox(
            "Sistema construtivo",
            list(SYSTEMS.keys()),
            help=TIPS["estrutura"],
            key=K("construir", "estrutura"),
            index=0,
        )

    # prós/contras dinâmicos (já atualiza ao mudar o selectbox)
    st.markdown("##### ✅ Prós & ❗Contras (para decidir rápido)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Vantagens**")
        for p in SYSTEMS[estrutura]["pros"]:
            st.write(f"• {p}")
    with c2:
        st.markdown("**Pontos de atenção**")
        for c in SYSTEMS[estrutura]["cons"]:
            st.write(f"• {c}")

    st.caption(
        "📌 Nota 2026: custos variam muito por acabamentos e zona. "
        "Usa estes valores como ponto de partida e ajusta com orçamentos reais."
    )

    st.divider()

    # ----------------------------
    # 2) FORM: inputs (só calcula quando clicas)
    # ----------------------------
    with st.form("form_construir", clear_on_submit=False):
        colL, colR = st.columns(2)

        with colL:
            preco_terreno = st.number_input(
                "Preço do terreno (€)",
                step=1000,
                min_value=0,
                value=int(ss_get(K("construir", "preco_terreno"), 50_000)),
                help=TIPS["preco_terreno"],
                key=K("construir", "preco_terreno_input"),
            )

        with colR:
            area_m2 = st.number_input(
                "Área útil (m²)",
                min_value=40,
                value=int(ss_get(K("construir", "area_m2"), 120)),
                step=5,
                help=TIPS["area_m2"],
                key=K("construir", "area_m2_input"),
            )

            # default do custo/m² depende do sistema (editável)
            custo_m2_default = int(SYSTEMS[estrutura]["custo_m2_default"])
            custo_m2 = st.number_input(
                "Custo base construção (€/m²)",
                min_value=600,
                value=int(ss_get(K("construir", "custo_m2"), custo_m2_default)),
                step=50,
                help=TIPS["custo_m2"],
                key=K("construir", "custo_m2_input"),
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            iva_reduzido = st.checkbox(
                "IVA reduzido (ex.: 6%)",
                value=bool(ss_get(K("construir", "iva_red"), False)),
                help=(
                    "⚠️ Nem toda a construção nova tem IVA 6%. "
                    "Em geral, 6% aplica-se em situações específicas (ex.: certas empreitadas de reabilitação/ARU). "
                    "Confirma com técnico/contabilista."
                ),
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
            prazo_default = int(SYSTEMS[estrutura]["prazo_meses_default"])
            prazo_obra_meses = st.slider(
                "Prazo de obra (meses)",
                6,
                24,
                value=int(ss_get(K("construir", "obra_meses"), prazo_default)),
                help=TIPS["prazo_obra"],
                key=K("construir", "prazo_obra"),
            )

        submitted = st.form_submit_button("✅ Calcular construção", use_container_width=True)


    if not submitted:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ----------------------------
    # Cálculo (não apaga Comprar)
    # ----------------------------
    fator = float(SYSTEMS[estrutura]["fator"])

    custo_construcao_base = float(area_m2) * float(custo_m2) * fator

    iva_pct = 0.06 if iva_reduzido else 0.23

    iva_construcao = custo_construcao_base * float(iva_pct)


    imprevistos = custo_construcao_base * (float(imprevistos_pct) / 100.0)

    total_construcao = (
        float(preco_terreno)
        + custo_construcao_base
        + imprevistos
        + iva_construcao
        + float(projetos_lic)
        + float(fiscalizacao)
    )

    # usa a taxa/prazo calculados em Comprar (se existirem)
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

    # guardar resultados SEM mexer nos de comprar
    st.session_state["entrada_build"] = float(entrada_build)
    st.session_state["mensal_build"] = float(mensal_build)

    # estado UI
    st.session_state["has_results"] = True
    st.session_state["active_mode"] = "construir"

    st.success("Cenário de construção calculado ✅")
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

    upfront_buy   = float(st.session_state.get("upfront_buy", 0.0) or 0.0)
    upfront_build = float(st.session_state.get("entrada_build", 0.0) or 0.0)
    mensal_buy    = float(st.session_state.get("mensal_compra", 0.0) or 0.0)
    mensal_build  = float(st.session_state.get("mensal_build", 0.0) or 0.0)

    if mensal_buy <= 0 and mensal_build <= 0:
        st.info("Preenche **Comprar** e/ou **Construir** para veres a comparação.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if mensal_buy > 0 and mensal_build > 0:
        ui_wow_result(
            upfront_buy,
            mensal_buy,
            upfront_build,
            mensal_build,
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("À cabeça (comprar)", euro0(upfront_buy))
            st.metric("Mensal (comprar)", euro0(mensal_buy))
        with col2:
            st.metric("À cabeça (construir)", euro0(upfront_build))
            st.metric("Mensal (construir)", euro0(mensal_build))

        st.markdown("#### 🧭 Nota")
        st.info("Só uma das opções está preenchida — completa a outra para comparar lado a lado.")

    st.markdown("</div>", unsafe_allow_html=True)


# ================================
# Conforto mensal (guia)
# ================================
def ui_conforto_mensal():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🧾 Cabe no teu conforto mensal?</h3>", unsafe_allow_html=True)

    st.caption("✅ Define um valor de conforto (o máximo que te sentes bem a pagar por mês). O RumoCasa compara com a mensalidade do teu cenário.")

    mensal_buy   = float(st.session_state.get("mensal_compra", 0.0))
    mensal_build = float(st.session_state.get("mensal_build", 0.0))

    # escolher a mensalidade "ativa"
    mensal = 0.0
    label = ""
    if mensal_buy > 0 and mensal_build > 0:
        # se já tens comparação, usa a menor (mais “provável” no teu cenário)
        if mensal_buy <= mensal_build:
            mensal = mensal_buy
            label = "Comprar"
        else:
            mensal = mensal_build
            label = "Construir"
    elif mensal_buy > 0:
        mensal = mensal_buy
        label = "Comprar"
    elif mensal_build > 0:
        mensal = mensal_build
        label = "Construir"

    if mensal <= 0:
        st.info("Preenche **Comprar** e/ou **Construir** primeiro para o RumoCasa avaliar o conforto mensal.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    conforto = st.number_input(
        "O teu conforto mensal (€)",
        min_value=0,
        step=25,
        value=int(st.session_state.get("conforto_mensal", 900)),
        help="Não é o 'máximo possível'. É o máximo que te deixa tranquilo mês após mês.",
        key="conforto_mensal_input",
    )
    st.session_state["conforto_mensal"] = float(conforto)

    folga = float(conforto) - float(mensal)

    st.markdown("### 📌 Resultado")
    if folga >= 0:
        st.success(
            f"Com este cenário (**{label}**), a mensalidade estimada é **{euro0(mensal)}** — "
            f"fica **dentro** do teu conforto (folga ~ **{euro0(folga)} / mês**)."
        )
        st.caption("💡 Dica: usa parte da folga para poupança/segurança (imprevistos, manutenção, taxas futuras).")
    else:
        st.warning(
            f"Com este cenário (**{label}**), a mensalidade estimada é **{euro0(mensal)}** — "
            f"fica **acima** do teu conforto (diferença ~ **{euro0(abs(folga))} / mês**)."
        )
        st.caption("💡 Caminhos típicos: aumentar entrada, reduzir preço alvo, alongar prazo, ou baixar TAEG (negociação).")

    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# Sensibilidade de juros (compra)
# ================================
def ui_sensibilidade():
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>{COPY['sens_title']}</h3>", unsafe_allow_html=True)
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

    st.caption("💡 Isto mostra o risco/impacto se as taxas mexerem. Uma diferença de 1pp pode alterar bastante a prestação.")

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

ui_conforto_mensal()   # 🧠 decisão emocional / vida real
ui_sensibilidade()     # 📉 risco financeiro

ui_poupanca()         # 🎯 plano de ação
ui_leads()
ui_parceiros()

ui_sticky_summary(sticky_placeholder)

st.markdown("---")
st.caption(COPY["disclaimer"])
st.markdown(f"**{COPY['closing']}**")





