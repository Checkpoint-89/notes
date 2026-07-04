def bfs(src, dst, graph):
    """
    BFS - Itératif
    - Plus court chemin dans un graphe non pondéré
    - Niveau dans un arbre - trouver tous les noeuds à distancek d'un noeud
    - Propagation - feu qui se propage, infection, nombre de pas pour remplir qqch
    - Word ladder - changer un mot en un autre, lettre par lettre, en un nombre minimale d'étapes
    """
    seen = {src}
    fifo = deque([(src, 0)])  # (nœud, distance)
    
    while fifo:
        node, dist = fifo.popleft()
        if node == dst:
            return dist
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                fifo.append((neighbor, dist + 1))
    
    return -1