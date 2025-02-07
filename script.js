async function fetchStockPrices() {
    try {
        // Faz a requisição à sua API no PythonAnywhere
        const url = 'https://edsonvinicius76.pythonanywhere.com/api/market';
        
        // Faz a requisição à API
        const response = await fetch(url);
        const data = await response.json();
        
        console.log("Dados recebidos:", data);  // Adicionando log para depuração

        // Mapeia os resultados para atualizar os elementos HTML correspondentes
        const stockData = {
            "Apple (AAPL)": "aapl",
            "Nvidia (NVDA)": "nvda",
            "Petrobras (PBR)": "petr4",
            "USD/BRL": "usdbrl"
        };

        // Atualiza os valores no front-end
        Object.keys(data).forEach(stock => {
            const elementId = stockData[stock];
            if (elementId) {
                let price;
                
                // Se for o USD/BRL, pega o valor do campo correto
                if (stock === "USD/BRL") {
                    price = data[stock]["USD/BRL"];
                } else if (data[stock] && data[stock].close) {
                    price = data[stock].close;
                } else {
                    console.error(`Preço não encontrado para ${stock}`);
                    return;  // Pula a atualização caso não encontre o preço
                }
                
                // Exibe os dados no frontend
                const formattedPrice = `R$ ${price.toFixed(2)}`;
                const element = document.getElementById(elementId);
                if (element) {
                    element.innerText = formattedPrice;
                } else {
                    console.error(`Elemento com ID ${elementId} não encontrado.`);
                }
            }
        });

    } catch (error) {
        console.error("Erro ao buscar cotações:", error);
        document.querySelectorAll(".price").forEach(el => el.innerText = "Erro ao carregar");
    }
}

// Atualiza a cada 30 segundos
setInterval(fetchStockPrices, 30000);

// Chama a função ao carregar a página
fetchStockPrices();
