var modal = document.querySelector(".modal-container");
var modalGuts = document.querySelector(".modal");
var modalGutsReally = document.querySelector(".modal-guts");
var modalOverlay = document.querySelector(".modal-overlay");
var closeButton = document.querySelector("#close-button");
var openButton = document.querySelector("#open-modal-id");
var confirmButton = document.querySelector("#confirm-button");


if (openButton) {
    var openButtonHref = openButton.getAttribute("href");

    confirmButton.addEventListener("click", function (event) {
        window.location.href = openButtonHref;
    });
    
    openButton.addEventListener("click", function(event) {
        event.preventDefault();
        modalGuts.classList.toggle("modal-guts-active");
        modalGutsReally.classList.toggle("modal-guts-active");
        modalOverlay.classList.toggle("modal-overlay-active");
    });
    
    closeButton.addEventListener("click", function (event) {
        modalGuts.classList.toggle("modal-guts-active");
        modalGutsReally.classList.toggle("modal-guts-active");
        modalOverlay.classList.toggle("modal-overlay-active");
    });
}


