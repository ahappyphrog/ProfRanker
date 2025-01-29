# Prof Ranker

Python script to algorithmically rank professors from the Cornell Class Roster based on rate my professor data.

## Installation

Run the following command to install all requirements:
`pip install -r requirements.txt`

## Running the script

1. Visit the Cornell [Class Roster](https://classes.cornell.edu/browse) and select all of the filters for classes you are interested in (FWS Seminars, Distribution Requirements ect.). Open Chrome dev tools and navigate to the "Network" tab. Refresh the page, download the HTML, and place it in the same folder as "main.py"

2. Run the following command to start the script:
`py main.py`

### Use the CLI with your number keys to make selections for files & ranking

3. Enter the number of the HTML file you would like to run (listed in the prompt)

4. Enter the number of the ranking mode you would like to use
- By Rating: Rank strictly by professor rating (greatest to least)
- By Difficulty: rank strictly by Difficulty (least to greatest)
- By Weighted Score: Use a basic algorithm to rank professors by high ratings, low difficulty, and high number of reviews (greatest to least)
- By All: Shows outputs of all above options

5. If you ranked professors by weighted score, you can adjust the weights of the algorithm to adjust it to preference (Press enter to use default weights)

Weighting Algorithm: (rating * w1) + ((5 - difficulty) * w2) + (math.log(ratings + 1) * w3 *.8)

The default value of weights is 1.0 (ex. to deprioritize review count, use .8 when prompted for review count weight)

6. View your results in the table and visit their profiles on Rate My Professor to read into comments ect. (ctrl + click to visit the link in vscode)
