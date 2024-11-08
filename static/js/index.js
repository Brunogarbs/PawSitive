// Verificação se o usuário está logado
if (localStorage.getItem("token") == null) {
    alert("Você precisa estar logado para acessar essa página!");
    window.location.href = "./static/html/signin.html";
}

// Recuperação dos dados do usuário logado
let userLogado = JSON.parse(localStorage.getItem("userLogado"));

// Exibição do nome do usuário logado no elemento #logado
let logado = document.querySelector("#logado");
logado.innerHTML = 'Olá <span class="laranja">' + userLogado.nome + '!</span> Bem-vindo ao <span class="laranja">Paws</span>itive';

// Função para sair (deslogar)
function sair() {
    localStorage.removeItem("token");
    localStorage.removeItem("userLogado");
    window.location.href = "./static/html/signin.html";
}

// Função para redirecionar para a página de Novo Cadastro
function NovoCadastro() {
    window.location.href = "./static/html/NovoCadastro.html";
}
// Função para carregar os animais no carrossel
function carregarAnimais() {
    fetch('http://localhost:5000/animais')  // Ajuste para o endereço correto se necessário
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar os animais');
            }
            return response.json();
        })
        .then(animais => {
            const container = document.querySelector('#carouselItems'); // Container do carrossel
            const indicators = document.querySelector('#carouselIndicators'); // Indicadores do carrossel
            let isActive = true; // Controla a primeira imagem como ativa

            // Verifica se há animais para exibir
            if (animais.length === 0) {
                console.log("Nenhum animal encontrado.");
                return;
            }

            animais.forEach((animal, index) => {
                // Criando o item do carrossel
                const item = document.createElement('div');
                item.classList.add('carousel-item');
                if (isActive) {
                    item.classList.add('active');
                    isActive = false; // Desativa após o primeiro item
                }

                // Adicionando a imagem
                const img = document.createElement('img');
                img.src = animal.foto;
                img.classList.add('d-block', 'w-100'); // Tamanho completo da imagem
                item.appendChild(img);

                // Adicionando o corpo do card com as informações do animal
                const cardBody = document.createElement('div');
                cardBody.classList.add('carousel-caption', 'd-none', 'd-md-block');
                item.appendChild(cardBody);

                const nome = document.createElement('h5');
                nome.innerHTML = animal.nome;
                cardBody.appendChild(nome);

                const sexo = document.createElement('p');
                sexo.innerHTML = `<strong>Sexo:</strong> ${animal.sexo}`;
                cardBody.appendChild(sexo);

                const cor = document.createElement('p');
                cor.innerHTML = `<strong>Cor:</strong> ${animal.cor}`;
                cardBody.appendChild(cor);

                const localizacao = document.createElement('p');
                localizacao.innerHTML = `<strong>Localização:</strong> ${animal.localizacao}`;
                cardBody.appendChild(localizacao);

                const observacoes = document.createElement('p');
                observacoes.innerHTML = `<strong>Observações:</strong> ${animal.observacoes}`;
                cardBody.appendChild(observacoes);

                // Adiciona o item no carrossel
                container.appendChild(item);

                // Criando o indicador do carrossel
                const indicator = document.createElement('li');
                indicator.setAttribute('data-target', '#carouselExampleIndicators');
                indicator.setAttribute('data-slide-to', index);
                if (index === 0) {
                    indicator.classList.add('active');
                }
                indicators.appendChild(indicator);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar os animais:', error);
            alert('Houve um problema ao carregar os dados!');
        });
}

// Chama a função para carregar os animais quando a página for carregada
window.onload = carregarAnimais;