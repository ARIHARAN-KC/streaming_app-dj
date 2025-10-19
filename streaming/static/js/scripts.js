// Search Bar - Live Search Feature
document.querySelector('.search-bar form').addEventListener('input', function(event) {
    const query = event.target.value.trim().toLowerCase();
    if (query.length > 2) {
        // Simulate a live search with a delay to mimic an API call (replace with real API call)
        setTimeout(() => {
            console.log(`Searching for: ${query}`); // Example log, replace with real search logic
            // Update UI with search results dynamically
        }, 300);
    }
});

// User Links - Dropdown for Profile/Logout
document.querySelector('.user-links').addEventListener('click', function(event) {
    if (event.target.tagName === 'A' && event.target.innerText === 'Profile') {
        event.preventDefault();
        const dropdown = document.createElement('div');
        dropdown.classList.add('dropdown-menu');
        dropdown.innerHTML = `
            <a href="#">View Profile</a>
            <a href="#">Logout</a>
        `;
        document.body.appendChild(dropdown);
        dropdown.style.position = 'absolute';
        dropdown.style.top = `${event.target.offsetTop + event.target.offsetHeight}px`;
        dropdown.style.left = `${event.target.offsetLeft}px`;

        // Close dropdown when clicking outside
        document.addEventListener('click', function closeDropdown(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.remove();
                document.removeEventListener('click', closeDropdown);
            }
        });
    }
});

// Sign Up Form Validation
document.querySelector('form').addEventListener('submit', function(event) {
    const password1 = document.querySelector('#password1').value;
    const password2 = document.querySelector('#password2').value;
    if (password1 !== password2) {
        event.preventDefault();
        alert('Passwords do not match!');
    }
});

// Password Strength Indicator
document.querySelector('#password1').addEventListener('input', function(event) {
    const strengthMeter = document.createElement('div');
    strengthMeter.classList.add('strength-meter');
    document.querySelector('form').appendChild(strengthMeter);

    const strength = calculatePasswordStrength(event.target.value);
    strengthMeter.textContent = `Strength: ${strength}`;
    strengthMeter.style.color = getStrengthColor(strength);
});

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length > 8) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[@$!%*?&]/.test(password)) strength += 1;
    return strength;
}

function getStrengthColor(strength) {
    switch (strength) {
        case 1: return 'red';
        case 2: return 'orange';
        case 3: return 'yellow';
        case 4: return 'blue';
        case 5: return 'green';
        default: return 'gray';
    }
}

// Login Form - Show/Hide Password
const passwordField = document.querySelector('#password');
const togglePasswordButton = document.createElement('button');
togglePasswordButton.type = 'button';
togglePasswordButton.textContent = 'Show';
togglePasswordButton.classList.add('toggle-password');

passwordField.parentNode.appendChild(togglePasswordButton);

togglePasswordButton.addEventListener('click', function() {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        togglePasswordButton.textContent = 'Hide';
    } else {
        passwordField.type = 'password';
        togglePasswordButton.textContent = 'Show';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input[type="text"], input[type="password"]');
    const submitButton = form.querySelector('button[type="submit"]');

    inputs.forEach(input => {
        input.addEventListener('input', () => {
            // Custom validation styles
            if (input.value.trim() !== '') {
                input.style.borderColor = '#4caf50';
            } else {
                input.style.borderColor = '#ddd';
            }
        });
    });

    form.addEventListener('submit', (event) => {
        let isValid = true;

        inputs.forEach(input => {
            if (input.value.trim() === '') {
                input.style.borderColor = '#ff6b6b';
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill out all fields.');
        } else {
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';
        }
    });
});
