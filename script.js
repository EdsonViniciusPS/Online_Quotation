async function fetchStockPrices() {
    try {
        // Lista de símbolos das ações e do USD para a API do Yahoo Finance
        const symbols = ["USDBRL=X", "NVDA", "AAPL", "PETR4.SA", "VALE3.SA"];
        const url = `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${symbols.join(",")}`;

        // Faz a requisição à API
        const response = await fetch(url);
        const data = await response.json();

        // Mapeia os resultados para atualizar os elementos HTML correspondentes
        const stockData = {
            "USDBRL=X": "usdbrl",
            "NVDA": "nvda",
            "AAPL": "aapl",
            "PETR4.SA": "petr4",
            "VALE3.SA": "vale3"
        };

        // Atualiza os valores no front-end
        data.quoteResponse.result.forEach(stock => {
            const elementId = stockData[stock.symbol];
            if (elementId) {
                document.getElementById(elementId).innerText = `R$ ${stock.regularMarketPrice.toFixed(2)}`;
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
