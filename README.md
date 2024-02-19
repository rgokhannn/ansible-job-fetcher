# Ansible Job Fetcher

This Python script is used to fetch completed jobs in Ansible and transfer this data to a database using an API request. The script fetches jobs that have been successfully completed and allows adding them based on criteria such as job name using filters.


## Project data transferred to the database

- Job name
- Job ID
- Job Date
- Survey Answers (the number of surveys can be increased according to demand)

  
## Usage

To be able to use the script without editing, the survey variables of completed jobs need to be defined as var1, var2, var3... This way, a standardized data source is established. When using this database table for data visualization (in environments like Grafana), there is no need to write complex queries.
