document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  try {
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Login response:", data); // Debug log

    if (data.Status === "Success") {
      window.location.href = data.redirect_url;
    } else {
      document.getElementById("message").innerText = data.Message || "Login failed!";
    }
  } catch (error) {
    console.error("Login error:", error);
    document.getElementById("message").innerText = "Something went wrong!";
  }
});





  


