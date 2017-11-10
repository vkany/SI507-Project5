# SI 507 F17 - Project 5 - OAuth & Data Processing

### DEADLINE: Sunday, November 12, at 11:59 PM

## To Submit

* Fork and clone this repository
* Edit and/or add the appropriate code files to complete the project
* Commit and push your changes to your fork on GitHub
* Submit the link to your GitHub repository (the fork) to the Project 5 assignment on Canvas

    * If you are submitting this assignment late AND would like to use a late day, comment on the assignment indicating that you would like to use a late day to avoid deduction

* Files that should be included in your repository when you submit it for a complete Project 5:

    * `SI507project5_tests.py`
    * `SI507project5_code.py`
    * `explanation.txt`
    * This `README.md`, because it's a fork -- but this should remain unedited to avoid conflict
    * `requirements.txt`, created from a `pip freeze` of the virtual environment you set up to work on this project
    * All CSV files your project creates, as examples
    * Any other files your project relies upon having in the same directory

See below for further instructions.

## Instructions

* Your goal in this project is to plan what data you want to get from an API in order to create CSV files of data that's interesting to you, set up a caching system for your data so that data is cached for a reasonable amount of time when you run the program, write unit tests for your project that will help you (and us!) ensure it works correctly, and ultimately write code to successfully gather and process data from a REST API that uses some form of complex authentication.

* You should end up with at least 2 different CSV files containing data (HINT: think about your projects 2 and 3 when you consider how you want to store data in CSV files! WHat you had to do in those projects may provide inspiration).

* However, this is just one small project, and we're scoping this relatively small. You should think about what *specifically* could be interesting to you (or interesting enough to examine it for this project; we understand that one of these 2 APIs may not offer *exactly* what you most want to investigate). That consideration and decision is part of the assignment! It's not generally easy to decide on how to use an API, or sort through its documentation, and it requires practice.

* We've provided steps and checkpoints in these instructions to follow the process of completing the project in an organized way!

* **Step 1:** Choose one of these APIs from which you want to get data.

  * [The Tumblr API](https://www.tumblr.com/docs/en/api/v2#auth) **HINT:** This shares a lot in common with the Twitter API! There are certainly client libraries that deal with Tumblr, but you may find it easier to adapt OAuth1 code we've discussed before.
  * [The Eventbrite API](https://www.eventbrite.com/developer/v3/)  -- [Here](https://www.eventbrite.com/developer/v3/api_overview/authentication/) is the page about authentication, since there are a lot of links on that initial page. You'll probably want to look at that page AND select a reasonable `GET` endpoint from the options listed.

 > You *may* use any client library (like for example [Spotipy](https://github.com/plamere/spotipy) or [Tweepy](http://www.tweepy.org/), although Tweepy is especially nice, and also has some flaws...) to get data from an API if you wish (but not data from Facebook, Twitter, or Spotify) -- but be warned that sometimes, figuring out a complex client library that isn't well documented is more challenging than adapting your own code that does not use a library! It all depends on your end goal and your specific situation.

  **Checkpoint #1:** You have selected 1 API, and read its documentation. You have looked at code from class and decidd which method of getting data from an OAuth-authenticated API is a good model for the API you are using in Project 5.

  **NOTE:** If you find this material confusing AND exciting (:)), you may want to stick to understanding the code presented in class, and adapting it for Tumblr. If you find this material exciting but not super confusing, because you have previous experience or really love this kind of thing, and want to push yourself even further, adapting one of the OAuth2 examples that do not have any caching system implemented already may be a fun exercise to try.

* **Step 2 (200 points):** Edit `explanation.txt` with a (short) paragraph or set of bulletpoints about the data you are accessing from this API, and what the CSV files you plan to produce will include. It should be something like this (of course, not for the Twitter API -- for either the Tumblr API or the Eventbrite API):

```
    I am accessing the Twitter search API and gathering:
    - 50 Tweets for each of 2 users I'm going to search for
    - For each tweet, I'll be accessing the tweet text, the number of hashtags, the time posted, and the user who posted the tweet
    - I'll write 2 CSV files, one for each user's search (even though searching for a user may result in tweets they did not post)
    - Data in each CSV file: 4 columns -- text, number hashtags, time posted, user who posted the tweet
    - URL for the API: <URL HERE>
    - If necessary, URL describing the authentication process for the API: <URL HERE>
```


**Checkpoint #2:** A completed `explanation.txt`


* **Step 3 (200 points):** Edit `SI507project5_tests.py` with unit tests for the project you plan. Don't change the name of this file. There should be at **least 1 subclass of `unittest.TestCase`**, at least **5 total test methods** (consider what you most need to test!), at least one use of the **`setUp`** and **`tearDown`** test methods.

    * Each of the test methods you write must be **good tests** (meaning they won't *always pass* -- or *always fail*, they will catch semantic errors -- not just syntax errors).

    **Checkpoint #3:** A completed `SI507project5_tests.py`

* **Step 4 (400 points for code, 100 points for CSV files):** Edit `SI507project5_code.py` as follows:

    * Don't change the name of this file, though you may write other files and import them into this one.

    * You must implement a caching system that ensures you will not run afoul of the rate limit of whatever API you use, and that you will not get data from the same request more than once per 12 hours, no matter how many times you run the program (at minimum. It could also be a week, 3 days, a month, whatever you want). *HINT:* Use the examples shown in class to implement functions that you can invoke to get and cache data from your API!

    * You may want to consider writing functions that can generalize your code, so it is easy to write more code as you go on.

    * You can borrow heavily from the code you saw in class, the examples on Canvas! But make sure these files you turn in run correctly and access the correct API (Tumblr, or Eventbrite).

  * You must get data from this API that does require some method of authentication to access it -- OAuth1 or OAuth2 (some APIs have some endpoints that require OAuth and some that do not). The data must be enough data that your code written in this file, when run, results in CSV files, as follows...

  * Your code must create at least 2 `.CSV` files of data with more than one column of data (e.g. one column of numbers 1, 2, 3, 4 ... and one column of names would not count. A spreadsheet provides numbers, you don't need Python for that). You may create more if you wish (e.g. Project 3 created 3 files) but you do not have to.

  * Your code should pass all of your unit tests by the time you submit it, for full credit (but it should NOT pass all of your unit tests when there's no code in `SI507project5_code.py` yet, of course).

  * There are no other requirements for your code in this project!

  **Checkpoint #4:**

      * A caching system for your API
      * Use of oAuth1 or oAuth2
      * 2+ CSV files of relevant data retrieved from the API
      * Tests written in Step 3 should pass
      * A completed `SI507project5_code.py`

* **Step 5 (100 points):** *Make sure you have a working virtual environment for this project.* You should include a `requirements.txt` file in your repository with the requirements for whatever virtual environment you use for this project. Perhaps it will require very little, perhaps you'll choose to use a complex client library and it will require a lot! **Points here will be allocated based upon whether you have included a reasonable `requirements.txt` file. You should *not* commit your virtual environment itself.** HINT: It will probably be useful to commit a `.gitignore` file in order to avoid committing all the files that are part of your virtual environment!

  **Checkpoint #5:** A completed `requirements.txt`
