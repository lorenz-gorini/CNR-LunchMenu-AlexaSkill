# CNR LunchMenu 
This is a simple Alexa Skill that uses WebScraping (with beautifulsoup library) to find the correct .doc file with the lunch menu at CNR (Bologna).

1. Opens the dashboard http://www.bo.cnr.it/mensa/bacheca/
2. Find the correct date you selected by voice command to Alexa. I am still thinking about the implementation because the date format is not consistent at all when uploaded. At the moment it opens the last uploaded menu webpage.
3. Opens the selected webpage and downloads the attachment .doc containing a table 
4. Returns and reads the content of the correct column (corresponding to the day you picked; this selection works)

The skill has been published.
