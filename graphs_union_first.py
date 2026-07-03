"""
Union first
- Compter les composantes connexes
- Détecter un cycle
- Détecter si deux points sont connectés
"""
def find(a, parents):
    """Find the root of node a"""
    while parents[a] != a:
        parents[a] = parents[parents[a]]
        a = parents[a]
    return a

def union(a,b, parents):
    ra,rb = find(a, parents), find(b, parents)
    if ra == rb:
        return True
    parents[ra] = rb
    return False

def count_connexes(links):
    nodes = set(n for l in links for n in l )
    parents = {node: node for node in nodes}

    for l in links:
        union(l[0], l[1], parents)

    count = 0
    for k,v in parents.items():
        if k == v:
            count += 1
    
    return count

def is_cycle(links):
    nodes = set(n for l in links for n in l )
    parents = {node: node for node in nodes}

    for l in links:
        if union(l[0], l[1], parents):
            return True
    return False


links = [[0,1], [1,2], [2,0], [3,4], [5,6], [6,7], [5,3]]
print("Number of connexes: ", count_connexes(links))
print("There is a cycle: ", is_cycle(links))

nodes = set(n for l in links for n in l )
parents = {node: node for node in nodes}
for l in links:
    union(l[0], l[1], parents)
print("0 et 2 connectés?: ", find(0,parents)==find(2,parents))
print("0 et 5 connectés?: ", find(0,parents)==find(5,parents))
