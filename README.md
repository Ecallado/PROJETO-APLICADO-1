# PROJETO-APLICADO-1

Repositório do **Projeto Aplicado 1** da disciplina do curso de **Banco de Dados**.

Este repositório foi organizado para concentrar a documentação do trabalho, os arquivos de dados, os scripts em Python e os materiais de apoio produzidos ao longo das etapas da disciplina.

---

## Integrantes
- Lucas de Lima Mendes
- Jaqueline Oliveira de Almeida
- Eduardo M. Pereira
- Kevin Barretos Santos

---

## Objetivo do projeto
Este projeto tem como objetivo organizar, documentar, explorar e analisar a base de dados escolhida pela equipe, seguindo os critérios definidos pela disciplina para as entregas do **Projeto Aplicado 1**.

Na **Etapa 1**, o foco foi a estruturação do repositório, organização do documento funcional, definição inicial do estudo, levantamento dos metadados e preparação da base.

Na **Etapa 2**, o foco passa a ser a **proposta de solução analítica** e a **análise exploratória de dados (EDA)**, com apoio de scripts em Python, estatística descritiva e gráficos.

---

## Tema do estudo
O projeto utiliza dados referentes à arrecadação do **Sistema de Controle de Receitas Estaduais (SCRE)**, disponibilizados em arquivos mensais no formato CSV/compactado, conforme a organização adotada pela equipe no trabalho.

Esses dados permitem acompanhar o comportamento das informações ao longo do tempo, possibilitando:
- comparações entre períodos;
- identificação de padrões;
- observação de tendências;
- preparação para análises mais aprofundadas;
- construção de indicadores descritivos para apoiar a interpretação do dataset.

---

## Proposta analítica
A proposta analítica da equipe consiste em investigar o comportamento do dataset ao longo dos meses disponíveis, buscando responder perguntas como:

- quais meses apresentam maior volume de registros;
- quais colunas apresentam maior variação;
- como os dados se distribuem estatisticamente;
- quais padrões podem ser observados na base;
- quais indícios iniciais podem apoiar análises futuras.

Para isso, a equipe utiliza **estatística descritiva** em Python, incluindo:
- média;
- mediana;
- moda;
- quartis;
- medidas de dispersão;
- frequência;
- visualizações gráficas.

---

## Estrutura do repositório

```text
PROJETO-APLICADO-1/
├── README.md
├── DOC/
│   ├── 01_planejamento/
│   ├── 02_referencias/
│   ├── documentos_principais/
│   └── materiais_auxiliares/
├── CODE/
│   ├── dados_brutos/
│   ├── dados_tratados/
│   ├── notebooks/
│   └── scripts/
└── old/
```

### DOC
Pasta com a documentação do projeto.

#### 01_planejamento
Contém os arquivos de planejamento inicial do projeto, como cronograma da equipe, organização das entregas e definição das etapas.

#### 02_referencias
Contém materiais de apoio, referências, orientações da disciplina e arquivos auxiliares utilizados no desenvolvimento do projeto.

#### documentos_principais
Contém os documentos centrais do trabalho, incluindo as versões atualizadas do documento funcional, proposta analítica, metadados e análise exploratória.

#### materiais_auxiliares
Pode conter imagens, rascunhos, arquivos complementares e outros materiais de suporte usados na construção do trabalho.

### CODE
Pasta com os arquivos relacionados à parte prática e aos dados do projeto.

#### dados_brutos
Contém os dados originais, sem tratamento, da forma como foram obtidos na fonte.

Nesta etapa, os arquivos mensais foram divididos em partes menores para viabilizar o versionamento no GitHub, mantendo a integridade lógica do dataset.

#### dados_tratados
Contém os dados já organizados, ajustados, consolidados ou preparados para uso nas análises.

#### notebooks
Contém notebooks utilizados para exploração, testes e análises preliminares dos dados.

#### scripts
Contém scripts auxiliares e códigos em Python utilizados para leitura, organização e análise exploratória da base.

### old
Pasta destinada a versões antigas, arquivos substituídos ou materiais preservados apenas para histórico.

---

## Dataset
Os arquivos utilizados no projeto correspondem a diferentes meses do ano de **2025**, organizados dentro da pasta `CODE/dados_brutos`.

Como o GitHub possui limitação de tamanho para upload de arquivos grandes, os arquivos do dataset foram separados em partes menores, preservando:
- o conteúdo original;
- a estrutura das colunas;
- o cabeçalho dos arquivos;
- a consistência da base para uso na análise.

Essa organização permite manter os dados versionados no repositório sem comprometer a estrutura lógica do dataset.

---

## Análise exploratória de dados
A análise exploratória desenvolvida nesta etapa tem como finalidade:
- conhecer melhor a estrutura do dataset;
- verificar quantidade de linhas e colunas;
- identificar tipos de dados;
- calcular medidas descritivas;
- observar frequências e distribuições;
- apoiar a proposta analítica do trabalho;
- gerar gráficos para facilitar a interpretação dos dados.

Os scripts em Python foram desenvolvidos para apoiar essa etapa e servir como base para análises futuras.

---

## Tecnologias e ferramentas utilizadas
- GitHub
- Git / Git Bash
- Python
- Jupyter Notebook
- CSV
- Word / documentação acadêmica

---

## Etapas do projeto

### Etapa 1
- organização do documento;
- criação e estruturação do repositório;
- cronograma da equipe;
- definição dos objetivos;
- identificação do dataset;
- levantamento inicial de metadados.

### Etapa 2
- atualização do documento funcional;
- inclusão da proposta analítica;
- desenvolvimento da análise exploratória de dados;
- construção de scripts em Python;
- aplicação de estatística descritiva;
- inclusão de gráficos de apoio à análise;
- organização dos materiais no GitHub.

---

## Como executar os scripts
Exemplo básico de execução local:

```bash
python CODE/scripts/eda_scr_2025_v2.py
```

> Observação: ajuste o caminho do script conforme a estrutura real da pasta `scripts` no repositório.

---

## Observações
Este repositório está sendo atualizado conforme o andamento das entregas e revisões da disciplina.

A documentação, os scripts e os dados podem receber ajustes ao longo das próximas etapas, conforme novas orientações da disciplina e evolução da análise.

Os arquivos de dados foram mantidos em partes menores para compatibilidade com o GitHub, sem desestruturar o dataset original.

---

## Status do projeto
Projeto em andamento, com evolução por etapas acadêmicas e versionamento contínuo no GitHub.
