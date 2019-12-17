let modal = document.querySelector(".modal-container");
let modalGuts = document.querySelector(".modal");
let modalGutsReally = document.querySelector(".modal-guts");
let modalOverlay = document.querySelector(".modal-overlay");
let closeButton = document.querySelector("#close-button");
let confirmButton = document.querySelector("#confirm-button");

let modalGutsHead = document.querySelector(".modal-guts-head");
let modalGutsContent = document.querySelector(".modal-guts-content");


let openInput = document.querySelector(".open-modal-input");
let openA = document.querySelector(".open-modal-a");


let openAll = document.querySelectorAll(".open-modal-all");
for (var i = 0; i < openAll.length; i++) {
    openAll[i].addEventListener("click", function (event) {
        if (!this.classList.contains("inp-active")) {
            if (this.tagName === "INPUT") {
                modalGutsHead.innerHTML = "Подтверждение действия";
                modalGutsContent.innerHTML ="Это действие может привести к изменениям в базе данных. Вы точно желаете продолжить?";
                confirmButton.innerHTML = "Продолжить";

                var self = this;
        
                confirmButton.addEventListener("click", function (event) {
                    self.click();
                });
            }

            if (this.tagName === "A") {
                modalGutsHead.innerHTML = "Подтверждение выхода";
                modalGutsContent.innerHTML ="Вы уверены, что хотите выйти?";
                confirmButton.innerHTML = "Выход";
        
                let allOpenButtonsHref = this.getAttribute("href");
        
                confirmButton.addEventListener("click", function (event) {
                    window.location.href = allOpenButtonsHref;
                });
            }

            event.preventDefault();
            this.classList.add("inp-active");
            modalGuts.classList.toggle("modal-guts-active");
            modalGutsReally.classList.toggle("modal-guts-active");
            modalOverlay.classList.toggle("modal-overlay-active");
        } else {

        }
    });
}

if (closeButton) {
    closeButton.addEventListener("click", function (event) {
        for (var i = 0; i < openAll.length; i++) {
            if (openAll[i].classList.contains("inp-active")) {
                openAll[i].classList.remove("inp-active");
            }
        }

        modalGuts.classList.toggle("modal-guts-active");
        modalGutsReally.classList.toggle("modal-guts-active");
        modalOverlay.classList.toggle("modal-overlay-active");
    });
}
