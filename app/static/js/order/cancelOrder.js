function cancelOrder(orderId) {
    const url = document.querySelector('meta[name="cancel-order"]').getAttribute('content');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify({ "order_id": orderId }),
        success: function(result) {
            console.log('Update successful:', result);
            if (result.success) {
              window.location.href = '/'
            } else {
                console.error('Failed to cancel order:', result.message);
            }
        },
        error: function(error) {
            console.error('Error canceling order:', error);
        }
    });
}
