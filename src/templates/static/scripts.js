document.getElementById("submitBtn").addEventListener("click", function (event) {
    event.preventDefault();

    // Extrai o texto e a rota escolhida pelo usuário e cria uma função de HTTP Request.
    const textInput = document.getElementById("textInput").value;
    const routeSelect = document.getElementById("routeSelect").value;
    const xhr = new XMLHttpRequest();

    // Abre a requisição POST para a rota escolhida
    xhr.open("POST", `/${routeSelect}/vision`, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Envia a resposta como JSON/string na tela
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            if (xhr.status === 200) {
                if (xhr.responseText) {

                    document.getElementById("output").innerText = JSON.stringify(response, null, 2);
                } else {
                    console.error("Empty response");
                }
            } else {
                document.getElementById("output").innerText = JSON.stringify(response, null, 2);
                console.error(`HTTP error ${xhr.status}: ${xhr.statusText}`);
            }
        }
    };

    xhr.send(JSON.stringify({ bucket: "imagens-grupo1", imageName: textInput }));
});