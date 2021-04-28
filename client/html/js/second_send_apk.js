var form = document.forms.namedItem("first-attack");
form.addEventListener('submit', function(ev) {

    var oOutput = document.querySelector('#result'),
        oData = new FormData(form);

    oData.append("CustomField", "This is some extra data");

    var oReq = new XMLHttpRequest();
    oReq.open("POST", "http://192.168.1.23:5000/api/second/upload/", true);
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            var jsonResponse = JSON.parse(oReq.responseText);
            console.log('json', jsonResponse);
            oOutput.innerHTML = "Uploaded!";
            document.querySelector('#first-dwn').style.display = 'block';
            document.querySelector('#first-dwn').href = 'http://192.168.1.23:5000/api/second/download/'+jsonResponse['filename'];
            document.querySelector('#first-dwn').download = jsonResponse['filename'];

        } else {
            oOutput.innerHTML = "Error " + oReq.status + " occurred when trying to upload your file.<br \/>";
        }
    };



    oReq.send(oData);
    ev.preventDefault();
}, false);