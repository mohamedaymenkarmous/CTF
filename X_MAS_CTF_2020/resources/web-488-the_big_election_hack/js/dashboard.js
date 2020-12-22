function changeResults() {
	/*Deleted to preserve space */
}


function loadData() {
	var db = firebase.firestore();
	db.collection("stats").doc("election-2020").get().then((doc) => {
		document.getElementById("winner-here").innerHTML = doc.data()["winner"];
		document.getElementById("winner-party-here").innerHTML = doc.data()["winner_party"];
	});
}


firebase.auth().onAuthStateChanged((user) => {
	if(user) {
		loadData();
	} else {
	}
});