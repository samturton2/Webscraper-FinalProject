import csv
import os
from flask import Flask, render_template, redirect
import pandas
from config_manager import itjobswatch_home_page_url
from src.itjobswatch_html_readers.itjobswatch_home_page_top_30 import ItJobsWatchHomePageTop30
from src.csv_generators.top_30_csv_generator import Top30CSVGenerator
import requests

from bucket import upload_file, download_file

app = Flask(__name__)

# The default homepage for the app
@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/team')
def MeetTheTeam():
    return render_template("team.html")

@app.route('/toolchain')
def ToolChain():
    return render_template("toolchain.html")

# A simple error page
@app.route('/error')
def error():
    return render_template("error.html")

# Redirect to the error page if the page is not found
@app.errorhandler(404)
def not_found(Exception):
    return redirect("/error")



@app.route('/list')
def no_headers():
    # If there is a pre-existing csv file this will remove it
    # This is to ensure the app always uses the newest data present
    if os.path.exists(os.getcwd()+"/ItJobsWatchTop30s3.csv"):
        os.remove(os.getcwd()+"/ItJobsWatchTop30s3.csv")
    live_response = requests.get("https://www.itjobswatch.co.uk/")

    if live_response.status_code:
        cwd=os.getcwd() +"/"
        top_30 = ItJobsWatchHomePageTop30(itjobswatch_home_page_url())
        Top30CSVGenerator().generate_top_30_csv(top_30.get_top_30_table_elements_into_array(),
                                                cwd, 'ItJobsWatchTop30s3.csv',
                                                top_30.get_table_headers_array())
        try:
            upload_file("ItJobsWatchTop30s3.csv", "eng74-final-project-bucket")
            download_file("eng74-final-project-bucket", "ItJobsWatchTop30s3.csv")
        except:
            pass
    # # If not then just download the s3 bucket data
    else:
        try:
            download_file("eng74-final-project-bucket", "ItJobsWatchTop30.csv")
        except:
            pass

    filename="ItJobsWatchTop30s3.csv"
    data = pandas.read_csv(filename, header=0)
    joblist = list(data.values)
    return render_template('list.html', joblist=joblist)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
