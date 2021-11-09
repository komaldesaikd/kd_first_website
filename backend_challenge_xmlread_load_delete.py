from flask import Flask,request
import pymongo
import xmltodict
import os
import yaml

app=Flask(__name__)


def yaml_loader(filepath):
    with open(filepath) as ipfile:
        data=yaml.load(ipfile, Loader=yaml.FullLoader)
    return data  
      
        
        
@app.route('/', methods=['GET','POST'])
def home():
    if(request.method == 'GET'):  
        data = "WELCOME!!!"
        return(data)    
    
@app.route('/load-data/<folder>/', methods=['GET'])
def loadData(folder):
 if(request.method == 'GET'):
  try:
   file_path=base_path+folder   
   files=os.listdir(file_path)   
   for file in files:
    filecompath=file_path+'\\'+file    
    
    with open(filecompath, encoding='utf8') as xmlfile:    
            obj=xmltodict.parse(xmlfile.read())
            query = SampleTable.insert_many([obj])            
   return "XML Files Data inserted in the Mongodb ...!!!"
  except Exception as e:
        print('File Not readable !!!',e)

@app.route('/delete-data/<folder>/', methods=['GET'])
def deleteData(folder):
     if(request.method == 'GET'):   
       try:  
         file_path= base_path + folder
         files=os.listdir(file_path)         
         for file in files:
             filecompath=file_path+'\\'+file                             
             with open(filecompath, encoding='utf8') as xmlfile: 
                    obj=xmltodict.parse(xmlfile.read())
                    query = SampleTable.delete_one(obj)         
         return "XML Files Deleted from Mongodb...!!!" 
       except Exception as e:
        print('File Not readable !!!',e)
    
@app.errorhandler(404)
def page_not_found(e):
    return("Provided page is not available, Please enter Valid URL!!!")  

@app.errorhandler(500)
def folder_not_found(e):
    return("Provided Directory is unavailable, Please provide correct directory!!!")       

if __name__=='__main__':
 try:
    file_path="data.yaml"
    data=yaml_loader(file_path)         
    connection_url=data['db_conn_url']
    base_path=data.get('base_path')
    db=data.get('db_nm')
    #db_coll=data.get('db_coll')
    client = pymongo.MongoClient(connection_url)
    Database = client.get_database(db)
    SampleTable = Database.xmldata
 except NameError as e:
    print('NameError',e)    
 except Exception as e:
    print('Some issue with Input Data or Database Connection!!!',e)
       
 app.run()