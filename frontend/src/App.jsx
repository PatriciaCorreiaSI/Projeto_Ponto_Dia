import { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import './App.css';
import './index.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  
  // Função para sair do sistema (limpa a mochila e o estado)
  const handleLogout = () =>{
    localStorage.removeItem('token');
    setToken(null);
  }

  if (!token) {
    return <Login setToken={setToken}/>
  }

  return (
    <div className="app-container">
      <header style={{
        display:"flex", 
        justifyContent:"space-between", 
        padding:"1rem", 
        background:"#282c34", 
        color:"white"
      }}>
        <h1 style={{margin:"0", fontSize:"1.2rem"}}>Ponto_Dia</h1>
        <button onClick={handleLogout} style={{
          background:"#ff4d4d" ,
          color:"white",
          border:"none",
          padding:"5px 15px",
          borderRadius:"4px",
          cursor:"pointer"
        }}
        >Sair</button>
      </header>
      <Dashboard token={token}/>
    </div>
  )
}

export default App;