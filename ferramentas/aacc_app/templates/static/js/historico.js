const aluno_context = JSON.parse(document.getElementById("aluno_context").textContent);

$(document).ready(carregarDados());

function carregarDados() {
    const csrfToken = getCookie("csrftoken");

    $.ajax({
        url: `listar_aac_aluno?aluno=${aluno_context}`,
        type: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfToken  // Adicione o token CSRF ao cabeçalho da solicitação
        },
        success: function(data) {

            if(data != "{}"){

                var tabelaCorpo = $('.tabela-corpo');
                tabelaCorpo.empty();

                data =  JSON.parse(data);
                $.each(data, function (chave, valor) {
                    var linha = $('<tr>');
                    linha.append($('<td>').addClass("text-center w-20").text(converterFormatoData(valor.data_envio)));
                    linha.append($('<td>').addClass("text-center w-20").text(valor.titulo));
                    var botaoCelulaInformações = $('<td>').addClass('text-center w-20');
                    var botaoInformações = $('<button>').addClass('btn btn-primary informações').text('Informações');
                    botaoCelulaInformações.append(botaoInformações);
                    linha.append(botaoCelulaInformações);

                    var botaoCelulaVisualizar = $('<td>').addClass('text-center w-20');
                    var botaoVisualizar = $('<button>').addClass('btn btn-primary visualizar').text('Visualizar');
                    botaoCelulaVisualizar.append(botaoVisualizar);
                    linha.append(botaoCelulaVisualizar);

                    if(valor.status == 0) status_final = "Aguardando encaminhamento"
                    else if (valor.status == 1) status_final = "Aguardando avaliação"
                    else if (valor.status == 2) status_final = "Aguardando confirmação"
                    else status_final = "Confirmada"

                    linha.append($('<td>').addClass("text-center w-20").text(status_final));
                    
                    tabelaCorpo.append(linha);

                    // Adicionar evento de clique ao botão
                    botaoVisualizar.on('click', function() {
                        abrirArquivoEmNovaAba(valor.doc);
                    });

                    botaoInformações.on('click', function() {
                        abrirModalInformações(chave, valor);
                    })

                });
            } else {

                $('#mensagemNaoEncontrado').show();
                $('#corpo').hide();
            }

            
        },
        error: function(error) {
            console.error('Erro na requisição:', error);
        }
    });

    $.ajax({
        url: 'listar_users',
        method: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfToken  // Adicione o token CSRF ao cabeçalho da solicitação
        },
        success: function(data) {
            // Limpar o conteúdo atual do select
            $('#selecaoProfessor').empty();
            data =  JSON.parse(data);
            $.each(data, function (chave, valor) {
                $('#selecaoProfessor').append(`<option value="${valor.username}">${valor.first_name} ${valor.last_name}</option>`);
            })
            // Iterar sobre os dados recebidos e adicionar as opções ao select
        },
        error: function(xhr, status, error) {
            console.error('Erro ao buscar usuários:', error);
        }
    });
};


function abrirModalInformações(chave, valor) {
    // Atualize o ID da modal conforme necessário
    var modalInformações = $('#modalInformações');

    $("#aluno").text(valor.aluno);
    $("#atividade").text(valor.atividade);
    $("#area").text(valor.area);
    $("#titulo").text(valor.titulo);
    $("#início").text(valor.inicio);
    $("#fim").text(valor.fim);
    $("#carga").text(valor.carga_horaria);

    // Exiba a modal
    modalInformações.modal('show');
}

// Função para abrir o arquivo em uma nova aba
function abrirArquivoEmNovaAba(caminhoArquivo) {
    window.open(`documentos/${encodeURIComponent(caminhoArquivo)}`, '_blank');
}

function converterFormatoData(dataString) {
    // Cria um objeto Date com a string no formato "YYYY-MM-DD"
    var data = new Date(dataString);

    // Obtém os componentes da data (dia, mês, ano)
    var dia = data.getDate();
    var mes = data.getMonth() + 1; // Mês é baseado em zero, então adicionamos 1
    var ano = data.getFullYear();

    // Formata os componentes para o formato desejado
    var dataFormatada = `${dia}/${mes}/${ano}`;

    return dataFormatada;
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Verifica se o cookie começa com o nome desejado
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}