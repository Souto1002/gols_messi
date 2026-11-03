"""Execute: streamlit run app.py."""
import pandas as pd
import plotly.express as px
import streamlit as st
from src.dados import CLEAN, NUMERICAS, ler_dados, filtrar, calcular_kpis, contar

st.set_page_config(page_title='Messi | Anatomia do gol', page_icon='⚽', layout='wide')
COR = '#167d9a'

@st.cache_data(show_spinner=False)
def carregar(versao):
    return ler_dados()


def grafico(fig, key):
    fig.update_layout(font=dict(family='Arial', size=13), margin=dict(l=12,r=12,t=45,b=20),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, key=key, config={'displaylogo': False})


def limpar_filtros():
    for key in ['anos', 'minutos', 'clubes', 'competicoes', 'mando', 'variaveis', 'metodo', 'bins']:
        st.session_state.pop(key, None)


def inteiro(n):
    return f'{n:,}'.replace(',', '.')

try:
    base = carregar(CLEAN.stat().st_mtime_ns)
except (OSError, ValueError, KeyError, pd.errors.ParserError):
    st.error('Não foi possível carregar a base. Confira data/clean/dataset.csv e o guia no README.')
    st.stop()

with st.sidebar:
    st.title('⚽ Messi / Dados')
    st.caption('Explore o recorte')
    st.button('Restaurar filtros', on_click=limpar_filtros, use_container_width=True)
    anos = st.slider('Intervalo de anos', int(base.year.min()), int(base.year.max()),
                     (int(base.year.min()), int(base.year.max())), key='anos')
    minutos = st.slider('Intervalo de minutos', int(base.goal_minute.min()), int(base.goal_minute.max()),
                        (int(base.goal_minute.min()), int(base.goal_minute.max())), key='minutos')
    clubes = st.multiselect('Clubes', sorted(base.club.unique()), default=sorted(base.club.unique()), key='clubes')
    competicoes = st.multiselect('Competições', sorted(base.competition.unique()),
                               default=sorted(base.competition.unique()), key='competicoes')
    mando = st.radio('Mando', ['Todos', 'Casa', 'Fora'], horizontal=True, key='mando')
    st.divider()
    st.caption('Laboratório • controles de análise')
    variaveis = st.multiselect('Variáveis quantitativas', list(NUMERICAS),
                              default=list(NUMERICAS)[:3], format_func=NUMERICAS.get, key='variaveis')
    metodo = st.selectbox('Método de correlação', ['pearson', 'spearman'],
                         format_func=str.title, key='metodo')
    bins = st.slider('Número de classes dos histogramas', 5, 40, 15, key='bins')
    st.caption('Filtros de anos, minutos, clubes, competições e mando afetam as duas abas. '
               'Os controles de análise afetam apenas o laboratório.')

df = filtrar(base, anos, minutos, clubes, competicoes, mando)
st.caption('FUTEBOL EM NÚMEROS / ANÁLISE EXPLORATÓRIA')
st.title('Messi: anatomia do gol')
st.write('Distribuições para investigar. Indicadores para contar histórias.')
st.caption(f'Base fornecida: {inteiro(len(base))} gols de clubes • '
           f'{base.date.min():%d/%m/%Y} a {base.date.max():%d/%m/%Y} • '
           f'Recorte atual: {inteiro(len(df))} gols ({len(df)/len(base):.1%}).')
if df.empty:
    st.warning('Nenhum gol neste recorte. Amplie os intervalos, selecione clubes e competições ou restaure os filtros.')
lab, editorial = st.tabs(['1 · Laboratório', '2 · Painel editorial'])

with lab:
    st.header('Distribuição e correlação')
    st.write('Cada linha representa um gol. Selecione variáveis e exclua faixas para observar como o padrão muda.')
    st.info('Placares finais repetem-se quando Messi marca várias vezes na mesma partida. '
            'O placar após o gol faz parte do placar final: a relação entre eles é parcialmente estrutural. '
            'A base traz placares como 7:9 e 10:11, sem documentar possível inclusão de disputas por pênaltis. '
            'As somas descrevem o placar informado. Correlação não demonstra causalidade ou eficiência do jogador.')
    if not df.empty:
        st.subheader('Como as variáveis se relacionam?')
        if len(variaveis) < 2:
            st.info('Selecione pelo menos duas variáveis para ver a correlação.')
        elif len(df) < 3:
            st.info('São necessários ao menos três gols para exibir a matriz.')
        else:
            constantes = [v for v in variaveis if df[v].nunique() < 2]
            validas = [v for v in variaveis if v not in constantes]
            if constantes:
                st.warning('Sem variação no recorte: ' + ', '.join(NUMERICAS[v] for v in constantes)
                           + '. Essas variáveis foram retiradas da matriz.')
            if len(validas) >= 2:
                corr = df[validas].rename(columns=NUMERICAS).corr(method=metodo)
                fig = px.imshow(corr, text_auto='.2f', zmin=-1, zmax=1,
                                color_continuous_scale='RdBu', color_continuous_midpoint=0,
                                title=f'Correlação de {metodo.title()} • n = {len(df)} gols', aspect='auto')
                fig.update_layout(height=420)
                grafico(fig, 'heatmap')
            else:
                st.info('Não há duas variáveis com variação suficiente neste recorte.')
        st.subheader('Como os valores se distribuem?')
        if not variaveis:
            st.info('Selecione ao menos uma variável para exibir um histograma.')
        colunas = st.columns(2)
        for i, var in enumerate(variaveis):
            with colunas[i % 2]:
                fig = px.histogram(df, x=var, nbins=bins, color_discrete_sequence=[COR],
                                   labels={var: NUMERICAS[var]}, title=NUMERICAS[var])
                fig.update_layout(yaxis_title='Quantidade de gols', bargap=0.08, height=320)
                grafico(fig, f'hist_{var}')
        st.caption('As classes são sugeridas ao Plotly, que ajusta limites para intervalos legíveis. '
                   'O minuto é o valor numérico do arquivo; não se reconstrói 45+X ou 90+X. '
                   'O ano é um índice temporal, incluído apenas quando selecionado.')
        with st.expander('Estatística descritiva do recorte'):
            if variaveis:
                st.dataframe(df[variaveis].rename(columns=NUMERICAS).describe().T, use_container_width=True)

with editorial:
    st.header('Histórias por trás dos gols')
    st.write('Para jornalistas e produtores de conteúdo esportivo: volume registrado, diversidade de adversários '
             'e participação de bola parada para orientar pautas e comparações descritivas.')
    if not df.empty:
        k = calcular_kpis(df)
        cols = st.columns(4)
        metricas = [
            ('Gols no recorte', inteiro(k['gols']), 'Uma linha do arquivo equivale a um gol.'),
            ('Partidas com gol no recorte', inteiro(k['partidas_com_gol']),
             'Chave: data, clube, adversário e competição. Não inclui jogos sem gol nem gols excluídos pelos filtros.'),
            ('Adversários distintos', inteiro(k['adversarios']), 'Nomes distintos no recorte.'),
            ('Gols de bola parada', f"{k['pct_bola_parada']:.1f}%".replace('.', ','),
             'Gols classificados como Penalty ou Direct free kick / todos os gols do recorte. Não inclui rebotes.')]
        for col, (nome, valor, ajuda) in zip(cols, metricas):
            col.metric(nome, valor, help=ajuda, border=True)
        serie = df.groupby('year').size().reindex(range(anos[0], anos[1]+1), fill_value=0).rename('Gols').reset_index()
        fig = px.line(serie, x='year', y='Gols', markers=True, title='1 / Gols por ano civil',
                      labels={'year': 'Ano'}, color_discrete_sequence=[COR])
        fig.update_layout(xaxis=dict(dtick=2), height=330)
        grafico(fig, 'gols_ano')
        st.caption('Anos inicial e final podem ser parciais. Zero significa ausência de gols neste recorte; '
                   'a base não informa se houve partidas disputadas.')
        c1, c2 = st.columns(2)
        with c1:
            top = contar(df, 'opponent', 10).sort_values(['Gols', 'opponent'])
            fig = px.bar(top, x='Gols', y='opponent', orientation='h', text='Gols',
                         title='2 / Adversários com mais gols sofridos (top 10)',
                         labels={'opponent':'Adversário'}, color_discrete_sequence=[COR])
            fig.update_layout(height=420)
            grafico(fig, 'adversarios')
        with c2:
            tipos = contar(df, 'goal_type').sort_values(['Gols', 'goal_type'])
            fig = px.bar(tipos, x='Gols', y='goal_type', orientation='h', text='Gols',
                         title='3 / Tipos de gol registrados', labels={'goal_type': 'Tipo de gol'},
                         color_discrete_sequence=['#9c516c'])
            fig.update_layout(height=420)
            grafico(fig, 'tipos')
        st.caption('Tipos de gol preservam a classificação da fonte. Empates no top 10 são resolvidos por ordem alfabética.')

st.divider()
with st.expander('Dados, metodologia e download'):
    st.write('Arquivo fornecido para a atividade acadêmica, sem fonte original ou licença informadas. '
             'A base cobre gols de clubes, incluindo Barcelona B, e não toda a carreira ou a seleção argentina. '
             'Não há dados de chutes, minutos jogados ou partidas sem gol; não se calculam taxas de conversão '
             'ou média de gols por partida disputada. “Sem assistência registrada” não prova jogada individual.')
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.download_button('Baixar recorte (CSV)', df.to_csv(index=False).encode('utf-8-sig'),
                       'messi_recorte.csv', 'text/csv', key='download')
st.caption('Projeto acadêmico • Python, Streamlit e Plotly • uso de IA documentado em prompts/.')
