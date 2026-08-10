# PROJETO DATATHON - ASSOCIAÇÃO PASSOS MÁGICOS.

# 🔮 Radar de Prevenção e Intervenção - Passos Mágicos

Este repositório contém o projeto final de Data Science e o aplicativo preditivo desenvolvido para a Associação Passos Mágicos. O objetivo do sistema é analisar o histórico de notas e indicadores psicossociais dos alunos para prever o risco de rebaixamento de Pedra e evasão escolar no ciclo seguinte.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Streamlit:** Construção do dashboard e interface web da aplicação.
* **Pandas & NumPy:** Limpeza, estruturação e manipulação da base de dados.
* **Scikit-Learn (Machine Learning):** Modelagem preditiva.
* **Imbalanced-learn (SMOTE):** Balanceamento de classes para aumentar o recall das bases de risco.
* **Matplotlib & Seaborn:** Geração dos gráficos analíticos.

## 📁 Estrutura do Repositório
* `app.py`: Arquivo principal contendo o código da interface Streamlit.
* `PassosMagicos_Clean.ipynb`: Notebook Jupyter com o trabalho de limpeza e preparação dos dados para a análise exploratória* 
* `PassosMagicos_Explore.ipynb`: Notebook Jupyter com a análise exploratória de dados (EDA) e geração do motor do modelo de machine learning.
* `modelo_passos_magicos_2023.pkl`: Modelo de Machine Learning treinado e exportado.
* `BASE_CONSOLIDADA.xlsx`: Base de dados tratada utilizada pelo algoritmo.
* `requirements.txt`: Arquivo com as dependências do projeto.
* `*.png` / `*.jpg`: Imagens e ícones consumidos pela aplicação web.
* `Projeto Passoa Magicos.pdf`: Análise executiva completa dos dados e insights obtidos.

## 🚀 Aplicativo

O aplicado construido para o projeto pode ser acessado através do link:

https://datathon-magical-walking.streamlit.app/

## 🧠 Lógica de Negócio e Funcionalidades
* **Análise Preditiva (What-If):** Simulador onde o educador insere o IDA, IEG, IPP e outros indicadores para visualizar a Pedra projetada do aluno.
* **Diagnóstico de Risco:** Motor de regras que cruza os inputs e dispara alertas específicos (ex: Esforço Não Convertido, Ilusão de Desempenho).
* **Dashboards Históricos:** Análise da evolução do INDE nos anos de 2022 a 2024.

## ✒️ Autor
* **Luci Aguiar** - Desenvolvimento de Dados e Interface.
