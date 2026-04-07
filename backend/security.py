from passlib.context import CryptContext
import bcrypt
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader


# Isso diz ao Swagger: crie um campo chamado Authorization onde eu vou colar o token
oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False)

# Carrega configuração de variáveis de ambiente (para dev usando dotenv, execute manualmente / use sua alternativa)
# Se quiser usar python-dotenv, instale com: pip install python-dotenv
# E crie arquivo backend/.env com SECRET_KEY.

SECRET_KEY = os.getenv("SECRET_KEY", "MINHA_CHAVE_SUPERSECRETA_2026")
if SECRET_KEY == "MINHA_CHAVE_SUPERSECRETA_2026":
    print("[security] AVISO: SECRET_KEY não definido. Usando valor padrão de desenvolvimento.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES", "60"))

def obter_usuario_logado(token: str = Depends(oauth2_scheme)):
    erro_autorizacao = HTTPException(status_code=401, detail="Token inválido ou expirado!")

    if not token:
        raise erro_autorizacao
    
    try:
        token_limpo = token.replace("Bearer ", "")

        payload = jwt.decode(token_limpo, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise erro_autorizacao
        return email
    except JWTError:
        raise erro_autorizacao


def criar_token_acesso(dados: dict):
    para_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expiracao})

    # Gera o crachá assinado
    token_jwt = jwt.encode(para_codificar, SECRET_KEY, algorithm= ALGORITHM)
    return token_jwt
# COnfiguramos o algoritmo Bcrypt 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def gerar_hash_senha(senha: str):
    # Transforma a string em bytes, gera o salt e o hash
    pwd_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hash_bytes.decode('utf-8')
# Tranforma de volta em string par ao banco

def verificar_senha(senha_pura: str, senha_hash: str):
    pwd_bytes = senha_pura.encode('utf-8')
    hash_bytes = senha_hash.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)
    