changeStatus = (status, orderId) => {
    const url = document.querySelector('meta[name="change-status"]').getAttribute('content');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: JSON.stringify({
            "order_id": orderId,
            "status": status,
        }),
        success: function(result) {
            console.log('Update successful:', result);
            if (result.success) {
              location.reload()
            } else {
                console.error('Failed to update:', result.message);
            }
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}
