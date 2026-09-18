document.getElementById('btn-checkout').addEventListener('clidocument.getElementById('btn-checkout').addEventListener('click', () => {
    const items = OrderBasket.getItems();
    const total = OrderBasket.getTotal();

    if (items.length === 0) {
        alert('Por favor, agregue productos a su carrito.');
        return;
    }

    let message = 'Su pedido:\n';
    items.forEach(item => {
        message += `${item.name} x${item.quantity} =
$${(item.price * item.quantity).toFixed(2)}\n`;
    });
    message += `Total: $${total.toFixed(2)}`;

    const waLink =
`https://wa.me/<NUMERO_TELEFONO>?text=${encodeURIComponent(me`https://wa.me/<NUMERO_TELEFONO>?text=${enodeURIComponent(message)}`;
    window.location.href = waLink;
});