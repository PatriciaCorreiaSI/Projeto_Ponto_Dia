from datetime import datetime
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlalchemy.orm import Session
from models import User, RegistroPonto
from database import get_db
from sqlalchemy import func
import security
import models

app = FastAPI()

# Liberação de segurança (CORS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que o Vite (5173) fale com o Python (8000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class UserCreate(BaseModel):
    email: str
    senha: str

@app.post("/usuarios/cadastro")
def cadastrar_usuario(usuario: UserCreate, db:Session = Depends(get_db)):
    try:
        # Verificar se o usuário já existe
        usuario_existente = db.query(models.User).filter(models.User.email == usuario.email).first()
        if usuario_existente:
            return{"erro": "Este email já está cadastrado."}
        
        # Transforma a senha em HASH (Segurança!)
        senha_criptografada = security.gerar_hash_senha(usuario.senha)
        # Sava no banco de dados
        novo_usuario = models.User(email=usuario.email, hashed_password = senha_criptografada)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        print(f"Sucesso: Usuário {novo_usuario.email} salvo com ID {novo_usuario.id}")

        return {"mesage": "Usuário criado com sucesso!", "id": novo_usuario.id}
    
    except Exception as e:
        print(f"Erro no servidor: {e}")
        return {"detalhe": str(e)}

# Cria as tabelas no banco de dados se elas não existirem
models.Base.metadata.create_all(bind=engine)

# Definindo o que o React vai nos enviar
class DadosPonto(BaseModel):
    entrada: str
    saida: str

@app.post("/usuarios/login")
def login(usuario: UserCreate, db: Session = Depends(get_db)):
    # Busca o usuário pelo email
    db_user = db.query(models.User).filter(models.User.email == usuario.email).first()

    # Se não achar o email ou a senha não bater...
    if not db_user or not security.verificar_senha(usuario.senha, db_user.hashed_password):
        return {"erro": "Email ou senha incorretos"}
    
    # Se deu tudo certo, cria o crachá (Token)
    token = security.criar_token_acesso(dados={"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "mensagem": f"Bem-Vindo(a), {db_user.email}!"
    }

@app.post("/ponto")
async def lancar_ponto(ponto: dict, db: Session = Depends(get_db), email_usuario: str = Depends(security.obter_usuario_logado)):
    # Verifica usuário logado
    usuario = db.query(models.User).filter(models.User.email == email_usuario).first()
    if not usuario:
        return {"erro": "Usuário não encontrado."}

    str_entrada = ponto.get("entrada")
    str_saida = ponto.get("saida")

    formato = "%Y-%m-%d %H:%M:%S"
    dt_ent = datetime.strptime(str_entrada, formato)
    dt_sai = datetime.strptime(str_saida, formato)

    diferenca = dt_sai - dt_ent
    horas_trabalhadas = round(diferenca.total_seconds() / 3600, 2)

    # Saldo do dia com jornada padrão de 8 horas
    jornada_padrao = 8.0
    saldo_dia = round(horas_trabalhadas - jornada_padrao, 2)

    novo_registro = RegistroPonto(
        entrada=str_entrada,
        saida=str_saida,
        total_trabalhado=horas_trabalhadas,
        saldo=saldo_dia,
        owner_id=usuario.id
    )

    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)

    status = "Positivo" if saldo_dia >= 0 else "Negativo"

    return {
        "mensagem": "Ponto registrado com sucesso!",
        "total": horas_trabalhadas,
        "saldo": saldo_dia,
        "saldo_dia": f"{saldo_dia}h",
        "status": status
    }

# Opcional: Rota para testar a API para a porta da frente não dar erro
@app.get("/historico-pontos")

def listar_pontos(db: Session = Depends(get_db), email_usuario:str = Depends(security.obter_usuario_logado)): # A blindagem está aqui
    
    #Agora o sistema só mostra os pontos que pertencem a esse emai!
    usuario = db.query(models.User).filter(models.User.email == email_usuario).first()
    #O SQAlchemy faz um SELECT * FROM registro_ponto
    return db.query(models.RegistroPonto).filter(models.RegistroPonto.owner_id == usuario.id).all()

@app.delete("/deletar-ponto/{ponto_id}")

def deletar_ponto(ponto_id: int, db: Session = Depends(get_db)):
    ponto = db.query(models.RegistroPonto).filter(models.RegistroPonto.id == ponto_id).first()
    if not ponto:
        return {"erro": "Registro não encontrado!"}
    
    db.delete(ponto)
    db.commit()
    return {"mesagem": "Registro deletado com sucesso!"}

@app.get("/saldo-geral")

def buscar_saldo(db: Session = Depends(get_db), email_usuario: str = Depends(security.obter_usuario_logado)):
    usuario = db.query(models.User).filter(models.User.email == email_usuario).first()
    if not usuario:
        return {"erro": "Usuário não encontrado."}

    total_acumulado = db.query(func.sum(models.RegistroPonto.saldo))
    total_acumulado = total_acumulado.filter(models.RegistroPonto.owner_id == usuario.id).scalar()

    return {"saldo_total": round(total_acumulado or 0, 2)}

@app.get("/usuario/saldo-geral")
async def obter_saldo(db: Session = Depends(get_db)):
    registros = db.query(RegistroPonto).all()
    total_horas = sum(reg.total_trabalhado for reg in registros if reg.total_trabalhado is not None)

    horas = int(total_horas)
    minutos = int((total_horas - horas) * 60)

    return {
        "saldo_horas": total_horas,
        "saldo_formatado": f"{horas}h {minutos}min"
    }
