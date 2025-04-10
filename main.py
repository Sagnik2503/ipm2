import os
from crewai import crew
for file in [
    'output/project_overview.json',
    'output/market_analysis.json'
]:
    if os.path.exists(file):
        os.remove(file)
        
try:
    crew().kickoff()
except Exception as e:
    print("💥 CrewAI execution failed!")
    print(e)

