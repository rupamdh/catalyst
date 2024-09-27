$(document).ready(function () {
    function updateCart() {
        $.ajax({
            url: '/get-side-cart/',
            type: 'GET',
            success: function (response) {
                $('#side_cart').html(response.html);
            },
            error: function (xhr, status, error) {
                console.log('Error');
                // Handle error
                console.error('Error updating cart:', error);
            }
        });
    }
    updateCart();
    
});