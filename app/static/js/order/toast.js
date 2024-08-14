$(document).ready(function() {
  $('.show-toast-btn').on('click', function() {
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
              The item has been added to the cart.
            </div>
          `
      });

      $('#toastContainer').append(toast);
      var bootstrapToast = new bootstrap.Toast(toast.get(0));
      bootstrapToast.show();
  });
});
