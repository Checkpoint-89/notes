# 1-sweep line
tasks = [(0, 30), (5, 10), (15, 20)]
def sweepline(tasks):
    starts = sorted((t[0] for t in tasks))
    ends = sorted((t[1] for t in tasks))
    s = 0
    e =0
    sweepline = [0]
    while s < len(starts) and e < len(ends):
        if starts[s] < ends[e]:
            s += 1
            sweepline.append(sweepline[-1]+1)
        else: 
            e += 1
            sweepline.append(sweepline[-1]-1)
    return max(sweepline)

# 2-heap
tasks = [(5, 10), (0, 30), (15, 20)]
def heap(tasks):
    import heapq
    tasks = sorted(tasks, key=lambda x: x[0])
    rooms = []

    for start, end in tasks:
        if rooms and rooms[0] < start:
            heapq.heapreplace(rooms, end) # libère la salle, réutilise
        else:
            heapq.heappush(rooms, end)
    return len(rooms)

# 3-hashmap
words = ["le", "chat", "est", "sur", "le", "tapis", "le", "chat", "est"]
def hashmap(words):
    from collections import defaultdict
    d = defaultdict(int)
    for w in words:
        d[w] += 1
    return sorted(d, key=lambda x: (-d[x], x))[:2]

# 4-sliding window (flexible size)
s = "aaaaa"
def sliding_w_flex(s):
    seen = {}
    longest = ""
    l = 0
    for r, c in enumerate(s):
        if c in seen and seen[c] >= l:
            l = seen[c] + 1
        seen[c] = r
        if r - l + 1 > len(longest):
            longest = s[l:r+1]
    return longest

# 5-sliding window (fixed size)
nums = [2, 1, 5, 1, 3, 2]
def sliding_window_fix(nums):
    k = 3
    l, r = 0, k
    cur_sum = sum(nums[l:r])
    max_sum = cur_sum
    while r<len(nums):
        l = l+1
        cur_sum = cur_sum - nums[l-1] + nums[r]
        max_sum = max(max_sum, cur_sum)
        r = r + 1
    return max_sum

# 6-target from unsorted list
nums = [11, 7, 2, 15]
target = 9
def target_unsorted(nums, target):
    seen = {}
    for i,n in enumerate(nums):
        if target - n in seen:
            return (seen[target-n], i)
        else:
            seen[n] = i
    return(-1, -1)

# 7-target from sorted list
nums = [2, 7, 11, 15]
target = 9
def target_sorted(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return (l,r)
        elif s < target:
            l += 1
        else:
            r -= 1
    return (-1, -1)

target_sorted(nums, target)

# 8-target with triplets
nums = [-1, 0, 1, 2, -1, -4]
target = 0
def triplets(nums, target):
    nums = sorted(nums)
    triplets = []
    for i, n in enumerate(nums[:-2]):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        t = target - n
        l, r = i+1, len(nums) - 1
        while l < r:
            s = nums[l] + nums[r]
            if s == t:
                triplets.append((nums[i], nums[l], nums[r]))
                while l < r and nums[l] == nums[l+1]:
                    l += 1
                while l < r and nums[r] == nums[r-1]:
                    r -= 1
                l += 1
                r -= 1
            elif s < t:
                l += 1
            else:
                r -= 1
    return triplets

# 9-duplicates
nums = [1, 2, 3, 4, 5, 6, 7, 2, 3]
k = 3
def dups(nums, k):
    seen = set()
    for i, n in enumerate(nums):
        if n in seen:
            return True
        seen.add(n)
        if len(seen) > k:
            seen.remove(nums[i - k])
    return False

dups(nums, k)   

# 10-sum_interval
nums = [1, 3, 2, 5, 1, 2]
target = 8
def sum_interval(nums, target):
    l = 0
    s = 0
    for r in range(len(nums)):
        s += nums[r]
        while s > target and l <=r:
            s -= nums[1]
            l += 1
        if s == target:
            return (l,r)
    return (-1,-1)

# 11-sum_interval2
nums = [1, 3, 2, 5, 1, 2]
k = 3
def sum_interval2(nums, k):
    s = sum(nums[0:k])
    sums = [s]
    for l in range(1,len(nums) - k + 1):
        s -= nums[l-1]
        s += nums[l+k-1]
        sums.append(s)
    return sums

# 12-prexix_0
nums = [3, 1, 1, -4, 2, 1]
def prefix_0(nums):
    seen = {0}
    s = 0
    for n in nums:
        s += n
        print(s, seen)
        if s in seen:
            return True
        seen.add(s)
    return False

# 13-prexix_2
nums = [3, 1, 1, -4, 2, 1]
target = 3
def prefix_2(nums):
    from collections import defaultdict
    seen = defaultdict(int)
    seen[0] = 1
    s = 0
    count = 0
    for n in nums:
        s += n
        count += seen[s - target]
        seen[s] += 1
    return count

# 14-heap_1
tasks = [(3, "envoyer email"), (1, "faire café"), (5, "déployer prod"), (2, "réunion")]
def heap_1(tasks):
    import heapq
    h = [(-p, name) for p, name in tasks]
    heapq.heapify(h)
    return [heapq.heappop(h)[1] for _ in range(len(h))]

# 15-heap_2
nums = [9, 1, 5, 7, 2, 3, 4]
k = 3
def heap_2(nums, k):
    import heapq
    h = []
    for n in nums:
        heapq.heappush(h,n)
        if len(h) > k:
            heapq.heappop(h)
    return h

# 16-mediane
stream = [5, 3, 8, 1, 9]
def mediane(stream):
    import heapq
    max_heap = []
    min_heap = []

    for item in stream:
        heapq.heappush(min_heap, item)
        if max_heap and min_heap[0] < -max_heap[0]:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))

        if len(min_heap) > len(max_heap) + 1:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
        elif len(min_heap) < len(max_heap):
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        
        if len(min_heap) == len(max_heap):
            yield (-max_heap[0] + min_heap[0]) / 2
        else:
            yield min_heap[0]

# 17-backtracking 1
sequences = []
n = 3
def get_seq(n, open=0, close=0, seq=""):
   
    if open == n and close == n:
        sequences.append(seq)
        return
    if open < n:
        get_seq(n, open=open+1, close=close, seq=seq+'(')
    if open > close:
        get_seq(n, open=open, close=close+1, seq=seq+')')

get_seq(n, open=0, close=0, seq="")   

# 18-backtracking 2
nums = [1, 2, 3]
sequences = []
def get_seq(nums, perm=[]):
    if len(nums) == 0:
            sequences.append(perm[:])
            return
    for i,num in enumerate(nums):
        perm.append(num)
        get_seq(nums[:i] + nums[i+1:], perm = perm)
        perm.pop()
get_seq(nums, perm=[])
sequences

# 19-backtracing 3
nums = [2, 3, 6, 7]
target = 7
sequences = []
def get_seq(nums, seq, s, target):
    if s == target:
        sequences.append(seq[:])
        return
    if s > target:
        return
    for i, n in enumerate(nums):
        seq.append(n)
        get_seq(nums[i:], seq, s + n, target)
        seq.pop()
get_seq(nums, [], s=0, target=target)
sequences

# 20-islands
from itertools import product
grid = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1]
]

def find_islands(grid):
    rows = len(grid)
    columns = len(grid[0])
    coord = list(product(range(rows), range(columns)))

    parents = {(i,j): (i,j) for i,j in coord}


    def find(x):
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parents[ry] = rx

    for i,j in coord:
        if grid[i][j] == 1:
            if i+1 < rows and grid[i+1][j] == 1:
                union((i,j), (i+1,j))
            if j+1 < columns and grid[i][j+1] == 1:
                union((i,j), (i,j+1))

    islands = {find(node) for node in parents if grid[node[0]][node[1]] == 1}
    return len(islands)