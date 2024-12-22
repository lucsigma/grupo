
import streamlit as st
import random
import time
import sqlite3

# Função para criar o banco de dados e a tabela
def criar_banco():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Função para inserir um usuário no banco de dados
def cadastrar_usuario(nome):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

# Função para excluir toda a lista de usuários com validação de senha
def excluir_todos_usuarios_com_senha(senha):
    if validar_senha(senha):
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        conn.close()
        return True
    return False

# Função para obter a lista de nomes cadastrados
def obter_nomes_cadastrados():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios")
    nomes = cursor.fetchall()
    conn.close()
    return [nome[0] for nome in nomes]

# Função para validar a senha
def validar_senha(senha):
    return senha == "1289"

# Configuração inicial da página
st.set_page_config(page_title="Sorteio de Nomes", layout="centered")

# Título do app
st.title("🎉 Sorteio ")
st.write("Bem-vindos ao sorteio do grupo!")

# Criar o banco de dados e a tabela se necessário
criar_banco()

# Cadastro de Nomes
st.subheader("Cadastre o seu nome")
nome_input = st.text_input("Digite seu nome:")

# Botão para cadastrar o nome
if st.button("Cadastrar"):
    if nome_input.strip():
        # Cadastra o nome do usuário no banco de dados
        cadastrar_usuario(nome_input)
        st.success(f"Usuário {nome_input} cadastrado com sucesso!")
    else:
        st.error("Por favor, insira um nome para cadastrar.")

# Exibir a lista de nomes cadastrados
st.subheader("Nomes Cadastrados:")
st.write("Boa sorte!")
nomes_cadastrados = obter_nomes_cadastrados()
if nomes_cadastrados:
    # Exibir os nomes cadastrados em formato de tabela
    st.table({"Nomes Cadastrados": nomes_cadastrados})

    # Botão para excluir toda a lista de nomes
    st.subheader("Excluir Todos os Nomes")
    senha_exclusao = st.text_input("Digite a senha para excluir todos os nomes:", type="password")

    if st.button("Excluir Todos"):
        if excluir_todos_usuarios_com_senha(senha_exclusao):
            st.success("Todos os nomes cadastrados foram excluídos com sucesso!")
            st.rerun()  # Atualiza a página para refletir a exclusão
        else:
            st.error("Senha incorreta! Não foi possível excluir os nomes.")
else:
    st.write("Nenhum nome cadastrado ainda.")

# Entrada da senha para realizar o sorteio
senha_input = st.text_input("Digite a senha para realizar o sorteio:", type="password")

# Se a senha for correta, realizar o sorteio diretamente da lista cadastrada
if validar_senha(senha_input):
    st.subheader("Sorteio")
    if nomes_cadastrados:
        # Botão para iniciar o sorteio
        if st.button("Sortear"):
            # Temporizador visual
            st.subheader("Sorteio iniciado...")
            countdown_placeholder = st.empty()  # Placeholder para o temporizador
            for i in range(10, 0, -1):  # Contagem regressiva de 10 a 1
                countdown_placeholder.write(f"⏳ Sorteando em {i} segundos...")
                time.sleep(1)

            # Limpa o temporizador
            countdown_placeholder.empty()

            # Sorteio
            nome_sorteado = random.choice(nomes_cadastrados)
            st.success(f"para béns O ganhador(a) é: {nome_sorteado} 🎉")
            st.balloons()
    else:
        st.warning("Nenhum nome cadastrado para realizar o sorteio.")
else:
    st.warning("A senha para realizar o sorteio é necessária!")

# Rodapé
st.markdown("---")
st.caption("Participe ❤ e ganhe você também!")