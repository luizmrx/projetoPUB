$(document).ready(function() {
    
    carregarDados()

    $('#encaminharSelecionadas').prop('disabled', true).removeClass('btn-primary').addClass('btn-secondary');  // Initially disable the button

    // Add event listener for checkbox changes
    $('.tabela-corpo').on('change', '.select-row', function() {
        updateEncaminharButtonState();
    });

    // Add event listener for the "Select All" checkbox
    $('#selectAll').on('change', function() {
        $('.select-row').prop('checked', this.checked);
        updateEncaminharButtonState();
    });

     // Add event listener for the "Encaminhar Selecionadas" button
     $('#encaminharSelecionadas').on('click', function() {
        if (!$(this).prop('disabled')) {
            abrirModalEncaminharMultiplas();
        }
    });
});

function carregarDados() {
    const csrfToken = getCookie("csrftoken");

    $.ajax({
        url: 'nao_encaminhadas',
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
                    var linha = $('<tr>').data('id', chave);
                    var checkbox = $('<td>').addClass('text-center w-5').append(
                        $('<input>').attr('type', 'checkbox').addClass('select-row')
                    );
                    linha.append(checkbox);
                    linha.append($('<td>').addClass("text-center w-20").text(converterFormatoData(valor.data_envio)));
                    linha.append($('<td>').addClass("text-center w-20").text(valor.atividade ));
                    var botaoCelulaInformações = $('<td>').addClass('text-center w-20');
                    var botaoInformações = $('<button>').addClass('btn btn-primary informações').text('Informações');
                    botaoCelulaInformações.append(botaoInformações);
                    linha.append(botaoCelulaInformações);

                    var botaoCelulaVisualizar = $('<td>').addClass('text-center w-20');
                    var botaoVisualizar = $('<button>').addClass('btn btn-primary visualizar').text('Visualizar');
                    botaoCelulaVisualizar.append(botaoVisualizar);
                    linha.append(botaoCelulaVisualizar);

                    var botaoCelulaEncaminhar = $('<td>').addClass('text-center w-20');
                    var botaoEncaminhar = $('<button>').addClass('btn btn-primary encaminhar').text('Encaminhar');
                    botaoCelulaEncaminhar.append(botaoEncaminhar);
                    linha.append(botaoCelulaEncaminhar);
                    
                    tabelaCorpo.append(linha);

                    // Adicionar evento de clique ao botão
                    botaoVisualizar.on('click', function() {
                        abrirArquivoEmNovaAba(valor.doc);
                    });

                    botaoEncaminhar.on('click', function() {
                        abrirModalEncaminhar(chave);
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
    // Event listener for the "Select All" checkbox
    $('#selectAll').on('change', function() {
        $('.select-row').prop('checked', this.checked);
    });

    // Event listener for the "Encaminhar Selecionadas" button
    $('#encaminharSelecionadas').on('click', function() {
        abrirModalEncaminharMultiplas();
    });

    // Event listener for the "Encaminhar" button in the modal
    $('#encaminharConfirmar').on('click', function() {
        confirmarEncaminhamento();
    });
};



function abrirModalEncaminhar(id_aacc) {
    var modalEncaminhar = $('#modalEncaminhar');
    modalEncaminhar.data('id_aacc', id_aacc);
    modalEncaminhar.data('multiple', false); // Single selection
    modalEncaminhar.modal('show');
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

function abrirModalEncaminharMultiplas() {
    var selectedIds = [];
    $('.select-row:checked').each(function() {
        var row = $(this).closest('tr');
        var id = row.data('id');
        selectedIds.push(id);
    });

    if (selectedIds.length === 0) {
        alert('Por favor, selecione pelo menos uma linha.');
        return;
    }

    var modalEncaminhar = $('#modalEncaminhar');
    modalEncaminhar.data('id_aaccs', selectedIds);
    modalEncaminhar.data('multiple', true); // Multiple selection
    modalEncaminhar.modal('show');
}

function confirmarEncaminhamento() {
    var professorSelecionado = $('#selecaoProfessor').val();
    var modalEncaminhar = $('#modalEncaminhar');
    var isMultiple = modalEncaminhar.data('multiple');
    const csrfToken = getCookie("csrftoken");

    if (isMultiple) {
        var id_AACCs = modalEncaminhar.data('id_aaccs');

        $.ajax({
            type: 'POST',
            url: 'encaminhar_selecionadas',
            data: {
                'id_avaliador': professorSelecionado,
                'id_aaccs': id_AACCs.join(",")
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                carregarDados();
            },
            error: function(error) {
                console.log(error);
            }
        });

    } else {
        var id_AACC = modalEncaminhar.data('id_aacc');

        $.ajax({
            type: 'POST',
            url: 'encaminhar',
            data: {
                'id_avaliador': professorSelecionado,
                'id_aacc': id_AACC
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                carregarDados();
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    $('#modalEncaminhar').modal('hide');
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

// Update the state of the "Encaminhar Selecionadas" button based on checkbox selection
function updateEncaminharButtonState() {
    var selectedCount = $('.select-row:checked').length;
    var button = $('#encaminharSelecionadas');

    if (selectedCount > 0) {
        button.prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary');
        $('.encaminhar').prop('disabled', true).removeClass('btn-primary').addClass('btn-secondary');
    } else {
        button.prop('disabled', true).removeClass('btn-primary').addClass('btn-secondary');
        $('.encaminhar').prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary');
    }
}