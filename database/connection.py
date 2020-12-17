from pymongo import MongoClient
from bson.objectid import ObjectId


class DBConnection:
    def __init__(self):
        # self.client = MongoClient(
        #     "mongodb+srv://robbyyt:proiectsgbd@cluster0.zhrr2.mongodb.net/encrypteddatabase?retryWrites=true&w=majority"
        # )
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["encrypteddatabase"]
        self.file_collection = self.db["files"]

    def add_one_file(self, file):
        return self.file_collection.insert_one(file).inserted_id

    def delete_one_file(self, file_id):
        return self.file_collection.delete_one({'_id': ObjectId(file_id)}).deleted_count

    def get_file_by_id(self, file_id):
        found = self.file_collection.find({'_id': ObjectId(file_id)})
        documents = []
        for doc in found:
            documents.append(doc)

        return documents


if __name__ == '__main__':
    conn = DBConnection()
    fid = conn.add_one_file({"key": "value"})
    # print(conn.delete_one_file("5fd949e3edf8df2e4bfa6cdb"))
    files = conn.get_file_by_id(fid)
    print(files)
