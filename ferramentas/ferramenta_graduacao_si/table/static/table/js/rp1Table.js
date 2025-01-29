
let auto_profs = JSON.parse(document.getElementById("auto_profs").textContent);
let total_profs = JSON.parse(document.getElementById("total_profs").textContent);
const dtl_profs = JSON.parse(document.getElementById("dtl_profs").textContent);
const restricos_hro = JSON.parse(document.getElementById("rest").textContent);
const impedimentos_totais = JSON.parse(document.getElementById("impedimentos_totais").textContent);

function openModal(title, messages) {
    const modalBody = document.getElementById("modalBody");
    modalBody.innerText = messages;
    $("#myModalLabel").html(title);
    const myModal = new bootstrap.Modal(document.getElementById("myModal"));
    myModal.show();
}
 
$(function() {
    coresRestrições();
})

$(document).ready(function() {

    let profsSelecionados = {"prof_rp1":{}, "prof_rp2":{}, "prof_rp3":{}};

    $(".icone").mouseover(function() {
        $(this).css("color", "blue");
    });

    $(".icone").mouseout(function() {
        $(this).css("color", "");
    });

    function adicionar_na_lista_dinamica(lista, nome__lista, dtl_profs){

        if(nome__lista){

            const valorPosOuLicencaPremio =  dtl_profs[nome__lista][2] != null ? dtl_profs[nome__lista][2] : "";
            const valorPrefOptativa = dtl_profs[nome__lista][3] != null ? dtl_profs[nome__lista][3] : "";
            const valorConsideracao = dtl_profs[nome__lista][4] != null ? dtl_profs[nome__lista][4] : "";

            let nome__prof = (`<h6 class="prof__rp">${dtl_profs[nome__lista][0]}:</h6>`)
            let posOuLicencaPremio = (`<li class="profs-justificativas__item">Pós-doc ou licença-prêmio: ${valorPosOuLicencaPremio}</li>`);
            let prefOptativa = (`<li class="profs-justificativas__item">Preferência optativa: ${valorPrefOptativa}</li>`);
            let consideracao = (`<li class="profs-justificativas__item">Consideração: ${valorConsideracao}</li>`);

            lista += nome__prof + posOuLicencaPremio + prefOptativa + consideracao;

        }

        return lista;

    }

    $(".bloco-linha").mouseover(function() {

        if(!$(this).find('ul').length){

            let lista = ('<ul class="profs-justificativas lista__rp1__baixo">');
            let lista__final = ('</ul>');
            let nome__lista = [];
            nome__lista[0] = $(this).closest('tr').find('.n_completo').eq(0).text().trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            nome__lista[1] = $(this).closest('tr').find('.n_completo').eq(1).text().trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            nome__lista[2] = $(this).closest('tr').find('.n_completo').eq(2).text().trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

            nome__lista[0] = nome__lista[0]!=null ? nome__lista[0]:null
            nome__lista[1] = nome__lista[1]!=null  ? nome__lista[1]:null
            nome__lista[2] = nome__lista[2]!=null  ? nome__lista[2]:null

            lista = adicionar_na_lista_dinamica(lista, nome__lista[0], dtl_profs);
            lista = adicionar_na_lista_dinamica(lista, nome__lista[1], dtl_profs);
            lista = adicionar_na_lista_dinamica(lista, nome__lista[2], dtl_profs);
            lista += lista__final;


            if(lista.includes("</li>")) {
                $(this).append(lista);

                const posicaoBlocoLinha = parseInt($(this).offset().top, 10);
                const alturaTela = parseInt($(window).height());

                if((posicaoBlocoLinha + 450)>alturaTela){
                    $(this).closest('tr').find('.profs-justificativas').removeClass('lista__rp1__baixo').addClass('lista__rp1__cima');
                }

            }  
        }
        
    });
    
    //Abre popUp
    $(document).on('click', '.icone', function (e) {              
        const cell = $(this).closest('td');
        const row = cell.closest('tr');

        //carrega o nome no popup
        $("#prof_rp1, #prof_rp3, #prof_rp2").val("");
        
        let count = 1;
        row.find('.n_completo').each(function(){
            const id = "#prof_rp" + count;
            $(id).val($(this).text().trim());
            count++;
        });
        count = 1;

        $("#popup").show();
        
        //Atualizando o auto_profs para o caso de haver algum campo já preenchido
        const campos = ["#prof_rp1", "#prof_rp2", "#prof_rp3"];
        campos.forEach(function(campoId){
            const valor = $(campoId).val();
            let campoIdDepoisDoHash = campoId.substring(1);

            //Note que auto_profs irá variar conforme as turmas em que o prof estiver inscrito na planilha de distribuição e conforme ele já estiver selecionado em alguma outra turma de RP1. Devido a essa variação, não podemos utiliza-lo como uma forma de parâmetro pois haverá casos em que o nome do prof não estará na lista, causando um erro para encontrar o valor no pop-up (caso do prof já estar escrito na tabela e dar somente 1 aula). Dessa forma, utilizamos o total_profs que não varia e permite uma verificação segura dos dados.
            if(total_profs.hasOwnProperty(valor)){
                atualizaAutoProfs(valor, campoIdDepoisDoHash);
            }
        });

        $("#submitForm").off("click").on("click", function(){
            controlaPopUp(cell.prev(), total_profs, profsSelecionados);
        });

    });

    $(function() {
        $("#prof_rp1, #prof_rp2, #prof_rp3").autocomplete({
            source: function(request, response) {
                let results = $.ui.autocomplete.filter(Object.keys(auto_profs), request.term);
                response(results);
            },
            minLength: 0,
            select: function(event, ui){
                let profSelecionado = ui.item.value;
                let profKey = $(this).attr('id');
                atualizaAutoProfs(profSelecionado, profKey);
            }
        })
    });

    function autoComplementar(){
        $("#prof_rp1, #prof_rp2, #prof_rp3").each(function(){
            let celula = $(this);
            celula.autocomplete({
                source: function(request, response) {
                    let results = $.ui.autocomplete.filter(Object.keys(auto_profs), request.term);
                    response(results);
                },
            })
        })
    }

    //Monitora os campos para restaurar a escolha do nome após apagado
    $("#prof_rp1, #prof_rp2, #prof_rp3").on("input", function() {

        let valorCampo = $(this).val();
        let professorKey = $(this).attr("id");

        if(valorCampo===""){
            if(profsSelecionados.hasOwnProperty(professorKey)){
                let dicioInterno = profsSelecionados[professorKey]
                Object.assign(auto_profs, dicioInterno);
                profsSelecionados[professorKey]={};
            }

        }
        autoComplementar();
    });

    function atualizaAutoProfs(prof, profKey){

        //Utilizamos total_profs para garantirmos o resultado independente da situação. O auto_profs deve ser utilizado apenas para armazenar o resultado final da consulta, e não para confirmarmos algum nome.
        profsSelecionados[profKey][prof]= total_profs[prof];
        delete auto_profs[prof];

        autoComplementar();
    };
    
   
    $("#closePopup").on("click", function(){
        $("#popup").hide()
        location.reload();
    })

    //Função a ser executada após o usuário clicar em Salvar
    function controlaPopUp(cell, apelidos, profsSelecionados){

        let resposta = {};
        const campo1Value = document.querySelector(".campo1").value;
        const campo2Value = document.querySelector(".campo2").value;
        const campo3Value = document.querySelector(".campo3").value;

        resposta = {
            professor1: campo1Value,
            professor2: campo2Value,
            professor3: campo3Value,
        }
        console.log(apelidos)
        console.log(resposta)
        
        campo1Value ? resposta.professor1 = apelidos[resposta.professor1] : ""
        campo2Value ? resposta.professor2 = apelidos[resposta.professor2] : ""
        campo3Value ? resposta.professor3 = apelidos[resposta.professor3] : ""
        console.log(resposta)
        
        let resp = []
        if(resposta.professor1 != "") resp.push(resposta.professor1)
        if(resposta.professor2 != "") resp.push(resposta.professor2)
        if(resposta.professor3 != "") resp.push(resposta.professor3)

        //valida nomes
        let validInput = true;
        const lProfs = [campo1Value, campo2Value, campo3Value];

        for (let i = 0; i < lProfs.length; i++) {
            let nomeEncontrado = false;
            const idAlerta = "#" + i;

            $(idAlerta).hide()
            //if (auto_profs.hasOwnProperty(lProfs[i])) nomeEncontrado = true;
            for(let key in profsSelecionados){
                //Verifica se o prof já preenchido está no mesmo indice dos profsSelecionados
                if(key.slice(7)==i+1 && profsSelecionados[key].hasOwnProperty(lProfs[i]))nomeEncontrado = true;
            }
            if(lProfs[i] === "") nomeEncontrado = true;

            if (!nomeEncontrado) {
                $(idAlerta).html("Nome inválido");
                $(idAlerta).css("color", "red");
                $(idAlerta).css("font-size", "12px");
                $(idAlerta).show()
                validInput = false;
                // break;
            }               
        }
 
        let prof_hr_err = false;
        if(validInput){
            const myEvent = { 
                id: $(cell).prev().text(),
                lProfs: lProfs,
                csrfmiddlewaretoken: window.CSRF_TOKEN
            };
            let prof_permitidos = lProfs;
            $.ajax({
                url: $("#url-data").data("url"),
                type: "POST",
                dataType: "json",
                data: JSON.stringify(myEvent),
                headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  "X-CSRFToken": getCookie("csrftoken"), 
                },
                success: (data) => {
                    console.log(data)
                    const erros = data["erros"];
                    const alertas = data["alertas"];
                    auto_profs = data["sugestoes"]
                    
                    const restricao_prof = data["restricao_prof"]
                    let falha = false;
                    
                    if(erros && erros.hasOwnProperty("prof_msm_hr")){
                        prof_hr_err = erros.hasOwnProperty("prof_msm_hr")
                    } 
                     
                    if(prof_hr_err){
                        openModal("ERRO", erros["prof_msm_hr"]);
                        let indice = prof_permitidos.indexOf(erros["nome_prof"])
                        if(indice !== -1){
                            prof_permitidos[indice]="";
                        }
                        falha = true;
                    }else{
                        cell.html(resp);
                    }
                    
                    if(alertas && Object.keys(alertas).length !== 0){

                        openModal("Warning(s)", alertas["alert2"]);
                        falha = true;
                    }

                    const row = cell.closest('tr');
                    row.find('.n_completo').remove();
                    console.log("Verifacaao")
                    console.log(prof_permitidos);
                    prof_permitidos.forEach(nome => {
                        row.append('<td class="d-none n_completo">'+nome+'</td>')
                        console.log(nome);
                    });
                    $(cell).removeClass("prof-na-restricão");
                    $(cell).removeClass("prof-no-impedimento");
                    $("#popup").hide();
                    cell.html(resp.join(","));
                    coresRestrições();
                    if(!falha) window.location.reload(); //Reseta profsSelecionados
                },

                error: (error) => {
                    alert("Ocorreu um erro ao manipular as informações");
                }
            });

            
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

 // Função para obter índices de células das restrições de horário de um professor
 function getCellIndexes(cellName) {
    const indexes = [];
    const indexes_rest = [];
    const indexes_imped = []
    const rest_prof = restricos_hro[cellName]
    const impedimentos = impedimentos_totais[cellName]
    indexes_rest.push(...rest_prof);
    indexes_imped.push(...impedimentos);
    indexes.push(indexes_rest)
    indexes.push(indexes_imped)
    return indexes;
}

function arrayCompare(first, last)
{
    var result = first.filter(function(item){ return last.indexOf(item) > -1});   
    return result.length;  
} 

function coresRestrições() {
    // dicionário de correspondencia
    //para aproveitar os indices da tabela de atribuição original

    const correspondencia = {
        "13": [22, 23, 33, 34, 35, 36],
        "14": [46, 47, 57, 58, 68, 69, 79, 80],
        "22": [2 , 3, 13, 14],
        "23": [22, 23, 33, 34, 35, 36],
        "24": [46, 47, 57, 58, 68, 69, 79, 80],
        "32": [2 , 3, 13, 14],
        "33": [26, 27, 39, 40],
        "34": [46, 47, 57, 58, 68, 69, 79, 80],
        "43": [26, 27, 39, 40],
        "44": [48, 49, 59, 60, 70, 71, 81, 82],
        "52": [4, 5, 15, 16],
        "53": [22, 23, 33, 34, 35, 36],
        "54": [48, 49, 59, 60, 70, 71, 81, 82],
        "64": [50, 51, 61, 62, 72, 73, 83, 84],
        "74": [50, 51, 61, 62, 72, 73, 83, 84]

    }

    let cells_profs = $('.si_profs');
    let cells_turmas = $('.codigo');
    
    for(let i = 0; i < 15; i++) {

        let conteudoCelulaProfs = cells_profs.eq(i).find('.prof_rp1_apelido');
        
        if(conteudoCelulaProfs.length){
            console.log(i);
            console.log(conteudoCelulaProfs);
            let turma = cells_turmas.eq(i)[0].innerText;
            conteudoCelulaProfs.each((index, apelido) => {
                console.log(apelido);
                console.log(apelido.innerText);
                console.log(correspondencia[turma]);
                
                if(arrayCompare(getCellIndexes(apelido.innerText)[0], correspondencia[turma]) == correspondencia[turma].length) {
        
                    $(apelido).addClass("prof-na-restricão");
                    
                }
                if(arrayCompare(getCellIndexes(apelido.innerText)[1], correspondencia[turma]) == correspondencia[turma].length) {
                   
                    $(apelido).addClass("prof-no-impedimento");
                    
                }
            });
        }
    }
};