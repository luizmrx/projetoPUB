document.getElementById("seguir").addEventListener("click", () => {
    url = "/home.html"
    seguirParaSistema(url);
})

document.getElementById("nova_planilha").addEventListener("click", () => {
    url = "/carregarplanilha.html"
    carregarNovaPlanilha(url);
})  




function seguirParaSistema(url) {
    fetch(url, {
        method: "get"
    }).then((result) => {
        window.location.href = "home.html";
    })
}

function carregarNovaPlanilha(url) {
    fetch(url, {
        method: "get"
    }).then((result) => {
        window.location.href = "carregarplanilha.html";
    })
}