
let auto_profs = JSON.parse(document.getElementById("auto_profs").textContent);
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
    $(".icone").mouseover(function() {
        $(this).css("color", "blue");
    });

    $(".icone").mouseout(function() {
        $(this).css("color", "");
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
        $("#submitForm").off("click").on("click", function(){
            controlaPopUp(cell.prev(), auto_profs);
        });

    });

    $(function() {
        $("#prof_rp1, #prof_rp2, #prof_rp3").autocomplete({
            source: function(request, response) {
                let results = $.ui.autocomplete.filter(Object.keys(auto_profs), request.term);
                response(results);
            },
            minLength: 0
        })
    });

    
   
    $("#closePopup").on("click", function(){
        $("#popup").hide()
    })

    function controlaPopUp(cell, apelidos){

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
        //Há um erro no valor que o campoValue terá devidos as alterações feitas em rp1_table. Como o sistema deleta o professor que já foi escohido, o array apelidos não terá um professor escolhido anteriormente, causando um erro no cadastramento de mais de um professor na mesma turma, dia e horário de rp1
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
            if (auto_profs.hasOwnProperty(lProfs[i])) nomeEncontrado = true;
            if(lProfs[i] === "") nomeEncontrado = true;

            if (!nomeEncontrado) {
                $(idAlerta).html("Nome inválido");
                $(idAlerta).css("color", "red");
                $(idAlerta).css("font-size", "12px");
                $(idAlerta).show()
                validInput = false;
                break;
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
                    
                    if(erros && erros.hasOwnProperty("prof_msm_hr")){
                        prof_hr_err = erros.hasOwnProperty("prof_msm_hr")
                    } 
                     
                    if(prof_hr_err){
                        openModal("ERRO", erros["prof_msm_hr"]);
                        let indice = prof_permitidos.indexOf(erros["nome_prof"])
                        if(indice !== -1){
                            prof_permitidos[indice]="";
                        }
                        console.log("Caso de teste");
                        console.log(prof_permitidos);
                    }else{
                        cell.html(resp);
                    }
                    
                    if(alertas && Object.keys(alertas).length !== 0){

                        openModal("Warning(s)", alertas["alert2"]);

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
        let conteudoCelulaProfs = cells_profs.eq(i)[0].innerText.split(",");
        let turma = cells_turmas.eq(i)[0].innerText
        conteudoCelulaProfs.forEach((apelido) => {

            if(apelido) {
                if(apelido[0] == " ") apelido = apelido.substring(1)
                
                if(arrayCompare(getCellIndexes(apelido)[0], correspondencia[turma]) == correspondencia[turma].length) {
                    console.log(cells_profs.eq(i))
                    cells_profs.eq(i).addClass("prof-na-restricão")
                }
                if(arrayCompare(getCellIndexes(apelido)[1], correspondencia[turma]) == correspondencia[turma].length) {
                    cells_profs.eq(i).addClass("prof-no-impedimento")
                }
                
            }
        })
    }
};