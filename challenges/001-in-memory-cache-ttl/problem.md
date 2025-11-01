# Day 001: Build an In-Memory Cache with TTL

**Date**: 2024-11-01  
**Difficulty**: Medium  
**Category**: Backend  
**Estimated Time**: 3-4 hours

## 🎯 Core Concept

Understanding **caching strategies**, **time-based expiration**, and **memory management**. This challenge will help you think about performance optimization and data lifecycle management - critical skills for building scalable applications.

## 🌍 Real-World Context

Every major application uses caching to reduce database load and improve response times. Redis, Memcached, and built-in application caches all implement TTL (Time To Live) mechanisms. Understanding how to build one from scratch will help you:
- Make better decisions about when and how to cache data
- Debug caching issues in production
- Optimize application performance
- Understand trade-offs between memory usage and speed

Companies like Netflix, Amazon, and Google use sophisticated caching layers that handle millions of requests per second. This is your foundation.

## 📋 Problem Statement

Build an in-memory cache system that stores key-value pairs with automatic expiration based on TTL (Time To Live). Your cache should efficiently manage memory and clean up expired entries.

### Requirements

1. **Basic Operations**:
   - `set(key, value, ttl)` - Store a key-value pair with TTL in seconds
   - `get(key)` - Retrieve value if key exists and hasn't expired
   - `delete(key)` - Remove a specific key
   - `clear()` - Remove all entries

2. **TTL Management**:
   - Each entry should expire after its TTL
   - Expired entries should not be returned by `get()`
   - Implement automatic cleanup of expired entries

3. **Additional Features**:
   - `has(key)` - Check if a non-expired key exists
   - `size()` - Return count of non-expired entries
   - `keys()` - Return array of all non-expired keys

### Constraints

- Must handle at least 10,000 entries efficiently
- Expired entries should be cleaned up automatically (not just on access)
- Thread-safe operations are NOT required (single-threaded is fine)
- Choose any programming language you're comfortable with

## ✅ Success Criteria

Your solution should:
- [ ] Pass all basic operation tests (set, get, delete, clear)
- [ ] Correctly handle TTL expiration (entries expire after specified time)
- [ ] Implement background cleanup mechanism
- [ ] Handle edge cases (expired keys, non-existent keys, zero/negative TTL)
- [ ] Include meaningful test cases demonstrating functionality
- [ ] Be well-documented with comments explaining key decisions

## 🚀 Bonus Challenges (Optional)

If you want to push further:
1. **Max Size Limit**: Implement LRU (Least Recently Used) eviction when cache reaches max capacity
2. **Statistics**: Track hit rate, miss rate, and eviction count
3. **Persistence**: Add ability to save/load cache state to/from disk
4. **TTL Refresh**: Implement `touch(key)` to reset a key's TTL without changing its value

## 💡 Hints & Resources

<details>
<summary>Click to see hints (try solving first!)</summary>

- **Hint 1**: Consider using a combination of a hash map for O(1) lookups and a priority queue or sorted structure for efficient expiration tracking
- **Hint 2**: For automatic cleanup, think about using timers/intervals or checking expiration lazily on access
- **Hint 3**: Store both the value AND the expiration timestamp with each entry
- **Hint 4**: Edge case to consider - what happens if someone sets TTL to 0 or negative number?

**Concept Reference**: 
- [Caching Strategies](https://aws.amazon.com/caching/)
- [Time-based expiration patterns](https://redis.io/commands/expire/)

</details>

## 📚 Keywords

`caching` `TTL` `data-structures` `performance` `memory-management` `expiration` `hash-map`

---

## 🎓 What You'll Learn

- How caching systems work under the hood
- Memory management and cleanup strategies
- Time-based data expiration patterns
- Performance optimization techniques
- Trade-offs between different cleanup approaches

---

**Next Steps**: 
1. Read the problem carefully
2. Plan your approach (what data structures will you use?)
3. Implement your solution
4. Test thoroughly with edge cases
5. Document your learning in `solution.md`
6. Share your insights on Dev.to and LinkedIn!

**Good luck! You've got this! 🚀**

---

**Remember**: The goal isn't just to complete the challenge, but to understand WHY each decision matters. Think about real-world applications as you build!