var ths = document.getElementsByTagName('th'),
    tds = document.getElementsByTagName('td'),
    wr = document.querySelector("#wrapper"),

function getCol(str) {
    var col = [];
    for (var i = 0; i < ths.length; i++) {
        if(ths[i].innerHTML.indexOf(str) !== -1) {
            var id = i;
            break;
        }
    }

    for (var i = 0; i < tds.length; i++) {
        col.push(tds[i].children[id]);
    }
    return col;
}

var approved = getCol("Approved");
for (var i = 0; i < approved.length; i++) {
    if(approved[i].innerHTML == "False") {
        approved[i].innerHTML = "";

    }
}
