# Justificativa das métricas

**Público-alvo:** jornalistas esportivos e produtores de conteúdo sobre futebol. A pergunta editorial é: “Como os gols registrados se distribuem no tempo, entre adversários e por tipo de jogada?”. Os indicadores apoiam seleção de pautas, não recomendação de escalação ou inferência de eficiência.

Todos os KPIs usam o mesmo recorte de anos, minutos, clubes, competições e mando. Selecionar variáveis, classes ou método de correlação altera apenas o laboratório. Não há comparação automática entre épocas com calendários e cobertura diferentes.

| Métrica | Variável e fórmula | Motivo e mensagem | Decisão apoiada |
|---|---|---|---|
| Gols no recorte | Número de linhas filtradas | Resume o volume disponível para a pauta | Dimensionar o recorte e contextualizar as contagens |
| Partidas com gol no recorte | Distintos de date, club, opponent, competition | Mostra em quantos jogos há gols que passaram pelos filtros | Distinguir volume de gols de frequência de jogos com gols no recorte |
| Adversários distintos | Contagem distinta de opponent | Expressa a diversidade de oponentes registrados | Escolher uma pauta geral ou concentrada em determinados adversários |
| Gols de bola parada (%) | 100 × gols com goal_type em {Penalty, Direct free kick} / todos os gols filtrados | Quantifica a participação dessas duas categorias na classificação disponível | Investigar a composição do repertório de gols |

**Valores de referência sem filtros:** 790 gols, 518 partidas com gol, 125 adversários e 18,6% de bola parada (147 / 790). Rebotes de pênalti não entram no numerador. Gols de tipo não informado continuam no denominador.

## Visuais e layout

1. **Linha anual:** auxilia a localizar períodos com maior volume de gols registrados. Usa ano civil, não a temporada textual. Anos inicial e final podem ser parciais; ausência de gols no recorte não informa partidas disputadas.
2. **Barras por adversário (top 10):** destaca duelos para pautas. Empates resolvidos alfabeticamente; não mede dificuldade do adversário nem ajusta pelo número de confrontos.
3. **Barras por tipo de gol:** mostra todas as categorias da fonte e os não informados. Categorias são preservadas; não se deduz que todas sejam classificações anatômicas ou mutuamente exclusivas na realidade, apenas rótulos únicos por registro.

Quatro cartões ficam antes dos três visuais. A sidebar é compartilhada pelas duas abas para manter o contexto do recorte. O tema combina azul, branco e uma cor secundária para os tipos de gol. Os rascunhos JPG são esquemas de planejamento preparados para esta entrega; não representam evidência de etapas realizadas nas datas das aulas.

## Limites

Não há dados para calcular taxa de acerto, gols por 90 minutos ou gols por todas as partidas disputadas. A seleção argentina não aparece. A chave de partida é operacional e não um ID oficial. Nenhum KPI deve ser apresentado como total oficial da carreira. Não foram calculados indicadores de vitória porque a orientação dos placares não é documentada no anexo.
