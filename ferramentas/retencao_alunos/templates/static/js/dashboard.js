var {year, semester} = getCurrentYearAndSemester()
mostra_ano_semestre()

const disciplines_autocomplete = JSON.parse(document.getElementById("disciplines").textContent);

$(function() {
    
    $("#disciplineInput").autocomplete({
        source: function(request, response) {
            let results = $.ui.autocomplete.filter(Object.keys(disciplines_autocomplete), request.term);
            response(results);
        },
        minLength: 2
    });
});

document.getElementById("botaoBuscar").addEventListener("click", function() {

    var valorInput = document.getElementById("disciplineInput").value;

    document.getElementById("codmat").innerHTML = valorInput

    var codigo = valorInput.substring(0, 7);
    
    renderiza_info_materia(`retorna_info_materia/?code=${codigo}&year=${year}&semester=${semester}`)
    
  });

document.getElementById("download_pdf_impar").addEventListener("click", function() {

    var semester_name = "1"

    downloadPDF(`generate_pdf/?semester=${semester}&year=${year}&semester_name=${semester_name}`)
    
  });

document.getElementById("download_pdf_par").addEventListener("click", function() {

    var semester_name = "2"

    downloadPDF(`generate_pdf/?semester=${semester}&year=${year}&semester_name=${semester_name}`)

});

document.getElementById('updateDataButton').addEventListener('click', function() {
    year = document.getElementById('yearSelector').value;
    semester = document.getElementById('semesterSelector').value;

    mostra_ano_semestre()
    
    renderiza_lista_materias_atrasados_impar()
    renderiza_lista_materias_atrasados_par()

    
});



var myChart_info;
var myChartPar;
var myChartImpar;

function mostra_ano_semestre(){

    document.querySelector(".ano_span").innerHTML = year
    document.querySelector(".semestre_span").innerHTML = semester
}

function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 170;
        let g = Math.random() * 170;
        let b = Math.random() * 170;
        bg_color.push(`rgba(${r}, ${g}, ${b})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }
    
    return [bg_color, border_color];
    
}


renderiza_lista_materias_atrasados_impar()
renderiza_lista_materias_atrasados_par()

function renderiza_lista_materias_atrasados_par(){

    url = `lista_materias_atrasados_par/?year=${year}&semester=${semester}`

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        if (myChartPar) {
            myChartPar.destroy(); // Destroy the existing chart if it exists
        }
        
        const ctx = document.getElementById('atrasados_disciplinas_par').getContext('2d');
       
        let labels = []
        let dados = []
        
        for (const chave in data) {
            labels.push(chave);
            dados.push(data[chave]);
        }

        var cores_produtos_mais_vendidos = gera_cor(qtd=20)
        myChartPar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: dados,
                    backgroundColor: cores_produtos_mais_vendidos[0],
                    borderColor: cores_produtos_mais_vendidos[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });


    })
  
}

function renderiza_lista_materias_atrasados_impar(){

    url = `lista_materias_atrasados_impar/?year=${year}&semester=${semester}` 

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

        if (myChartImpar) {
            myChartImpar.destroy(); // Destroy the existing chart if it exists
        }
        
        const ctx = document.getElementById('atrasados_disciplinas_impar').getContext('2d');
       
        let labels = []
        let dados = []
        
        for (const chave in data) {
            labels.push(chave);
            dados.push(data[chave]);
        }

        var cores_produtos_mais_vendidos = gera_cor(qtd=20)
        myChartImpar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: dados,
                    backgroundColor: cores_produtos_mais_vendidos[0],
                    borderColor: cores_produtos_mais_vendidos[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });


    })
  
}

function renderiza_info_materia(url) {

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('informaçao_disciplina').getContext('2d');
        let labels = []
        let dados = []
        
        if (myChart_info) {
            myChart_info.destroy(); // Destrua o gráfico anterior
        }


        labels = ["alunos cursando", "alunos a cursar - período ideal", "alunos a cursar - atrasados"]
        dados = [data["students currently studdying"],
         data["students to study - ideal period"],
          data["students to study - late"]]
        
        var cores_produtos_mais_vendidos = gera_cor(qtd=4)
        myChart_info = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dados,
                    backgroundColor: cores_produtos_mais_vendidos[0],
                    borderColor: cores_produtos_mais_vendidos[1],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                color: 'black',
                                size: '15'
                            }
                        }
                    }
                }
            }
            
        });


    })
  
}

function downloadPDF(url) {
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'relatorio.pdf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        });
}

function carregarTabela(url) {
    var tbody = document.querySelector('#tabela');

    // Limpar o conteúdo anterior da tabela
    tbody.innerHTML = '';

    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
    //Preencher a tabela com os dados
    
    aluno =  {}
    for (const chave in data) {
        aluno[chave.substring(0,11)] = [data[chave]["qtd_late"], chave.slice(-4)]
    }

    // Converter o objeto em uma matriz de pares chave-valor
    var dataArray = Object.entries(aluno);
    // Ordenar a matriz com base nos valores (índice 1)
    dataArray.sort(function(a, b) {
        return b[1][0] - a[1][0];
    });

    // Reconstruir o objeto a partir da matriz ordenada
    aluno = Object.fromEntries(dataArray.slice(0,10));


    for (var alunoKey in aluno) {
        if (data.hasOwnProperty(alunoKey)) {
            var disciplinasAtrasadas = data[alunoKey];
            var row = tbody.insertRow();
            var cellAluno = row.insertCell(0);
            var cellDisciplinas = row.insertCell(1);
            var anoIngresso = row.insertCell(2)

            cellAluno.textContent = alunoKey;
            cellDisciplinas.textContent = disciplinasAtrasadas["qtd_late"];
            anoIngresso.textContent = disciplinasAtrasadas["start_year"]
        }
    }
    
    })

    
}


function getCurrentYearAndSemester() {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth() + 1; // Months are zero-based, so add 1

    let currentSemester;
    if (currentMonth >= 1 && currentMonth <= 6) {
        currentSemester = 1;
    } else {
        currentSemester = 2;
    }

    return {
        year: currentYear,
        semester: currentSemester
    };
}