from engine.tree_searcher import TreeSearcher


AI = TreeSearcher(4)


with open("test/test.txt", "r") as f:
    print(AI.get_best_recommendation(f.read()))
