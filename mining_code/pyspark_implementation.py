from pymongo import MongoClient
from pprint import pprint
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("app") \
    .getOrCreate()

client = MongoClient(port=27017)
print(client)
db=client.project_db
coll = db.drugs
print(coll)
sample=coll.find({}, {id:0})
print(sample)
json_projects = []
for project in sample:
    json_projects.append(project)
# json_projects = json.dumps(json_projects, default=json_util.default)
# sample = db.drugs.find({}).count()
# print(json_projects)
# df = spark.createDataFrame(json_projects)
# print(df)
# print(sample)
# serverStatusResult=db.command("serverStatus")
# # pprint(serverStatusResult)
# print(serverStatusResult)