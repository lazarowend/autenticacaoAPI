from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoa, Token
from secrets import token_hex

app = FastAPI()
def conecta_banco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, user: str, senha: str):
    session = conecta_banco()
    usuario = session.query(Pessoa).filter_by(usuario=user, senha=senha).all()
    if len(usuario) == 0:
        x = Pessoa(nome=nome, usuario=user, senha=senha)
        session.add(x)
        session.commit()
        return {'status': 'sucesso'}
    elif len(usuario) > 0:
        return {'status': 'Usuário já cadastrado'}

@app.post('/login')
def login(usuario: str, senha: str):
    session = conecta_banco()
    user = session.query(Pessoa).filter_by(usuario=usuario, senha=senha).all()
    if len(user) == 0:
        return {'Status': 'Usuario inexistente'}
    
    while True:
        token = token_hex(50)
        token_existe = session.query(Token).filter_by(token=token).all()
        if len(token_existe) == 0:
            pessoa_existe = session.query(Token).filter_by(id_pessoa=user[0].id).all()
            if len(pessoa_existe) == 0:
                novo_token = Token(id_pessoa=user[0].id, token=token)
                session.add(novo_token)
            else:
                pessoa_existe[0].token = token
            session.commit()
            break
        
    return token