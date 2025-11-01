from collections import OrderedDict
import time
import threading

class InMemoryCacheTTL:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.cache: OrderedDict[str, str] = OrderedDict()
            self.timestamps: OrderedDict[str, float] = OrderedDict()
            self._lru_size = 3
            self._lock = threading.Lock()
            self._cleanup_interval = 60
            self._cleanup_thread = threading.Thread(
            target=self._auto_cleanup, daemon=True)
            self._cleanup_thread.start()
            self._initialized = True
    
    def _auto_cleanup(self):
        while True:
            time.sleep(self._cleanup_interval)
            with self._lock:
                self.delete_expired_keys()

    def delete_expired_keys(self):
        current_time = time.time()
        self.timestamps.update(sorted(self.timestamps.items(), key=lambda item: item[1]))
        while self.timestamps:
            key, expiry_time = next(iter(self.timestamps.items()))
            if expiry_time < current_time:
                self.cache.pop(key, None)
                self.timestamps.pop(key, None)
            else:
                break
    
    def get_key(self, key: str):
        with self._lock:
            if key in self.cache:
                value = self.cache[key]
                expiry_time = self.timestamps[key]
                if expiry_time >= time.time():
                    self.cache.move_to_end(key)
                    return value
                else:
                    self.cache.pop(key, None)
                    self.timestamps.pop(key, None)
                    return None

    def set_key(self, key: str, value: any, ttl: int = 60):
        if ttl <= 0:
            raise ValueError("TTL must be a positive integer")
        with self._lock:
            if len(self.cache) >= self._lru_size:
                poped_item_key, _ = self.cache.popitem(last=False)
                self.timestamps.pop(poped_item_key, None)
            current_time = time.time()
            expiry_time = current_time + ttl
            self.cache[key] = value
            self.timestamps[key] = expiry_time
    
    def delete_key(self, key: str):
        with self._lock:
            self.cache.pop(key, None)
            self.timestamps.pop(key, None)
    
    def clear_cache(self):
        with self._lock:
            self.cache.clear()
            self.timestamps.clear()


def main():
    cache = InMemoryCacheTTL()
    print("🧪 Running Cache Tests...\n")

    # Test 1: Basic set/get
    cache.set_key("user", "kevin", 3)
    assert cache.get_key("user") == "kevin"
    print("✅ Test 1 Passed: Basic set/get")

    # Test 2: TTL expiry
    print("⏳ Waiting for key expiry (3s)...")
    time.sleep(4)
    assert cache.get_key("user") is None
    print("✅ Test 2 Passed: TTL expiry works")

    # Test 3: LRU eviction (capacity = 3)
    cache.set_key("a", "A")
    cache.set_key("b", "B")
    cache.set_key("c", "C")
    cache.set_key("d", "D")  # should evict "a"
    assert "a" not in cache.cache
    print("✅ Test 3 Passed: LRU eviction works")

    # Test 4: Access order update
    cache.get_key("b")  # access "b" -> most recently used
    cache.set_key("e", "E")  # should evict "c"
    assert "c" not in cache.cache
    print("✅ Test 4 Passed: Access order maintained")

    # Test 5: Auto cleanup thread
    cache.set_key("temp", "123", 2)
    time.sleep(3)
    assert cache.get_key("temp") is None
    print("✅ Test 5 Passed: Auto cleanup thread removes expired keys")

    print("\n🎉 All tests passed successfully!")


if __name__ == "__main__":
    main()
    