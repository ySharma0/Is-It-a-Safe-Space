# Is-It-a-Safe-Space

## What it does
Our website takes in a user inputted URL and classifies the safety of the site for a user. We classify the site based on three filters: profanity, hate speech, and safe. We also keep track of the most frequented sites that are either dangerous or safe to allow our users an easy-to-access list of options to check out or avoid.

## How we built it
We built the website using Python Flask, Jinja2, and HTML/CSS. The website was able to become dynamic because of Jinja2 which allowed easy integration with the data from our server.

When the user submits a URL, we have our Selenium web-driver pull the raw HTML ( which includes the javascript-loaded text ). We then pass this to BeautifulSoup to parse and filter the data. After this, we pass the data chunk by chunk into our natural language processing model. The model then outputs a classification on the type of text entered: profanity, hate speech, other. We then use this to classify the overall website.
