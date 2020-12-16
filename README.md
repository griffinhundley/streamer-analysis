# Streamer Analysis

**Author**: Griffin Hundley
***

![](images/twitch-generic-email-1-1-1-1.jpg)

## Overview

Twitch is a social platform for livestreaming video games, music, art, and more.  For most people making content on the platform, livestreaming started out as a hobby for people sharing their love of gaming - something they do only because its fun.  For a select few who build a strong community and gain a larger audience, they can turn their channel into a primary source of income by becoming a partner with Twitch.

Being a partner has a lot of perks, but also a few restrictions.  Partners get a subscription button added to their channel, where viewers can pay $5 for 1 month access to subscriber-only emotes, no advertisements, and channel specific rewards.  Partners also get a share of the ad revenue for ads ran on their channel.  As part of the contract that partners sign, they cannot livestream on other platforms.

As of February 2020, there are 3.8 million unique broadcasters on the website, with an average of 56,000 concurrent broadcasters, and 1.44 million concurrent viewers at a given time.  Of those 3.8 million broadcasters, there are roughly 41,000 partners. Source: Mansoor Iqbal https://www.businessofapps.com/data/twitch-statistics/

***

## Business Problem

![](images/twitch-average-monthly-broadcasters.png)

Source: Mansoor Iqbal https://www.businessofapps.com/data/twitch-statistics/

Livestreaming is emerging as a premiere online industry, with significant growth over the years.  As of December 2020, the effects of COVID are still being realized, however there are reports of 24-50% increase in Twitch viewership as a result of the pandemic lockdowns.

Online entertainment isn't going anywhere but up.  As a result of increasing scale, more online companies must rely on automated systems.  For example - Twitch competitors Youtube Live and Facebook Gaming use automated systems to detect copywrite infringment and obscene content.  As the number of broadcasters and viewers continues to rise, and as the entertainment industry shifts more online, the number of people turning to livestreaming as a source of income increases.  

Applications for partnership are currently reviewed manually by Twitch staff, with applicants waiting 2-4 weeks to get results.  Because partnership is approved manually by different individuals, there can be a personal selective bias towards or against certain demographics.  In some cases, very successful streamers with well above average metrics have been denied partnership, while much smaller channels are approved, leading to distrust between the broadcaster and Twitch.  

The goal of this analysis is to provide a model that can approve or deny channels for partnership based on their channel metrics, removing the need for manual review, which frees up resources, decreases feedback time to streamers on the status of their partnership application, and having a system without personal influences.  Additionally, the nature of the model allows for dynamically adjusting the threshold for approval, to make it more or less strict depending on the needs of Twitch.

Source: Thomas Wilde https://www.geekwire.com/2020/twitch-sets-audience-record-october-pandemic-continues-fuel-livestreaming-growth/

***

## Data

Over the course of a week, at different times during the day, the Twitch API was queried through all of the pages of currently live broadcasters to generate a list of \~800,000 broadcasters.  These broadcasters were then filtered to only channels older than 60 days, with over 900 viewers (\~300,000 broadcasters).  This is to filter out brand new channels, and only to examine channels that meet the basic number of viewers to be considered for partnership as described in the Path to Partnership achievement. From the twitch api, the data being collected covers:

```view_count```: total number of lifetime channel views

```account_age```: time since account creation

```broadcaster_type```: (partner, affiliate, unaffiliated)

From these \~300K broadcasters, a random sample of 10% of those channels (\~30k) was chosen to obtain a reasonably sized dataset.  For these \~30k channels, data was webscraped from twitchtracker.com.  The channel metrics being examined are lifetime aggregate channel data.  The specific metrics gathered are:

```hours_streamed```: total number of hours stream has been live

```average_viewers```: average number of concurrent viewers

```peak_viewers```: peak number of concurrent viewers

```days_of_activity```: total number of days where stream was live

```total_games_streamed```: total number of games streamed

```daily_broadcast_time```:  average hours channel is live per day

```hours_watched_daily```: average number of hours watched by viewers per day

```followers_per_stream```: average number of followers gained per stream

```views_per_stream```: average number of concurrent viewers per stream

```followers_per_hour```: average number of followers per hour

```views_per_hour```: average number of views per hour

```hours_watched```: total hours watched by viewers

```active_days_per_week```: average of how many days per week the broadcast is live

```average_games```:  average number of games played per stream

### Data Assumptions

A key assumption being made with this analysis is that a channel's total lifetime aggregate metrics can be used to classify a channel by partnership.  Not having access to the date when a channel is partnered, analysis can only be made on the metrics as they currently are, not when the channel was partnered.  As a result, theoretically this biased analysis should produce a harsher classifier, with the idea that once a channel is partnered it will continue to grow and inflate its metrics, and by association inflate the decision boundary.  If a model produced from this analysis were to be used by Twitch in its partnership approval process, in deployment, Twitch would have access to those specific metrics and would not have this bias. 

Features not used in this analysis that Twitch currently uses in their partner selection is chat interaction - how active are the viewers in the chat room.  This information would theoretically be important to classifying small streams, as a small stream with a very active chat could be partners.

Additionally, Twitch makes a distinction between 'natural' views and views gained through hosts and raids (when one channel sends all of its viewers to another channel, and only natural views count towards their decision.  This analysis has no method of identifying natural views from views gained through hosts or raids, and will assume that views are natural.  The theoretical effect of this assumption is a slight deflation of importance in view-related features.
***

## Methods

Describe the process for analyzing or modeling the data. For Phase 1, this will be descriptive analysis.

***
Questions to consider:
* How did you prepare, analyze or model the data?
* Why is this approach appropriate given the data and the business problem?
***

## Results

Present your key results. For Phase 1, this will be findings from your descriptive analysis.

***
Questions to consider:
* How do you interpret the results?
* How confident are you that your results would generalize beyond the data you have?
***

Here is an example of how to embed images from your sub-folder:

### Visual 1
![graph1](./images/viz1.png)

## Conclusions

Provide your conclusions about the work you've done, including any limitations or next steps.

***
Questions to consider:
* What would you recommend the business do as a result of this work?
* What are some reasons why your analysis might not fully solve the business problem?
* What else could you do in the future to improve this project?
***

## For More Information

Please review our full analysis in [our Jupyter Notebook](./dsc-phase1-project-template.ipynb) or our [presentation](./DS_Project_Presentation.pdf).

For any additional questions, please contact **name & email, name & email**

## Repository Structure

Describe the structure of your repository and its contents, for example:

```
├── __init__.py                         <- .py file that signals to python these folders contain packages
├── README.md                           <- The top-level README for reviewers of this project
├── dsc-phase1-project-template.ipynb   <- Narrative documentation of analysis in Jupyter notebook
├── DS_Project_Presentation.pdf         <- PDF version of project presentation
├── code
│   ├── __init__.py                     <- .py file that signals to python these folders contain packages
│   ├── visualizations.py               <- .py script to create finalized versions of visuals for project
│   ├── data_preparation.py             <- .py script used to pre-process and clean data
│   └── eda_notebook.ipynb              <- Notebook containing data exploration
├── data                                <- Both sourced externally and generated from code
└── images                              <- Both sourced externally and generated from code
```