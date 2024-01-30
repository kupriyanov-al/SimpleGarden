window.onload = function () {

    function html_table_to_excel(type) {
        var data = document.getElementById('tbl');
        var COL_INDEX = 1;
        var file = XLSX.utils.table_to_book(data, { sheet: "sheet1"});
        
        var ws = file.Sheets[file.SheetNames[0]];
        ws["!cols"] = [{ wpx: 150 }, { wpx: 80 }, { wpx: 80 }, { wpx: 80}, { wpx: 80 }];
        ws["!cols"].s = {
            font: {
                bold: true,
                color: "000000",
                sz: '11'
            },
            fill: {
                type: 'pattern',
                patternType: 'solid',
                fgColor: { rgb: "e8f0f8" }
            }
        }
        XLSX.write(file, { bookType: type, bookSST: true, type: 'base64' });

        XLSX.writeFile(file, 'file.' + type);
    }



    btnExl.onclick = function () {
        html_table_to_excel('xlsx')
    }
    

}
    

    
    






