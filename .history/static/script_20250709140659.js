document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("promptForm");
  const loader = document.getElementById("loader");
  const output = document.getElementById("output");

  if (form) {
    form.addEventListener("submit", () => {
      loader.style.display = "inline-block";
    });
  }

  if (typeof content !== "undefined" && output) {
    let index = 0;
    const typeText = () => {
      if (index < content.length) {
        output.textContent += content.charAt(index);
        index++;
        setTimeout(typeText, 15);
      }
    };
    output.textContent = "";
    typeText();
  }
});
