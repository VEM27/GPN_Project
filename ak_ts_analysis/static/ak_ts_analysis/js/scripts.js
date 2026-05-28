

document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Убираем active со всех
      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(content => content.style.display = "none");

      // Активируем нужную
      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      document.getElementById(target).style.display = "block";
    });
  });
});

document.getElementById("arrowBtn").addEventListener("click", function () {

    const viewer = document.getElementById("pdfViewer");
    const arrowImg = this.querySelector("img");
    const rightContainer = document.getElementById("right");
    const leftContainer = document.getElementById("left");

    if (viewer.style.display === "none") {
      viewer.style.display = "block";
      arrowImg.classList.remove("rotate-left");
      arrowImg.classList.add("rotate-right");
    } else {
      viewer.style.display = "none";
      arrowImg.classList.remove("rotate-right");
      arrowImg.classList.add("rotate-left");
    }


    if (rightContainer.style.width === "50%" || rightContainer.style.width === "") {
      leftContainer.style.width = "100%";
      rightContainer.style.padding = "5px";
      rightContainer.style.width = "10px";
    } else {
      rightContainer.style.width = "50%";
      rightContainer.style.padding = "10px";
      leftContainer.style.width = "50%";
    }

  });
