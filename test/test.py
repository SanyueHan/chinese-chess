from time_analyzer.timer import Timer

from config import AI_SEARCH_DEPTH
from engine.tree_searcher import TreeSearcher


AI = TreeSearcher(AI_SEARCH_DEPTH)


with open("test/test.txt", "r") as f:
    print(AI.get_best_recommendation(f.read()))

Timer.explain_performance_by_name()
