<p align="center">
<img src="logo.png"/>
</p>

# Tenable CTF 2021 Writeup
This repository serves as a writeup for Tenable CTF 2021

## The ultimate mutant marvel taem-up

**Category:** Tenable
**Points:** 25
**Description:**

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/_description.PNG"/>
</p>

File: [resources/tenable-25-the_ultimate_mutant_marvel_team_up/Linux_Scan.db](Linux_Scan.db)

### Write-up
In this task, we need  to install Nessus scanner and use it to read the encrypted database, so I've installed its community version (free with a trial version).

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/1.PNG"/>
</p>

In the main page, there was an "Import" button that I've used to upload the Nessus Database "Linux_Scan.db" with the required password.

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/2.PNG"/>
</p>

And that's how we got the scan results called "Linux Scan". When we access this scan:

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/3.PNG"/>
</p>

I tried to search for the flag in the Filter input but I wasn't be able to find it.

But I found something that could be interesting which is the Export button:

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/4.PNG"/>
</p>

We know that the file that we've imported was a Nessus DB but what about the Nessus export?

After I exported the file and I downloaded it I got a text file [resources/tenable-25-the_ultimate_mutant_marvel_team_up/Linux_Scan_uuo914.nessus](Linux_Scan_uuo914.nessus) which contains the flag.

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/5.PNG"/>
</p>

The flag contains an encoded HTML character which is the "'".

So the flag is ``flag{1t's eXt3n51bl3}``.

_____



## Knowledge is knowing a tomato is a fruit

**Category:** Tenable
**Points:** 25
**Description:**

<p align="center">
<img src="resources/tenable-25-knowledge_is_knowing_a_tomato_is_a_fruit/_description.PNG"/>
</p>

File: [resources/tenable-25-the_ultimate_mutant_marvel_team_up/Linux_Scan.db](Linux_Scan.db)

### Write-up
This is the continuity of the previous task.

In this task, I tried to download the scan results for the host `172.26.48.53` using the "Download" link:

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/1.PNG"/>
</p>

I searched for the flag in the downloaded .txt [resources/tenable-25-knowledge_is_knowing_a_tomato_is_a_fruit/kb_172.26.48.53.txt](kb_172.26.48.53.txt) file and I found it:

<p align="center">
<img src="resources/tenable-25-the_ultimate_mutant_marvel_team_up/2.PNG"/>
</p>

So, the flag is ``flag{bu7 n07 putt1ng 1t 1n 4 fru17 s@l4d, th@t5 W1SD0M}``.
___










# Scoreboard

In this CTF, we played as a team ``S3c5murf`` with [Likkrid](https://twitter.com/RidhaBejaoui1) and [v3rlust](https://twitter.com/dal0ul) and we got ranked 100th/1762:

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

The tasks that I've solved
<p align="center">
<img src="scoreboard/me1.PNG"/>
</p>
<p align="center">
<img src="scoreboard/me2.PNG"/>
</p>
<p align="center">
<img src="scoreboard/me3.PNG"/>
</p>
<p align="center">
<img src="scoreboard/me4.PNG"/>
</p>
<p align="center">
<img src="scoreboard/me5.PNG"/>
</p>

All the tasks that we've solved and we didn't solved as a team:
<p align="center">
<img src="scoreboard/tasks1.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks2.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks3.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks4.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks5.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks6.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks7.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks8.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks9.PNG"/>
</p>
<p align="center">
<img src="scoreboard/tasks10.PNG"/>
</p>


CTFTime event: [https://ctftime.org/event/1266](https://ctftime.org/event/1266)
