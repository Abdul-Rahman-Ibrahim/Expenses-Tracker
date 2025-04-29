















// const usernameField = document.querySelector("#usernameField");
// const usernameFeedBackArea = document.querySelector(".username-invalid-feedback");

// // const emailField = document.querySelector("#emailField");
// // const passwordField = document.querySelector("#passwordField");

// const submitButton = document.querySelector("#submitField");

// usernameField.addEventListener("keyup", (e) => {
//     const usernameVal = e.target.value;

//     usernameField.classList.remove("is-invalid");
//     usernameFeedBackArea.style.display = "none";

//     if (usernameVal.length > 0) {
//         fetch("/authentication/validate-username/", {
//             body: JSON.stringify({username: usernameVal, from_: "login"}),
//             method: "POST",
//         })
//             .then((res) => res.json())
//             .then((data) => {
//                 if (data.username_error) {
//                     usernameField.classList.add("is-invalid");
//                     usernameFeedBackArea.style.display = "block";
//                     usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`;
//                     submitButton.disabled = true;
//                 }else{
//                     submitButton.disabled = false;
//                 }
//             })
//     }
// });


// // const handleDataValidation = (field, feedBackArea, viewName, validationType, e) => {
// //     const fieldVal = e.target.value;

// //     field.classList.remove("is-invalid");
// //     feedBackArea.style.display = "none";

// //     if (fieldVal.length > 0) {
// //         fetch("/authentication/"+`${viewName}/`, {
// //             body: JSON.stringify({ username: fieldVal, from_: validationType }),
// //             method: "POST",
// //         })
// //             .then((res) => res.json())
// //             .then((data) => {
// //                 if (data.from_ == "login"){
// //                     if ()
// //                 }
// //             })
// //     }
// // }