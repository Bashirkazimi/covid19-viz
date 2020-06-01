# covid19-viz
This project aims to visualize reports for countries with the highest number of COVID19 cases around the globe. Additionally, it reports cases for Afghanistan (my home country), and Bangladesh (my wife's home country). The data is loaded in real time from the daily updated report by Johns Hopkins University on [this](https://github.com/CSSEGISandData/COVID-19) Github repository. 

## Technologies and services used:
- Python
- Flask
- Plotly
- Heroku
- Pandas
- Bootstrap
- HTML

The app is deployed and running [here](https://global-covid-viz.herokuapp.com/).

## Instructions for deploying


First, a new folder was created for the web app and all of the folders and files were moved into the folder:

```
mkdir web_app
mv -t web_app covid wrangling_scripts covid.py
```

The next step was to create a virtual environment and then activate the environment:

```
conda update python
python3 -m venv covid
source covid/bin/activate
```

Then, pip install the Python libraries needed for the web app

```
pip install flask pandas plotly gunicorn
```

The next step was to install the heroku command line tools:

```
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
https://devcenter.heroku.com/articles/heroku-cli#standalone-installation
heroku —-version
```

And then log into heroku with the following command

```
heroku login
```

Heroku asks for your account email address and password, which you type into the terminal and press enter.

The next steps involved some housekeeping:
`remove app.run()` from covid.py


type `cd web_app` into the Terminal so that you are inside the folder with your web app code.
Then create a proc file, which tells Heroku what to do when starting your web app:

```
touch Procfile
```

Then open the Procfile and type:
```
web gunicorn covid:app
```

Next, create a requirements file, which lists all of the Python library that your app depends on:
```
pip freeze > requirements.txt
```
And initialize a git repository and make a commit:

```
git init
git add .
git commit -m ‘first commit’
```

Now, create a heroku app:

```
heroku create global-covid-viz 
```

where `global-covid-viz` is a unique name that nobody else on Heroku has already used.

The heroku create command should create a git repository on Heroku and a web address for accessing your web app. You can check that a remote repository was added to your git repository with the following terminal command:
```
git remote -v
```
Next, you need to push your git repository to the remote heroku repository with this command:
```
git push heroku master
```
Now, you can type your web app's address in the browser to see the results.

## Acknowledgments

The code and depoloyment was created using the template for a sample dashboard by [Udacity Data Science Nanodegree Program](https://classroom.udacity.com/nanodegrees/nd025/dashboard/overview). 
