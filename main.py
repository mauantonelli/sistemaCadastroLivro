import psycopg2
from config import DB_CONFIG


def conectar_banco():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexão ao banco de dados PostgreSQL bem-sucedida!")
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados PostgreSQL:", e)
        return None

def criar_tabela(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS bandas (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            ano_de_formacao INT,
            integrantes TEXT[]
        );
        ''')
        conn.commit()
        cur.close()
        print("Tabela 'bandas' criada com sucesso!")
    except psycopg2.Error as e:
        print("Erro ao criar tabela:", e)

def cadastrar_banda(conn, nome, ano_de_formacao, integrantes):
    try:
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO bandas (nome, ano_de_formacao, integrantes)
        VALUES (%s, %s, %s)
        RETURNING id;
        ''', (nome, ano_de_formacao, integrantes))
        id_banda = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"Banda cadastrada com sucesso! ID: {id_banda}")
    except psycopg2.Error as e:
        print("Erro ao cadastrar banda:", e)

def cadastrar_album(conn, nome_banda, album_nome, ano_lancamento):
    try:
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO albuns (nome_banda, nome_album, ano_lancamento)
        VALUES (%s, %s, %s);
        ''', (nome_banda, album_nome, ano_lancamento))
        conn.commit()
        cur.close()
        print("Álbum cadastrado com sucesso para a banda", nome_banda)
    except psycopg2.Error as e:
        print("Erro ao cadastrar álbum:", e)

def listar_bandas(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
        SELECT * FROM bandas;
        ''')
        bandas = cur.fetchall()
        cur.close()
        print("Listagem de bandas:")
        for banda in bandas:
            print("ID:", banda[0])
            print("Nome:", banda[1])
            print("Ano de Formação:", banda[2])
            print("Integrantes:", banda[3])
            print("-------------------------")
    except psycopg2.Error as e:
        print("Erro ao listar bandas:", e)

def menu_cadastro():
    print("Digite 1 para cadastrar a banda")
    print("Digite 2 para cadastrar o álbum")
    print("Digite 3 para listar as bandas")

def banda_matriz():
    conn = conectar_banco()
    if conn is None:
        return

    criar_tabela(conn)

    while True:
        menu_cadastro()
        opcao = input("Digite a opção desejada (ou 's' para sair): ")

        if opcao == '1':
            nome = input("Digite o nome da banda: ")
            ano_de_formacao = int(input("Digite o ano de formação da banda: "))
            integrantes = input("Digite os integrantes da banda (separados por vírgula): ").split(',')
            cadastrar_banda(conn, nome, ano_de_formacao, integrantes)
        elif opcao == '2':
            nome_banda = input("Digite o nome da banda: ")
            album_nome = input("Digite o nome do álbum: ")
            ano_lancamento = int(input("Digite o ano de lançamento do álbum: "))
            cadastrar_album(conn, nome_banda, album_nome, ano_lancamento)
        elif opcao == '3':
            listar_bandas(conn)
        elif opcao == 's':
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

banda_matriz()