import pandas as pd
import pytest
from src.dados import RAW, preparar, ler_dados, calcular_kpis, filtrar


def test_exportacao_preserva_eventos():
    esperado = preparar(pd.read_csv(RAW))
    pd.testing.assert_frame_equal(esperado, ler_dados())
    assert len(esperado) == 790
    assert esperado.duplicated().sum() == 0


def test_kpis_base():
    k = calcular_kpis(ler_dados())
    assert k['gols'] == 790
    assert k['partidas_com_gol'] == 518
    assert k['adversarios'] == 125
    assert k['pct_bola_parada'] == pytest.approx(147 / 790 * 100)


def test_filtro_limites_e_vazio():
    df = ler_dados()
    args = (df, (2004, 2026), (2, 110), list(df.club.unique()), list(df.competition.unique()))
    assert len(filtrar(*args, 'Todos')) == 790
    assert len(filtrar(*args, 'Casa')) + len(filtrar(*args, 'Fora')) == 790
    assert filtrar(df, (2004, 2004), (65, 65), ['FC Barcelona B'], ['2ª B - Grupo III'], 'Casa').shape[0] == 1
    vazio = filtrar(df, (2004, 2026), (2, 110), [], [], 'Todos')
    assert calcular_kpis(vazio) == dict(gols=0, partidas_com_gol=0, adversarios=0, pct_bola_parada=0)


def test_placares_e_assistencia():
    df = preparar(pd.read_csv(RAW))
    assert df.iloc[0].match_total_goals == 3
    assert df.iloc[0].score_total_at_goal == 3
    assert df.assist_player.eq('Sem assistência registrada').sum() == 240
    assert df.goal_type.eq('Não informado').sum() == 5
    df.loc[0, 'match_score'] = 'inválido'
    with pytest.raises(ValueError, match='Placar inválido'):
        preparar(df)
