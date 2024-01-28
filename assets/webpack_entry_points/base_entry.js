//import "../js/htmx.min.js";
import "../js/alpine.js";
import "../img/content/hhu_logo.svg";
import getCookie from "../js/getCookie.js";
import { testTypescript } from "../ts/test.ts";
import "../css/main.css";
import { get } from "jquery";

async function onChangeConversation(event) {
    var conversation_id = event.target.id
    console.log("change_conversation: ", window.change_conversation,)
    var response = await $.ajax({
        url: `${window.change_conversation}`,
        method: 'POST',
        dataType: 'json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        data: { "conversation": conversation_id },
        success: function (response) {
            // Handling the successful response
            console.log('Data received:', response);
        },
        error: function (xhr, status, error) {
            // Handling errors
            console.error('Request failed:', status, error);
        }
    });
    window.location.reload();
}

async function onCreateConversation(event) {
    console.log("create_conversation: ", window.create_conversation,)
    var response = await $.ajax({
        url: `${window.create_conversation}`,
        method: 'POST',
        dataType: 'json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        },
        data: {},
        success: function (response) {
            // Handling the successful response
            console.log('Data received:', response);
        },
        error: function (xhr, status, error) {
            // Handling errors
            console.error('Request failed:', status, error);
        }
    });
    window.location.reload();
}

document.body.addEventListener("htmx:afterRequest", (event) => {
    var exit = false
    if (exit) {
        return
    }
    console.log("htmx-event: ", event.detail.target.id);
    // filters for specific htmx events and their targets to trigger component specific initialization
    if (event.detail.target.id == "mailbox-div-snapshot") {

    }
    if (event.detail.target.id == "conversation-log") {
        // Get the scrollable element
        var scrollableElement = document.getElementById("conversation-log")
        // Scroll the element to the bottom
        scrollableElement.scrollTop = scrollableElement.scrollHeight;
    }
    if (event.detail.target.id == "htmx-past-conversations") {
        $(".conversation-list").find("a").not(".selected").on("click", function (event) {
            onChangeConversation(event)
        })
        $("#new-conversation-button").on("click", function (event) {
            onCreateConversation(event)
        })
    }
})

document.addEventListener("DOMContentLoaded", function () {
    $("question-form").on("submit", function (event) {
    })
})

async function createQuestionObject(response_dict) {
    var questionId = response_dict["id"]
    var finished = response_dict["state"]
    var question = response_dict["question"]
    var answer = response_dict["answer"]
    var pairDiv = $(`#question-${questionId}`)

    if (pairDiv.length == 0) {
        let sampleDiv = $("#question-template")
        pairDiv = sampleDiv.clone()
        pairDiv.attr("id", `question-${questionId}`)
        pairDiv.removeClass("hidden")
        // add new answer text TODO: make this go word for word like chatgpt for chat simulation
        pairDiv.find(".question-text").append(question)

        $("#conversation-log").append(pairDiv)
    }
    // add new answer text TODO: make this go word for word like chatgpt for chat simulation
    pairDiv.find(".answer-text").append(answer)
    if (finished == "unfinished") {
        var response = await $.ajax({
            url: window.regular_pull,
            method: 'POST',
            dataType: 'json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
            },
            data: { question_id: questionId },
            success: function (response) {
                // Handling the successful response
                console.log('Data received:', response);
            },
            error: function (xhr, status, error) {
                // Handling errors
                console.error('Request failed:', status, error);
            }
        });
        let new_response_dict = response
        pairDiv = createQuestionObject(new_response_dict)
    }
    if (finished == "failed") {
        console.log("question generation failed", questionId)
        return pairDiv
    }
    return pairDiv
}

async function onSubmitQuestion(event) {
    event.preventDefault();
    var value = $("#id_question").get(0).value
    console.log("value", value)
    // Making a GET request using $.ajax()
    var response = await $.ajax({
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
    createQuestionObject(response)
}

//async function onChangeModel(event) {
//var response = await $.ajax({
//url: window.change_conversation,
//method: 'POST',
//dataType: 'json',
//headers: {
//"X-Requested-With": "XMLHttpRequest",
//"X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
//},
//data: { question_id: questionId },
//success: function (response) {
//// Handling the successful response
//console.log('Data received:', response);
//},
//error: function (xhr, status, error) {
//// Handling errors
//console.error('Request failed:', status, error);
//}
//});
//}


window.onSubmitQuestion = onSubmitQuestion
window.onChangeConversation = onChangeConversation
