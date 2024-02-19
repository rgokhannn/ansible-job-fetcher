import requests
import json
import pyodbc
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import time
username = "admin"
password = "admin"
 
server = "SQL_Server_IP"
database = "DB_NAME"
usernamedb = "DB_USER"
passworddb = "DB_PASSWORD"
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={usernamedb};PWD={passworddb}'
 
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
# You can specify the range of jobs for which data is required in the loop.  The next time the script runs, it should start from this job ID.
# The best practice is to run this script every day and on the last day the script is run, assign the last job ID to a variable. 
# This way, the next time it runs, it will continue from the last job ID.
    for i in range(77, 4377):
        try:
            url = "AWX_URL/api/v2/jobs/"+str(i)+"/"
            auth = (username, password)
            # Send API Request
            response = requests.get(url, auth=(username,password))
   
            if response.status_code == 200:
                data = response.json()
            else:
#                print("Job ID:",str(i),"API request failed. Error code:", response.status_code)
                data = None
   
            # API response handling
            if data:
                if 'summary_fields' in data and 'inventory' in data['summary_fields'] and 'name' in data['summary_fields']['inventory']:
                    inventory_name = data['summary_fields']['inventory']['name']
#                    print("Inventory Name:", inventory_name)
                else:
                    print("Incorrect or incomplete data structure")
       
                if 'summary_fields' in data and 'job_template' in data['summary_fields'] and 'name' in data['summary_fields']['job_template']:
                    job_name = data['summary_fields']['job_template']['name']
#                    You can specify Job Template name here, in order to filter your fetched jobs.          
#                                                  Example                    
                    if ("Site" in job_name or "ELK" in job_name or "Rabbit" in job_name or "Redis" in job_name):
                        pass
                    else:
#                     If its not desired job name, print that.
                        print("Another Job")
                        continue
                else:
                    print("Incorrect or incomplete data structure")
                    continue
       
                if "extra_vars" in data:
                    extra_vars_json = data["extra_vars"]
                    try:
                        extra_vars = json.loads(extra_vars_json)
                        Job_Id = data.get("id")

                        domino_id = extra_vars.get("DominoID", "0")

                        Name = data.get("name")

                        job_date = datetime.strptime(data.get("created"), "%Y-%m-%dT%H:%M:%S.%fZ")
                        job_date_2 = job_date + timedelta(hours=3)
                        Date = job_date_2.strftime("%d/%m/%Y %H:%M:%S")
                        
                        var1 = extra_vars.get("var1","-")
                        var2 = extra_vars.get("var2","-")
                        var3 = extra_vars.get("var3","-")
                        var4   = extra_vars.get("var4","-")
                        var5   = extra_vars.get("var5","-")
                        var6   = extra_vars.get("var6","-")
                        var7 = extra_vars.get("var7", "-")
                        

#                     Print output for check which data pushed DB.
                        print("Job ID:",Job_Id)
                        print("Domino ID:",domino_id)
                        print("Job Name",Name)
                        print("Job Date",Date)
                        print("var1",var1)
                        print("var2",var2)
                        print("var3",var3)
                        print("var4:",var4)
                        print("var5:",var5)
                        print("var6:",var6)
                        print("var7:",var7)
                        print("---------------------------------------\n---------------------------------------")
                        
                    except json.JSONDecodeError:
                        print("extra_vars content is not valid JSON.")
                else:
                    print("No 'extra_vars' found in the API response.")
            else:
                print("")


            insert_query = "INSERT INTO TABLE_NAME (Job_Id,Domino_ID,Name,Date,var1,var2,var3,var4,var5,var6,var7 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (Job_Id, domino_id, Name, Date, var1, var2, var3, var4, var5, var6, var7))

            time.sleep(1)
            pass
        except Exception as e:
            print(f"An error occured: {str(e)}")
 
finally:
    conn.commit()
    conn.close()
