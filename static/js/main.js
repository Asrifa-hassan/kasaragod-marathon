// Small progressive enhancement: update selected race option styling.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".race-option input").forEach((radio) => {
    radio.addEventListener("change", () => {
      document.querySelectorAll(".race-option").forEach((card) => card.classList.remove("selected"));
      radio.closest(".race-option")?.classList.add("selected");
    });
  });
});
