document.getElementById('fileInput').addEventListener('change', function(e) {
    var file = e.target.files[0];
    var reader = new FileReader();

    reader.onload = function(e) {
        var fileContent = e.target.result;
        document.getElementById('fileContent').textContent = fileContent;
    };

    reader.readAsText(file);
})

const fs = require('fs')
fs.readFile('tp.txt', (err, inputD) => {
    if (err) throw err;
    console.log(inputD.toString());
})