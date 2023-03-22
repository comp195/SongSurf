function updateSearchLabel(label) {
    document.getElementById("search_label").textContent = label;
  }

  function hideAdditionalBoxes() {
    document.getElementById("additional_box_1").style.display = "none";
    document.getElementById("additional_box_2").style.display = "none";
    document.getElementById("additional_box_3").style.display = "none";
  }

  function showAdditionalBoxes(count) {
    for (let i = 1; i <= count; i++) {
      document.getElementById("additional_box_" + i).style.display = "list-item";
    }
  }