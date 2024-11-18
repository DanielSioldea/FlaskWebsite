
console.log("jQuery version:", jQuery.fn.jquery); // Debugging line
$(document).ready(function () {
    setTimeout(function () {
        $(".alert").fadeOut("slow", function () {
            $(this).remove();
        });
    }, 5000);
});

// Checkout disable/enable feature
document.addEventListener('DOMContentLoaded', function () {
    var checkoutButton = document.getElementById('checkoutButton');
    var cartCount = parseInt(document.getElementById('cart-count').getAttribute('data-cart-count'), 10) || 0;

    // Disable the checkout button if the cart is empty
    if (cartCount === 0) {
        checkoutButton.disabled = true;
    }
});

// JavaScript to toggle chat window
function toggleChat() {
    var chatWindow = document.getElementById('chatWindow');

    if (chatWindow.classList.contains('open')) {
        chatWindow.classList.add('closing');
        chatWindow.classList.remove('open');

        setTimeout(function () {
            chatWindow.classList.remove('closing');
            chatWindow.style.display = 'none';
        }, 300); // Match the transition duration
    } else {
        chatWindow.style.display = 'flex';
        setTimeout(function () {
            chatWindow.classList.add('open');
        }, 10); // Slight delay to trigger the transition
    }
}

// JavaScript to handle resizing
const chatWindow = document.getElementById('chatWindow');
const resizeHandle = document.querySelector('.resize-handle');

// Set min and max dimensions
const minWidth = 250; // Minimum width
const minHeight = 150; // Minimum height
const maxWidth = 600; // Maximum width
const maxHeight = 600; // Maximum height

resizeHandle.addEventListener('mousedown', function (e) {
    e.preventDefault();
    window.addEventListener('mousemove', resize);
    window.addEventListener('mouseup', stopResize);
});

function resize(e) {
    let newWidth = chatWindow.offsetWidth - (e.clientX - chatWindow.offsetLeft);
    let newHeight = chatWindow.offsetHeight - (e.clientY - chatWindow.offsetTop);

    // Apply min and max constraints
    newWidth = Math.max(minWidth, Math.min(maxWidth, newWidth));
    newHeight = Math.max(minHeight, Math.min(maxHeight, newHeight));

    // Update the size of the chat window
    chatWindow.style.width = newWidth + 'px';
    chatWindow.style.height = newHeight + 'px';

    // Adjust position to keep it in bottom right
    chatWindow.style.bottom = '80px'; // Fixed bottom distance
    chatWindow.style.right = '20px'; // Fixed right distance
}

function stopResize() {
    window.removeEventListener('mousemove', resize);
    window.removeEventListener('mouseup', stopResize);
}


document.addEventListener('DOMContentLoaded', function () {
    const countrySelect = document.getElementById('country');
    const stateSelect = document.getElementById('state');

    // Object mapping countries to their respective states/provinces
    const states = {
        US: ['AL', 'AK', 'AZ', 'AR', 'AS', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
            'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH',
            'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
            'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'],

        CAN: ['AB', 'BC', 'MB', 'NT', 'NU', 'ON', 'PEI', 'QC', 'SK', 'YT']
    };

    // Function to update state dropdown based on selected country
    function updateStateOptions(countryCode) {
        // Clear out existing options in state select
        stateSelect.innerHTML = '<option value="">Choose...</option>';

        if (states[countryCode]) {
            // Add new options for the selected country
            states[countryCode].forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        }
    }

    // Event listener for when the country selection changes
    countrySelect.addEventListener('change', function () {
        const selectedCountry = countrySelect.value;
        updateStateOptions(selectedCountry);
    });
});



// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

document.addEventListener('DOMContentLoaded', function () {
    const cartCount = parseInt(document.getElementById('cart-count').getAttribute('data-cart-count'), 10) || 0;
    const checkoutButton = document.querySelector('.btn-primary[type="submit"]');

    // Disable the button if cart is empty
    checkoutButton.disabled = (cartCount === 0);

    // JS to perform correct expiration date formatting
    var expirationInput = document.getElementById('cc-expiration');
    expirationInput.addEventListener('input', function (e) {
        var value = e.target.value.replace(/\D/g, '');
        if (value.length > 4) {
            value = value.slice(0, 4);
        }
        if (value.length > 2) {
            value = value.slice(0, 2) + '/' + value.slice(2);
        }
        e.target.value = value;
    });

    expirationInput.addEventListener('keydown', function (e) {
        var value = e.target.value;
        if (e.key === 'Backspace' && value.length === 3 && value.includes('/')) {
            expirationInput.value = value.slice(0, -1);
        }
    });

    // JS to perform correct CVV formatting
    var cvvInput = document.getElementById('cc-cvv');
    cvvInput.addEventListener('input', function (e) {
        var value = e.target.value.replace(/\D/g, '');
        if (value.length > 3) {
            value = value.slice(0, 3);
        }
        e.target.value = value;
    });

    // JS to perform correct card number formatting
    var cardNumberInput = document.getElementById('cc-number');
    cardNumberInput.addEventListener('input', function (e) {
        var value = e.target.value.replace(/\D/g, '');
        if (value.length > 16) {
            value = value.slice(0, 16);
        }
        value = value.match(/.{1,4}/g);
        if (value) {
            value = value.join(' ');
        }
        e.target.value = value;
    });

});

// JS to handle the logout confirmation
document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logoutLink');

    logoutLink.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default action

        const userConfirmed = confirm('Are you sure you want to log out?');

        if (userConfirmed) {
            window.location.href = logoutLink.href; // Proceed with the logout
        }
    });
});
