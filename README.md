# Simula a tua Casa — MVP (Streamlit)

Este é um MVP simples para simular **entrada necessária, custos à cabeça, prestação de crédito** e **comparação arrendar vs comprar**, com a opção de **colar o link** de um anúncio (placeholder no MVP).

## Como executar localmente
1) Crie um ambiente virtual (opcional, recomendado):
```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```
2) Instale dependências:
```
pip install -r requirements.txt
```
3) Execute a app:
```
streamlit run app.py
```
4) A app vai abrir no browser (URL local).

## Notas
- Este MVP usa **custos de compra** como **% do preço** (ajustável). Em versões futuras, trocamos por **cálculo de IMT + Selo + Escritura** por escalões reais.
- O campo **colar URL** tenta **inferir preço** se existir um número claro no link. Nas próximas iterações, faremos scraping leve do anúncio.
- O botão "Gerar resumo" cria um **CSV** com o cenário para partilhar/guardar.
