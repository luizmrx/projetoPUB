export {controlaPopUp}

import { coresRestrições } from "../main.js";
function controlaPopUp(cell, apelidos) {

        let resposta = {};

        document.getElementById("popup").style.display = "block";
        
        document.getElementById("closePopup").addEventListener("click", function() {
            document.getElementById("popup").style.display = "none";
            coresRestrições();
            location.reload(true);
        });
        
        document.getElementById("submitForm").addEventListener("click", function() {

            const campo1Value = document.querySelector(".campo1").value;
            const campo2Value = document.querySelector(".campo2").value;
            const campo3Value = document.querySelector(".campo3").value;

            resposta = {
                professor1: campo1Value,
                professor2: campo2Value,
                professor3: campo3Value
            }
            
            campo1Value ? resposta.professor1 = apelidos[resposta.professor1] : ""
            campo2Value ? resposta.professor2 = apelidos[resposta.professor2] : ""
            campo3Value ? resposta.professor3 = apelidos[resposta.professor3] : ""
            
            let resp = []
            if(resposta.professor1 != "") resp.push(resposta.professor1)
            if(resposta.professor2 != "") resp.push(resposta.professor2)
            if(resposta.professor3 != "") resp.push(resposta.professor3)

            // Feche o pop-up
            document.getElementById("popup").style.display = "none";
            cell.html(resp.join(" / "));
            coresRestrições();

        });
    
    }

