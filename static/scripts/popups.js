function success_popup(message) {
    $("div.success").text(message)
    $("div.success").fadeIn(300).delay(1500).fadeOut(400);
}

function failure_popup(message) {
    $("div.failure").text(message)
    $("div.failure").fadeIn(300).delay(1500).fadeOut(400);
}

function warning_popup(message) {
    $("div.warning").text(message)
    $("div.warning").fadeIn(300).delay(1500).fadeOut(400);
}