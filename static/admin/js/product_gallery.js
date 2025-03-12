document.addEventListener("DOMContentLoaded", function () {
    let uploadField = document.createElement("input");
    uploadField.type = "file";
    uploadField.multiple = true;
    uploadField.accept = "image/*";
    uploadField.style.display = "none";

    let button = document.createElement("button");
    button.textContent = "Upload Multiple Images";
    button.type = "button";
    button.classList.add("button");

    button.addEventListener("click", function () {
        uploadField.click();
    });

    uploadField.addEventListener("change", function (event) {
        let files = event.target.files;
        if (files.length > 0) {
            let formData = new FormData();
            let productId = document.querySelector("#id_name").value;

            formData.append("product_id", productId);
            for (let i = 0; i < files.length; i++) {
                formData.append("images", files[i]);
            }

            fetch("/admin/shop/product/upload-multiple-images/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.reload();
            })
            .catch(error => console.error("Error:", error));
        }
    });

    let fieldset = document.querySelector(".inline-group");
    if (fieldset) {
        fieldset.appendChild(button);
        fieldset.appendChild(uploadField);
    }
});
