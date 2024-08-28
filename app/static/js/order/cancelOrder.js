function cancelOrder(status, orderId) {
    if (status != "Pending") {
        var toast = $('<div>', {
            class: 'toast',
            role: 'alert',
            'aria-live': 'assertive',
            'aria-atomic': 'true',
            html: `
              <div class="toast-header">
                <img src="/static/images/favicons/favicon.ico" class="rounded me-2" style="width: 20px; height: 20px;">
                <strong class="me-auto">Foodwagon</strong>
                <small class="text-muted">just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
              </div>
              <div class="toast-body">
                You can only cancel the order when it is in Pending status.
              </div>
            `
        });
  
        $('#toastContainer').append(toast);
        var bootstrapToast = new bootstrap.Toast(toast.get(0));
        bootstrapToast.show();
    }
    else {
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
                    if (window.location.href.includes('/res/order-detail')) {
                        window.location.href = '/res/order'
                    } else {
                        window.location.href = '/orderhistory'
                    }
                } else {
                    console.error('Failed to cancel order:', result.message);
                }
            },
            error: function(error) {
                console.error('Error canceling order:', error);
            }
        });
    }
}
