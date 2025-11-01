## What I am using to implement:
- Python 
- collections.OrderedDict
- threading
- time
- Singleton Design Pattern
- threading.Lock

## Approach:
There can be two approaches to implement an in-memory cache with TTL and LRU eviction policy. 
1. On expired time cleanup using a background thread.
2. On access cleanup. 

Both approaches have their pros and cons.
1. On expired time cleanup:
   ### Pros: 
   - The cache size is controlled more strictly as expired items are removed in the background.
   - We get more predictable memory usage.
   ### Cons: 
   - Requires a background thread which adds complexity and resource usage.
   - Required continues monitoring of the cache which may not be necessary for all use cases. If we want seconds precision on TTL, this approach required more lookups.
2. On access cleanup:
    ### Pros: 
    - Simpler implementation without the need for a background thread.
    - Simply check and delete the expired items when accessing the cache.
    ### Cons: 
    - Cache size may temporarily exceed the limit until the next access.
    - Memory will not be freed until next access.
    
Looking at the pros and cons, I have implemented the combination of both approaches. A background thread to cleanup expired items at 60 second intervals (as most of the keys have this ttl expected) and also checking for expired items on access(for ttl less than 60 sec). This way we can ensure that the cache size is controlled more strictly while also keeping the implementation relatively simple.

To implement an in-memory cache with TTL (Time-To-Live) and LRU (Least Recently Used) eviction policy, we can use Python's `OrderedDict` from the `collections` module. This allows us to maintain the order of insertion and efficiently manage the cache size.

> OrderedDict internally used doubly linked list to maintain the order of keys, which helps in implementing LRU cache efficiently.

> it's Average time complexity for get, set and move_to_end operations is O(1).

I maintain two `OrderedDict`s:
1. `cache`: to store the actual key-value pairs.
2. `timestamps`: to store the timestamps of when each key was added or last accessed.

and a LRU size limit to control the maximum number of items in the cache.

now lets undetstand each operations one by one:

### Set Operation:
- First we check if we are in the limit of LRU(Least Recently Used) size, if not we evict the least recently used item.
- Then we add the new key-value pair to the `cache` and record the current timestamp in the `timestamps` dictionary. 
- `cache` will be used as key value storage and LRU implementation while `timestamps` will be used to track the age of each item for TTL management.
- As we used the `OrderedDict`, the new key will be added to the end of the order, marking it as the most recently used.

### Get Operation:
- When retrieving a value, we first check if the key exists in the `cache`.
- If it exists, we check if the item has expired by comparing the current time with the stored timestamp(TTL).
- If the item has expired, we remove it from both `cache` and `timestamps`, and return `None`.
- If the item is still valid, we update its position in the `cache` to mark it as recently used using `move_to_end` method and return the value.

### Auto Cleanup:
- A background thread runs periodically to clean up expired items from the cache.
- This thread sleeps for a defined interval (e.g., 60 seconds) and then iterates through the `timestamps` dictionary to remove any items that have exceeded their TTL.
- It first sort the items based on their timestamps to ensure we are checking the oldest items first, which is more efficient.
> As we will be checking each 60 second, the sorting complexity of O(n log n) will be acceptable here.

### Delete Operation:
- The delete operation simply removes the specified key from both the `cache` and `timestamps` dictionaries if it exists.

### Clenup Operation:
- It cleans up the entire cache by clearing both the `cache` and `timestamps` dictionaries.

### Thread Safety:
- To ensure thread safety, especially when multiple threads might be accessing or modifying the cache simultaneously, we use a threading lock (`self._lock`).
- This lock is acquired before any modification to the `cache` or `timestamps` and released afterward

### Singleton Pattern:
- The `InMemoryCache` class is implemented as a singleton to ensure that only one instance of the cache exists throughout the application.


