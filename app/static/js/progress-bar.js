$(document).ready(function() {
    var statusBarValue = $(".progress-bar.orderitem-progress-bar").attr("aria-valuenow")
    $(".progress-bar.orderitem-progress-bar").css("width", statusBarValue + "%")
})
