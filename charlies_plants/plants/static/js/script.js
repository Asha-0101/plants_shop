// SEARCH ICON
document.getElementById('searchIcon').addEventListener('click', function() {
    var mobileSearchBar = document.getElementById('mobileSearchBar');
    mobileSearchBar.classList.toggle('d-none');
});




// QUANTITY | ADD TO CART
document.addEventListener("DOMContentLoaded", function () {
    const btnPlus = document.getElementById("btnPlus");
    const btnMinus = document.getElementById("btnMinus");
    const txtQty = document.getElementById("textQty");
    const pid = document.getElementById("pid").value; // Get the product ID value
    const tkn = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const btnCart = document.getElementById("btnCart");

    // Quantity increment
    btnPlus.addEventListener("click", function () {
        let qty = parseInt(txtQty.value, 10);
        qty = isNaN(qty) ? 0 : qty;
        if (qty < 10) {
            qty++;
            txtQty.value = qty;
        }
    });

    // Quantity decrement
    btnCart.addEventListener("click", function () {
        let qty = parseInt(txtQty.value, 10);
    
        if (qty > 0) {
            let postObj = {
                product_qty: qty,
                pid: pid,
                token: tkn
            };
    
            console.log("Attempting to send request:", postObj); //  Log data before sending
    
            fetch("/addtocart/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": tkn
                },
                body: JSON.stringify(postObj)
            })
            .then(response => {
                console.log("Fetch Response:", response); //  Log response
                if (!response.ok) {
                    if (response.status === 401) {
                        console.warn("User is not authenticated. Redirecting to login.");
                        Swal.fire({
                            icon: 'error',
                            title: 'Not Logged In',
                            text: 'You must be logged in to add items to the cart. Redirecting to login...',
                        }).then(() => {
                            window.location.href = "/login/"; // Redirect to login page
                        });
                    } else {
                        console.error("❌ Server error:", response.status);
                        Swal.fire({
                            icon: 'error',
                            title: 'Server Error',
                            text: 'An error occurred while processing your request. Please try again later.',
                        });
                    }
                    return response.text(); // Read response even if not JSON
                }
                return response.json();
            })
            .then(data => {
                if (typeof data === "string") {
                    console.error("Unexpected Response (Not JSON):", data);
                    Swal.fire({
                        icon: 'error',
                        title: 'Unexpected Response',
                        text: 'The server returned an unexpected response. Please try again.',
                    });
                    return;
                }
                console.log("Response Data:", data); //  Log response data
                if (data.status === "Success") {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success!',
                        text: 'Plant added to cart successfully!',
                    });
                } else {
                    // Show SweetAlert2 alert for failed add-to-cart
                    Swal.fire({
                        icon: 'warning',
                        title: 'Add to Cart Failed',
                        text: `Add to cart failed: ${data.status}`,
                    });
                }
            })
            .catch(error => {
                console.error("❌ Fetch Error:", error); //  Log any errors
                Swal.fire({
                    icon: 'error',
                    title: 'Network Error',
                    text: 'An error occurred while connecting to the server. Please check your internet connection.',
                });
            });
        } else {
            Swal.fire({
                icon: 'warning',
                title: 'Invalid Quantity',
                text: 'Please enter a valid quantity.',
            });
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Select all trash buttons
    const trashButtons = document.querySelectorAll('.btn-outline-danger');

    trashButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default action

            // Get the URL from the parent anchor tag
            const removeUrl = button.closest('a').getAttribute('href');

            // Show SweetAlert confirmation dialog
            Swal.fire({
                title: 'Are you sure?',
                text: 'Do you want to remove this item from your cart?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, remove it!',
                cancelButtonText: 'No, keep it'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirect to the removal URL
                    window.location.href = removeUrl;
                }
            });
        });
    });
});



