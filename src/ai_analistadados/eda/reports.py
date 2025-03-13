from ydata_profiling import ProfileReport

#Criar e salvar o relatório EDA
def report_html(df):
    profile = ProfileReport(df, explorative=True)
    return profile.to_html()

def report_json(df):
    profile = ProfileReport(df, explorative=True)
    return profile.to_json()