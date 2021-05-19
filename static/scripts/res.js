function highlightWord(el) {

    // var id = clickedelement.getElementById("articleID")

    var pel = el.parentElement

    clearTables()

    var cel = pel.children
    var id = cel[3].innerHTML
    var table = document.getElementById('DiseaseTable')

    pel.style.backgroundColor = "#ffcbc0"


    for (var r = 0, n = table.rows.length; r < n; r++) {
        let row = table.rows[r]
        let rownum = row.cells[3].innerHTML

        row.style.backgroundColor = ""

        if (rownum === id) {
            row.style.backgroundColor = "#ffcbc0"
        }

    }
}

function clearTables() {
    var table1 = document.getElementById('GeneTable')

    for (var r = 0, n = table1.rows.length; r < n; r++) {
        let row = table1.rows[r]

        row.style.backgroundColor = ""
    }
}