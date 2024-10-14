const quoteText = document.querySelector("#text");
const author = document.querySelector("#author");
const quoteButton = document.querySelector("#new-quote");
const addQuoteButton = document.querySelector("#submit-btn");

async function fetchQuotes() {
    try {
        const response = await fetch('http://localhost:8000/quotes');
        const quotes = await response.json();
        console.log(quotes);
        return quotes;
    } catch (error) {
        return [];
    }
}

async function createQuotes() {
    const quoteInput = document.querySelector("#quote-input").value;
    const authorInput = document.querySelector("#author-input").value;
    const colorInput = document.querySelector("#color-input").value;

    const data = {
        quote: quoteInput,
        author: authorInput,
        color: colorInput
    };

    try {
        const response = await fetch('http://localhost:8000/add-quote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        console.log(response);  // Log the full response object

        if (response.ok) {
            const result = await response.json();
            console.log('Quote added:', result);
        } else {
            console.error("Failed to add quote:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function onLoad() {
    const quotes = await fetchQuotes();  // Fetch quotes from the backend
    const randomQuote = Math.floor(Math.random() * quotes.length);
    const { quote, author: quoteAuthor, color } = quotes[randomQuote];
    const body = document.body.style;
    const button = quoteButton.style;
    const animate = 'background-color 0.5s ease';

    quoteText.innerHTML = `${quote}`;
    author.innerHTML = `${quoteAuthor}`;
    body.transition = animate;
    body.backgroundColor = color;
    body.color = color;
    button.backgroundColor = color;
    button.transition = animate;
}

quoteButton.addEventListener('click', () => {
    onLoad();
});

addQuoteButton.addEventListener('click', (e) => {
    e.preventDefault();
    createQuotes();
})

onLoad();
