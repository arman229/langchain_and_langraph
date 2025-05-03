#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
import re
from crewai.flow import Flow, listen, start
from matching_job_profile.crews.read_cv_crew.read_cv import ReadCvCrewNew
from matching_job_profile.crews.match_cv_crew.cv_matching import MatchCvCrewNew
import requests
import urllib.parse
import json
import requests
from bs4 import BeautifulSoup
import csv
import os 
from matching_job_profile.crews.single_crew.single_crew  import SingleCvCrewNew 








csv_file = "./src/matching_job_profile/crews/match_cv_crew/data/job_listings_new.csv"
def scrape_job_links(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser") 
            job_links = [a["href"] for a in soup.find_all("a", class_="base-card__full-link") if a.get("href")]
            return { 
                "links": job_links,
            }
        else:
            print(f"Failed to fetch job details from {url}")
            return None
    except Exception as e:
        print("Error scraping job details:", e)
        return None

def scrape_job_description(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_title = soup.find("h1").text if soup.find("h1") else "No Title Found"
            company_name = soup.find("a", class_="topcard__org-name-link").text if soup.find("a", class_="topcard__org-name-link") else "No Company Found"
            job_description = soup.find("div", class_="description__text").text if soup.find("div", class_="description__text") else "No Description Found"
            return {
                "title": job_title.strip(),
                "company": company_name.strip(),
                "description": job_description.strip(),
                "link": url,
            }
        else:
            print(f"Failed to fetch job details from {url}")
            return None
    except Exception as e:
        print("Error scraping job details:", e)
        return None


class MatchProfilePositionFlowNew(Flow):
    # @start()
    # def starts(self):       
    #     inputs = {                
    #         'path_to_jobs_csv': './src/matching_job_profile/crews/single_crew/data/jobs.csv',
    #         'path_to_cv': './src/matching_job_profile/crews/single_crew/data/cv.md'
    #     }
    #     print("Starting the flow",inputs)
    #     resp = MatchToProposalCrew().crew().kickoff(inputs=inputs)
    #     print(f'\n\n\n\n\n Final response={resp.raw}')
    #     with open('matchjobss.md','w') as f:
    #         f.write(resp.raw)
            
    @start()
    def cv_reader_fun(self):
        inputs = {                
            'path_to_jobs_csv': './src/matching_job_profile/crews/single_crew/data/jobs.csv',
            'path_to_cv': './src/matching_job_profile/crews/single_crew/data/cv.md'
        } 
        crew = SingleCvCrewNew().crew().kickoff(inputs=inputs)
        raw_result = crew.raw 
        
        
        print(f'\n\n\n\n\n:{raw_result}')
        return 
        def clean_json_string(json_str): 
            json_str = re.sub(r"```json|```", "", json_str).strip() 
            pattern = r'("((?:\\.|[^"\\])*)")'
            def replacer(match): 
                inner_text = match.group(2)
                escaped_text = inner_text.replace("\n", "\\n")
                return f'"{escaped_text}"'
            return re.sub(pattern, replacer, json_str, flags=re.DOTALL)
        cleaned_json = clean_json_string(raw_result)
        try:
            data = json.loads(cleaned_json)  
            return data 
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
         
    # @listen(cv_reader_fun)
    def linkden_job_finder(self, cv_data): 
 
        job_titles = cv_data.get("job_titles", [])
        country = cv_data["summary"].get("Country Name", "Worldwide")
        print('job_titles',job_titles)
        if not job_titles:
            print("No job titles found in the CV data.")
            return
        
 
        
        for title in job_titles[0]: # Note that this is a list of titles  not single value 
            
            query = f"{title} site:linkedin.com/jobs in {country}"
            encoded_query = urllib.parse.quote(query)
            url = f"https://google.serper.dev/search?q={encoded_query}&apiKey={os.getenv('SERPER_API_KEY')}"
            print(f'url={url}')
            print(f"Fetching jobs for: {title}")
            response = requests.get(url)
            
            print(f'response=={response.json()}')
            if response.status_code == 200:
                job_links_list = []
                data = response.json()
                for result in data.get("organic", []): 
                    link = result.get("link", "") 
                    job_links_list.append(link)

                 
                
                print(f"job_links_list={job_links_list} {len(job_links_list)}")
                all_job_details = []
                if job_links_list:
                    for joblink in job_links_list[1:3]: # Limiting to 3 jobs for now It is a list of jobs links
                        print(f"Scraping job details for: {joblink}")
                        job_links = scrape_job_links(joblink)
                        print(f"job_links={job_links}")
                        if not job_links:
                            continue
                        for link in job_links['links']:
                            print(f"Scraping job description for: {link}")
                            job_detail = scrape_job_description(link)
                            print(f"job_detail={job_detail}")
                            if job_detail:
                                all_job_details.append(job_detail)


                
                headers = ["title", "company", "description", "link"]

                # Save to CSV
                with open(csv_file, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(all_job_details)

                print("✅ Job listings saved to job_listings.csv") 
            else:
                print(f"Error fetching data for {title}:", response.status_code)

    # @listen(linkden_job_finder)
    # @start()
    # def finalize_job_listings(self):
    #     inputs = {
    #     'path_to_jobs_csv': './src/matching_job_profile/crews/match_cv_crew/data/job_listings_new.csv',
    #     'path_to_cv': './src/matching_job_profile/crews/match_cv_crew/data/cv.md'
    # }
    #     resp = MatchCvCrewNew().crew().kickoff(inputs=inputs)
    #     with open('matchjob.md','w') as f:
    #         f.write(resp.raw)
    #     print(f'\n\n\n\n\n Final response={resp.raw}')
         
 

def kickoff():
    resp = MatchProfilePositionFlowNew()
    resp.kickoff()


def plot():
    resp = MatchProfilePositionFlowNew()
    resp.plot()



 