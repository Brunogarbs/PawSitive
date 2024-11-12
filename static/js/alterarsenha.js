// Função para sair
function index() {
    window.location.href = "/";
}


function sair() {
    localStorage.removeItem("token");
    localStorage.removeItem("userLogado");
    window.location.href = "../html/signin.html";
}

function NovoCadastro() {
    window.location.href = "../html/NovoCadastro.html";
}

function RemoverAnimal() {
    window.location.href = "../html/removeranimal.html";
}



document.getElementById('alterar-senha-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const usuario = document.getElementById('usuario').value;
    const senha_atual = document.getElementById('senha_atual').value;
    const nova_senha = document.getElementById('nova_senha').value;

    const dados = {
        usuario: usuario,
        senha_atual: senha_atual,
        nova_senha: nova_senha
    };

    fetch('/alterar_senha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('mensagem').innerText = data.message;
    })
    .catch(error => {
        document.getElementById('mensagem').innerText = "Erro ao alterar a senha.";
    });
});
