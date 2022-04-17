$('#slider1, #slider2, #slider3, #slider4, #slider5').owlCarousel({
    loop: false,
    margin: 20,
    autoplay: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
        },
        600: {
            items: 3,
            nav: true,
        },
        1000: {
            items: 5,
            nav: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            // console.log(data)
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            // console.log(data)
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function (data) {
            // console.log(data)
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})