function payClick() {
    if (changedInputs.size != 0) {
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
                You haven't saved your changes.
              </div>
            `
        });
  
        $('#toastContainer').append(toast);
        var bootstrapToast = new bootstrap.Toast(toast.get(0));
        bootstrapToast.show();
    }
    else {
        const url = $('meta[name="create-order"]').attr('content');
        const csrfToken = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            url: url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(response) {
                window.location.href = "/order/" + response.order_id;
            },
            error: function(error) {
                alert("Payment failed! Please try again.");
            }
        });
    }
}
