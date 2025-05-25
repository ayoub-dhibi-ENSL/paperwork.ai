# paperwork.ai
This project was built during the Paris AI Hackaton organized by {Tech:Europe} held @ La Cristallerie the 24th and 25th of May 2025.
## (I hate filling boring administrative documents)
The project aims to alleviate the pain associated with doing tedious paperwork. For example searching informations in dozens of files and pictures in order to complete a document (intership agreement, taxes declaration, ...).

## The problem tackled
When completing a document for paperwork the search-copy-paste process gets very time consuming mainly due to the research procedure i.e. finding the right information in the right document by opening multiple PDFs and images (documents scans for example). We aim to reduce drastically the time needed for the search phase

## How it is tackled

The project currently offers a rather static and very simple but efficient approach to the problem. The working environement has to be setup like this 
<ul>
  <li>In the working directory you shold have the two scripts "gradioUI.py" and "agent.py"</li>
  <li>Moreover you should have a target.pdf file which is the document you are trying to complete (subscription for, taxes declaration, ...)</li>
  <li>Finally you want to create an "user_data" directory in the working directory. The user_data directory should contain as much as possible informative documents about you, for example your ID, IBAN, previously filled paperwork, ...</li>
</ul>
Some specific setup regarding the scripts is to be find further.
The agent will use his OCR tools to determine what data is needed to complete your paperwork, then he will scrap this data from multiple sources, namely the user_data directory and a tool connected to your email that get all the exchanges you had with your school administration, your future advisor, etc and use the data from these exchanges to further complete your paperwork.

## Future ameliorations and stuff I want to change
<ul>
  <li> The ultimate feature I want to add is a tool that will take the final JSON and generate a completed version of the PDF so we cut the copy-paste steps, a refinment could be to train a model on the specific handwritting of the user and make the agent complete the PDF with similar handwritting style </li>
  <li> A better UI and a web version where you can upload the user_data directory </li>
  <li> Make the workflow/logic of the agent less dependant on the prompts </li>
</ul>







