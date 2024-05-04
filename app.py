from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
import csv
import codecs
import uvicorn
import os
import yaml
import time
import pandas as pd
import openpyxl

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
timestr = time.strftime("%Y%m%d-%H%M%S")

#####
def convert_yaml(file):
    file=open(file)

    x = csv.reader(file)
    file_arr=[]
    for  r in x :
        file_arr.append(r)
#####

#def xlsx_to_csv(file):
    #data_xls = pd.read_excel(file, index_col=None)
    #data_xls.to_csv("xlsxCSV.csv", encoding='utf-8', index=False)

#####    

@app.get("/Welcome")
def read_root():
    return {"Hello":"User"}

@app.post("/upload")
def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file = pd.read_excel(file.file.read(), index_col=0).to_dict()
    #print(f"file {file}")
    #background_tasks.add_task(file.file.close)
    return (file)

@app.post("/file/uploadndownload")
def upload_n_downloadfile(file: UploadFile):
    file1 = pd.read_excel(file.file.read(), index_col=0).to_dict()
    #pickling_on = open("csvReader.pickle","wb")
    #pickle.dump(csvReader, pickling_on)
    #pickling_on.close()
    new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0], timestr)
        # Write the data to a file
        # Store the saved file
    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
    with open(SAVE_FILE_PATH, "w") as f:
            yaml.dump(file1, f)

        # Return as a download
    return FileResponse(
            path=SAVE_FILE_PATH,
            media_type="application/octet-stream",
            filename=new_filename)    
     