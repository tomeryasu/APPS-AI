gdocument.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("promptForm");
  const loader = document.getElementById("loader");
  const output = document.getElementById("output");
  const input = document.getElementById("modalPrompt");
  const suggestionPills = document.querySelectorAll(".suggestion-pill");

  // Create or get the download button
  let downloadBtn = document.getElementById("downloadBtn");
  if (!downloadBtn) {
    downloadBtn = document.createElement("a");
    downloadBtn.id = "downloadBtn";
    downloadBtn.style.display = "none";
    downloadBtn.textContent = "Download your app";
    downloadBtn.className = "nav-btn";
    downloadBtn.style.marginTop = "24px";
    if (output && output.parentNode) {
      output.parentNode.appendChild(downloadBtn);
    } else {
      document.body.appendChild(downloadBtn);
    }
  }

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
    downloadBtn.style.display = "none";
    try {
      // 1. Get AI output
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      hideLoader();
      if (data.output && output) {
        typeText(data.output);
      }
      // 2. Build app and show download link
      const buildRes = await fetch("/build", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const buildData = await buildRes.json();
      if (buildData.download_url) {
        downloadBtn.href = buildData.download_url;
        downloadBtn.style.display = "inline-block";
        downloadBtn.setAttribute("download", "");
      }
    } catch (err) {
      hideLoader();
      if (output)
        output.textContent = "Something went wrong. Please try again.";
      downloadBtn.style.display = "none";
    }
  }

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (input) submitPrompt(input.value);
    });
  }

  suggestionPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      if (input) {
        input.value = pill.textContent;
        submitPrompt(pill.textContent);
      }
    });
  });
});
