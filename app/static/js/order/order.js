function payClick() {
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
