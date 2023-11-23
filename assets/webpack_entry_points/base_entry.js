//import "../js/htmx.min.js";
import "../js/alpine.js";
import "../img/content/hhu_logo.svg";
import getCookie from "../js/getCookie.js";
import { testTypescript } from "../ts/test.ts";
import "../css/main.css";

document.body.addEventListener("htmx:afterRequest", (event) => {
    var exit = false
    if (exit) {
        return
    }
    console.log("htmx-event: ", event.detail.target.id);
    // filters for specific htmx events and their targets to trigger component specific initialization
    if (event.detail.target.id == "mailbox-div-snapshot") {

    }
})

document.addEventListener("DOMContentLoaded", function () {
    $("question-form").on("submit", function (event) {
    })
})


function onSubmitQuestion(event) {
    event.preventDefault();
    var value = $("#id_question").get(0).value
    console.log("value", value)
    // Making a GET request using $.ajax()
    $.ajax({
        url: window.new_question_url,
        method: 'POST',
        dataType: 'json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        data: { question_text: value, question_id: null },
        success: function (response) {
            // Handling the successful response
            console.log('Data received:', response);
        },
        error: function (xhr, status, error) {
            // Handling errors
            console.error('Request failed:', status, error);
        }
    });
}

window.onSubmitQuestion = onSubmitQuestion