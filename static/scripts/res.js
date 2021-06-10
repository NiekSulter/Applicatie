function highlightWord(el) {

    var pel = el.parentElement

    var pel2 = pel.parentElement

    var tableName = ""

    if (pel2.innerText.includes("Gene")) {
        tableName = 'DiseaseTable'
    } else {
        tableName = 'GeneTable'
    }

    clearTables('GeneTable')
    clearTables('DiseaseTable')

    var cel = pel.children
    var id = cel[3].innerHTML
    var table = document.getElementById(tableName)

    let element = document.getElementById("htmlTag")
    let currentStatus = element.getAttribute("data-color-mode")

    if (currentStatus === "light") {
        pel.style.backgroundColor = "#ffcbc0"
    } else {
        pel.style.backgroundColor = "#2D5D7B"
    }


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

function clearTables(tableName) {
    var table1 = document.getElementById(tableName)

    for (var r = 0, n = table1.rows.length; r < n; r++) {
        let row = table1.rows[r]

        row.style.backgroundColor = ""
    }
}

// DARK & LIGHT MODE CODE

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

$( document ).ready(function() {
    let cook = decodeURIComponent(document.cookie)
    if(cook){
        setColorMode(cook.split("=")[1])
    }
});
