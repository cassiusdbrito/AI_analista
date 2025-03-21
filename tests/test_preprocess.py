from ai_analistadados.eda import preProcessing
import pandas as pd

df = preProcessing.preProcess(r"C:\Users\cassi\AI_analistaDados\src\ai_analistadados\data\titanic.csv")

def test_preprocess(df_inicio, df_final):
    df_inicio = pd.read_csv(df_inicio)
    assert not df_inicio.equals(df_final)

# t = test_preprocess(r"C:\Users\cassi\AI_analistaDados\src\ai_analistadados\data\titanic.csv", df)
# print(t)