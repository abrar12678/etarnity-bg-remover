document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");
    const menuIcon = document.getElementById("menuIcon");
    const closeIcon = document.getElementById("closeIcon");
    const fileInput = document.getElementById("signatureInput");
    const livePreview = document.getElementById("livePreview");
    const livePreviewContainer = document.getElementById("livePreviewContainer");
    const dropZone = document.getElementById("dropZone");
    const modeSelect = document.getElementById("modeSelect");
    const colorPickerWrapper = document.getElementById("colorPickerWrapper");

    if (menuToggle && mobileMenu && menuIcon && closeIcon) {
        function openMobileMenu() {
            mobileMenu.classList.remove("max-h-0", "grid-rows-[0fr]", "opacity-0", "-translate-y-2");
            mobileMenu.classList.add("mt-4", "max-h-96", "grid-rows-[1fr]", "opacity-100", "translate-y-0");

            menuIcon.classList.add("hidden");
            closeIcon.classList.remove("hidden");
        }

        function closeMobileMenu() {
            mobileMenu.classList.remove("mt-4", "max-h-96", "grid-rows-[1fr]", "opacity-100", "translate-y-0");
            mobileMenu.classList.add("max-h-0", "grid-rows-[0fr]", "opacity-0", "-translate-y-2");

            menuIcon.classList.remove("hidden");
            closeIcon.classList.add("hidden");
        }

        menuToggle.addEventListener("click", function () {
            const isClosed = mobileMenu.classList.contains("max-h-0");

            if (isClosed) {
                openMobileMenu();
            } else {
                closeMobileMenu();
            }
        });

        mobileMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", function () {
                closeMobileMenu();
            });
        });
    }

    if (fileInput && livePreview && livePreviewContainer) {
        fileInput.addEventListener("change", function () {
            const file = this.files && this.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (e) {
                livePreview.src = e.target.result;
                livePreviewContainer.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        });
    }

    if (dropZone && fileInput) {
        ["dragenter", "dragover"].forEach((eventName) => {
            dropZone.addEventListener(eventName, function (e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add("border-orange-500", "bg-orange-50");
            });
        });

        ["dragleave", "drop"].forEach((eventName) => {
            dropZone.addEventListener(eventName, function (e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove("border-orange-500", "bg-orange-50");
            });
        });

        dropZone.addEventListener("drop", function (e) {
            const files = e.dataTransfer.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                const event = new Event("change", { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        });
    }

    function toggleColorPicker() {
        if (!modeSelect || !colorPickerWrapper) return;

        if (modeSelect.value === "logo") {
            colorPickerWrapper.classList.remove("hidden");
        } else {
            colorPickerWrapper.classList.add("hidden");
        }
    }

    if (modeSelect) {
        modeSelect.addEventListener("change", toggleColorPicker);
        toggleColorPicker();
    }
});