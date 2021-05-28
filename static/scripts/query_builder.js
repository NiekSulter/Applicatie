function getInput(el) {
    let input = document.getElementById("zoekterm").value
    let keyword = el.value

    console.log(input, keyword)
}

function setSelectedTerm(el) {
    let buttonSpan = document.getElementById("fieldButtonText")
    let buttonDiv = document.getElementById("selectmenu")
    let buttonList = Array.from(buttonDiv.getElementsByTagName("button"))
    buttonSpan.innerHTML = el.innerText

    buttonList.forEach((button) => {button.setAttribute("aria-checked", "false")});

    el.setAttribute("aria-checked", "true")
}

function getQueryTerm(keyword, term) {
    let queryBox = document.getElementById("queryBox")
    let cook = decodeURIComponent(document.cookie)
    let lastKeyword

    if(cook) {
        lastKeyword = cook.split("=")[1]
    }

    switch (keyword) {
        case "AND":

            break;
        case "OR":

            break;
        case "NOT":

            break;
    }

}