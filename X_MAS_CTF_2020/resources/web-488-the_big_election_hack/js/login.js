function login() {
	var email = document.getElementById('email').value;
	var password = document.getElementById('pass').value;
	firebase.auth().signInWithEmailAndPassword(email, password).catch((error) => {
		alert(error.message);
		console.log(error.message);
  	});
}

firebase.auth().onAuthStateChanged((user) => {
	if(user) {
		document.location.href = "/dashboard.html";
	}
});