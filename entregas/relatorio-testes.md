# Relatório de testes locais

Preparação do ZIP: **03/11/2026 (UTC)**. Estes resultados se referem ao projeto local, não a uma aplicação publicada.

## Ambiente e comandos

- Python 3.12.14, pandas 2.2.3, Streamlit 1.51.0 e Plotly 6.4.0.
- `python -m pytest -q`: **8 testes passaram**.
- Notebook `notebooks/eda_revisada.ipynb`: execução integral por nbclient, com resultados e gráficos salvos, sem células com erro.
- Servidor local: `python -m streamlit run app.py`, em `http://127.0.0.1:8501`.
- Chromium 151.0.7922.34 via Playwright, usando contexto novo e isolado, sem sessão de login.

## Cobertura automatizada (pytest / Streamlit AppTest)

| Cenário | Resultado |
|---|---|
| CSV tratado igual à transformação da base original | Passou; 790 eventos preservados, sem duplicatas exatas |
| KPIs integrais | 790 gols, 518 partidas com gol, 125 adversários e 18,6% de bola parada |
| Limites inclusivos dos filtros, mando e recorte vazio | Passou |
| Soma dos placares, marcadores de assistência e tipo de gol | Passou; placar inválido gera erro explícito |
| Duas abas, quatro métricas e sete gráficos padrão no total | Passou |
| Zero, uma e quatro quantitativas selecionadas | Passou; orientação para seleção insuficiente |
| Anos, minutos, clubes, competições, mando, método e classes | Passou; widgets respondem sem exceção |
| Botão de restauração | Retornou aos 790 gols |
| Recorte vazio, minuto constante e recorte com apenas um gol | Passou; orientações exibidas sem quebrar o app |

## Conferência no navegador local

- As duas abas foram abertas por clique em um contexto isolado.
- Laboratório padrão: um heatmap e três histogramas visíveis.
- Painel editorial: quatro KPIs e três visuais visíveis.
- Expansor de metodologia aberto; download CSV realizado e validado com 790 linhas de dados.
- Restauração dos filtros executada; total confirmado em 790.
- Sem erros JavaScript de página durante esses passos.
- Verificação básica de título em viewport de 390 × 844; não equivale a teste completo de todos os aparelhos.
- Capturas locais: `dashboard1-local.png` e `dashboard2-local.png`. Os rascunhos de planejamento são os dois arquivos JPG, separados dessas capturas.

## Revisão de dados expostos

A entrega contém apenas o CSV esportivo fornecido, a versão tratada, código, notebooks, gráficos e documentação. Não foram identificadas credenciais, tokens, senhas, e-mails privados de acesso ou arquivos de secrets nos arquivos incluídos. O código não solicita segredos, não lê variáveis de ambiente e não usa APIs externas para buscar dados. O `.gitignore` exclui ambientes virtuais, `.env` e `.streamlit/secrets.toml`.

Não se atribui ao dataset uma licença desconhecida. A confirmação da origem e da permissão de redistribuição está indicada em `data/README.md`.

## Pendente após publicação

Não houve deploy público. A checagem em janela anônima de uma **URL pública**, a configuração de acesso público e o link real no README devem ser realizados pelo aluno. Registrar os resultados em `checklist-publicacao.md`; os itens não foram marcados como concluídos antecipadamente.
