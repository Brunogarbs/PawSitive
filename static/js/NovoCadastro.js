// Função para sair
function sair() {
    localStorage.removeItem("token");
    localStorage.removeItem("userLogado");
    window.location.href = "../html/signin.html";
}

let msgError = document.querySelector('#msgError');
let msgSuccess = document.querySelector('#msgSuccess');

document.getElementById('animalForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Captura os dados do formulário
    const userId = JSON.parse(localStorage.getItem("userLogado"))?.id;
    const animal = document.getElementById('animal').value;
    const sexo = document.getElementById('sexo').value;
    const cor = document.getElementById('cor').value;
    const localizacao = document.getElementById('localizacao').value;
    const foto = document.getElementById('foto').files[0];
    const observacoes = document.getElementById('observacoes').value;
    

    if (!userId) {
        msgError.setAttribute('style', 'display: block');
        msgError.innerHTML = '<strong>Usuário não encontrado!</strong>';
        msgSuccess.setAttribute('style', 'display: none');
        return;
    }

    if (foto && window.FileReader) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Converte a imagem para Base64
            const fotoBase64 = e.target.result;

            // Cria um objeto para armazenar os dados
            const novoCadastro = {
                animal: animal,
                sexo: sexo,
                cor: cor,
                localizacao: localizacao,
                foto: fotoBase64,
                observacoes: observacoes,
                id_usuario: userId  // Adiciona o ID do usuário
            };

            // Envia os dados para o servidor Flask
            fetch('/cadastrar_animal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(novoCadastro)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao cadastrar animal');
                }
                return response.json();
            })
            .then(data => {
                msgSuccess.setAttribute('style', 'display: block');
                msgSuccess.innerHTML = '<strong>' + data.message + '</strong>';
                msgError.setAttribute('style', 'display: none');
                msgError.innerHTML = '';

                setTimeout(() => {
                    window.location.href = '/'; 
                    document.getElementById('animalForm').reset(); // Reseta o formulário
                }, 3000);
            })
            .catch(error => {
                msgError.setAttribute('style', 'display: block');
                msgError.innerHTML = '<strong>' + error.message + '</strong>';
                msgSuccess.innerHTML = '';
                msgSuccess.setAttribute('style', 'display: none');
            });
        };
        reader.readAsDataURL(foto);
    } else {
        msgError.setAttribute('style', 'display: block');
        msgError.innerHTML = '<strong>Preencha todos os campos corretamente antes de cadastrar</strong>';
        msgSuccess.innerHTML = '';
        msgSuccess.setAttribute('style', 'display: none');
    }
});

