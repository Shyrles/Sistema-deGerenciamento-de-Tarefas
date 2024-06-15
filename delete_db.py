import os
import psutil

def close_file_handlers(db_path):
    # Iterar por todos os processos ativos
    for proc in psutil.process_iter():
        try:
            # Obter a lista de arquivos abertos pelo processo
            flist = proc.open_files()
            for f in flist:
                if f.path == db_path:
                    print(f"Fechando o arquivo {db_path} do processo {proc.pid}")
                    proc.terminate()  # Tenta terminar o processo
                    proc.wait()  # Espera o processo terminar
        except Exception as e:
            print(f"Erro ao fechar o processo {proc.pid}: {e}")

db_path = "./new_test.db"

# Fechar processos que estão usando o arquivo
close_file_handlers(db_path)

# Verifica se o arquivo existe
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"Arquivo {db_path} deletado com sucesso.")
    except PermissionError as e:
        print(f"Erro de permissão: {e}")
else:
    print(f"O arquivo {db_path} não existe.")
