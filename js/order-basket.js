const OrderBasket = (() => {
    let basket =
JSON.parse(localStorage.getItem('cyberniche_basket')) || [];

    const saveToLocalStorage = () => {
        localStorage.setItem('cyberniche_basket',
JSON.stringify(basket));
    };

    const addItem = (product) => {
        const existingItem = basket.find(item => item.id ===
product.id);
        if (existingItem) {
            existingItem.quantity += product.quantity;
        } else {
            basket.push(product);
        }
        saveToLocalStorage();
        updateUI();
    };

    const removeItem = (productId) => {
        basket = basket.filter(item => item.id !==
productId);
        saveToLocalStorage();
        updateUI();
    };

    const getItems = () => basket;

    const getTotal = () => basket.reduce((total, item) =>
total + (item.price * item.quantity), 0);

    const clear = () => {
        basket = [];
        saveToLocalStorage();
        updateUI();
    };

    const updateUI = () => {
        const totalAmountElement =
document.getElementById('total-amount');
        if (totalAmountElement) {
            totalAmountElement.textContent =
`$${getTotal().toFixed(2)}`;
        }
    };

    updateUI();

    return {
        addItem,
        removeItem,
        getItems,
        getTotal,
        clear
    };
})();

document.getElementById('btn-checkout').addEventListener('clidocument.getElementById('btn-checkout').addEventListener('click', () => {
    // Lógica para ver el pedido
});