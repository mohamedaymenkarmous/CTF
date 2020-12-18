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

CTFTime event: [https://ctftime.org/event/1209](https://ctftime.org/event/1209)
