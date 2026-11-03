"""Transformações compartilhadas pela EDA, pelo app e pelos testes."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/messi_all_goals.csv'
CLEAN = ROOT / 'data/clean/dataset.csv'
NUMERICAS = {
    'goal_minute': 'Minuto registrado do gol',
    'match_total_goals': 'Soma do placar final informado',
    'score_total_at_goal': 'Soma do placar após o gol',
    'year': 'Ano do gol',
}
MATCH_KEY = ['date', 'club', 'opponent', 'competition']


def preparar(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='raise')
    df['goal_minute'] = pd.to_numeric(df['goal_minute'], errors='raise')
    df['year'] = df['date'].dt.year.astype('int64')
    # Não se presume qual lado do placar representa o clube de Messi.
    for origem, destino in [('match_score', 'match_total_goals'),
                             ('score_at_goal', 'score_total_at_goal')]:
        partes = df[origem].str.extract(r'^(\d+):(\d+)$')
        if partes.isna().any().any():
            raise ValueError(f'Placar inválido em {origem}')
        df[destino] = partes.astype(int).sum(axis=1)
    df['assist_player'] = df['assist_player'].fillna('Não informado').replace(
        {'Not Applicable': 'Sem assistência registrada'})
    df['goal_type'] = df['goal_type'].fillna('Não informado').replace(
        {'Not reported': 'Não informado'})
    return df


def ler_dados(caminho=CLEAN):
    return pd.read_csv(caminho, parse_dates=['date'])


def filtrar(df, anos, minutos, clubes, competicoes, mando):
    mask = df['year'].between(*anos) & df['goal_minute'].between(*minutos)
    mask &= df['club'].isin(clubes) & df['competition'].isin(competicoes)
    if mando != 'Todos':
        mask &= df['venue'].eq({'Casa': 'Home', 'Fora': 'Away'}[mando])
    return df.loc[mask].copy()


def calcular_kpis(df):
    total = len(df)
    return {
        'gols': total,
        'partidas_com_gol': len(df[MATCH_KEY].drop_duplicates()),
        'adversarios': df['opponent'].nunique(),
        'pct_bola_parada': 100 * df['goal_type'].isin(
            ['Penalty', 'Direct free kick']).sum() / total if total else 0.0,
    }


def contar(df, coluna, top=None):
    result = df.groupby(coluna, observed=True).size().rename('Gols').reset_index()
    result = result.sort_values(['Gols', coluna], ascending=[False, True])
    return result.head(top) if top else result
