let btn = document.querySelector('.fa-eye');

btn.addEventListener('click', () => {
    let inputSenha = document.querySelector('#senha');
    if (inputSenha.getAttribute('type') === 'password') {
        inputSenha.setAttribute('type', 'text');
    } else {
        inputSenha.setAttribute('type', 'password');
    }
});

let usuario = document.querySelector('#usuario');
let userLabel = document.querySelector('#userLabel');
let senha = document.querySelector('#senha');
let senhaLabel = document.querySelector('#senhaLabel');
let msgError = document.querySelector('#msgError');

function entrar() {
    const userData = {
        usuario: usuario.value,
        senha: senha.value
    };

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Usuário ou senha incorretos');
        }
        return response.json();
    })
    .then(data => {
        // Sucesso no login
        localStorage.setItem('token', Math.random().toString(16).substr(2) + Math.random().toString(16).substr(2));
        localStorage.setItem('userLogado', JSON.stringify(data.user));
        window.location.href = '/'; 

    })
    .catch(error => {
        // Falha no login
        userLabel.setAttribute('style', 'color: red');
        usuario.setAttribute('style', 'border-color: red');
        senhaLabel.setAttribute('style', 'color: red');
        senha.setAttribute('style', 'border-color: red');
        msgError.setAttribute('style', 'display: block');
        msgError.innerHTML = error.message;
        usuario.focus();
    });
}
