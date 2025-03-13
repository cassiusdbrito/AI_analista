import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def preProcess(filename):
    #Carregar os dados
    df = pd.read_csv(filename)

    #Tratar valores nulos
    imputer = SimpleImputer(strategy="median")  # Pode ser "median" ou "most_frequent"
    df_imputed = pd.DataFrame(imputer.fit_transform(df.select_dtypes(include=["number"])), columns=df.select_dtypes(include=["number"]).columns)

    #Normalizar variáveis numéricas
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed), columns=df_imputed.columns)

    # Codificar variáveis categóricas
    encoder = OneHotEncoder(sparse_output=False, drop="first")
    df_categorical = pd.DataFrame(encoder.fit_transform(df.select_dtypes(include=["object"])))

    #Combinar os dados processados
    df_final = pd.concat([df_scaled, df_categorical], axis=1)

    return df_final


def train_test(df_final):
    #Separar treino e teste
    X_train, X_test, y_train, y_test = train_test_split(df_final.drop("target", axis=1), df_final["target"], test_size=0.2, random_state=42)

    return X_train, y_train, X_test, y_test