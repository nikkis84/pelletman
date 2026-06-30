CMPT 310 – Pelletman
Matthew, Niki, Nur, Cyprian
Files
main.py -> game loop + visualization
env.py -> environment + evaluation
minimax.py -> minimax search
ghost.py -> ghost movement
parser.py -> map loading
maps -> maze files
How to Run Documentation
1. Installation
pip install pygame
2. Running
python main.py
3. Fine-tuning
## Map Selection:
    - In the file main.py, at line number 99 change file path to the desired map#
    - Loads different grid layouts

## Depth Selection:
    - In the file main.py, at line number 103 change depth # 
    - Higher depths, Pelletman can see more moves in the future (Can affect performance)
