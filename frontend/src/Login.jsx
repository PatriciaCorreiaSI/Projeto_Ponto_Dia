import { useState } from "react";
import axios from "axios";
import "./index.css";

function Login({ setToken }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleLogin = async (e) => {
    if (e && typeof e.preventDefault === "function") e.preventDefault(); // Evita que a página recarregue
    console.log("Iniciando handleLogin...");

    setErro(""); // Limpa erros antigos

    try {
      console.log("Chamando API do Python...");
      // Chamada para a nova rota de login no Python
      const response = await axios.post(
        "http://127.0.0.1:8000/usuarios/login",
        {
          email: email,
          senha: senha,
        },
      );

      console.log("Resposta completa do servidor:", response.data);

      if (response.data.erro) {
        setErro(response.data.erro);
        return;
      }

      const tokenRecebido = response.data.access_token;

      if (tokenRecebido) {
        console.log("Sucesso! Guardando token...");

        // Salva na "mochila" do navegador para não deslogar ao dar F%
        localStorage.setItem("token", tokenRecebido);

        // Avisa o restante do App que estamos logados!
        setToken(tokenRecebido);
        setErro("");
        return;
      }

      setErro("Email ou senha incorretos. Tente novamente!");
    } catch (error) {
      const mensagem =
        error?.response?.data?.erro ||
        error?.response?.data?.detail ||
        "Email ou senha incorretos. Tente novamente!";
      setErro(mensagem);
      console.error("Erro ao fazer login:", error);
    }
  };

  return (
    <div
      className="login-container"
      style={{ padding: "20px", maxWidth: "300px", margin: "auto" }}
    >
      <h2>Ponto do Dia - Login</h2>
      <form onSubmit={(e) => handleLogin(e)}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          autoComplete="username"
          onChange={(e) => setEmail(e.target.value)}
          required
        ></input>
        <br></br>
        <input
          type="password"
          name="password"
          placeholder="Senha"
          value={senha}
          autoComplete="current-password"
          onChange={(e) => setSenha(e.target.value)}
          required
        ></input>
        <br></br>
        <button
          type="button"
          onClick={(e) => handleLogin(e)}
          style={{ cursor: "pointer", zIndex: "1000" }}
        >
          Entrar
        </button>
      </form>
      {erro && <p style={{ color: "red" }}>{erro}</p>}
    </div>
  );
}
export default Login;
