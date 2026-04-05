# -*- coding: utf-8 -*-
"""
Etapa 2 - Análise Exploratória de Dados (EDA)
Dataset: SCR.data / operações de crédito no Brasil - ano de 2025

O script foi ajustado para a estrutura real do repositório:
- CODE/dados_brutos/
- CODE/scripts/
- DOC/materiais_auxiliares/tabelas_eda/
- DOC/materiais_auxiliares/graficos_eda/

Ele também funciona se for executado fora do repositório, desde que os CSVs
estejam na mesma pasta do script ou na pasta atual.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

SCRIPT_DIR = Path(__file__).resolve().parent
CWD = Path.cwd().resolve()


def encontrar_raiz_repositorio() -> Path | None:
    """Tenta localizar a raiz do repositório a partir do script e da pasta atual."""
    candidatos = [SCRIPT_DIR, CWD, *SCRIPT_DIR.parents, *CWD.parents]
    vistos: set[Path] = set()

    for base in candidatos:
        if base in vistos:
            continue
        vistos.add(base)
        if (base / "CODE" / "dados_brutos").exists():
            return base
    return None


REPO_ROOT = encontrar_raiz_repositorio()


def resolver_pasta_dados() -> Path:
    """Localiza onde estão os CSVs."""
    candidatos = []
    if REPO_ROOT:
        candidatos.append(REPO_ROOT / "CODE" / "dados_brutos")
    candidatos.extend([SCRIPT_DIR, CWD])

    for pasta in candidatos:
        if any(pasta.glob("scrdata_2025*.csv")):
            return pasta

    raise FileNotFoundError(
        "Nenhum arquivo 'scrdata_2025*.csv' foi encontrado. "
        "Verifique se os dados estão em CODE/dados_brutos/ ou na mesma pasta do script."
    )


DADOS_DIR = resolver_pasta_dados()

if REPO_ROOT:
    TABELAS_DIR = REPO_ROOT / "DOC" / "materiais_auxiliares" / "tabelas_eda"
    GRAFICOS_DIR = REPO_ROOT / "DOC" / "materiais_auxiliares" / "graficos_eda"
else:
    TABELAS_DIR = SCRIPT_DIR / "eda_outputs"
    GRAFICOS_DIR = SCRIPT_DIR / "graficos"

TABELAS_DIR.mkdir(parents=True, exist_ok=True)
GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)


def localizar_arquivos_csv() -> list[Path]:
    """Prioriza arquivos divididos em partes; se não existirem, usa os arquivos mensais completos."""
    arquivos_partes = sorted(DADOS_DIR.glob("scrdata_2025*_part*.csv"))
    if arquivos_partes:
        return arquivos_partes

    arquivos_completos = sorted(
        p for p in DADOS_DIR.glob("scrdata_2025*.csv") if "_part" not in p.stem
    )
    if arquivos_completos:
        return arquivos_completos

    raise FileNotFoundError(f"Nenhum CSV válido foi encontrado em: {DADOS_DIR}")


ARQUIVOS = localizar_arquivos_csv()


def nomes_relativos(arquivos: Iterable[Path]) -> list[str]:
    if REPO_ROOT:
        return [str(p.relative_to(REPO_ROOT)) for p in arquivos]
    return [p.name for p in arquivos]


ARQUIVOS_RELATIVOS = nomes_relativos(ARQUIVOS)


def safe_divide(numerador: pd.Series, denominador: pd.Series) -> pd.Series:
    denominador = denominador.replace(0, np.nan)
    return numerador / denominador



def carregar_arquivos() -> pd.DataFrame:
    """Lê todos os CSVs de 2025 e consolida em um único DataFrame."""
    dfs: list[pd.DataFrame] = []

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
    base["data_base"] = pd.to_datetime(base["data_base"], errors="coerce")

    for coluna in COLUNAS_NUMERICAS:
        if coluna in base.columns:
            base[coluna] = pd.to_numeric(base[coluna], errors="coerce")

    return base



def validar_consistencia(df: pd.DataFrame) -> dict:
    """Executa validações básicas de coerência matemática da base."""
    quebra_carteira_ativa = (
        (df["carteira_ativa"] - (df["carteira_a_vencer"] + df["carteira_vencida"])).round(2) != 0
    ).sum()

    quebra_carteira_vencida = (
        (
            df["carteira_vencida"]
            - (df["vencido_de_15_ate_90_dias"] + df["vencido_acima_de_90_dias"])
        ).round(2)
        != 0
    ).sum()

    return {
        "quebras_carteira_ativa": int(quebra_carteira_ativa),
        "quebras_carteira_vencida": int(quebra_carteira_vencida),
    }



def gerar_resumo_estrutura(df: pd.DataFrame) -> None:
    """Gera um resumo geral da estrutura do dataset."""
    base_sem_origem = df.drop(columns=["arquivo_origem"], errors="ignore")
    resumo = {
        "pasta_dados": str(DADOS_DIR),
        "arquivos_analisados": ARQUIVOS_RELATIVOS,
        "total_arquivos": len(ARQUIVOS),
        "total_linhas": int(len(df)),
        "total_colunas": int(df.shape[1]),
        "periodo_inicial": str(df["data_base"].min().date()) if df["data_base"].notna().any() else None,
        "periodo_final": str(df["data_base"].max().date()) if df["data_base"].notna().any() else None,
        "nulos_total": int(df.isna().sum().sum()),
        "duplicatas_total": int(base_sem_origem.duplicated().sum()),
        "valor_-1_em_numero_de_operacoes": int((df["numero_de_operacoes"] == -1).sum()),
        "distintos_categoricos": {
            col: int(df[col].nunique(dropna=True)) for col in COLUNAS_CATEGORICAS if col in df.columns
        },
        "consistencia": validar_consistencia(df),
    }

    with open(TABELAS_DIR / "resumo_estrutura.json", "w", encoding="utf-8") as arquivo:
        json.dump(resumo, arquivo, ensure_ascii=False, indent=2)



def gerar_estatistica_descritiva(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula estatísticas descritivas para cada coluna numérica."""
    linhas = []

    for coluna in COLUNAS_NUMERICAS:
        if coluna not in df.columns:
            continue

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
        TABELAS_DIR / "estatistica_descritiva.csv",
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
    resumo_mensal["tx_inadimplencia"] = safe_divide(
        resumo_mensal["carteira_inadimplencia"], resumo_mensal["carteira_ativa"]
    )
    resumo_mensal["tx_problematico"] = safe_divide(
        resumo_mensal["ativo_problematico"], resumo_mensal["carteira_ativa"]
    )
    resumo_mensal.to_csv(TABELAS_DIR / "resumo_mensal.csv", index=False, encoding="utf-8-sig")

    resumo_uf = (
        df.groupby("uf")[["carteira_ativa", "carteira_inadimplencia"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_uf["tx_inadimplencia"] = safe_divide(
        resumo_uf["carteira_inadimplencia"], resumo_uf["carteira_ativa"]
    )
    resumo_uf.to_csv(TABELAS_DIR / "resumo_uf.csv", encoding="utf-8-sig")

    resumo_cliente = (
        df.groupby("cliente")[["carteira_ativa", "carteira_inadimplencia", "ativo_problematico"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_cliente["tx_inadimplencia"] = safe_divide(
        resumo_cliente["carteira_inadimplencia"], resumo_cliente["carteira_ativa"]
    )
    resumo_cliente["tx_problematico"] = safe_divide(
        resumo_cliente["ativo_problematico"], resumo_cliente["carteira_ativa"]
    )
    resumo_cliente.to_csv(TABELAS_DIR / "resumo_cliente.csv", encoding="utf-8-sig")

    resumo_segmento = (
        df.groupby("segmento")[["carteira_ativa", "carteira_inadimplencia"]]
        .sum()
        .sort_values("carteira_ativa", ascending=False)
    )
    resumo_segmento["tx_inadimplencia"] = safe_divide(
        resumo_segmento["carteira_inadimplencia"], resumo_segmento["carteira_ativa"]
    )
    resumo_segmento.to_csv(TABELAS_DIR / "resumo_segmento.csv", encoding="utf-8-sig")



def gerar_graficos(df: pd.DataFrame) -> None:
    """Cria gráficos para apoiar a análise exploratória."""
    resumo_mensal = (
        df.groupby("data_base")[["carteira_ativa", "carteira_inadimplencia", "ativo_problematico"]]
        .sum()
        .reset_index()
        .sort_values("data_base")
    )
    resumo_mensal["tx_inadimplencia"] = safe_divide(
        resumo_mensal["carteira_inadimplencia"], resumo_mensal["carteira_ativa"]
    )

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
    plt.barh(resumo_uf.index.astype(str), resumo_uf["carteira_ativa"] / 1e12)
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
    resumo_cliente["tx_inadimplencia"] = safe_divide(
        resumo_cliente["carteira_inadimplencia"], resumo_cliente["carteira_ativa"]
    )

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
    print(f"Pasta de dados: {DADOS_DIR}")
    print(f"Tabelas geradas em: {TABELAS_DIR}")
    print(f"Gráficos gerados em: {GRAFICOS_DIR}")
    print(f"Arquivos lidos: {len(ARQUIVOS)}")


if __name__ == "__main__":
    main()
