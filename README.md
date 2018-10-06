MySQL Database Schemas/Structures Comparison Script based on <b>'Python'</b> language.

<b>Script Compare : </b>
1) Table Attributes
2) Table Structure [Column data-type / definition, indexes, foreign keys constraints]
3) Table Columns
4) Table Indexes
5) Table Foreign Key Constraints
6) Table Triggers
7) DB Routine / Event / Procedure / Function
8) DB Views
9) Above All Options

<b>Script Benefits : </b>
1) User-friendly
2) Eliminate mistakes
3) Deploy changes from dev, to test, to production
4) Find and fix errors caused by differences between databases
5) Generate SQL scripts that can be manually edited before running
6) Speed up the deployment of new database schema updates
7) DB schemas can synchronize between local to local, local to remote, remote to remote.

<b>Check Sample Videos on Youtube Link :</b> https://www.youtube.com/channel/UC30lKncvpa8kKtPsIE3WrrQ

If you like videos then please share it to your friends too. 
If you / your friends want to use / run this script then put your email id in comment box. I'll share the installation and procedure steps.
Don't forget to Like or Subscribe to my youtube channel to get more videos.

<b>Installation process on ubuntu OS version <= 14 : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql version <= 5.5) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-lamp-on-ubuntu-14-04-quickstart
2) Install <b>'Python'</b> version 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pip <br>
3) Install python <b>'PyMySQL'</b> for python version 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update  <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pymysql <br>
4) Create <b>'bin'</b> folder in your home directory level & set 774 permission to <b>'bin'</b> created folder recursively.
5) Copy mysql diff db script for python version 2.7 into <b>'bin'</b> directory.
   <b>File name :</b> diffDB2.py <br>
6) Open terminal and goto created <b>bin</b> directory level. Type <b>'diffDB2.py'</b> and press <b>'ENTER'</b> button. <br>
7) Go ahead steps-wise with script.

<b>Installation process on ubuntu OS version 18.0 : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql version >= 5.7) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04
2) After installed mysql and phpmyadmin. <br>
   Remove 'ONLY Full Group BY' option permanently. <Br>
   Remove 'zero in default date' & 'zero in default datetime' option permanently.
3) Install <b>'Python'</b> version <= 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pip <br>
4) Install python <b>'PyMySQL'</b> for python version <= 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update  <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to <b>'bin'</b> created folder recursively.
6) Copy mysql diff db script for python version <= 2.7 into <b>'bin'</b> directory.
   <b>File name :</b> diffDB2.py
7) Open terminal and go to home directory level only. Type <b>'diffDB2.py'</b> and press <b>'ENTER'</b> button.
8) Now follow step-wise <b>'diffDB2.py'</b> script procedure for MYSQL DB schemas comparsion.

<b>Installation process on ubuntu OS version 18.0 : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql version >= 5.7) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04
2) After installed mysql and phpmyadmin. <br>
   Remove 'ONLY Full Group BY' option permanently. <Br>
   Remove 'zero in default date' & 'zero in default datetime' option permanently.
3) Install <b>'Python'</b> version >= 3.0 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python3.6 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python3-pip <br>
4) Install python <b>'PyMySQL'</b> for python version >= 3.0 <br>
   <b>Run command via terminal :</b> sudo apt-get update  <br>
   <b>Run command via terminal :</b> sudo apt-get install python3-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to <b>'bin'</b> created folder recursively.
6) Copy mysql diff db script for python version >= 3.6 into <b>'bin'</b> directory.
   <b>File name :</b> diffDB3.py
7) Open terminal and go to home directory level only. Type <b>'diffDB3.py'</b> and press <b>'ENTER'</b> button.
8) Now follow step-wise <b>'diffDB3.py'</b> script procedure for MYSQL DB schemas comparsion.

<b>Installation process on linux/debian OS version 9 : </b>

1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   Link : https://www.linuxbabe.com/debian/install-lamp-stack-debian-9-stretch <br>
2) Install phpmyadmin <br>
   <b>Run command via terminal :</b> sudo apt-get install phpmyadmin <br>
   <b>Link : </b> https://www.youtube.com/watch?v=p08xghuzBwc <br>
3) Install <b>'Python'</b> version <= 2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update  <br>
   <b>Run command via terminal : </b> sudo apt-get install python-pip  <br>
4) Install python <b>'PyMySQL'</b> for python version <= 2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to <b>'bin'</b> created folder recursively. <br>
6) Copy mysql diff db script for python version <= 2.7 into 'bin' directory. <br>
   <b>File name : </b> diffDB2.py <br>
7) Open terminal and go to home directory level only. <br>
8) Goto <b>'bin'</b> directory level & press 'ENTER' button <br>
9) Type <b>'python diffDB2.py'</b> and press 'ENTER' button. <br>
10) Now follow step-wise 'diffDB2.py' script procedure for MYSQL DB schemas comparsion.

<b>Installation process on linux/debian OS version 9 : </b>

1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   Link : https://www.linuxbabe.com/debian/install-lamp-stack-debian-9-stretch <br>
2) Install phpmyadmin <br>
   <b>Run command via terminal :</b> sudo apt-get install phpmyadmin <br>
   <b>Link : </b> https://www.youtube.com/watch?v=p08xghuzBwc <br>
3) Install <b>'Python'</b> version >= 3.0 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python3.6 <br>
   <b>Run command via terminal : </b> sudo apt-get update  <br>
   <b>Run command via terminal : </b> sudo apt-get install python3-pip  <br>
4) Install python <b>'PyMySQL'</b> for python version >= 3.0 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python3-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to <b>'bin'</b> created folder recursively. <br>
6) Copy mysql diff db script for python version >= 3.0 into 'bin' directory. <br>
   <b>File name : </b> diffDB3.py <br>
7) Open terminal and go to home directory level only. <br>
8) Goto <b>'bin'</b> directory level & press 'ENTER' button <br>
9) Type <b>'python diffDB3.py'</b> and press 'ENTER' button. <br>
10) Now follow step-wise <b>'diffDB3.py'</b> script procedure for MYSQL DB schemas comparsion.

<b>Installation process on windows OS version 10 : </b>
1) Install <b>'XAMPP'</b> <br>
   Link : https://pureinfotech.com/install-xampp-windows-10/
2) Install <b>'Python'</b> version <= 2.7 only <br>
   Link : https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a
3) Open command prompt and Goto directory <b>'c:/python27/script'</b> and press <b>'ENTER'</b> button
4) Type this  <b>'pip install pymysql'</b> command and press <b>'ENTER'</b> button
5) Start <b>'XAMPP'</b> server
6) Copy mysql diff db script for python version <= 2.7 into your <b>'Downloads'</b> directory <br>
   <b>File name :</b> diffDB2.py
7) Open command prompt and goto <b>'Downloads'</b> directory and type <b>'diffDB2.py'</b> command and press <b>'ENTER'</b> button
8) Now follow step-wise <b>'diffDB2.py'</b> script procedure for MYSQL DB schemas comparsion.

<b>Installation process on windows OS version 10 : </b>
1) Install <b>'XAMPP'</b> <br>
   Link : https://pureinfotech.com/install-xampp-windows-10/
2) Install <b>'Python'</b> version >= 3.6 only <br>
   Link : https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a
3) Open command prompt and Goto directory <b>'c:/python36/script'</b> and press <b>'ENTER'</b> button
4) Type this  <b>'pip install pymysql'</b> command and press <b>'ENTER'</b> button
5) Start <b>'XAMPP'</b> server
6) Copy mysql diff db script for python version >= 3.6 into your <b>'Downloads'</b> directory <br>
   <b>File name :</b> diffDB3.py
7) Open command prompt and goto <b>'Downloads'</b> directory and type <b>'diffDB3.py'</b> command and press <b>'ENTER'</b> button
8) Now follow step-wise <b>'diffDB3.py'</b> script procedure for MYSQL DB schemas comparsion.

<b>Any suggestions, improvements, facing issues etc. Contact on given below details.</b> <br>
Author Name : Chirag D Jain <br>
Mobile & What's App : 91+ 9975967186 <br>
Email : chirag.jain@digitaledu.net <br>
Country : India <br>
