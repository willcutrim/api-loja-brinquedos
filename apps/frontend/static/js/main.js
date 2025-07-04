function letraFaltante(nome) {
  const abc = 'abcdefghijklmnopqrstuvwxyz'.split('');
  const usado = nome.toLowerCase().replace(/[^a-z]/g, '').split('');
  for (let l of abc) if (!usado.includes(l)) return l;
  return '-';
}

function getToken() {
  return localStorage.getItem("access_token");
}

function fetchAuth(url) {
  const token = getToken();
  if (!token) {
    window.location.href = "/login/";
    return Promise.reject("Sem token");
  }

  return fetch(url, {
    headers: { Authorization: "Bearer " + token }
  })
  .then(res => {
    if (!res.ok) {
      if (res.status === 401) window.location.href = "/login/";
      throw new Error("Erro de autenticação");
    }
    return res.json();
  })
  .catch(error => {
    console.error("Erro ao buscar:", error);
    return null;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname === "/clientes/") {
    const form = document.getElementById("clienteForm");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const payload = {
          nome: document.getElementById("nome").value,
          email: document.getElementById("email").value,
          nascimento: document.getElementById("nascimento").value
        };
        fetch("/api/clientes/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
          },
          body: JSON.stringify(payload)
        })
        .then(res => {
          if (!res.ok) throw new Error("Erro ao cadastrar cliente");
          return res.json();
        })
        .then(() => {
          alert("Cliente cadastrado com sucesso!");
          form.reset();
          location.reload();
        })
        .catch(err => alert("Erro: " + err.message));
      });
    }

    fetchAuth("/api/clientes/")
      .then(clientes => {
        if (!clientes || !Array.isArray(clientes)) {
          document.getElementById("clientes-list").innerHTML = "Erro ao carregar clientes.";
          return;
        }

        const div = document.getElementById("clientes-list");
        div.innerHTML = `
          <table class="table table-striped">
            <thead><tr><th>Nome</th><th>Email</th><th>Nascimento</th><th>Letra Faltante</th></tr></thead>
            <tbody>
              ${clientes.map(c => `
                <tr>
                  <td>${c.nome}</td>
                  <td>${c.email}</td>
                  <td>${c.nascimento}</td>
                  <td>${letraFaltante(c.nome)}</td>
                </tr>`).join('')}
            </tbody>
          </table>
        `;
      });
  }

  if (window.location.pathname === "/clientes/estatisticas/") {
    fetchAuth("/api/vendas/estatisticas/destaques/")
      .then(data => {
        if (!data) return;
        document.getElementById("destaques").innerHTML = `
          <div class="card p-3">
            <p><strong>Maior Volume:</strong> ${data.maior_volume?.nome || '-'}</p>
            <p><strong>Maior Média:</strong> ${data.maior_media?.nome || '-'}</p>
            <p><strong>Maior Frequência:</strong> ${data.maior_frequencia?.nome || '-'}</p>
          </div>
        `;
      });

    fetchAuth("/api/vendas/estatisticas/total-por-dia/")
      .then(data => {
        if (!data || !Array.isArray(data)) return;
        new Chart(document.getElementById('graficoVendas'), {
          type: 'bar',
          data: {
            labels: data.map(i => i.data),
            datasets: [{
              label: 'Vendas por Dia',
              data: data.map(i => i.total),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true }
            }
          }
        });
      });
  }
});
