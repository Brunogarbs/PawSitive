let btn = document.querySelector('#verSenha');
let btnConfirm = document.querySelector('#verConfirmSenha');

let nome = document.querySelector('#nome');
let labelNome = document.querySelector('#labelNome');
let validNome = false;

let usuario = document.querySelector('#usuario');
let labelUsuario = document.querySelector('#labelUsuario');
let validUsuario = false;

let senha = document.querySelector('#senha');
let labelSenha = document.querySelector('#labelSenha');
let validSenha = false;

let confirmSenha = document.querySelector('#confirmSenha');
let labelConfirmSenha = document.querySelector('#labelConfirmSenha');
let validConfirmSenha = false;

let msgError = document.querySelector('#msgError');
let msgSuccess = document.querySelector('#msgSuccess');

// Validação dos campos
function validarCampo(input, label, minLength, validationType) {
    if (input.value.length < minLength) {
        label.setAttribute('style', 'color: red');
        label.innerHTML = `${label.innerHTML} *Insira no mínimo ${minLength} caracteres`;
        input.setAttribute('style', 'border-color: red');
        return false;
    } else {
        label.setAttribute('style', 'color: white');
        label.innerHTML = label.innerHTML.split(' *')[0]; // Remove a mensagem de erro
        input.setAttribute('style', 'border-color: white');
        return true;
    }
}

nome.addEventListener('keyup', () => validNome = validarCampo(nome, labelNome, 3));
usuario.addEventListener('keyup', () => validUsuario = validarCampo(usuario, labelUsuario, 5));
senha.addEventListener('keyup', () => validSenha = validarCampo(senha, labelSenha, 6));

confirmSenha.addEventListener('keyup', () => {
    if (senha.value !== confirmSenha.value) {
        labelConfirmSenha.setAttribute('style', 'color: red');
        labelConfirmSenha.innerHTML = 'Confirmar Senha *As senhas não conferem';
        confirmSenha.setAttribute('style', 'border-color: red');
        validConfirmSenha = false;
    } else {
        labelConfirmSenha.setAttribute('style', 'color: white');
        labelConfirmSenha.innerHTML = 'Confirmar Senha';
        confirmSenha.setAttribute('style', 'border-color: white');
        validConfirmSenha = true;
    }
});

// Função para cadastrar o usuário
async function cadastrar() {
    if (validNome && validUsuario && validSenha && validConfirmSenha) {
        const newUser = {
            nome: nome.value,
            usuario: usuario.value,
            senha: senha.value
        };

        try {
            const response = await fetch('/cadastrar', { // Ajuste a URL se necessário
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newUser)
            });

            if (response.ok) {
                msgSuccess.setAttribute('style', 'display: block');
                msgSuccess.innerHTML = '<strong>Cadastrando usuário...</strong>';
                msgError.setAttribute('style', 'display: none');
                msgError.innerHTML = '';

                setTimeout(() => {
                    window.location.href = '../html/signin.html';
                }, 3000);
            } else {
                throw new Error('Erro ao cadastrar usuário');
            }
        } catch (error) {
            msgError.setAttribute('style', 'display: block');
            msgError.innerHTML = `<strong>${error.message}</strong>`;
            msgSuccess.innerHTML = '';
            msgSuccess.setAttribute('style', 'display: none');
        }
    } else {
        msgError.setAttribute('style', 'display: block');
        msgError.innerHTML = '<strong>Preencha todos os campos corretamente!</strong>';
        msgSuccess.innerHTML = '';
        msgSuccess.setAttribute('style', 'display: none');
    }
}

// Exibir/ocultar senha
btn.addEventListener('click', () => {
    let inputSenha = document.querySelector('#senha');
    inputSenha.setAttribute('type', inputSenha.getAttribute('type') === 'password' ? 'text' : 'password');
});

btnConfirm.addEventListener('click', () => {
    let inputConfirmSenha = document.querySelector('#confirmSenha');
    inputConfirmSenha.setAttribute('type', inputConfirmSenha.getAttribute('type') === 'password' ? 'text' : 'password');
});
