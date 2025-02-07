'use strict';
//Carregando os dados enviados do views.py e que serão utilizados no javascript
const semestre = parseInt(JSON.parse(document.getElementById("smt").textContent));
const dtl_profs = JSON.parse(document.getElementById("dtl_profs").textContent);
const auto_profs = JSON.parse(document.getElementById("auto_profs").textContent);
const cods_auto_ext = JSON.parse(document.getElementById("cods_auto_ext").textContent);
const cods_auto_obrig = JSON.parse(document.getElementById("cods_auto_obrig").textContent);
const mtr_auto_nome = JSON.parse(document.getElementById("mtr_auto_nome").textContent);
const restricos_hro = JSON.parse(document.getElementById("rest").textContent);
const impedimentos_totais = JSON.parse(document.getElementById("impedimentos_totais").textContent);
let cod_mtr_sugestao = JSON.parse(document.getElementById("cod_mtr_sugestao").textContent);
const cod_mtr_sugestao_completo = JSON.parse(document.getElementById("cod_mtr_sugestao_completo").textContent);

export function setCodMtr(new_value) {
    cod_mtr_sugestao = new_value;
}

// console.log(auto_profs);
// console.log(dtl_profs);
// console.log(restricos_hro);

// const turmas_rp = JSON.parse(document.getElementById("turmas_rp").textContent);

// importando os módulos
import { save_edition } from "./modules/crud_turmas.js";
import { controlaPopUp } from "./modules/popUp.js"
// exportando para o crud_turmas
export {cods_auto_ext, cods_auto_obrig, semestre, openModal, editable, coresRestrições, cod_mtr_sugestao}; 

//lista de disciplinas do CB que não podem ser editadas
const listaCB = ["ACH0021 TADI", "ACH0141 SMD", "ACH0041 RP1"]

//Armazena o código da matéria no caso de update
let valor_materia;

//exibe a caixa de mensagens para alertas
function openModal(title, messages) {
    const modalBody = document.getElementById("modalBody");
    modalBody.innerText = messages;
    $("#myModalLabel").html(title);
    const myModal = new bootstrap.Modal(document.getElementById("myModal"));
    myModal.show();
}

//Lida com os ícones de restrição
// Variáveis de controle para o ícone
let markCells = false;
let transparent = false;
let impedimento = false;
 
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

function padronizaNome(nome, dicio){
    let nomeFormatado = Object.keys(dicio).find(chave => dicio[chave].trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") === nome.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""));
    return nomeFormatado.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

$(document).ready(function () {
    
    //Controla o paste para só colar texto nas células
    document.querySelector(".editable").addEventListener("paste", function(e) {
        e.preventDefault();
        const text = e.clipboardData.getData("text/plain");
        text.trim();
        document.execCommand("insertHTML", false, text);
    });


    //Trecho para autocompletar a turma extra
    $(function() {
        // Configura o plugin Autocomplete para o input com ID "my-autocomplete-input"
        $("#mtr").autocomplete({
        source: Object.keys(mtr_auto_nome),
        minLength: 2, // Começa a exibir sugestões a partir de 2 caracteres
        
        select: function(event, ui) {
            // Função chamada quando um item é selecionado
            document.getElementById("cod").innerHTML = mtr_auto_nome[ui.item.value]
            document.getElementById("cod").style.display="block";
        }
        });
    });

    $(function() {
        coresRestrições();
    })

    //Lida com os detalhes do professor
    $(function() {
        $("#prof").autocomplete({
            source: function(request, response) {
                let results = $.ui.autocomplete.filter(Object.keys(auto_profs), request.term);
                response(results);
            },
            minLength: 2, // Começa a exibir sugestões a partir de 2 caracteres
            select: function(event, ui) {
                // Função chamada quando um item é selecionado
                // Carrega as informações de detalhes do professor 
                $('.red-transparent').removeClass('red-transparent');
                $('.red-impedimento').removeClass('red-impedimento');
                $('#checkRestricaoHro').prop('checked', false);
                const nome_prof = ui.item.value.trim().toLowerCase().normalize("NFD");
                document.getElementById("nome").innerHTML = dtl_profs[nome_prof][0]|| "Sem informações";
                document.getElementById("apelido").innerHTML = dtl_profs[nome_prof][1] || "Sem informações";
                document.getElementById("pos_doc").innerHTML = dtl_profs[nome_prof][2] || "Sem informações";
                document.getElementById("pref").innerHTML = dtl_profs[nome_prof][3] || "Sem informações";
                document.getElementById("consideracao").innerHTML = dtl_profs[nome_prof][4] || "Sem informações";
                document.getElementById("infos_prof").style.display="block";
            }
        });
    });

    //autocomplete do pop-up de rp
    $(function() {
        $("#prof_rp1, #prof_rp2, #prof_rp3").autocomplete({
            source: function(request, response) {
                let results = $.ui.autocomplete.filter(cod_mtr_sugestao_completo["ACH0042 RP2"], request.term);
                response(results);
            },
            minLength: 0
        })
    });

    // Manipula o clique no ícone de "X" para fechar os detalhes do professor
    $('#fechar_info').click(function() {
        $('.red-transparent').removeClass('red-transparent');
        $('.red-impedimento').removeClass('red-impedimento');
        $('#prof').val("");
        $('#infos_prof').hide(); 
    });

    $('#checkRestricaoHro').change(function() {
        if ($(this).is(':checked')) {
            let cells = $('#tbl1 td');
            let apelidoProf = $('#apelido').text();
            // console.log("1-----------");
            // console.log(apelidoProf);
            let indexes = getCellIndexes(apelidoProf)[0];
            indexes.forEach(function (index) {
                cells.eq(index).addClass('red-transparent');
            });
            let indexes_imped = getCellIndexes(apelidoProf)[1];
            indexes_imped.forEach(function (index) {
                cells.eq(index).addClass('red-impedimento');
            });
            transparent = true;
            impedimento = true;
        }else{
            $('.red-transparent').removeClass('red-transparent');
            $('.red-impedimento').removeClass('red-impedimento');
            transparent = false;
            impedimento = true;
        }
    });


    $('.editable td').hover(function () {
        if (!markCells) {
            const cell = $(this);
            const cellText = cell.text().trim();
            const isEditable = cell.is('[contenteditable="true"]');
            let colIndex = cell[0].cellIndex;
            const rowIndex = cell.closest('tr')[0].rowIndex;
            const table = $(this).closest('table'); 
            const id = table.attr('id'); 
            if(id === "tbl1"){
                const specialRows = [5, 9, 11];
                if ($.inArray(rowIndex, specialRows) !== -1) colIndex++;
            }

            if (colIndex % 2 === 0 && cellText !== "" && !isEditable) {
                cell.find('i.fa').remove();
                cell.append('<i class="fa fa-clock-o"></i>');

                if(cellText.includes("/")){ //Caso de rp2 com mais de 1 prof

                    let lista = ('<ul class="profs-justificativas lista__rp2__direita">');
                    let lista__final = ('</ul>');
                    let apelidos = cellText.split("/");

                    apelidos.forEach(apelido => lista = adicionar_na_lista_dinamica(lista, padronizaNome(apelido, auto_profs), dtl_profs));

                    lista += lista__final;
                    cell.append(lista);

                    const listaDimensao = document.querySelector('.profs-justificativas').getBoundingClientRect();
                    const larguraTela = parseInt(window.innerWidth);

                    if((parseInt(listaDimensao.x) + 250 > larguraTela)){
                        cell.closest('td').find('.profs-justificativas').removeClass('lista__rp2__direita').addClass('lista__rp2__esquerda');
                    }

                }else{
                    let lista = ('<ul class="profs-justificativas lista__direita">');
                    let lista_final = ('</ul>');

                    lista = adicionar_na_lista_dinamica(lista, padronizaNome(cellText, auto_profs), dtl_profs);

                    lista += lista_final;
                    cell.append(lista);  // Adiciona a lista à célula

                    const listaDimensao = document.querySelector('.profs-justificativas').getBoundingClientRect();
                    const larguraTela = window.innerWidth;
                    if(listaDimensao.right>larguraTela){
                        document.querySelector('.profs-justificativas').classList.replace('lista__direita', 'lista__esquerda');
                    }

                }
            }
        }
    }, function () {
        if (!markCells) {
            $(this).find('i').remove();
            $(this).find('ul').remove();
        }
    });

    function adaptaParaExt(listaOriginal) {
        let novaLista = [];

        for (let i = 0; i < listaOriginal.length; i++) {
            let valor = listaOriginal[i];

            if (valor >= 0 && valor <= 21) {
                novaLista.push(valor);
            }else if (valor >= 46 && valor <= 56) {

                const novoValor = valor - 24;
                novaLista.push(novoValor);
                const valorFinal = novoValor + 11;
                novaLista.push(valorFinal);
            }
        }

        return novaLista;
    }

    // $(document).on('click', '#showPopup', function(event) {
    //     controlaPopUp()})

    //Mostra a restrições quando o ícone é clicado
    $(document).on('click', '.editable td i', function (e) {
        const icon = $(this);
        markCells = !markCells;
        const table = $(this).closest('table');
        const id = table.attr('id');
        $('#checkRestricaoHro').prop('checked', false);

        if (markCells) {
            icon.removeClass('fa-clock-o').addClass('fa-check-circle');
            icon.closest('td').find('ul').remove();
            icon.closest('table').find('td').removeClass('red-transparent');
            icon.closest('table').find('td').removeClass('red-impedimento');
            // Adiciona a classe 'red-transparent' a células
            const cells = icon.closest('table').find('td');
            const apelidoComInformacoes = icon.parent().text().trim();
            console.log("2---------");
            console.log(apelidoComInformacoes);

            const apelidos = apelidoComInformacoes.split("/");
            apelidos.forEach((apelido, index) => {
                // apelidos[index]  = apelido.trim();
                console.log("verificando no forEach");
                console.log(apelido);
                console.log(typeof apelido);
                // const apelido = apelidoComInformacoes.trim();
                let indexes = getCellIndexes(apelido)[0];
                let indexes_imp = getCellIndexes(apelido)[1];

                if(id === "tbl_ext"){
                    indexes = adaptaParaExt(indexes)
                    indexes_imp = adaptaParaExt(indexes_imp)
                }
                if (indexes.length > 0) {
                    indexes.forEach(function (index) {
                        cells.eq(index).addClass('red-transparent');
                    });
                    transparent = true;
                    indexes_imp.forEach(function (index) {
                        cells.eq(index).addClass('red-impedimento');
                    });
                    impedimento = true;
                } else {
                        // Remove todas as mensagens flutuantes existentes
                    $('.floating-message').remove();
                    // Exibir mensagem flutuante
                    const message = $('<div/>', {
                        class: 'floating-message',
                        text: 'Sem restrição'
                    });
                    const iconPosition = icon.offset();
                    const iconWidth = icon.outerWidth();
                    const iconHeight = icon.outerHeight();
                    const messageTop = iconPosition.top + iconHeight; // Ajuste a distância vertical conforme necessário
                    const messageLeft = iconPosition.left + iconWidth; // Ajuste a distância horizontal conforme necessário
                    message.css({
                        top: messageTop,
                        left: messageLeft
                    });
                    $('body').append(message);

                    // Remover a mensagem flutuante quando o mouse é movido para fora do ícone
                    icon.on('mouseleave', function() {
                        message.remove();
                        cells.find('i').remove();
                    });

                    markCells = false;

                }

            });

            
            

        } else {
            icon.removeClass('fa-check-circle').addClass('fa-clock-o');
            icon.closest('table').find('td').removeClass('red-transparent');
            icon.closest('table').find('td').removeClass('red-impedimento');
            transparent = false;
            impedimento = false
        }
    });

    $(".editable td").on("dblclick", handleDoubleClick);

    function handleDoubleClick(event) {
        const cell = event.currentTarget; // A célula em que ocorreu o duplo clique
        const target = event.target; // O elemento alvo do clique dentro da célula
        //se a disciplina for do CB, não pode ser editada
        if(listaCB.includes($(this)[0].innerText)) return
        let colIndex = cell.cellIndex;
        const rowIndex = cell.parentNode.rowIndex;
        let is_ext = true;
        const table = $(this).closest('table');
        const id = table.attr('id');

        if(id === "tbl1"){
            is_ext = false;
            const specialRows = [5, 9, 11];
            if ($.inArray(rowIndex, specialRows) !== -1) colIndex++;
        }

        //coluna das turmas não deve ser editável
        if(colIndex === 11 || colIndex % 2 === 0) return

        // Verifica se o alvo do clique é o ícone
        if (!target.classList.contains('fa')) editable.edit(cell, rowIndex, colIndex, is_ext);

    }

});

 // Função para obter índices de células das restrições de horário de um professor
 function getCellIndexes(cellName) {

    // if(cellName.includes("/")){
    //     const apelidos = cellName.split("/");
    //     apelidos.forEach((apelido, index) => {
    //         apelidos[index]  = apelido.trim();
    //         getCellIndexes(apelidos[index]);
    //     });
    // }else{

    const indexes = [];
    const indexes_rest = [];
    const indexes_imped = [];
    console.log("+++++++++");
    console.log(typeof cellName);
    const rest_prof = restricos_hro[cellName.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")]
    console.log("teste no getCellIndexes");
    console.log(cellName);
    console.log(restricos_hro);
    console.log(rest_prof);
    const impedimentos = impedimentos_totais[cellName.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")]
    indexes_rest.push(...rest_prof);
    indexes_imped.push(...impedimentos);
    indexes.push(indexes_rest)
    indexes.push(indexes_imped)
    return indexes;

    // }
    
    

    
}
// Atenção nessa função após a alteração do dtl_profs
function coresRestrições() {
    let cells = $('#tbl1 td');
    for(let i = 0; i < 90; i++) {
        let conteudoCelula = cells.eq(i)[0].innerText.split(" / ");
        console.log(conteudoCelula);
        conteudoCelula.forEach((apelido) => {

            if(apelido) {
                Object.keys(dtl_profs).map((professor) => {
                    if(dtl_profs[professor][1] == apelido) {
                        console.log("cores");
                        console.log(apelido);
                        if(getCellIndexes(apelido.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""))[0].includes(i)) {
                            cells.eq(i).addClass("prof-na-restricão")
                        }
                        if(getCellIndexes(apelido.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""))[1].includes(i)) {
                            cells.eq(i).addClass("prof-no-impedimento")
                        }
                    }
                })
            }
            if(listaCB.includes(apelido)) cells.eq(i).addClass("materia-cb-bloqueada")
        })
    }
};


//Manipula o processo de edição das células
const editable = {
    icon: null,
    rowIndex: 0,
    colIndex: 0,
    selected : null, // current selected cell
    previousValue : "",
    is_ext : false,

    // (B) "CONVERT" TO EDITABLE CELL
    edit: (cell, row, col, ext) => {
        editable.is_ext = ext;
        $('#checkRestricaoHro').prop('checked', false);
        // Remove ícone presente na célula
        $(cell).closest('table').find('i').remove();
        $(cell).closest('table').find('ul').remove();

        // Remove a classe 'red-transparent' das células marcadas
        if(transparent){
            $(cell).closest('table').find('td.red-transparent').removeClass('red-transparent');
            transparent = false;
            markCells = !markCells;
        }

        //Como toda vez que o impedimento for verdadeiro a "transparent" é true,
        //não é necessário negar novamente o markCells
        if(impedimento){
            $(cell).closest('table').find('td.red-impedimento').removeClass('red-impedimento');
            impedimento = false;
        }

        $(cell).closest('table').find('i').remove();
        editable.previousValue = $(cell).html().replace(/&nbsp;/g, '').trim();
        editable.rowIndex = row;
        editable.colIndex = col;

        // (B1) REMOVE "DOUBLE CLICK TO EDIT"
        cell.ondblclick = "";

        // (B2) EDITABLE CONTENT
        $(cell).attr("contenteditable", "true");
        $(cell).focus();

        const temp_cods = Object.keys(cods_auto_obrig).concat(Object.keys(cods_auto_ext));
        const uniqueTempCods = removeDuplicates(temp_cods);

        // (B2.1) ADD AUTOCOMPLETE
        if (col % 2 === 0){

            if($(cell).prev()[0].innerText == "ACH0042 RP2") {
                controlaPopUp($(cell), auto_profs);
            }
            else {
                //autocompleta com o nome do professor
                  // Elementos que estão em list1, mas não em list2
                  const list1 = cod_mtr_sugestao_completo[$(cell).prev()[0].innerText];
                  const list2 = cod_mtr_sugestao[$(cell).prev()[0].innerText];
                  console.log("----------")
                  console.log(list2)

                  const uniqueInList1 = difference(list1, list2);
                  let list_sugestao = cod_mtr_sugestao[$(cell).prev()[0].innerText]

                  uniqueInList1.forEach(function(word) {

                      if(searchInTableRows(cell, word) === true){
                          list_sugestao.push(word)
                      }

                  });

                $(cell).autocomplete({

                    source: function(request, response) {
                        response(list_sugestao);
                    },
                    minLength: 1,
                    select: function(event, ui) {
                        const nomeProf = ui.item.value;
                        const apelidoProf = auto_profs[nomeProf];
                        $(cell).html(apelidoProf);
                        $(cell).removeClass("prof-na-restricão");
                        $(cell).removeClass("prof-no-impedimento");
                        coresRestrições();
                        return false;
                    }
                }).focus(function() {
                    $(this).autocomplete("search");
                });
            }
        }
        else {
            //autocompleta com a matéria
            $(cell).autocomplete({
                source: function(request, response) {
                    let results;
                    //linhas entre [4,6] são do vespertino
                    if ((row >= 4 && row <= 6) || editable.is_ext) {

                        results = $.ui.autocomplete.filter(uniqueTempCods, request.term);
                    } else {
                        results = $.ui.autocomplete.filter(Object.keys(cods_auto_obrig), request.term);
                    }
                    response(results.slice(0, 4));
                },
                minLength: 2,
                select: function(event, ui) {
                    $(cell).html(ui.item.value);
                    return false;
                }
            }).focus(function() {
                $(this).autocomplete("search");
            });
        }

        // (C3) "MARK" CURRENT SELECTED CELL
        editable.selected = cell;

        // (C4) PRESS ENTER/ESC OR CLICK OUTSIDE TO END EDIT
        // A ideia do ESC é recuperar o valor de antes do usuário modificar
        // ainda falta implementar
        if($(cell).prev()[0]){

            if($(cell).prev()[0].innerText == "ACH0042 RP2") {
                let anterior = $(cell)[0].innerText;

                $("#submitForm").on("click", editable.close);

            }
            else {
                window.addEventListener("click", editable.close);
                cell.onkeydown = evt => {
                    if (evt.key=="Enter" || evt.key=="Escape") {
                        editable.close(evt.key=="Enter" ? true : false);
                        return false;
                    }
                };
            }
        } else {
            window.addEventListener("click", editable.close);
                cell.onkeydown = evt => {
                    if (evt.key=="Enter" || evt.key=="Escape") {
                        editable.close(evt.key=="Enter" ? true : false);
                        return false;
                    }
                };
        }

    },

    removeEditable: (selected, isCod, valueUser, v_nextCell, v_prevCell) =>{

        // Impede o usuário de deixar um par incompleto

        let v_cell_lado;
        let cell_lado;
        if(isCod){
            v_cell_lado = v_nextCell;
            cell_lado = $(selected).next();
        }else{
            v_cell_lado = v_prevCell;
            cell_lado = $(selected).prev();
        }

        if(valueUser == "" && v_cell_lado != "") $(cell_lado).html("")

        // REMOVE "EDITABLE"
        window.getSelection().removeAllRanges();
        $(selected).attr("contenteditable", "false");

        // RESTORE CLICK LISTENERS
        window.removeEventListener("click", editable.close);
        selected.onkeydown = "";
        selected.ondblclick = () => editable.edit(selected);
    },

    // (C) END "EDIT MODE"
    close: evt => {
        if (evt.target !== editable.selected) {
            let valueUser = $(editable.selected).html().replace(/&nbsp;/g, '').replace(/<br>/g, '').replace(/<ul[\s\S]*?<\/ul>/g, '').trim();
            const col = editable.colIndex;
            const row = editable.rowIndex;
            let caso_update = false;

            // tira ícones que podem estar nas células posterior e anterior
            $(editable.selected).find("i").remove();

            let nextCell = $(editable.selected).next();
            const prevCell = $(editable.selected).prev();
            let valueNextCell = nextCell.get(0) ? $(nextCell).html().replace(/&nbsp;/g, '').trim() : "indefinido";
            const valuePrevCell = prevCell.get(0) ? $(prevCell).html().replace(/&nbsp;/g, '').trim() : "indefinido";

            const colCod = col % 2 !== 0;
            let validInput = false;
            // console.log("Teste");
            //Note que o valueUser nunca será "", se o usuário não escrever nada, o seu valor será <br>.
            if(valueUser==="<br>")valueUser="";
            if (colCod && valueUser !== "") {
                let ExistMtr = false;
                if (cods_auto_obrig.hasOwnProperty(valueUser)) ExistMtr = true;
                const mtr_ext_valida = cods_auto_ext.hasOwnProperty(valueUser)
                if((row >= 4 && row <= 6 && mtr_ext_valida) | (mtr_ext_valida && editable.is_ext))  ExistMtr = true;

                if (!ExistMtr) {
                    const msg_erro = "Código de Matéria inválido, consulte o desejado na tabela abaixo";
                    erro_entrada(msg_erro, colCod, valueUser, valueNextCell, valuePrevCell, editable.is_ext)

                }else{

                    console.log(valueUser);
                    console.log(editable.previousValue);
                    if(valueUser!==editable.previousValue && editable.previousValue!==""){
                        //Caso de update
                        //valueUser="";
                        //valueNextCell="";
                        console.log("Caso de update");
                        caso_update=true;
                        //nextCell.html("");
                    }
                    validInput = true;
                }

            }else if(valueUser !== ""){
                let ExistProf = false;

                //checar se é o caso de RP
                if(valuePrevCell == "ACH0042 RP2") {
                    const nomesSeparados = valueUser.split(" / ");
                    nomesSeparados.forEach(function (name) {
                        const nomeEncontrado = Object.keys(auto_profs).find(function(nome) {
                            return auto_profs[nome] === name;
                        });

                        if (nomeEncontrado) {
                            console.log(name + " encontrado")
                            ExistProf = true
                        } else {
                            console.log(name + " não encontrado")
                            ExistProf = false
                        }

                        if(!ExistProf){
                            erro_entrada("Nome do professor inválido", colCod, valueUser, valueNextCell, valuePrevCell, editable.is_ext);
                        }else{
                            validInput = true;
                        }
                    } )
                }
                else {
                    const nomeEncontrado = Object.keys(auto_profs).find(function(nome) {
                        return auto_profs[nome] === valueUser;
                    });

                    if (nomeEncontrado) ExistProf = true

                    if(!ExistProf){
                        erro_entrada("Nome do professor inválido", colCod, valueUser, valueNextCell, valuePrevCell, editable.is_ext);
                    }else{
                        validInput = true;
                    }
                }
            }

            editable.removeEditable(editable.selected, colCod, valueUser, valueNextCell, valuePrevCell);

            //Exceção das duas células da segunda linha do vespertino 1
            //A próxima coluna e a anterior podem ser indefinidas
            // const parIncompletoDireita = validInput && colCod &&  valueNextCell === "";
            let parIncompletoDireita=false;
            let vl = { "extra": false };

            if((validInput && colCod &&  valueNextCell === "")||caso_update){
                //Precisamos armazenar a materia anterior da atual em caso de update
                vl["mtr_ant"]=editable.previousValue;
                valor_materia=vl["mtr_ant"];
                // console.log("Testando vl");
                // console.log(vl["mtr_ant"]);
                parIncompletoDireita= true;
            }


            const parIncompletoEsquerda = validInput && !colCod && valuePrevCell === "";

            // (C4) Se a célula ao lado estiver vazia ela fica editável
            //o indice 0 tem o elemento DOM da célula
            if(parIncompletoDireita) editable.edit(nextCell.get(0), row, col + 1, editable.is_ext)
            if(parIncompletoEsquerda) editable.edit(prevCell.get(0), row, col - 1, editable.is_ext);

            //(C5) Se o par de células estiver completo chama o save_edition


            if(editable.is_ext) vl["extra"] = true;
            if(validInput && (editable.previousValue !== valueUser) && ((colCod && !parIncompletoDireita  && valueUser !== "")
            || (!colCod && !parIncompletoEsquerda && valueUser !== ""))){
                //"i/u" == insert/update
                console.log(editable.previousValue);
                if(editable.previousValue !== ""){


                    //update


                    vl["mtr_ant"]=valor_materia;
                    console.log("update ver");
                    console.log(vl["mtr_ant"]);
                    if(colCod) vl["ant_cod"] = editable.previousValue;
                    else {
                        vl["ant_prof"] = editable.previousValue;
                    }
                    save_edition.extrairDados(editable.selected, col, row, colCod, "u", vl);


                }else{
                    console.log("insert ver");
                    //insert
                    save_edition.extrairDados(editable.selected, col, row, colCod, "i", vl);


                }

            }

            //(C6) caso de deleção
            if(editable.previousValue !== "" && valueUser === ""){
                if(colCod){
                    vl["pf"] = valueNextCell;
                    vl["cod"] = editable.previousValue;
                    nextCell.html("");
                }else{
                    vl["pf"] = editable.previousValue;
                    vl["cod"] = valuePrevCell;
                    prevCell.html("");
                }
                //"d" == delete
                save_edition.extrairDados(editable.selected, col, row, colCod, "d", vl);
            }

        }
    }
};

function erro_entrada(msg, isCod, v_User, v_nextCell, v_PrevCell, ext){
    openModal("ERRO", msg);
    $('#myModal').on('hidden.bs.modal', () => {
        if (editable.previousValue !== "") $(editable.selected).html(editable.previousValue);
        else $(editable.selected).html("");
        editable.removeEditable(editable.selected, isCod, v_User, v_nextCell, v_PrevCell);
        // Foca novamente na célula se a entrada for inválida
        editable.edit(editable.selected, editable.rowIndex, editable.colIndex, ext);
        return;
    });
}

function removeDuplicates(arr) {
    return arr.filter((item, index) => arr.indexOf(item) === index);
}


function searchInTableRows(cell, word) {
    // Pegamos a tabela e as linhas da tabela
    const $table = $(cell).closest('table');
    const $rows = $table.find('tr');
    let rowIndex = $(cell).closest('tr').index()

    // Determinamos as linhas a serem buscadas com base nas condições fornecidas
    let rowsToSearch = [];
    // console.log("-----")
    // console.log(rowIndex)

    if (rowIndex === 0 || rowIndex === 1) {
        rowsToSearch = [2, 1];
    } else if (rowIndex === 7 || rowIndex === 9) {
        rowsToSearch = [7, 9];
    } else if (rowIndex === 8 || rowIndex === 10) {
        rowsToSearch = [8, 10];
    } else if (rowIndex === 3 || rowIndex === 5) {
        rowsToSearch = [3, 5];
    } else {
        console.log('Linha não especificada para busca.');
        return false;
    }

    // Função para verificar se a palavra está em uma linha
    function containsWord($row, word) {
        const $cells = $row.find('td');
        let found = false;
        $cells.each(function() {
            if ($(this).text().includes(word)) {
                found = true;
                return false; // Para o loop ao encontrar a palavra
            }
        });
        return found;
    }

    // Faz a busca nas linhas determinadas
    let found = false;
    rowsToSearch.forEach(function(index) {
        console.log("linhas pesquisada")
        console.log(index)

        const $currentRow = $rows.eq(index - 1); // Ajustando para índice 0-based
        if (containsWord($currentRow, word)) {
            found = true;
        }
    });

    if (found) {
        console.log('Palavra encontrada.');
        return true;
    } else {
        console.log('Palavra não encontrada.');
        return false;
    }
}

// Função para encontrar elementos exclusivos em cada lista
function difference(arr1, arr2) {
    return arr1.filter(element => !arr2.includes(element));
}

