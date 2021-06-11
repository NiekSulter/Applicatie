/**
 * function to get the user input from the "Add term to query" textfield along with the selected keyword.
 * @param el the selected keyword button
 */
function getInput(el) {
    let input = document.getElementById("zoekterm").value
    let AON = el.value

    console.log(input, AON)

    document.getElementById("det_keyword").removeAttribute("open")

    getQueryTerm(input, AON)
}

/**
 * function to get all possible options from the "field" selector
 * @returns {HTMLButtonElement[]} array with all possible options
 */
function getButtonList() {
    let buttonDiv = document.getElementById("selectmenu")
    return Array.from(buttonDiv.getElementsByTagName("button"))
}

/**
 * function the place a checkmark when a user selects a search field with "field" selector
 * @param el field selector element
 */
function setSelectedTerm(el) {
    let buttonSpan = document.getElementById("fieldButtonText")
    let buttonList = getButtonList()
    buttonSpan.innerHTML = el.innerText

    buttonList.forEach((button) => {button.setAttribute("aria-checked", "false")});

    el.setAttribute("aria-checked", "true")

    document.getElementById("det_field").removeAttribute("open")
}

/**
 * function to combine the user input, selected keyword and search field into a single entry, this entry gets added to the query box.
 * @param term the user submitted term
 * @param AON the user selected keyword
 */
function getQueryTerm(term, AON) {
    let queryBox = document.getElementById("queryBox")
    let buttonList = getButtonList()
    let keyword

    buttonList.forEach((button) => {(button.getAttribute("aria-checked") === "true") ? keyword = button.value : null})

    let termFormatted

    if (keyword === "All fields") {
        termFormatted = `${term}`
    } else {
        termFormatted = `${term}[${keyword}]`
    }

    if(queryBox.value.length !== 0) {
        queryBox.value = "(" + queryBox.value + ")" + ` ${AON} ` + `(${termFormatted})`
    } else {
        queryBox.value = termFormatted
    }
}