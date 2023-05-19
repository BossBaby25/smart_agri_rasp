from pymongo import MongoClient

# MongoDB connection settings
mongodb_host = 'localhost'
mongodb_port = 27017

# Connect to MongoDB
client = MongoClient(mongodb_host, mongodb_port)

# Access a database and collection
db = client['mydatabase']
collection = db['mycollection']

# Perform MongoDB operations
document = {'name': 'John', 'age': 30}
collection.insert_one(document)

# Close MongoDB connection
client.close()
