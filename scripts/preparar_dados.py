"""Execute da raiz: python scripts/preparar_dados.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.dados import RAW, CLEAN, preparar

if __name__ == '__main__':
    df = preparar(pd.read_csv(RAW))
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN, index=False, date_format='%Y-%m-%d')
    print(f'{len(df)} gols exportados para {CLEAN.relative_to(CLEAN.parents[2])}')
