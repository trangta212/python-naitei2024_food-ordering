function addToCart(itemId) {
    const url = $('meta[name="add-to-cart-url"]').attr('content');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    const currentUrl = window.location.href;

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
            const redirectUrl = new URL(response.url);
            if (currentUrl.endsWith('menu')) {
                redirectUrl.searchParams.set('next', '/menu');
            } else {
                redirectUrl.searchParams.set('next', '/');
            }

            window.location.href = redirectUrl.toString();
        }
    })
}
