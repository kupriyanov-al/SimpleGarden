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
   
    
    

    // var myModal = document.getElementById('staticBackdrop1')
    // myModal.addEventListener('shown.bs.modal', function () {
    //     console.log("MODAL")
    //     window.location.href = document.URL +'user/login'
    // })
    var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop1'), {
        keyboard: false
    })

    // var modal_btn = document.getElementById('btn_modal_show');
    // modal_btn.addEventListener('click', function (e) {
    //     window.location.href = '{/user/login}'
    // } )
    // console.log(document.URL)

    if (window.location.pathname == '/user/login/'){
        myModal.show()
    }

    // console.log(document.URL)
    // console.log(window.location.host);
    // console.log(window.location.hostname);
    // console.log(window.location.pathname);

}
    

    
    






