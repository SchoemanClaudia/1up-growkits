document.addEventListener("DOMContentLoaded", function () {
    const deleteCheckboxes = document.querySelectorAll("input[type='checkbox'][id$='-DELETE']");

    deleteCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function (e) {
            if (checkbox.checked) {
                const confirmed = confirm("Are you sure you want to delete this item from the order?");
                if (!confirmed) {
                    checkbox.checked = false;
                }
            }
        });
    });
});
