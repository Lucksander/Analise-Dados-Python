import os
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import pandas as pd


def selecionar_e_plotar():
    # 1. Ocultar a janela principal do Tkinter (queremos apenas o diálogo de arquivo)
    root = Tk()
    root.withdraw()

    print("Aguardando seleção do arquivo...")

    # 2. Abrir a janela de seleção de arquivo (filtrando por arquivos CSV)
    caminho_arquivo = askopenfilename(
        title="Selecione o arquivo CSV de clientes",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
    )

    # Se o usuário fechar a janela sem selecionar nenhum arquivo
    if not caminho_arquivo:
        messagebox.showwarning("Cancelado", "Nenhum arquivo foi selecionado.")
        return

    try:
        # 3. Ler o arquivo CSV selecionado
        # O argumento encoding='utf-8' ou 'latin1' ajuda a evitar erros com acentos
        df = pd.read_csv(caminho_arquivo, encoding="utf-8")

        # Verificar se a coluna 'Cidade' existe no arquivo
        if "Cidade" not in df.columns:
            # Tenta buscar com variações comuns caso haja erro de maiúscula/minúscula
            colunas_com_c = [c for c in df.columns if "cidade" in c.lower()]
            if colunas_com_c:
                coluna_cidade = colunas_com_c[0]
            else:
                raise ValueError(
                    "A coluna 'Cidade' não foi encontrada no arquivo CSV."
                )
        else:
            coluna_cidade = "Cidade"

        # 4. Contar a quantidade de clientes por cidade
        contagem_cidades = df[coluna_cidade].value_counts()

        # 5. Criar o gráfico de barras usando o Matplotlib
        plt.figure(figsize=(9, 5))
        contagem_cidades.plot(kind="bar", color="mediumpurple", edgecolor="black")

        # Personalizar o gráfico com base no arquivo real
        nome_base = os.path.basename(caminho_arquivo)
        plt.title(
            f"Distribuição de Clientes por Cidade\n(Fonte: {nome_base})",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Cidades", fontsize=12)
        plt.ylabel("Quantidade de Clientes", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Ajustar o layout e exibir
        plt.tight_layout()
        plt.show()

    except Exception as e:
        # Se algo der errado (arquivo corrompido, falta de colunas, etc), mostra um alerta na tela
        messagebox.showerror(
            "Erro ao processar arquivo", f"Não foi possível ler o arquivo:\n{e}"
        )


# Executar a função
if __name__ == "__main__":
    selecionar_e_plotar()