const usernameField = document.querySelector("#usernameField");
const usernameFeedBackArea = document.querySelector(".username-invalid-feedback");

const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".email-invalid-feedback");

const passwordField = document.querySelector("#passwordField");
const passwordFeedBackArea = document.querySelector(".password-invalid-feedback");
const showPasswordToggle = document.querySelector(".show-password-toggle");

const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

const submitButton = document.querySelector("#submitField");

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    usernameFeedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username/", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",

        })
            .then((res) => res.json())
            .then((data) => {
            usernameSuccessOutput.style.display = "none";
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                usernameFeedBackArea.style.display = "block";
                usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitButton.disabled = true;
            } else {
                submitButton.disabled = false;
            }
        });
    }
});


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email/", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error) {
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                    submitButton.disabled = true;
                } else {
                    submitButton.disabled = false
                }
            })
    }
})



const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Show") {
        showPasswordToggle.textContent = "Hide";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "Show";
        passwordField.setAttribute("type", "password");
    }
};
showPasswordToggle.addEventListener("click", handleToggleInput);

passwordField.addEventListener("keyup", (e) => {
    const passwordVal = e.target.value;

    passwordField.classList.remove("is-invalid");
    passwordFeedBackArea.style.display = "none";

    if (passwordVal.length > 0) {
        fetch("/authentication/validate-password/", {
            body: JSON.stringify({ password: passwordVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.password_invalid) {
                    passwordField.classList.add("is-invalid");
                    passwordFeedBackArea.style.display = "block";
                    passwordFeedBackArea.innerHTML = `<p>${data.password_invalid}</p>`;
                    submitButton.disabled = true;         
                } else {
                    submitButton.disabled = false; 
                }
            })
    }

}
)