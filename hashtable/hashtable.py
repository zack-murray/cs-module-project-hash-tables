class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        if capacity < MIN_CAPACITY:
            self.capacity = MIN_CAPACITY
        else:
            self.capacity = capacity
        self.key_count = 0
        self.storage = [None] * capacity

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # The load factor is the number of keys stored in the hash table divided by the capacity
        return self.key_count / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for character in key:
            hash = (hash * 33) + ord(character)

        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Instantiate index key  
        index = self.hash_index(key) 
        if self.storage[index] is None:
            # If list is empty, add entry
            self.storage[index] = HashTableEntry(key, value)
            # Increase the key count
            self.key_count += 1
            # If load factor > 0.7
            if self.get_load_factor() > 0.7:
                # Double the size of the hash table 
                self.resize(self.capacity * 2)
        else: 
            # Set current pointer to index key 
            cur = self.storage[index]
            while cur is not None:
                # Check node for same key
                if cur.key == key:
                    # If same key, replace with new value
                    cur.value = value
                    return
                # If node after pointer is none
                if cur.next is None:
                    # Break so position isn't lost 
                    break
                cur = cur.next
            # Node not found, append to the end of the list
            cur.next = HashTableEntry(key, value)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        # If list is empty 
        if self.storage[index] is None:
            return (f'Warning, key not found in the hash table')
        else:
            # If found and only entry
            if self.storage[index].next is None:
                # Effectively delete it
                self.storage[index] = None
                # Decrease the key count
                self.key_count -= 1 
                return
            else:
                # Set current pointer
                cur = self.storage[index]
                # If current node is the key
                if cur.key == key:
                    # Remove it and decrease key count
                    self.storage[index] = self.storage[index].next
                    self.key_count -= 1
                    return 
                # If current node isn't key and next node isn't None
                while cur.next is not None:
                    # Traverse down list and check if next node = key 
                    if cur.next.key == key:
                        # Remove it and decrease key count
                        cur.next = cur.next.next
                        self.key_count -= 1
                        return
                    # If still not found, keep traversing
                    cur = cur.next
                # Key not found at location
                return (f'Warning, key not found at location')
                



    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        # If hash table is empty
        if self.storage[index] is None:
            return None
        else:
            # Set current pointer
            cur = self.storage[index]
            # Start traversing
            while cur is not None:
                # Check each node's key as you traverse
                if cur.key == key:
                    return cur.value
                # If still not found, keep traversing
                cur = cur.next
            # Return None if key is not found
            return None
        

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Instantiate old storage as a copy of itself
        old_storage = self.storage.copy()
        # Set new capacity, key count, storage
        self.capacity = new_capacity
        self.key_count = 0
        self.storage = [None] * self.capacity
        # Rehash old storage into new hash table
        for node in old_storage:
            while node is not None:
                self.put(node.key, node.value)
                node = node.next



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
