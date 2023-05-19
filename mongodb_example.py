from pymongo import MongoClient

# MongoDB connection settings
mongodb_uri = "mongodb+srv://meraj154213:iCFmmhPjFdUk2hvV@cluster0.hj5abn5.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(mongodb_uri)

# Access a database and collection
db = client['mydatabase']
collection = db['testdb']

# Perform MongoDB operations
document = {'name': 'John', 'age': 30}
collection.insert_one(document)

# Close MongoDB connection
client.close()
