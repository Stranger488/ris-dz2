let modal = document.querySelector(".modal-container");
let modalGuts = document.querySelector(".modal");
let modalGutsReally = document.querySelector(".modal-guts");
let modalOverlay = document.querySelector(".modal-overlay");
let closeButton = document.querySelector("#close-button");
let confirmButton = document.querySelector("#confirm-button");

let modalGutsHead = document.querySelector(".modal-guts-head");
let modalGutsContent = document.querySelector(".modal-guts-content");

let allOpenButtons = document.querySelectorAll(".open-modal");

let openInput = document.querySelector(".open-modal-input");
let openA = document.querySelector(".open-modal-a");

let formSubmit = document.getElementById("form-submit-id");
console.log(formSubmit);

if (openInput) {
    openInput.addEventListener("click", function(event) {
        if (!openInput.classList.contains("inp-active")) {
            if (openInput.tagName === "INPUT") {
                modalGutsHead.innerHTML = "Подтверждение действия";
                modalGutsContent.innerHTML ="Это действие может привести к изменениям в базе данных. Вы точно желаете продолжить?";
                confirmButton.innerHTML = "Продолжить";
        
                confirmButton.addEventListener("click", function (event) {
                    formSubmit.click();
                });
            }
    
            event.preventDefault();
            formSubmit.classList.toggle("inp-active");
            modalGuts.classList.toggle("modal-guts-active");
            modalGutsReally.classList.toggle("modal-guts-active");
            modalOverlay.classList.toggle("modal-overlay-active");
        }
    });
}

if (openA) {
    openA.addEventListener("click", function(event) {
        if (openA.tagName === "A") {
            modalGutsHead.innerHTML = "Подтверждение выхода";
            modalGutsContent.innerHTML ="Вы уверены, что хотите выйти?";
            confirmButton.innerHTML = "Выход";
    
            let allOpenButtonsHref = openA.getAttribute("href");
    
            confirmButton.addEventListener("click", function (event) {
                window.location.href = allOpenButtonsHref;
            });
        }
    
        if (formSubmit) {
            formSubmit.classList.toggle("inp-active");
        }

        event.preventDefault();
        modalGuts.classList.toggle("modal-guts-active");
        modalGutsReally.classList.toggle("modal-guts-active");
        modalOverlay.classList.toggle("modal-overlay-active");
    });
}


if (closeButton) {
    closeButton.addEventListener("click", function (event) {
        if (formSubmit) {
            formSubmit.classList.toggle("inp-active");
        }
        modalGuts.classList.toggle("modal-guts-active");
        modalGutsReally.classList.toggle("modal-guts-active");
        modalOverlay.classList.toggle("modal-overlay-active");
    });
    
}
