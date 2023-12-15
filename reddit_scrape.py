import os
import praw
import requests, re
from dotenv import load_dotenv
from datetime import datetime

# change this to whichever directory you want
BASE_DIR = "D:/Twitter_n_Insta/MemeCollection" 

def init_agent():
    user_agent = os.getenv("USER_AGENT")
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=user_agent
    )
    return reddit

def make_monthly_dir():
    directory = datetime.now().strftime("%Y%m")
    path = os.path.join(BASE_DIR, directory)
    os.mkdir(path)    

def save_file_to_monthly_directory(file_response, file_name: str):
    directory = datetime.now().strftime("%Y%m")
    monthly_dir  = os.path.join(BASE_DIR, directory)    

    # Check if the monthly directory exists, create it if not
    if not os.path.exists(monthly_dir):
        os.mkdir(monthly_dir)

    # Create the full path for the file in the monthly directory
    file_path = os.path.join(monthly_dir, file_name)

    # Save the file to the monthly directory
    with open(file_path, "wb") as f:
        f.write(file_response.content)


def scrape_data(agent :praw.Reddit, limit:int = 10):    
    for submission in agent.subreddit('ProgrammerHumor').hot(limit=limit):
        file_name = submission.url.split("/")
        if len(file_name) == 0:
            file_name = re.findall("/(.*?)", submission.url)
        file_name = file_name[-1]
        if "." not in file_name:
            file_name += ".jpg"
        print(file_name)            
        r = requests.get(submission.url)        
        save_file_to_monthly_directory(r, file_name)
        

def load_config():
    load_dotenv()
    

def start():
    load_config()
    reddit = init_agent()
    make_monthly_dir()
    scrape_data(reddit, limit=50)


if __name__ == "__main__":
    start()
