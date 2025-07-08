document.getElementById("searchInput").addEventListener("input", function () {
  const query = this.value.toLowerCase();
  const items = document.querySelectorAll("#resultsList li");
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? "block" : "none";
  });
});