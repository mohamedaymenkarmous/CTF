const functions = require('firebase-functions');

exports.setResults2020 = functions.https.onCall((data, context) => {
	// make sure the user is a real elector
	if(!context.auth || context.auth.token.email === null || !context.auth.token.email.includes("kuhi.to") || !context.auth.token.email_verified) {
		return {success: false, message: "You're not an elector!"};
	}
	if(data.winner_party !== "The Orange Party") {
		return {success: false, message: "Nope"};
	}
	return {success: true, message: "Good job! The flag is: " + functions.config().the.flag};
});
