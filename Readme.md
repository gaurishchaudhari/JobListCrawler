## Required Python packages

pip3 install requests <br/>
pip3 install lxml <br/>
pip3 install bs4 <br/>

## How to run

<i>python3 crawl_so_job_urls.py</i>

<b>Mode = 1:</b>  This will crawl all job urls from paginated results of https://stackoverflow.com/jobs?pg=X <br/>
The output will be saved to ./output/job_urls.txt

<b>Mode = 2:</b>  This will crawl each individual job url from job_urls.txt file and dumps the raw job details available in json files. If the job id is already crawled, it will skip the particular url. <br/>
The output will be saved to ./output/jobs/*.txt

<b>Mode = 3:</b>  This will parse all individual job json files and produces a TSV output. This mode can run offline and does not require connection to web. <br/>
The output will be saved to ./output/JobPostings.tsv
