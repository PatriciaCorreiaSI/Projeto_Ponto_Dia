import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

function Dashboard({ token }) {
  const [pontos, setPontos] = useState([]);
  const [entrada, setEntrada] = useState("");
  const [saida, setSaida] = useState("");
  const [horaEntrada, setHoraEntrada] = useState("");
  const [horaSaida, setHoraSaida] = useState("");
  const [saldoGeral, setSaldoGeral] = useState(0);
  const [resultado, setResultado] = useState(null);

  // Função para buscar os dados no back-end (Python)
  const carregarHistorico = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(
        "http://127.0.0.1:8000/historico-pontos",
        {
          headers: {
            Authorization: `Bearer ${token}`, // Aqui o axios entrega o crachá
          },
        },
      );

      setPontos(response.data); // O axios ja traz o JSON pronto e .data
    } catch (error) {
      console.error("Erro de autenticação: ", error);
    }
  };

  useEffect(() => {
    carregarHistorico();
  }, []);

  const carregarSaldoGeral = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:8000/saldo-geral", {
        headers: {
          // Aqui enviamos o crachá para o Python
          Authorization: `Bearer ${token}`,
        },
      });
      setSaldoGeral(response.data.saldo_total);
    } catch (error) {
      console.error("Erro na busca pelo saldo geral:", error);
    }
  };

  // Hook que roda a função carregarSaldoGeral assim que a página abre
  useEffect(() => {
    carregarSaldoGeral();
  }, []);

  const handleLancarPonto = async (e) => {
    e.preventDefault();

    try {
      const dadosParaEnviar = {
        entrada: `${entrada} ${horaEntrada}:00`,
        saida: `${saida} ${horaSaida}:00`,
      };

      // Fazemos a requisição POST para o servidor (Python)
      const resposta = await axios.post(
        "http://127.0.0.1:8000/ponto",
        dadosParaEnviar,
        { headers: { Authorization: `Bearer ${token}` } },
      );

      alert("Ponto registrado com sucesso!");
      setEntrada("");
      setSaida("");
      setHoraEntrada("");
      setHoraSaida("");

      if (resposta.data) {
        setResultado(resposta.data);
      }

      // Atualiza a tela para o novo ponto aparecer
      carregarHistorico();
      carregarSaldoGeral();
    } catch (error) {
      console.error(error);
      alert("Erro ao salvar. Sua sessão pode ter expirado.");
    }
  };

  const deletarRegistro = async (id) => {
    if (window.confirm("Tem certeza dque deseja apagar este registro?")) {
      await axios.delete(`http://127.0.0.1:8000/deletar-ponto/${id}`);
      carregarHistorico();
      carregarSaldoGeral();
    }
  };

  return (
    <div
      style={{ fontFamily: "sans-serif", padding: "20px", textAlign: "center" }}
    >
      <h1>Ponto do Dia</h1>

      <div
        style={{
          border: "1px solid #ccc",
          padding: "20px",
          borderRadius: "8px",
          display: "inline-block",
        }}
      >
        <div
          style={{
            borderBottom: "2px solid #555",
            padding: "10px",
            borderRadius: "8px",
            display: "flex",
            justifyContent: "center",
            color: "#a3b84a",
          }}
        >
          Saldo Geral: {saldoGeral}
        </div>

        <h3>Entrada</h3>
        <label>Data</label>
        <input
          type="date"
          value={entrada}
          onChange={(e) => setEntrada(e.target.value)}
        />
        <br />
        <label>Hora</label>
        <input
          type="time"
          value={horaEntrada}
          onChange={(e) => setHoraEntrada(e.target.value)}
        />

        <hr />

        <h3>Saída</h3>
        <label>Data</label>
        <input
          type="date"
          value={saida}
          onChange={(e) => setSaida(e.target.value)}
        />
        <br />
        <label>Hora</label>
        <input
          type="time"
          value={horaSaida}
          onChange={(e) => setHoraSaida(e.target.value)}
        />

        <br />
        <br />
        <button
          onClick={handleLancarPonto}
          style={{ padding: "10px 20px", cursor: "pointer" }}
        >
          Submeter
        </button>
      </div>

      {resultado && (
        <div
          style={{
            marginTop: "20px",
            color: resultado.saldo >= 0 ? "green" : "red",
          }}
        >
          <p>Total de horas trabalhadas: {resultado.total}</p>
          <p>Saldo do dia: {resultado.saldo}</p>
          <p>Status: {resultado.status}</p>
        </div>
      )}

      <div
        style={{
          marginTop: "40px",
          width: "100%",
          maxWidth: "600px",
          margin: "0 auto",
        }}
      >
        <h3>Seu Histórico de Ponto</h3>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "10px",
          }}
        >
          <thead>
            <tr style={{ borderBottom: "2px solid #555", textAlign: "center" }}>
              <th>Ações</th>
              <th>Data</th>
              <th>Entrada</th>
              <th>Saída</th>
              <th>Saldo</th>
            </tr>
          </thead>
          <tbody>
            {pontos.map((ponto) => (
              <tr key={ponto.id} style={{ borderBottom: "1px solid #333" }}>
                <td>
                  <button
                    onClick={() => deletarRegistro(ponto.id)}
                    style={{
                      background: "transparent",
                      border: "none",
                      cursor: "pointer",
                      color: "#FF5252",
                    }}
                  >
                    Deletar
                  </button>
                </td>
                <td>{ponto.entrada.split(" ")[0]}</td>
                <td>{ponto.entrada.split(" ")[1]}</td>
                <td>{ponto.saida.split(" ")[1]}</td>
                <td
                  style={{
                    color: ponto.saldo >= 0 ? "#4CAF50" : "#FF5252",
                    fontWeight: "bold",
                  }}
                >
                  {ponto.saldo}h
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
