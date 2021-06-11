/**
 * function for highlighting a clicked table row. The function grabs the
 * row & table from the el variable. Afterwards the colour of the row will be set
 * depending on the current theme: light or dark.
 * @param el clicked element
 */
function highlightWord(el) {

    var pel = el.parentElement

    var pel2 = pel.parentElement

    var tableName = ""

    if (pel2.innerText.includes("Gene")) {
        tableName = 'DiseaseTable'
    } else {
        tableName = 'GeneTable'
    }

    /* clearing both tables before new rows are coloured.*/
    clearTables('GeneTable')
    clearTables('DiseaseTable')

    var cel = pel.children
    var id = cel[3].innerHTML
    var table = document.getElementById(tableName)

    /* grabbing the current theme from the html page */
    let element = document.getElementById("htmlTag")
    let currentStatus = element.getAttribute("data-color-mode")

    if (currentStatus === "light") {
        pel.style.backgroundColor = "#ffcbc0"
    } else {
        pel.style.backgroundColor = "#2D5D7B"
    }

    /* colouring the selected table row and all table rows in the opposite table where the ArticleIDs overlap */
    for (var r = 0, n = table.rows.length; r < n; r++) {
        let row = table.rows[r]
        let rownum = row.cells[3].innerHTML

        row.style.backgroundColor = ""

        if (rownum === id) {
            if (currentStatus === "light") {
                row.style.backgroundColor = "#ffcbc0"
            } else {
                row.style.backgroundColor = "#2D5D7B"
            }
        }
    }
}

/**
 * function to clear all rows in both tables.
 * @param tableName HTML ID
 */
function clearTables(tableName) {
    var table1 = document.getElementById(tableName)

    for (var r = 0, n = table1.rows.length; r < n; r++) {
        let row = table1.rows[r]

        row.style.backgroundColor = ""
    }
}


/**
 * function for grabbing the current colour mode.
 * If the current mode is light, dark will be selected and vice versa.
 * A cookie with the selected colour mode will be set in the user's browser.
 */
function checkColorMode() {
    let element = document.getElementById("htmlTag")
    let currentStatus = element.getAttribute("data-color-mode")

    if(currentStatus === "light") {
        setColorMode("dark", element)
        document.cookie = "status=dark"
    } else {
        setColorMode("light", element)
        document.cookie = "status=light"
    }
}

/**
 * function for change the colour mode in the base.html file.
 * @param mode the selected colour mode.
 */
function setColorMode(mode){
    let element = document.getElementById("htmlTag")

    if(mode === "dark") {
        element.setAttribute("data-color-mode", "dark")
        element.setAttribute("data-dark-theme", "dark_dimmed")
    } else {
        element.setAttribute("data-color-mode", "light")
        element.setAttribute("data-dark-theme", "light")
    }
}

/**
 * JQuery function to determine the user specified colour mode on page load.
 */
$( document ).ready(function() {
    let cook = decodeURIComponent(document.cookie)
    if(cook){
        setColorMode(cook.split("=")[1])
    }
});
