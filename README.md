# The impact of Elon Musk's tweets on Dogecoin

The current analysis aims at studying the effect of Elon Musk tweets on the Dogecoin rally in 2021.

To what extent Musk's activity on Twitter influenced the behavior of the Dogecoin market? <br>
Do his tweets have an impact on the Dogecoin market alone, or also on other cryptocurrencies? <br>
Do Musk’s tweets need to reference Dogecoin to have an effect?

Such questions are further addressed, and elaborated with the analysis' results, in <br>
https://drive.google.com/file/d/1lQtpb55U2NpoJ-yC2KxaXj87bFASLou8/view?usp=sharing

## Project structure

```
├── .gitignore              
├── requirements.txt
│
├── analysis.ipynb              <- the main notebook with the anlysis carried out
├── analysis_read.html          <- an easy readable .html version of the notebook
│
├── import_data.py              <- cusotm module with functions to import data into the notebook
├── tweets_impact.py            <- cusotm module with functions to report price differences at tweet times 
├── visualization.py            <- cusotm module with plotting functions (using bokeh)
│
├── data                        <- directory containg raw data used for the analysis
│   ├── BTC-USD.csv
│   ├── DOGE-USG.csv
│   ├── SOL-USD.csv
│   └── elon_tweets.csv
│
└── drafts                      <- working code, eventually discarded for the project report
    ├── text_cleaning.py
    └── predictive_model.py
```