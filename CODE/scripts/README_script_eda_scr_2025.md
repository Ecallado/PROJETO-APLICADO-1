# README — Script `eda_scr_2025_v3.py`

## Finalidade
O script `eda_scr_2025_v3.py` foi desenvolvido para executar a **Análise Exploratória de Dados (EDA)** do dataset **SCR.data / operações de crédito no Brasil - 2025**.

O objetivo do script é:
- localizar os arquivos CSV do projeto;
- consolidar os dados em uma única base;
- validar consistência básica do dataset;
- calcular estatísticas descritivas;
- gerar tabelas-resumo para apoio analítico;
- criar gráficos para o documento da Etapa 2.

---

## Onde o script deve ficar
O arquivo deve ser armazenado em:

```text
CODE/scripts/eda_scr_2025_v3.py
```

---

## Onde os dados devem ficar
O script foi ajustado para procurar os arquivos CSV principalmente em:

```text
CODE/dados_brutos/
```

Ele aceita dois formatos de entrada:
- **arquivos mensais completos**, como:
  - `scrdata_202501.csv`
- **arquivos divididos em partes**, como:
  - `scrdata_202501_part01.csv`
  - `scrdata_202501_part02.csv`
  - etc.

Se existirem arquivos em partes, o script prioriza esse formato.

---

## O que o script faz

### 1. Localiza a raiz do repositório
Função:
- `encontrar_raiz_repositorio()`

Responsabilidade:
- identifica automaticamente a raiz do projeto a partir da pasta atual ou da pasta do script;
- verifica se existe a estrutura `CODE/dados_brutos/`.

---

### 2. Localiza a pasta de dados
Função:
- `resolver_pasta_dados()`

Responsabilidade:
- encontra onde estão os arquivos `scrdata_2025*.csv`;
- primeiro tenta usar `CODE/dados_brutos/`;
- se não encontrar, tenta a pasta do script ou a pasta atual.

---

### 3. Seleciona os arquivos CSV que serão lidos
Função:
- `localizar_arquivos_csv()`

Responsabilidade:
- identifica os arquivos válidos para análise;
- prioriza arquivos quebrados em partes (`_part`);
- se não houver partes, usa os arquivos completos.

---

### 4. Carrega e consolida os dados
Função:
- `carregar_arquivos()`

Responsabilidade:
- lê todos os CSVs selecionados;
- usa separador `;`, decimal `,` e codificação `utf-8-sig`;
- adiciona a coluna `arquivo_origem` para rastrear de qual arquivo veio cada registro;
- converte `data_base` para data;
- converte colunas numéricas para formato numérico.

Resultado:
- gera um único `DataFrame` consolidado com todos os dados analisados.

---

### 5. Valida consistência da base
Função:
- `validar_consistencia(df)`

Responsabilidade:
- verifica se as relações matemáticas principais do dataset estão corretas.

Validações aplicadas:
- `carteira_ativa = carteira_a_vencer + carteira_vencida`
- `carteira_vencida = vencido_de_15_ate_90_dias + vencido_acima_de_90_dias`

Resultado:
- informa quantas quebras de consistência foram encontradas.

---

### 6. Gera resumo estrutural do dataset
Função:
- `gerar_resumo_estrutura(df)`

Responsabilidade:
- cria um resumo geral da base analisada.

Informações geradas:
- pasta de origem dos dados;
- arquivos analisados;
- total de arquivos;
- total de linhas;
- total de colunas;
- período inicial e final;
- quantidade total de nulos;
- duplicatas;
- quantidade de `-1` em `numero_de_operacoes`;
- quantidade de valores distintos nas colunas categóricas;
- resultado da validação de consistência.

Arquivo gerado:
- `resumo_estrutura.json`

---

### 7. Gera estatística descritiva
Função:
- `gerar_estatistica_descritiva(df)`

Responsabilidade:
- calcula estatísticas descritivas das colunas numéricas.

Métricas calculadas:
- média;
- mediana;
- moda;
- primeiro quartil (Q1);
- terceiro quartil (Q3);
- desvio-padrão;
- valor mínimo;
- valor máximo.

Arquivo gerado:
- `estatistica_descritiva.csv`

---

### 8. Gera resumos analíticos
Função:
- `gerar_resumos_analiticos(df)`

Responsabilidade:
- cria tabelas-resumo por dimensões importantes do dataset.

Arquivos gerados:
- `resumo_mensal.csv`
- `resumo_uf.csv`
- `resumo_cliente.csv`
- `resumo_segmento.csv`

Principais indicadores calculados:
- carteira ativa;
- carteira de inadimplência;
- ativo problemático;
- taxa de inadimplência;
- taxa de ativo problemático.

---

### 9. Gera gráficos para a análise exploratória
Função:
- `gerar_graficos(df)`

Responsabilidade:
- cria visualizações para apoiar a interpretação dos dados.

Gráficos gerados:
- `grafico_carteira_ativa_mes.png`
- `grafico_taxa_inadimplencia_mes.png`
- `grafico_top10_ufs.png`
- `grafico_taxa_cliente.png`

---

### 10. Executa o fluxo principal
Função:
- `main()`

Responsabilidade:
- organiza a execução completa do script na ordem correta:
  1. carregar dados;
  2. gerar resumo estrutural;
  3. gerar estatística descritiva;
  4. gerar resumos analíticos;
  5. gerar gráficos.

---

## Pastas de saída
Se o script estiver sendo executado dentro do repositório, os arquivos gerados serão salvos em:

### Tabelas
```text
DOC/materiais_auxiliares/tabelas_eda/
```

### Gráficos
```text
DOC/materiais_auxiliares/graficos_eda/
```

Se o script for executado fora do repositório, ele salva os resultados em pastas locais chamadas:
- `eda_outputs/`
- `graficos/`

---

## Como executar
Na raiz do repositório, usar:

```bash
python CODE/scripts/eda_scr_2025_v3.py
```

---

## Bibliotecas utilizadas
O script utiliza:
- `pandas`
- `numpy`
- `matplotlib`
- `json`
- `pathlib`

Se necessário, instalar com:

```bash
pip install pandas numpy matplotlib
```

---

## Observações importantes
- O script foi ajustado para funcionar com a estrutura real do repositório do grupo.
- Ele não altera os arquivos brutos do dataset.
- O foco do script é gerar saídas analíticas para a Etapa 2.
- A coluna `arquivo_origem` é criada apenas para rastreamento interno da análise.
- O valor `-1` em `numero_de_operacoes` não é removido automaticamente; ele apenas é contabilizado no resumo estrutural.

---

## Resumo final
Em termos simples, o script:
1. encontra os CSVs;
2. junta tudo em uma base única;
3. verifica coerência básica dos dados;
4. calcula estatísticas descritivas;
5. gera tabelas para análise;
6. gera gráficos para o trabalho.
