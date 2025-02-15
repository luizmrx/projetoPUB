// código daptado de rp1Table.js
let auto_profs = JSON.parse(document.getElementById("auto_profs").textContent);
const profs_impedimento = JSON.parse(document.getElementById("profs_impedimento").textContent);
const profs_nao_gosta = JSON.parse(document.getElementById("profs_nao_gosta").textContent);
const dtl_profs = JSON.parse(document.getElementById("dtl_profs").textContent);

function openModal(title, messages) {
    const modalBody = document.getElementById("modalBody");
    modalBody.innerText = messages;
    $("#myModalLabel").html(title);
    const myModal = new bootstrap.Modal(document.getElementById("myModal"));
    myModal.show();
}

$(document).ready(function() {
    //Colore os profs no carregamento da página
    $('.si_profs').each(function () {
        const apelido_prof = $(this).text().trim()
        if (profs_nao_gosta.includes(apelido_prof)) 
            $(this).css("color", "orange");

        if (profs_impedimento.includes(apelido_prof)) 
            $(this).css("color", "red");
        
        
    });
    
    // Remove a classe .si_profs de todas as células
    $('.si_profs').removeClass('si_profs');

    $(".bloco-linha").mouseover(function() {
        
        let lista = ('<ul class="profs-justificativas lista__tadi__baixo">');
        let lista__final = ('</ul>');
        let nome__lista = $(this).closest('tr').find('.n_completo').text().trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

        if(nome__lista){
            const valorPosOuLicencaPremio =  dtl_profs[nome__lista][2] != null ? dtl_profs[nome__lista][2] : "";
            const valorPrefOptativa = dtl_profs[nome__lista][3] != null ? dtl_profs[nome__lista][3] : "";
            const valorConsideracao = dtl_profs[nome__lista][4] != null ? dtl_profs[nome__lista][4] : "";

            let posOuLicencaPremio = (`<li class="profs-justificativas__item">Pós-doc ou licença-prêmio: ${valorPosOuLicencaPremio}</li>`);
            let prefOptativa = (`<li class="profs-justificativas__item">Preferência optativa: ${valorPrefOptativa}</li>`);
            let consideracao = (`<li class="profs-justificativas__item">Consideração: ${valorConsideracao}</li>`);

            lista += posOuLicencaPremio + prefOptativa + consideracao + lista__final;

            $(this).append(lista);

            const listaDimensao = document.querySelector('.profs-justificativas').getBoundingClientRect();
            const alturaTela = window.innerHeight;
            if(listaDimensao.bottom>alturaTela){
                document.querySelector('.profs-justificativas').classList.replace('lista__tadi__baixo', 'lista__tadi__cima');
            }
        }

    });

    $(".bloco-linha").mouseout(function() {
        $(this).find('ul').remove();
    });

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
        $("#prof_tadi").val("");

        row.find('.n_completo').each(function(){
            $("#prof_tadi").val($(this).text().trim());
        });

        $("#popup").show();
        $("#submitForm").off("click").on("click", function(){
            controlaPopUp(cell.prev(), auto_profs);
        });
    });


    $(function() {
        $("#prof_tadi").autocomplete({
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
    
        resposta = {
            professor: campo1Value,
        }
        
        campo1Value ? resposta.professor = apelidos[resposta.professor] : ""

        
        let resp = []
        if(resposta.professor1 != "") resp.push(resposta.professor)

        //valida nomes
        let validInput = true;
        const lProfs = [campo1Value];
        let nomeEncontrado = false; 
        const idAlerta = "#0";

        $(idAlerta).hide()
        if (auto_profs.hasOwnProperty(lProfs[0])) nomeEncontrado = true;
        if(lProfs[0] === "") nomeEncontrado = true;

        if (!nomeEncontrado) {
            $(idAlerta).html("Nome inválido");
            $(idAlerta).css("color", "red");
            $(idAlerta).css("font-size", "12px");
            $(idAlerta).show()
            validInput = false;
        }
        let prof_hr_err = false;

        if(validInput){
            const myEvent = { 
                id: $(cell).prev().text(),
                lProfs: lProfs,
                csrfmiddlewaretoken: window.CSRF_TOKEN
            };
            
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
                    const erros = data["erros"]
                    const alertas = data["alertas"]
                    const restricao_prof = data["restricao_prof"]
                    auto_profs = data["sugestoes"]
                    // const cred_err = erros.hasOwnProperty("credito")
                    if(erros && erros.hasOwnProperty("prof_msm_hr")){
                        prof_hr_err = erros.hasOwnProperty("prof_msm_hr")
                    } 
                    
                    if(prof_hr_err){
                        openModal("ERRO", erros["prof_msm_hr"]);
                    }else{
                        cell.html(resp);
                    }
                    
                    if(alertas && Object.keys(alertas).length !== 0){

                        let alerta_msg = "";
    
                        if(alertas.hasOwnProperty("aula_manha_noite")){
                            alerta_msg += alertas["aula_manha_noite"]
                        }
    
                        if(alertas.hasOwnProperty("alert2")){
                            //Alerta de quando um msm professor dá aula no noturno 2
                            // e no matutino 1 no dia posterior
                            alerta_msg += alertas["alert2"]
                        }
                        openModal("Warning(s)", alerta_msg);

                    }
                    
                    if(restricao_prof && restricao_prof["prof_nao_gosta_hr"]){
                        cell.css("color", "orange");
                    }

                    if(restricao_prof && restricao_prof["impedimento"]){
                        cell.css("color", "red");
                    }

                    
                },
                error: (error) => {
                    alert("Ocorreu um erro ao manipular as informações");
                }
            });

            const row = cell.closest('tr');
            row.find('.n_completo').remove();
            lProfs.forEach(nome => {
                row.append('<td class="d-none n_completo">'+nome+'</td>')
            });
            
            $("#popup").hide();            
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