$(document).ready(carregarDados());

function carregarDados() {

    const csrfToken = getCookie("csrftoken");

    var informacaoUsuario = document.getElementById("nrousp").innerText;


    $.ajax({
        url: `nao_avaliadas?id_avaliador=${informacaoUsuario}`,
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
                    linha.append($('<td>').addClass("text-center w-20").text(valor.atividade));
                    var botaoCelulaInformações = $('<td>').addClass('text-center w-20');
                    var botaoInformações = $('<button>').addClass('btn btn-primary informações').text('Informações');
                    botaoCelulaInformações.append(botaoInformações);
                    linha.append(botaoCelulaInformações);
    
                    var botaoCelulaVisualizar = $('<td>').addClass('text-center w-20');
                    var botaoVisualizar = $('<button>').addClass('btn btn-primary visualizar').text('Visualizar');
                    botaoCelulaVisualizar.append(botaoVisualizar);
                    linha.append(botaoCelulaVisualizar);
    
                    var botaoCelulaAvaliar = $('<td>').addClass('text-center w-20');
                    var botaoAvaliar = $('<button>').addClass('btn btn-primary encaminhar').text('Avaliar');
                    botaoCelulaAvaliar.append(botaoAvaliar);
                    linha.append(botaoCelulaAvaliar);

                    var botaoCelulahistorico = $('<td>').addClass('text-center w-20');
                    var botaohistorico = $('<button>').addClass('btn btn-primary historico').text('Histórico');
                    botaoCelulahistorico.append(botaohistorico);
                    linha.append(botaoCelulahistorico);
                    
                    tabelaCorpo.append(linha);
    
                    // Adicionar evento de clique ao botão
                    botaoVisualizar.on('click', function() {
                        abrirArquivoEmNovaAba(valor.doc);
                    });
                    

                    botaoAvaliar.on('click', function() {
                        abrirModalAvaliar(chave, valor.carga_horaria);
                    });

                    botaoInformações.on('click', function() {
                        abrirModalInformações(chave, valor);
                    })

                    botaohistorico.on('click', function() {
                        historico_aluno(valor.aluno)
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
};

function abrirModalAvaliar(id_aacc, cargaHoraria) {
    // Atualize o ID da modal conforme necessário
    var modalAvaliar = $('#modalAvaliar');

    $("#carga_solicitada").text(cargaHoraria);


    modalAvaliar.data('id_aacc', id_aacc);

    // Exiba a modal
    modalAvaliar.modal('show');
}

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

function historico_aluno(aluno) {

    window.open(`historico_page?aluno=${aluno}`);

}

function confirmarAvaliacao(status) {
    // Aqui, você pode obter o valor do campo de seleção e processar o encaminhamento conforme necessário
    var comentarios = $('#comentarios').val();

    var carga_aprovada = $('#cargaaprovada').val()
    
    var id_AACC = $('#modalAvaliar').data('id_aacc');

    const csrfToken = getCookie("csrftoken");

    $.ajax({
        type: 'POST',
        url: 'avaliar',  
        data: {
            'comentarios': comentarios,
            'id_aacc': id_AACC,
            'status': status,
            'carga_aprovada': carga_aprovada
        },
        headers: {
            'X-CSRFToken': csrfToken 
        },
        success: function(response) {

            carregarDados()

        },
        error: function(error) {
            console.log(error);
        }
    });


    // Feche a modal após o processamento
    $('#modalAvaliar').modal('hide');
}

// Função para abrir o arquivo em uma nova aba
function abrirArquivoEmNovaAba(caminhoArquivo) {
    window.open(`documentos/${caminhoArquivo}`, '_blank');
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