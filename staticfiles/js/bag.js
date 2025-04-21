function submitRemoveItem(itemType, itemId) {
    const form = document.querySelector(`.bag-item-form-${itemType}-${itemId}`);
    if (form) {
        const quantityInput = form.querySelector('input[name="quantity"]');
        if (quantityInput) {
            quantityInput.value = 0;
            form.submit();
        } else {
            console.warn(`Quantity input not found in form: ${itemType}-${itemId}`);
        }
    } else {
        console.warn(`Remove form not found for item: ${itemType}-${itemId}`);
    }
}
