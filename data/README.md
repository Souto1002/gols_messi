# Dados e dicionário

Base: anexo `messi_all_goals (1).csv` fornecido para a atividade. Não há URL externa ou licença declarada no arquivo. Não foi possível verificar sua origem ou completude. Atribuição original: **PENDENTE de confirmação com quem forneceu a base**. Não se atribui uma licença ao dataset neste projeto.

`raw/messi_all_goals.csv` mantém os 790 registros e 16 campos fornecidos. O notebook histórico original também é preservado. `clean/dataset.csv` contém os registros tratados e 3 campos derivados (19 campos no total). A limpeza não elimina linhas, nem supõe que todos os gols da carreira estejam presentes.

| Coluna | Significado / uso |
|---|---|
| competition | Competição, categoria |
| match_stage | Rodada ou fase; mistura números e textos, mantida categórica |
| date | Data da partida, convertida para data |
| venue | Home ou Away, utilizado no filtro de mando |
| club | Clube de Messi |
| opponent | Adversário; grafias preservadas |
| match_score | Placar final textual, preservado sem presumir a orientação |
| player_position | Posição categórica (LW, AM, CF, RW, SS) |
| goal_minute | Minuto numérico como fornecido; 2 a 110 |
| score_at_goal | Placar textual após o gol |
| goal_type | Tipo de gol; Not reported → Não informado |
| assist_player | Assistente; Not Applicable → Sem assistência registrada |
| season | Temporada fornecida; não corrigida ou reinterpretada como ano civil |
| goal_decade | Década categórica fornecida |
| is_home_goal | Indicador de mando fornecido; preservado |
| goal_minute_bucket | Faixa de minuto fornecida; preservada, não usada para reconstruir minutos |
| year | **Derivada:** ano civil de date; quantitativa temporal opcional |
| match_total_goals | **Derivada:** soma dos dois lados de match_score |
| score_total_at_goal | **Derivada:** soma dos dois lados de score_at_goal |

Zero valores nulos formais e zero duplicatas exatas no CSV fornecido; há 240 assistências sem registro e 5 gols de tipo não informado. Esses marcadores não são provas de jogadas individuais. Datas: 2004-09-05 a 2026-03-07.

Chave operacional de partida: `date + club + opponent + competition`, produzindo 518 partidas com gol. Não há identificador oficial de partida, então a contagem depende dessa chave. Não se removem registros iguais em outros campos: mais de um gol na mesma partida é legítimo.

O download do app contém apenas o recorte deste dataset e os campos derivados. Não há upload de dados privados, autenticação ou chamadas a APIs externas no código do app.

## Ressalva dos placares

Há três registros em duas partidas com placares finais `7:9` e `10:11` (FC Dallas, 2023-08-07; Nashville SC, 2023-08-20). A convenção de inclusão de disputas por pênaltis não está documentada. Por isso, as somas são tratadas como valores do **placar informado**, não como total certificado de gols no tempo regulamentar ou na prorrogação. Os valores são mantidos e sinalizados, sem correção por suposição.
