# PIC16A-Twitter-API
Made by Melina Diaz, Tracy Charles, Michelle Pang

**What's happening?**
- Using the Twitter API, we made a dataframe of tweets about UCLA. With this dataframe, we can do cool stuff like sentiment analysis, clustering, etc


**Files:**
1. `demo.ipynb` is the end-to-end demo. (Long Description)
2. `requirements.txt` 
3. `making_dataframe.py` makes the JSON and CSV files that are necessary to make the dataframe. You don't need this, since we supplied a CSV file, but if you want to modify the CSV file to look for different keywords, include different features, this is how you would do it. Run make_call(bearer_token, ...)
4. 
Use `curl -H "Authorization: Bearer BEARER TOKEN" URL` in command line

URL examples are:
- https://api.twitter.com/2/tweets/search/recent?query=from:ucla returns the 10 most recent tweets (id, text) from UCLA

1. Project name.
2. Names of group members (if you don’t want to for privacy, add usernames).
3. Short description of the project.
4. Instructions on how to install the package requirements. If you used the conda line above, your instruction should have the line conda create --name NEWENV --file requirements.txt.
5. Detailed description of the demo file. This includes detailed instructions on how to run it, what output one should expect to see, and any explanations or interpretations of the result. There should be at least 2 figures embedded in this section. It can be screenshots of your game, or plots generated by your data visualization code. Make sure these figures have appropriate titles and captions, and are sufficiently explained in your text.
6. Scope and limitations, including ethical implications, accessibility concerns, and ideas for potential extensions.
7. License and terms of use (probably MIT license).
8. References and acknowledgement.
9. (If appropriate) background and source of the dataset.
10. (If appropriate) links to any tutorials you used, and at least 3 specific things you implemented that differentiates your project from what’s already in the tutorial.
