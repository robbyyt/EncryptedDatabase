from pymongo import MongoClient


class DBConnection:
    """
    Establishes a connection to the MongoDB Database and provides methods for adding, retrieving and deleting a file.
    """
    def __init__(self):
        # self.client = MongoClient(
        #     "mongodb+srv://robbyyt:proiectsgbd@cluster0.zhrr2.mongodb.net/encrypteddatabase?retryWrites=true&w=majority"
        # )
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["encrypteddatabase"]
        self.file_collection = self.db["files"]

    def add_one_file(self, file):
        """
        :param file:
        An object that will store useful information that will be needed when decrypting the file.
        :return:
        The id (generated by MongoDB) of the inserted file.
        """
        return self.file_collection.insert_one(file).inserted_id

    def delete_one_file(self, file_id):
        """
        :param file_id:
        UID of the file that we want to delete.
        :return:
        The number of deleted files.
        """
        return self.file_collection.delete_one({'uid': file_id}).deleted_count

    def get_file_by_id(self, file_id):
        """
        :param file_id:
        UID of the file that we want to retrieve.
        :return:
        Array of documents that match the uid given as input.
        """
        found = self.file_collection.find({'uid': file_id})
        documents = []
        for doc in found:
            documents.append(doc)

        return documents
