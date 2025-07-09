document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("promptForm");
  const loader = document.getElementById("loader");
  const output = document.getElementById("output");
  const input = document.getElementById("modalPrompt");
  const suggestionPills = document.querySelectorAll(".suggestion-pill");

  function showLoader() {
    if (loader) loader.style.display = "inline-block";
  }
  function hideLoader() {
    if (loader) loader.style.display = "none";
  }
  function typeText(text) {
    if (!output) return;
    let index = 0;
    output.textContent = "";
    function type() {
      if (index < text.length) {
        output.textContent += text.charAt(index);
        index++;
        setTimeout(type, 15);
      }
    }
    type();
  }

  async function submitPrompt(prompt) {
    if (!prompt.trim()) return;
    showLoader();
    if (output) output.textContent = "";
    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      hideLoader();
      if (data.output && output) {
        typeText(data.output);
      }
    } catch (err) {
      hideLoader();
      if (output) output.textContent = "Something went wrong. Please try again.";
    }
  }

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (input) submitPrompt(input.value);
    });
  }

  suggestionPills.forEach(pill => {
    pill.addEventListener("click", () => {
      if (input) {
        input.value = pill.textContent;
        submitPrompt(pill.textContent);
      }
    });
  });
});
