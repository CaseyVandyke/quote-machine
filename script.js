import quotes from './quote.js';
const quoteText = document.querySelector("#text");

const randomQuote = Math.floor(Math.random() * quotes.length);

quoteText.innerHTML += `${quotes[randomQuote].quote}`




