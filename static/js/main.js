// main.js
document.addEventListener("DOMContentLoaded", function () {
    var submenuCategories = document.querySelectorAll(".main-nav .submenu a");

    submenuCategories.forEach(function (categoryLink) {
        categoryLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = this.getAttribute("href"); // Redirect to the selected category page
        });
    });
});
