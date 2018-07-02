<p align="center">
<img src="logo.png"/>
</p>

# Carthage Cyber Arena Finals 2018 Writeup
This repository serves as a writeup for Carthage Cyber Arena Finals which are solved by The Emperors team

## Sockpuppet

**Category:** Forensics, Log Analysis, Event Correlation
**Points:** 4
**Description:**

>Our twitter account manager received threatening direct messages from one of our follower, he did not answer or repport the issue until we found him dead in his car. The account was unactive for days, and appears to represent a fake identity.

>We belive you can help the authorities to  solve  this  case. By crawling the twitter account we found two tweets  linking our website. We provide you the  links  and  our  website  log  file during these tweets dates. We expect you to provide us with  the suspected ip address signature along with the latest timestamp.

>Example: CCA{307254cdb562c5e55a54a32d3078fca2-1262389554273517}

>* TWEET#1

>  DATETIME: 2010-01-01T09:19:48.324566

>  HOST: 7bcf4a5537c0191a69cb51f8319938e7.host

>  PATH: 40a23d02813a2feb174b43a9a9dbc423.path

>* TWEET#2

>  DATETIME: 2010-01-01T16:12:10.430003

>  HOST: 7bcf4a5537c0191a69cb51f8319938e7.host

>  PATH: f2bbb5b05a7b92b1d41cfa7716c3e810.path

>* LOG FILE

>  [sockpuppet.7z](resources/forensics-4-sockpuppet/sockpuppet.7z)

>Notice

> - SOME CRITICAL INFORMATIONS ARE SIGNED USING MD5HMAC

>   AND PADDED WITH A DOT THAN THE DATA CATEGORY.

> - ALL DATES ARE SHIFTED TO UTC TIME ZONE



### Write-up
In this task, we have to find which ip visit the website through the host, the path1 and the path2 as described in the description.

So first, we should extract the common IPs in the log file usings these information:

```
path1="40a23d02813a2feb174b43a9a9dbc423.path"
path2="f2bbb5b05a7b92b1d41cfa7716c3e810.path"
comm -12 <(cat sockpuppet | grep $path1 | cut -d' ' -f1 | sort | uniq) <(cat sockpuppet | grep $pat2 | cut -d' ' -f1 | sort | uniq) | sort | uniq
```

Output:

```
08d033ed2123e11257e71e39d8f2b4b1.ip
23fba2bb6af39b23fdac3134fb1ed7b1.ip
49da60aeba8fcfcba2913bdef0de464d.ip
4ad69299d0d19032d3ea9be8f088aebe.ip
6400be853eb7473314b122610caad8b0.ip
66ab10232318b822603bd2a3fbf42457.ip
7021b220bacaf7fcd532487b32636702.ip
8fa644ff6432092c5649007a0131e59d.ip
9e6fab2f88b869eb6c8e7eb12ee037e8.ip
bb52d580383d528a9d6deb353951ec11.ip
d9c58d1a14511f560b53af75ffc671bb.ip
e1a4de585f55c7add5d66714e98ab309.ip
ef401264dfe3e6546bc178f23ed18eef.ip
ff0b685e14820409660087abc1a90636.ip
```

So, we got 14 suspected IPs.

Since the flag is in this format: `CCA{IPAddress-Timestamp}`, we should convert the Datetime for the suspected line from UTC Date to the Unix Timestamp. The biggest mistake is to convert that Datetime from Local Time (not UTC).

But in my Linux distribution, I can easily convert a datetime from Local date to Unix Timestand and then I add 1 hour (from Tunisia) to get a correct timestamp.

A tryharder person will try to validate this task using 14 flags from the 14 IPs and that's so easy:

```
ips=$(comm -12 <(cat sockpuppet | grep "40a23d02813a2feb174b43a9a9dbc423.path" | cut -d' ' -f1 | sort | uniq) <(cat sockpuppet | grep "f2bbb5b05a7b92b1d41cfa7716c3e810.path" | cut -d' ' -f1 | sort | uniq) | sort | uniq
for ip in $ips; do echo "CCA{"$(echo $ip | sed -r 's/\.ip//g')-$(expr $(date -d "$(cat sockpuppet | grep $ip | grep -E "40a23d02813a2feb174b43a9a9dbc423.path|f2bbb5b05a7b92b1d41cfa7716c3e810.path" | tail -n1 | cut -d' ' -f3 | sed -r 's/\[//g' | sed -r 's/\]//g' )" +%s) + 0)$(cat sockpuppet | grep $ip | grep -E "40a23d02813a2feb174b43a9a9dbc423.path|f2bbb5b05a7b92b1d41cfa7716c3e810.path" | tail -n1 | cut -d' ' -f3 | sed -r 's/\[//g' | sed -r 's/\]//g' | cut -d'.' -f2)"}"; done
```

Output:

```
CCA{08d033ed2123e11257e71e39d8f2b4b1-1262386592782796}
CCA{23fba2bb6af39b23fdac3134fb1ed7b1-1262385970594141}
CCA{49da60aeba8fcfcba2913bdef0de464d-1262386194689380}
CCA{4ad69299d0d19032d3ea9be8f088aebe-1262386350697372}
CCA{6400be853eb7473314b122610caad8b0-1262365522572331}
CCA{66ab10232318b822603bd2a3fbf42457-1262342805884942}
CCA{7021b220bacaf7fcd532487b32636702-1262385307261268}
CCA{8fa644ff6432092c5649007a0131e59d-1262386054757994}
CCA{9e6fab2f88b869eb6c8e7eb12ee037e8-1262372081750348}
CCA{bb52d580383d528a9d6deb353951ec11-1262369249442483}
CCA{d9c58d1a14511f560b53af75ffc671bb-1262352527685386}
CCA{e1a4de585f55c7add5d66714e98ab309-1262357753571165}
CCA{ef401264dfe3e6546bc178f23ed18eef-1262376641957029}
CCA{ff0b685e14820409660087abc1a90636-1262375200733461}
```

So the flag is in that list.

But we will explain how really we should get the flag.

If we look to the logs of these IPs, we will find that there is 2 IPs that are accessing to the website from an X11 forwarding browser using a "Mozilla/5.0 (X11; Linux x86_64)" browser and that's enough to be suspected.

Now, we got 2 suspected IPs and for me that's enough to start validating one of the 2 flags.

The given logs of the real suspected IP is :

```
ip=e1a4de585f55c7add5d66714e98ab309.ip
cat sockpuppet | grep $ip

e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T07:54:01.492523] "GET 40a23d02813a2feb174b43a9a9dbc423.path HTTP/1.1" 200 10908 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T07:54:01.507292] "GET a5bade6b2f6f8ccc8eb0b913bfe35440.path HTTP/1.1" 200 6188 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T07:54:01.585604] "GET f2e230e0d1bc6fa4961d8beec2a68b38.path HTTP/1.1" 200 9087 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T07:54:01.589038] "GET 51df09fdc589bafbc5a611840bfdde2a.path HTTP/1.1" 200 14880 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.571165] "GET f2bbb5b05a7b92b1d41cfa7716c3e810.path HTTP/1.1" 200 3567 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.586660] "GET a5bade6b2f6f8ccc8eb0b913bfe35440.path HTTP/1.1" 200 6188 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.591763] "GET 82480d55fcf3c5fb265b5fc49b47cfac.path HTTP/1.1" 200 9848 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.665622] "GET 51df09fdc589bafbc5a611840bfdde2a.path HTTP/1.1" 200 14880 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.671838] "GET d6ac4a761d9ee82c68f3ee088fde51c3.path HTTP/1.1" 200 15005 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T23:18:17.313985] "GET 0828fab382438fae63425e597a22800c.path HTTP/1.1" 200 10153 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
```

So, the path1 and path2 have been visited exists in this logs:

```
ip=e1a4de585f55c7add5d66714e98ab309.ip
cat sockpuppet | grep $ip | grep -E "40a23d02813a2feb174b43a9a9dbc423.path|f2bbb5b05a7b92b1d41cfa7716c3e810.path"

e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T07:54:01.492523] "GET 40a23d02813a2feb174b43a9a9dbc423.path HTTP/1.1" 200 10908 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
e1a4de585f55c7add5d66714e98ab309.ip 7bcf4a5537c0191a69cb51f8319938e7.host [2010-01-01T15:55:53.571165] "GET f2bbb5b05a7b92b1d41cfa7716c3e810.path HTTP/1.1" 200 3567 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"
```

Finally the flag is ``CCA{e1a4de585f55c7add5d66714e98ab309-1262357753571165}``.











# Scoreboard

This is the scoreboard and the ranking for the first 13 teams in this CTF :

Summary:

<p align="center">
<img src="scoreboard/ALL.PNG"/>
</p>

Tasks:

<p align="center">
<img src="scoreboard/1.PNG"/>
</p>

