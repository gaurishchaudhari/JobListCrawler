import requests
from bs4 import BeautifulSoup
import os
import sys
import json
import time
import re

# ======================================
# Install following pacakges
# ======================================
# pip3 install requests
# pip3 install lxml
# pip3 install bs4


# ======================================
# Get all job urls from stack overflow
# ======================================
def so_crawl_all_job_urls():

    data_dir = './output'
    output_file = os.path.join(data_dir, 'job_urls.txt')
    num_urls_detected = 0

    base_url = 'https://stackoverflow.com/jobs?pg={}'
    page_no = 1
    page_limit = 3  # Check max pages: 135

    while page_no <= page_limit:
        page_url = base_url.format(page_no)
        print("Crawling page: {}".format(page_url))
        content = requests.get(page_url).text
        bs = BeautifulSoup(content, "lxml")
        script_tag = bs.find("script", {"type": "application/ld+json"})
        job_urls_content = json.loads(script_tag.contents[0])
        pg_urls = []
        for item in job_urls_content['itemListElement']:
            url = str(item['url'])
            pg_urls.append(url)

        with open(output_file, 'a', encoding='utf-8') as fout:  # append mode
            for url in pg_urls:
                fout.write("{}\n".format(url))
                num_urls_detected += 1

        page_no += 1
        time.sleep(3)  # sleep for 3 sec to avoid throttling

    page_no -= 1
    print("Number of Job pages crawled: {}".format(page_no))
    print("Number of Job urls detected: {}".format(num_urls_detected))
    print("Job Urls output file written to {}".format(output_file))


# ======================================
# Crawl job post url and parse required fields
# ======================================

def so_parse_all_job_posting():
    data_dir = './output'
    job_posts_dir = './output/jobs'

    parsed_jobs = []
    for file in os.listdir(job_posts_dir):
        file_path = os.path.join(job_posts_dir, file)
        with open(file_path, 'r', encoding='utf-8') as fin:
            content = fin.read()
            jobj = json.loads(content)

            title = ""
            if 'title' in jobj:
                title = jobj['title']

            company = ""
            if 'hiringOrganization' in jobj and 'name' in jobj['hiringOrganization']:
                company = jobj['hiringOrganization']['name']

            location = ""
            if 'jobLocation' in jobj and len(jobj['jobLocation']) > 0:
                location_parts = []
                if 'address' in jobj['jobLocation'][0]:
                    address = jobj['jobLocation'][0]['address']

                    if 'addressLocality' in address:
                        locality = address['addressLocality']
                        location_parts.append(locality)
                    elif 'addressRegion' in address:
                        region = address['addressRegion']
                        location_parts.append(region)

                    if 'addressCountry' in address:
                        country = address['addressCountry']
                        location_parts.append(country)

                location = ", ".join(location_parts)

            skills = ""
            if 'skills' in jobj:
                skills = ', '.join(jobj['skills'])

            description = ""
            if 'description' in jobj:
                desc_bs = BeautifulSoup(jobj['description'], "lxml")
                # get fill desc
                description = ' '.join([p.replace('\n', ' ').replace('\r', '') for p in desc_bs.find_all(text=True)])

            parsed_jobs.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Skills': skills,
                'Description': description
            })

    print("Number of parsed jobs: {}".format(len(parsed_jobs)))

    output_file = os.path.join(data_dir, 'JobPostings.tsv')
    with open(output_file, 'w', encoding='utf-8') as fout:
        # header
        fout.write("{}\n".format("\t".join([
            "Title",
            "Company",
            "Location",
            "Skills",
            "Description",
        ])))
        # data
        for jobj in parsed_jobs:
            fout.write("{}\n".format("\t".join([
                jobj["Title"],
                jobj["Company"],
                jobj["Location"],
                jobj["Skills"],
                jobj["Description"],
            ])))

    print("Output written to {}".format(output_file))


def so_crawl_all_job_postings():

    data_dir = './output'
    job_urls_file = os.path.join(data_dir, 'job_urls.txt')

    counter = 0
    with open(job_urls_file, 'r', encoding='utf-8') as fin:
        for line in fin:
            job_url = line.strip()
            counter += 1
            #if counter > 7:
            #    break
            print("[{}] Parsing {}".format(counter, job_url))
            match = re.search(r"https://stackoverflow.com/jobs/([0-9]+)/", job_url)
            if match is not None:
                job_id = match.group(1)
                output_file = os.path.join(data_dir, "jobs", "{}.txt".format(job_id))
                if os.path.exists(output_file):
                    print("Job is already crawled. Continue ...")
                    continue
                content = requests.get(job_url).text
                bs = BeautifulSoup(content, "lxml")
                script_tag = bs.find("script", {"type": "application/ld+json"})
                job_post_content = script_tag.contents[0]
                with open(output_file, 'w', encoding='utf-8') as fout:
                    fout.write(job_post_content)
                print("Written {}".format(output_file))

            time.sleep(3)  # sleep for 3 sec to avoid throttling

    counter -= 1
    print("Number of job posts crawled: {}".format(counter))


# ======================================
# Main program
# ======================================
def main():
    print("Start")

    mode = "2"

    if mode == "1":
        so_crawl_all_job_urls()

    if mode == "2":
        so_crawl_all_job_postings()

    if mode == "3":
        so_parse_all_job_posting()

    print("Done")


if __name__ == '__main__':
    main()