function submitBagForm(itemId) {
    const form = document.querySelector(`.bag-item-form-${itemId}`);
    if (form) {
        form.submit();
    }
}

function submitRemoveItem(itemId) {
    const form = document.querySelector(`.bag-item-form-${itemId}`);
    if (form) {
        const quantityInput = form.querySelector('input[name="quantity"]');
        quantityInput.value = 0;
        form.submit();
    }
}
