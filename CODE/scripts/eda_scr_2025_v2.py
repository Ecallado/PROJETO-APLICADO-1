# -*- coding: utf-8 -*-
"""
Etapa 2 - Análise Exploratória de Dados (EDA)
Dataset: SCR.data / operações de crédito no Brasil - ano de 2025

Objetivo do script
------------------
1. Ler todos os arquivos mensais scrdata_2025*.csv.
2. Consolidar o dataset em um único DataFrame.
3. Calcular estatísticas descritivas das colunas numéricas:
   - média
   - mediana
   - moda
   - quartil 1 (Q1)
   - quartil 3 (Q3)
   - desvio-padrão
   - mínimo
   - máximo
4. Gerar resumos mensais e por categorias.
5. Gerar gráficos para apoiar a análise exploratória.

Como usar
---------
1. Coloque este arquivo na mesma pasta dos CSVs de 2025.
2. Execute:
      python eda_scr_2025_v2.py
3. Verifique a pasta "eda_outputs" e a pasta "graficos".

Observação
----------
A coluna "numero_de_operacoes" contém o valor -1 em vários registros.
Esse valor foi mantido na base, pois parece representar um código do
próprio dataset (por exemplo, indisponibilidade ou regra de divulgação).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ARQUIVOS = sorted(Path(".").glob("scrdata_2025*.csv"))
OUTDIR = Path("eda_outputs")
GRAFICOS_DIR = Path("graficos")

OUTDIR.mkdir(exist_ok=True)
GRAFICOS_DIR.mkdir(exist_ok=True)

COLUNAS_NUMERICAS = [
    "numero_de_operacoes",
    "a_vencer_ate_90_dias",
    "a_vencer_de_91_ate_360_dias",
    "a_vencer_de_361_ate_1080_dias",
    "a_vencer_de_1081_ate_1800_dias",
    "a_vencer_de_1801_ate_5400_dias",
    "a_vencer_acima_de_5400_dias",
    "carteira_a_vencer",
    "vencido_de_15_ate_90_dias",
    "vencido_acima_de_90_dias",
    "carteira_vencida",
    "carteira_ativa",
    "carteira_inadimplencia",
    "ativo_problematico",
]

COLUNAS_CATEGORICAS = [
    "uf",
    "segmento",
    "cliente",
    "cnae_ocupacao",
    "porte",
    "modalidade",
    "submodalidade",
    "origem",
    "indexador",
]


def carregar_arquivos() -> pd.DataFrame:
    """Lê todos os CSVs de 2025 e consolida em um único DataFrame."""
    if not ARQUIVOS:
        raise FileNotFoundError(
            "Nenhum arquivo 'scrdata_2025*.csv' foi encontrado na pasta atual."
        )

    dfs = []
    for caminho in ARQUIVOS:
        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="utf-8-sig",
            decimal=",",
        )
        df["arquivo_origem"] = caminho.name
        dfs.append(df)

    base = pd.concat(dfs, ignore_index=True)
    base["data_base"] = pd.to_datetime(base["data_base"])
    return base


def validar_consistencia(df: pd.DataFrame) -> dict:
    """Executa validações básicas de coerência matemática da base."""
    quebra_carteira_ativa = (
        (df["carteira_ativa"] - (df["carteira_a_vencer"] + df["carteira_vencida"])).round(2) != 0
    ).sum()

    quebra_carteira_vencida = (
        (df["carteira_vencida"] - (df["vencido_de_15_ate_90_dias"] + df["vencido_acima_de_90_dias"])).round(2) != 0
    ).sum()

    return {
        "quebras_carteira_ativa": int(quebra_carteira_ativa),
        "quebras_carteira_vencida": int(quebra_carteira_vencida),
    }


def gerar_resumo_estrutura(df: pd.DataFrame) -> None:
    """Gera um resumo geral da estrutura do dataset."""
    resumo = {
        "arquivos_analisados": [p.name for p in ARQUIVOS],
        "total_arquivos": len(ARQUIVOS),
        "total_linhas": int(len(df)),
        "total_colunas": int(df.shape[1]),
        "periodo_inicial": str(df["data_base"].min().date()),
        "periodo_final": str(df["data_base"].max().date()),
        "nulos_total": int(df.isna().sum().sum()),
        "duplicatas_total": int(df.drop(columns=["arquivo_origem"]).duplicated().sum()),
        "valor_-1_em_numero_de_operacoes": int((df["numero_de_operacoes"] == -1).sum()),
        "distintos_categoricos": {col: int(df[col].nunique()) for col in COLUNAS_CATEGORICAS},
        "consistencia": validar_consistencia(df),
    }

    with open(OUTDIR / "resumo_estrutura.json", "w", encoding="utf-8") as arquivo:
        json.dump(resumo, arquivo, ensure_ascii=False, indent=2)


def gerar_estatistica_descritiva(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estatísticas descritivas para cada coluna numérica:
    média, mediana, moda, quartis, desvio-padrão, mínimo e máximo.
    """
    linhas = []

    for coluna in COLUNAS_NUMERICAS:
        serie = df[coluna]
        moda = serie.mode(dropna=True)

        linhas.append(
            {
                "coluna": coluna,
                "media": serie.mean(),
                "mediana": serie.median(),
                "moda": moda.iloc[0] if not moda.empty else np.nan,
                "q1": serie.quantile(0.25),
                "q3": serie.quantile(0.75),
                "desvio_padrao": serie.std(),
                "minimo": serie.min(),
                "maximo": serie.max(),
            }
        )

    estatistica = pd.DataFrame(linhas)
    estatistica.to_csv(
        OUTDIR / "estatistica_descritiva.csv",
        index=False,
        encoding="utf-8-sig",
    )
    return estatistica


def gerar_resumos_analiticos(df: pd.DataFrame) -> None:
    """Gera resumos mensais e por categorias relevantes."""
    resumo_mensal = (
        df.groupby("data_base")[["carteira_ativa", "carteira_inadimplencia", "ativo_problematico"]]
        .sum()
        .reset_index()
        .sort_values("data_base")
    )
    resumo_mensal["tx_inadimplencia"] = (
        resumo_mensal["carteira_inadimplencia"] / resumo_mensal["carteira_ativa"]
    )
    resumo_mensal["tx_problematico"] = (
        resumo_mensal["ativo_problematico"] / resumo_mensal["carteira_ativa"]
    )
    resumo_mensal.to_csv(OUTDIR / "resumo_mensal.csv", index=False, encoding="utf-8-sig")

    resumo_uf = (
        df.groupby("uf")[["carteira_ativa", "carteira_inadimplencia"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_uf["tx_inadimplencia"] = resumo_uf["carteira_inadimplencia"] / resumo_uf["carteira_ativa"]
    resumo_uf.to_csv(OUTDIR / "resumo_uf.csv", encoding="utf-8-sig")

    resumo_cliente = (
        df.groupby("cliente")[["carteira_ativa", "carteira_inadimplencia", "ativo_problematico"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_cliente["tx_inadimplencia"] = resumo_cliente["carteira_inadimplencia"] / resumo_cliente["carteira_ativa"]
    resumo_cliente["tx_problematico"] = resumo_cliente["ativo_problematico"] / resumo_cliente["carteira_ativa"]
    resumo_cliente.to_csv(OUTDIR / "resumo_cliente.csv", encoding="utf-8-sig")

    resumo_segmento = (
        df.groupby("segmento")[["carteira_ativa", "carteira_inadimplencia"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_segmento["tx_inadimplencia"] = resumo_segmento["carteira_inadimplencia"] / resumo_segmento["carteira_ativa"]
    resumo_segmento.to_csv(OUTDIR / "resumo_segmento.csv", encoding="utf-8-sig")


def gerar_graficos(df: pd.DataFrame) -> None:
    """Cria gráficos para apoiar a análise exploratória."""
    resumo_mensal = (
        df.groupby("data_base")[["carteira_ativa", "carteira_inadimplencia", "ativo_problematico"]]
        .sum()
        .reset_index()
        .sort_values("data_base")
    )
    resumo_mensal["tx_inadimplencia"] = resumo_mensal["carteira_inadimplencia"] / resumo_mensal["carteira_ativa"]

    meses = resumo_mensal["data_base"].dt.strftime("%m/%Y")

    plt.figure(figsize=(10, 5))
    plt.plot(meses, resumo_mensal["carteira_ativa"] / 1e12, marker="o")
    plt.title("Carteira ativa total por mês (R$ trilhões)")
    plt.xlabel("Mês de referência")
    plt.ylabel("R$ trilhões")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "grafico_carteira_ativa_mes.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(meses, resumo_mensal["tx_inadimplencia"] * 100, marker="o")
    plt.title("Taxa de inadimplência por mês (%)")
    plt.xlabel("Mês de referência")
    plt.ylabel("% da carteira ativa")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "grafico_taxa_inadimplencia_mes.png", dpi=180)
    plt.close()

    resumo_uf = (
        df.groupby("uf")[["carteira_ativa"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
        .head(10)
        .sort_values("carteira_ativa", ascending=True)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(resumo_uf.index, resumo_uf["carteira_ativa"] / 1e12)
    plt.title("Top 10 UFs por carteira ativa acumulada em 2025")
    plt.xlabel("R$ trilhões")
    plt.ylabel("UF")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "grafico_top10_ufs.png", dpi=180)
    plt.close()

    resumo_cliente = (
        df.groupby("cliente")[["carteira_ativa", "carteira_inadimplencia"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_cliente["tx_inadimplencia"] = resumo_cliente["carteira_inadimplencia"] / resumo_cliente["carteira_ativa"]

    plt.figure(figsize=(8, 5))
    plt.bar(resumo_cliente.index.astype(str), resumo_cliente["tx_inadimplencia"] * 100)
    plt.title("Taxa de inadimplência por tipo de cliente")
    plt.xlabel("Tipo de cliente")
    plt.ylabel("% da carteira ativa")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "grafico_taxa_cliente.png", dpi=180)
    plt.close()


def main() -> None:
    df = carregar_arquivos()
    gerar_resumo_estrutura(df)
    gerar_estatistica_descritiva(df)
    gerar_resumos_analiticos(df)
    gerar_graficos(df)
    print("EDA concluída com sucesso.")
    print("Arquivos gerados nas pastas 'eda_outputs' e 'graficos'.")


if __name__ == "__main__":
    main()
