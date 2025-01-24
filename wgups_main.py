#class for hash table with collision handling capabilities via chaining
class ChainingHashTable:

    #constructor initializing table with empty lists
    def __init__(self, capacity = 10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    #method for insertions and updates
    def insert(self, key, value):

        #assings an index generated via the built in hash function
        bucket = hash(key) % len(self.table)
        #assings whatever is in that index
        bucket_list = self.table[bucket]

        #check if kv pair already in bucket_list
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        #else append to bucket_list
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    #method for searching via key
    def search(self, key):

        #figures out where this key would be in the list
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #search list via key and return value if found
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]

        #else return None
        return None

    #method for removing via key
    def remove(self, key):

        #figures out where this key would be in the list
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        #search list via key and remove both kv if found
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])


h = ChainingHashTable()
h.insert