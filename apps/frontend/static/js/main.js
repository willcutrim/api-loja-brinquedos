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
  const token = getToken();
  if (!token) {
    alert("Você precisa estar logado.");
    window.location.href = "/login/";
    return;
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`
  };

  // 🔄 Carrega clientes em qualquer página com <select id="cliente">
  const selectCliente = document.getElementById("cliente");
  if (selectCliente) {
    fetchAuth("/api/clientes/")
      .then(clientes => {
        if (!clientes || !Array.isArray(clientes)) return;
        selectCliente.innerHTML = '<option value="">Selecione um cliente</option>';
        clientes.forEach(cliente => {
          const opt = document.createElement("option");
          opt.value = cliente.id;
          opt.textContent = cliente.nome;
          selectCliente.appendChild(opt);
        });
      });
  }

  // 🧾 Cadastrar Venda (qualquer página com form-venda)
  const formVenda = document.getElementById("form-venda");
  if (formVenda) {
    formVenda.addEventListener("submit", async (e) => {
      e.preventDefault();

      const cliente = document.getElementById("cliente").value;
      const data = document.getElementById("data").value;
      const valor = document.getElementById("valor").value;

      if (!cliente || !data || !valor) {
        alert("Preencha todos os campos!");
        return;
      }

      const payload = {
        cliente_id: parseInt(cliente),
        data,
        valor: parseFloat(valor)
      };

      const msg = document.getElementById("resposta-venda");

      try {
        const res = await fetch("/api/vendas/", {
          method: "POST",
          headers,
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          msg.className = "alert alert-success mt-3";
          msg.textContent = "✅ Venda cadastrada com sucesso!";
          formVenda.reset();
        } else {
          const err = await res.json();
          msg.className = "alert alert-danger mt-3";
          msg.textContent = "❌ Erro: " + JSON.stringify(err);
        }

        msg.classList.remove("d-none");
      } catch (err) {
        alert("Erro ao enviar requisição.");
        console.error(err);
      }
    });
  }

  // 🧑‍💼 Cadastro de clientes (página /clientes/)
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
          headers,
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
        if (div) {
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
        }
      });
  }

  // 📊 Estatísticas
  if (window.location.pathname === "/clientes/estatisticas/") {
    fetchAuth("/api/vendas/estatisticas/destaques/")
      .then(data => {
        if (!data) return;
        document.getElementById("destaques").innerHTML = `
          <div class="row text-center g-3">
            <div class="col-md-4">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body">
                  <h6 class="card-title text-muted">Maior Volume</h6>
                  <h5 class="card-text">${data.maior_volume?.nome || '-'}</h5>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body">
                  <h6 class="card-title text-muted">Maior Média</h6>
                  <h5 class="card-text">${data.maior_media?.nome || '-'}</h5>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card shadow-sm border-0 h-100">
                <div class="card-body">
                  <h6 class="card-title text-muted">Maior Frequência</h6>
                  <h5 class="card-text">${data.maior_frequencia?.nome || '-'}</h5>
                </div>
              </div>
            </div>
          </div>
        `;
      });

    fetchAuth("/api/vendas/estatisticas/total-por-dia/")
      .then(data => {
        if (!data || !Array.isArray(data)) return;
        new Chart(document.getElementById('graficoVendas'), {
          type: 'bar',
          data: {
            labels: data.map(i => new Date(i.data).toLocaleDateString('pt-BR')),
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
