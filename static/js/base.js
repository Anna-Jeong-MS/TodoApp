$(document).ready(function () {
    getAddresses()
    
    function getAddresses(){
        const url = 'address/read'

        $.ajax({
            url: url,
            method: "GET",
            contentType: "application/json",
        }).done(function (addresses) {
            console.log(addresses)
            loadTodos(addresses)
        });
    }

    function loadTodos(addresses){
        for (const address of addresses) {
            $('#addressContainer').append('<tr>\
                <th scope="row">'+address.id+'</th>\
                <td>'+address.first_name+'</td>\
                <td>'+address.last_name+'</td>\
                <td>'+address.email+'</td>\
                <td>'+address.gender+'</td>\
                <td>'+address.ip_address+'</td>\
                </tr>')
        }
    }

    
    $('#addAddress').click(function () {
        const url = 'address/add'

        const data = {
            "first_name": String($('#inputFirstName').val()),
            "last_name": String($('#inputLastName').val()),
            "email": String($('#inputEmail').val()),
            "gender": String($('#inputGender').val()),
            "ip_address": String($('#inputIPAddress').val())
        }

        var inputData = JSON.stringify(data)
        console.log(inputData)

        $.ajax({
            url: url,
            method: "POST",
            data: inputData,
            dataType: "json",
            contentType: "application/json",
        }).done(function (result) {
            $('#inputFirstName').val('')
            $('#inputLastName').val('')
            $('#inputEmail').val('')
            $('#inputGender').val('Male').prop("selected",true);
            $('#inputIPAddress').val('')
            $('#addressContainer').empty()
            getAddresses()
        });
    })

    $('#btnConnect').click(function () {
        const url = 'connect_to_db'

        const data = {
            "serverName": String($('#txtServerName').val()),
            "admin": String($('#txtAdmin').val()),
            "password": String($('#txtPassword').val()),
        }

        var inputData = JSON.stringify(data)

        $.ajax({
            url: url,
            method: "POST",
            data: inputData,
            dataType: "json",
            contentType: "application/json",
        }).done(function (result) {
            $('#result').append('  <div class="alert alert-primary" role="alert">\
            DB Connection Success!\
          </div>')
        });
    })
});