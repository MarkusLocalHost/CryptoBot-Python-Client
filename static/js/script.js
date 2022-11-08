const foodItems = document.querySelector(".food-items");
const foodItemTemplate = document.querySelector('#food-item');
const cart = document.querySelector('.cart');
const cartItemTemplate = document.querySelector('#cart-item');
const cartItems = document.querySelector('.cart__items');
const cartTotalPrice = document.querySelector('.cart__total-price');
const cartFurtherButton = document.querySelector('.cart__further');

Telegram.WebApp.ready()
configureThemeColor(Telegram.WebApp.colorScheme);
configureMainButton({text: 'view cart', color: '#008000', onclick: mainButtonClickListener});
Telegram.WebApp.MainButton.show();

function mainButtonClickListener() {
    if (Telegram.WebApp.MainButton.text.toLowerCase() === 'view cart') {
        configureMainButton({text: 'close cart', color: '#FF0000', onclick: mainButtonClickListener});
    } else {
        configureMainButton({text: 'view cart', color: '#008000', onclick: mainButtonClickListener});
    }
    cart.classList.toggle('active');
}

function configureMainButton({text, color, textColor = '#ffffff', onclick}) {
    Telegram.WebApp.MainButton.text = text.toUpperCase();
    Telegram.WebApp.MainButton.color = color;
    Telegram.WebApp.MainButton.textColor = textColor;
    Telegram.WebApp.MainButton.onClick(onclick);
}

function configureThemeColor(color) {
    if (color === 'dark') {
        document.documentElement.style.setProperty('--body-background-color', '#1f1e1f');
        document.documentElement.style.setProperty('--title-color', 'white');
        document.documentElement.style.setProperty('--sub-text-color', 'white');
    }
}
