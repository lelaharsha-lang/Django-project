document.getElementById("loginForm").addEventListener("submit", function(event) {
  event.preventDefault(); // prevent page reload

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const mobile = document.getElementById("mobile").value;

  // Simple validation example
  if (mobile.length !== 10) {
    document.getElementById("message").textContent = "Mobile number must be 10 digits.";
    document.getElementById("message").style.color = "red";
    return;
  }

  document.getElementById("message").textContent = `Welcome, ${username}! Your form is submitted.`;
  document.getElementById("message").style.color = "green";
});
