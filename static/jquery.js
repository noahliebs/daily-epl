function showList(input) {
	var datalist = document.querySelector("datalist");
	if (input.value) {
		datalist.id = "players";
	} else {
		datalist.id = "";			
	}
}

function toggleInstructions(id) {
    var div = document.getElementById(id);
    div.style.display = div.style.display == "none" ? "block" : "none";
}