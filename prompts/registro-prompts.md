# Registro do uso de IA

## Solicitação recebida (resumo fiel, não transcrição literal)

Resolver uma atividade baseada na EDA fornecida, criando um app Streamlit com dois dashboards: laboratório de distribuição/correlação e painel com 3 a 5 KPIs para um público definido. Incluir seleção de variáveis, slider de intervalo, heatmap, histogramas, três visuais editoriais, notebooks, `app.py`, `entregas/`, dois rascunhos e `prompts/`. Entregar como repositório organizado em ZIP para o aluno iniciar seu próprio GitHub.

## Entradas efetivamente consultadas

- Notebook `analise_messi_goals_(1).ipynb`.
- Dataset `messi_all_goals (1).csv`.
- PDFs “Aula 21 - Streamlit parte 1”, “Aula 22 - Streamlit parte 2” e “Aula 23 - Streamlit parte 3”.

## Decisões tomadas durante a geração

- Corrigir a análise de `assist`/`type` para os nomes reais `assist_player`/`goal_type`.
- Derivar quantitativas por soma dos placares e ano, preservando as categorias.
- Usar duas abas e filtros compartilhados, com proteção para recortes vazios e variáveis constantes.
- Escolher jornalistas esportivos como público; evitar taxas que exigem jogos sem gol, chutes ou minutos jogados.
- Não alegar publicação ou testes públicos que não foram realizados.
- Não inventar fonte, licença externa ou histórico de commits.

## Modelo de prompt para manutenção (sugestão, não uma interação já realizada)

“Contexto: projeto Messi em Streamlit, com CSV tratado em data/clean/dataset.csv. Público do dashboard 2: jornalistas. Preserve a unidade por gol, os filtros compartilhados e os quatro KPIs documentados. Não calcule conversão ou médias sobre partidas sem gol, pois esses dados não existem. Ao modificar o app, rode os testes e atualize as justificativas e limitações. Saída esperada: arquivos alterados e resumo da validação.”
