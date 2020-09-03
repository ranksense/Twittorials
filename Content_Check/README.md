## About the Script
* This script will generate a visual diff file that shows you the difference in content between a desktop and mobile page
* For websites with a separate mobile page, often times content can be lost when transitioning to mobile
* Creating this diff file will allow you to see the client-side changes.
* This script will be using repl.it to run

## How to Use It
* **Step 1:** Click on this [repl.it link](https://repl.it/@snupet/Checking-Content-of-Mobile-vs-Desktop#main.py) to open the code in your browser.
* If you'd like to keep a copy of the script, click "fork" at the top of the repl
* If you are running the script from your PC, add the script to a folder, and then add the following files to that folder:
  * desktop_content.txt
  * diff.html
  * mobile_content.txt
* **Step 2:** Click on "Run" at the top, and wait for repl.it to install the necessary libraries
* **Step 3:** When prompted, enter the URL of the desktop and mobile site separately
* **Step 4:** After the code finishes, download the package as a .zip and open the "diff.html" to see the results
  * It is important to note that the HTML can be so large that you will need to scroll horizontally to find both parts of the diff file

## Viewing the Diff

* On the left side of the diff, you will see the **rendered HTML** and what has been removed (highlighted in red)
* On the right side of the diff, you will see the **rendered HTML** and what has been added (highlighted in green)
* **(Note)** You may need to scroll far to the right of the diff file in order to view the right half
