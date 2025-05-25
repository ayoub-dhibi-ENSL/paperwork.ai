# paperwork.ai 
## (I hate filling boring administrative documents)
<p>This project was built during the Paris Hackaton organized by {Tech:Europe} held @ La Cristallerie the 24th and 25th of May 2025</p>
## The problem tackled
<p>
The project aims to alleviate the pain associated with doing tedious paperwork. For example searching informations in dozens of files and pictures in order to complete a document (intership agreement, taxes declaration, ...)
</p>
## How it is tackled
<p>
The project currently offers a rather static and very simple but efficient approach to the problem. The working environement has to be setup like this 
<ul>
  <li>In the working directory you shold have the two scripts "gradioUI.py" and "agent.py"</li>
  <li>Moreover you should have a target.pdf file which is the document you are trying to complete (subscription for, taxes declaration, ...)</li>
  <li>Finally you want to create an "user_data" directory in the working directory. The user_data directory should contain as much as possible informative documents about you, for example your ID, IBAN, previously filled paperwork, ...</li>
</ul>
Some specific setup regarding the scripts is to be find further.
The agent will use his OCR tools to determine what data is needed to complete your paperwork, then he will scrap this data from multiple sources, namely the user_data directory and tool connected to your email from

</p>

