D1 = {'ok': 1, 'nok': 2}
D2 = {'ok': 2, 'new': 3}
D_UNION = D1 | D2
print(f"D_UNION: {D_UNION}")

D_INTERSECTION = D1.keys() & D2.keys()
D_INTERSECTION = {key: D1.get(key, D2.get(key)) for key in D_INTERSECTION}
print(f"D_INTERSECTION: {D_INTERSECTION}")


D_DIFF = D1.keys() - D2.keys()
D_DIFF = {key: D1[key] for key in D_DIFF}
print(f"D1 - D2: {D_DIFF}")

D_MERGE = {}
for k, v in D1.items():
    D_MERGE[k] = D_MERGE.get(k, 0) + v
for k, v in D2.items():
    D_MERGE[k] = D_MERGE.get(k, 0) + v
print(f"D_MERGE: {D_MERGE}")
