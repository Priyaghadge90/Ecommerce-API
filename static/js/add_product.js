document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("addProductForm");

  form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);

      fetch("/add_product", {
          method: "POST",
          body: formData
      })
      .then(response => {
          if (response.redirected) {
              window.location.href = response.url;
          } else {
              return response.json();
          }
      })
      .then(data => {
          if (data && data.Status === "Error") {
              alert(data.Message || "Something went wrong");
          }
      })
      .catch(error => {
          console.error("Error:", error);
      });
  });
});

  


