document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  try {
    const response = await fetch("/add_product", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Add Product response:", data); // Debug log

    if (data.Status === "Success") {
      window.location.href = data.redirect_url;  // Redirect to products page
    } else {
      document.getElementById("message").innerText = data.Message || "Failed to add product!";
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("message").innerText = "Something went wrong!";
  }
});


  


