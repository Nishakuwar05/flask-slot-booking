function toggleDropdown() {
    let dropdown = document.getElementById("dropdownMenu");
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "flex";
    } else {
        dropdown.style.display = "none";
    }
}

// Close dropdown when clicking outside
document.addEventListener("click", function(event) {
    let menuBtn = document.querySelector(".menu-btn");
    let dropdown = document.getElementById("dropdownMenu");

    if (!menuBtn.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = "none";
    }
});