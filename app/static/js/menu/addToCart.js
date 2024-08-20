function addToCart(itemId) {
    const url = $('meta[name="add-to-cart-url"]').attr('content');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: new URLSearchParams({
            'item_id': itemId
        })
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
}
