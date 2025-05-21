const form = document.getElementById("authForm");
const signupBtn = document.getElementById("signupBtn");
const signinBtn = document.getElementById("signinBtn");
const letsLearn = document.getElementById("letsLearn");
const title = document.getElementById("title");

signupBtn.addEventListener("click", function () {
    form.action = "/signup";
    title.textContent = "Sign Up";
    signupBtn.classList.remove("disable");
    signinBtn.classList.add("disable");
});

signinBtn.addEventListener("click", function () {
    form.action = "/login";
    title.textContent = "Login";
    signinBtn.classList.remove("disable");
    signupBtn.classList.add("disable");
});