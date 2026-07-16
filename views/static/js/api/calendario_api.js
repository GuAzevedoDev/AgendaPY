
const resposta = await fetch("/agendar/calendario", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            data,
            idFuncionario: id_funcionario
        })
    });
    return await resposta.json();

