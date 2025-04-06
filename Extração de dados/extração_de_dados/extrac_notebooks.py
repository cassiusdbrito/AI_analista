import nbformat
import os

def extrair_codigos_notebooks():
    # Diretório com notebooks
    notebooks_dir = 'notebooks/'
    
    for notebook in os.listdir(notebooks_dir):
        if notebook.endswith('.ipynb'):
            with open(os.path.join(notebooks_dir, notebook)) as f:
                nb = nbformat.read(f, as_version=4)
                
                # Extrair células de código
                codigos = []
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        codigos.append(cell.source)
                
                # Salvar em arquivo
                with open(f'dados_treinamento/exemplos/notebooks/{notebook[:-6]}.txt', 'w') as f:
                    f.write('\n\n'.join(codigos))