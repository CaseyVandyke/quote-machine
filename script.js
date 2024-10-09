import quotes from './quote.js';
const quoteText = document.querySelector("#text");
const author = document.querySelector("#author");
const quoteContainer = document.querySelector("#quote-box");
const quoteButton = document.querySelector("#new-quote");

function onLoad() {
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

onLoad();