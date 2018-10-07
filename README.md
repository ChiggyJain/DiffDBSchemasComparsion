<b>MySQL Database Schemas/Structures Comparison Script based on 'Python' language.</b>

<b>Usecase :</b>
Usecase :
A) <b>'db_master1'</b> database is your perfect database which covered schemas & structures like tables, indexes, foreign keys, triggers, routines etc. as per product requirements. <br>
B) <b>'db_testing1'</b> database is your raw database which covered schemas like tables, indexes, foreign keys, triggers, routines etc. as per product requirements, but raw <b>'db_testing1'</b> database is missing some schemas as compared to perfect <b>'db_master1'</b> database due to some reasons. <br>
   <b>Missing schemas on raw 'db_testing1' database might be :</b> <br>
   1) New columns on existing tables <br>
   2) Need to change existing columns definition on existing tables <br>
   3) Need to change existing columns datatype on existing tables <br>
   4) New tables on existing database <br>
   5) New indexes on existing tables <br>
   6) Need to change existing indexes definition on existing tables <br>
   7) New triggers on existing tables <br>
   8) Need to change existing triggers definition on existing tables <br>
   9) New functions/routines/events on database <br>
   10) Need to change existing functions/routines/events definition on database <br>
   11) New views on database <br>
   12) Need to change existing views definition on database <br>
   
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

<b>Installation process on ubuntu OS version <= 14 [for python2.7] : </b>
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
5) Copy script for python version 2.7 into created <b>'bin'</b> directory. <br>
   <b>Download file name :</b> diffDB2.py <br>
6) Open terminal and goto created <b>bin</b> directory level. Type <b>'diffDB2.py'</b> and press <b>'ENTER'</b> button. <br>
7) Go ahead steps-wise with script.

<b>Installation process on ubuntu OS version 18.0 [for python2.7] : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql version >= 5.7) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04
2) After installed mysql and phpmyadmin. <br>
   Remove 'ONLY Full Group BY' option permanently. <Br>
   Remove 'zero in default date' & 'zero in default datetime' option permanently.
3) Install <b>'Python'</b> version 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pip <br>
4) Install python <b>'PyMySQL'</b> for python version 2.7 <br>
   <b>Run command via terminal :</b> sudo apt-get update  <br>
   <b>Run command via terminal :</b> sudo apt-get install python-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively.
6) Copy script for python version 2.7 into created <b>'bin'</b> directory.
   <b>Download file name :</b> diffDB2.py <br>
7) Open terminal and goto created <b>bin</b> directory level. Type <b>'diffDB2.py'</b> and press <b>'ENTER'</b> button. <br>
8) Go ahead steps-wise with script.

<b>Installation process on ubuntu OS version 18.0 [for python3.6]: </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql version >= 5.7) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04
2) After installed mysql and phpmyadmin. <br>
   Remove 'ONLY Full Group BY' option permanently. <Br>
   Remove 'zero in default date' & 'zero in default datetime' option permanently.
3) Install <b>'Python'</b> version 3.6 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python3.6 <br>
   <b>Run command via terminal :</b> sudo apt-get update <br>
   <b>Run command via terminal :</b> sudo apt-get install python3-pip <br>
4) Install python <b>'PyMySQL'</b> for python version 3.6 <br>
   <b>Run command via terminal :</b> sudo apt-get update  <br>
   <b>Run command via terminal :</b> sudo apt-get install python3-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively.
6) Copy script for python version 3.6 into created <b>'bin'</b> directory.
   <b>Download file name :</b> diffDB3.py <br>
7) Open terminal and goto created <b>bin</b> directory level. Type <b>'diffDB3.py'</b> and press <b>'ENTER'</b> button. <br>
8) Go ahead steps-wise with script.

<b>Installation process on linux/debian OS version 9 [for python2.7] : </b>

1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   Link : https://www.linuxbabe.com/debian/install-lamp-stack-debian-9-stretch <br>
2) Install phpmyadmin <br>
   <b>Run command via terminal :</b> sudo apt-get install phpmyadmin <br>
   <b>Link : </b> https://www.youtube.com/watch?v=p08xghuzBwc <br>
3) Install <b>'Python'</b> version 2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update  <br>
   <b>Run command via terminal : </b> sudo apt-get install python-pip  <br>
4) Install python <b>'PyMySQL'</b> for python version 2.7 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively. <br>
6) Copy script for python version 2.7 into created <b>'bin'</b> directory. <br>
   <b>Download file name :</b> diffDB2.py <br>
7) Open terminal and goto created <b>'bin'</b> directory & press <b>'ENTER'</b> button. <br>
8) Type <b>'python diffDB2.py'</b> and press <b>'ENTER'</b> button. <br>
9) Go ahead steps-wise with script.

<b>Installation process on linux/debian OS version 9 [for python3.6] : </b>

1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   Link : https://www.linuxbabe.com/debian/install-lamp-stack-debian-9-stretch <br>
2) Install phpmyadmin <br>
   <b>Run command via terminal :</b> sudo apt-get install phpmyadmin <br>
   <b>Link : </b> https://www.youtube.com/watch?v=p08xghuzBwc <br>
3) Install <b>'Python'</b> version 3.6 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python3.6 <br>
   <b>Run command via terminal : </b> sudo apt-get update  <br>
   <b>Run command via terminal : </b> sudo apt-get install python3-pip  <br>
4) Install python <b>'PyMySQL'</b> for python version 3.6 <br>
   <b>Run command via terminal : </b> sudo apt-get update <br>
   <b>Run command via terminal : </b> sudo apt-get install python3-pymysql <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively. <br>
6) Copy script for python version 3.6 into created <b>'bin'</b> directory. <br>
   <b>Download file name :</b> diffDB3.py <br>
7) Open terminal and goto created <b>'bin'</b> directory & press <b>'ENTER'</b> button. <br>
8) Type <b>'python3 diffDB3.py'</b> and press <b>'ENTER'</b> button. <br>
9) Go ahead steps-wise with script.

<b>Installation process on centos OS version 6 [for python2.7] : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-centos-6
2) Install <b>'Python'</b> version 2.7 <br>
   <b>Link :</b> https://tecadmin.net/install-python-2-7-on-centos-rhel/
3) Install <b>'Pip'</b> for python version 2.7 <br>
   <b>Run command via terminal :</b> curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"  <br>
   <b>Run command via terminal :</b> python2.7 get-pip.py --user <br>
4) Install python <b>'PyMySQL'</b> for python version 2.7 <br>
   <b>Link : </b> https://unix.stackexchange.com/questions/254294/make-python-2-7-the-default-python-in-centos-making-an-alias-didnt-work 
   <b>Run command via terminal :</b> sudo rm -r /usr/bin/python  <br>
   <b>Run command via terminal :</b> sudo ln -s /usr/local/bin/python2.7 /usr/bin/python <br>
   <b>Run command via terminal :</b> pip install pymysql --user <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively. <br>
5) Copy script for python version 2.7 into created <b>'bin'</b> directory. <br>
   <b>Download file name :</b> diffDB2.py <br>
6) Open terminal and goto created <b>bin</b> directory level. Type <b>'python2.7 diffDB2.py'</b> and press <b>'ENTER'</b> button. <br>
7) Go ahead steps-wise with script.


<b>Installation process on centos OS version 6 [for python3.6] : </b>
1) Install <b>'Lampstack'</b> i.e (php, apache2, mysql) <br>
   <b>Link :</b> https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-centos-6
2) Install <b>'Python'</b> version 2.7 <br>
   <b>Link :</b> https://tecadmin.net/install-python-3-6-on-centos/
   <b>Link :</b> https://danieleriksson.net/2017/02/08/how-to-install-latest-python-on-centos/
3) Install <b>'Pip'</b> for python version 3.6 <br>
   <b>Run command via terminal :</b> wget https://bootstrap.pypa.io/get-pip.py  <br>
   <b>Run command via terminal :</b> python3.6 get-pip.py --user <br>
4) Install python <b>'PyMySQL'</b> for python version 2.7 <br>
   <b>Link : </b> https://unix.stackexchange.com/questions/254294/make-python-2-7-the-default-python-in-centos-making-an-alias-didnt-work 
   <b>Run command via terminal :</b> sudo rm -r /usr/bin/python  <br>
   <b>Run command via terminal :</b> sudo ln -s /usr/local/bin/python3.6 /usr/bin/python <br>
   <b>Run command via terminal :</b> pip3.6 install pymysql --user <br>
5) Create <b>'bin'</b> folder in your home directory level & set 774 permission to created <b>'bin'</b> folder recursively. <br>
5) Copy script for python version 3.6 into created <b>'bin'</b> directory. <br>
   <b>Download file name :</b> diffDB3.py <br>
6) Open terminal and goto created <b>bin</b> directory level. Type <b>'python3.6 diffDB3.py'</b> and press <b>'ENTER'</b> button. <br>
7) Go ahead steps-wise with script.

<b>Installation process on windows OS version 10 [for python2.7] : </b>
1) Install <b>'XAMPP'</b> <br>
   Link : https://pureinfotech.com/install-xampp-windows-10/
2) Install <b>'Python'</b> version 2.7 <br>
   Link : https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a
3) Open command prompt and Goto directory <b>'c:/python27/script'</b> and press <b>'ENTER'</b> button
4) Type this <b>'pip install pymysql'</b> command and press <b>'ENTER'</b> button
5) Start <b>'XAMPP'</b> server
6) Copy mysql diff db script for python version 2.7 into your <b>'Downloads'</b> directory <br>
   <b>Download file name :</b> diffDB2.py <br>
7) Open command prompt and goto <b>'Downloads'</b> directory and type <b>'diffDB2.py'</b> command and press <b>'ENTER'</b> button
8) Go ahead steps-wise with script.

<b>Installation process on windows OS version 10 [for python3.6] : </b>
1) Install <b>'XAMPP'</b> <br>
   Link : https://pureinfotech.com/install-xampp-windows-10/
2) Install <b>'Python'</b> version3.6 <br>
   Link : https://datascience.com.co/how-to-install-python-2-7-and-3-6-in-windows-10-add-python-path-281e7eae62a
3) Open command prompt and Goto directory <b>'c:/python36/script'</b> and press <b>'ENTER'</b> button
4) Type this  <b>'pip install pymysql'</b> command and press <b>'ENTER'</b> button
5) Start <b>'XAMPP'</b> server
6) Copy mysql diff db script for python version 3.6 into your <b>'Downloads'</b> directory <br>
   <b>Download file name :</b> diffDB2.py <br>
7) Open command prompt and goto <b>'Downloads'</b> directory and type <b>'diffDB3.py'</b> command and press <b>'ENTER'</b> button
8) Go ahead steps-wise with script.


<b>Any suggestions, improvements, facing issues etc. Contact on given below details.</b> <br>
Author Name : Chirag D Jain <br>
Mobile & What's App : 91+ 9975967186 <br>
Email : chirag.jain@digitaledu.net <br>
Country : India <br>
