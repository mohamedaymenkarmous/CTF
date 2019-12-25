function generateRandom (length) {
	var result = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	var charactersLength = characters.length;

	for (var i = 0; i < length; i++)
		result += characters.charAt (Math.floor (Math.random () * charactersLength));

	return result;
}

function vote (id, upvote) {
	var xhttp = new XMLHttpRequest ();
	xhttp.open ("GET", "/vote.php?g=1", false);
	xhttp.send ();
	var work = xhttp.responseText;

	var statusElement = document.getElementById ("status");
	statusElement.className = "status";
	statusElement.innerText = "CPU Voting on Idea #" + id + " ...";

	var found = false;
	while (!found) {
		var randomLength = Math.floor (7 + Math.random () * 18);
		var stringGen = generateRandom (randomLength);
		var md5Gen = md5 ("watch__bisqwit__" + stringGen);

		if (md5Gen.substring (0, work.length).localeCompare (work) === 0) {
			var url = "/vote.php?id=" + id + "&h=" + stringGen;
			if (upvote === 1)
				url += "&u=1";

			xhttp.open ("GET", url, false);
			xhttp.send ();
			found = true;
		}
	}

	location.href = "/";
}