from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def abrir():
    app = AppTest.from_file(APP, default_timeout=30).run()
    assert not app.exception
    return app


def test_paineis_e_kpis():
    app = abrir()
    assert len(app.tabs) == 2
    assert len(app.metric) == 4
    assert app.metric[0].value == '790'
    assert app.metric[1].value == '518'
    assert app.metric[2].value == '125'
    assert app.metric[3].value == '18,6%'
    assert len(app.get('plotly_chart')) == 7


def test_zero_uma_todas_variaveis():
    app = abrir()
    for variaveis, graficos in [([], 3), (['goal_minute'], 4),
                                (['goal_minute','match_total_goals','score_total_at_goal','year'], 8)]:
        app.multiselect(key='variaveis').set_value(variaveis).run()
        assert not app.exception
        assert len(app.get('plotly_chart')) == graficos


def test_widgets_e_restauracao():
    app = abrir()
    app.slider(key='anos').set_value((2023, 2026)).run()
    assert 0 < int(app.metric[0].value) < 790
    app.slider(key='minutos').set_value((60, 90)).run()
    app.multiselect(key='clubes').set_value(['Inter Miami CF']).run()
    app.multiselect(key='competicoes').set_value(['MLS']).run()
    app.radio(key='mando').set_value('Fora').run()
    app.selectbox(key='metodo').set_value('spearman').run()
    app.slider(key='bins').set_value(25).run()
    assert not app.exception
    assert 0 < int(app.metric[0].value) < 790
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value == '790'


def test_recorte_vazio_e_constante():
    app = abrir()
    app.multiselect(key='clubes').set_value([]).run()
    assert not app.exception
    assert not app.metric
    assert len(app.warning) > 0
    app.button[0].click().run()
    app.slider(key='minutos').set_value((65, 65)).run()
    assert not app.exception
    assert any('Sem variação' in w.value for w in app.warning)
    app.slider(key='anos').set_value((2004, 2004)).run()
    assert not app.exception
    assert app.metric[0].value == '1'
