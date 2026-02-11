const API_BASE_URL = "http://localhost:8000";

function formatarData(isoString) {
  return new Date(isoString).toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function classeLotacao(nivel) {
  if (["baixa", "media", "alta"].includes(nivel)) return nivel;
  return "media";
}

async function carregarLinhas() {
  const container = document.getElementById("linhas-container");
  container.innerHTML = "<p>Carregando dados...</p>";

  try {
    const response = await fetch(`${API_BASE_URL}/linhas`);
    const linhas = await response.json();

    if (!linhas.length) {
      container.innerHTML = "<p>Nenhuma linha encontrada.</p>";
      return;
    }

    container.innerHTML = "";

    linhas.forEach((linha) => {
      const card = document.createElement("article");
      card.className = "card";

      const horariosHtml = linha.horarios
        .map((horario) => {
          const nivel = horario.parada.lotacao?.nivel || "media";
          return `
            <div class="horario">
              <p><strong>Parada:</strong> ${horario.parada.nome} (${horario.parada.bairro})</p>
              <p><strong>Saída:</strong> ${formatarData(horario.saida)} | <strong>Chegada:</strong> ${formatarData(horario.chegada)}</p>
              <p><strong>Trânsito:</strong> ${horario.status_transito}</p>
              <p>
                <strong>Lotação:</strong>
                <span class="badge ${classeLotacao(nivel)}">${nivel}</span>
              </p>
            </div>
          `;
        })
        .join("");

      card.innerHTML = `
        <h3>Linha ${linha.codigo}</h3>
        <p>${linha.nome}</p>
        ${horariosHtml}
      `;

      container.appendChild(card);
    });
  } catch (error) {
    container.innerHTML = "<p>Erro ao carregar dados da API.</p>";
    console.error(error);
  }
}

carregarLinhas();
