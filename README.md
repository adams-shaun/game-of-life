A GAME OF LIFE

Simple implementation of Conway's game of life, with a few caveats:
* Board is not 'infinite', rather bound by the size of user-defined grid
* No boundary conditions implemented for grid boundary life evaluations

High Notes
* Some implementation details may be non-ideal, there are reasons for this
    * Display as much knowledge of modern OOP python as possible
    * time limitations
* Used the standard libraries to simplify things

Things I would like to Add
* Put this library behind an API (JSON-RPC maybe?)
* Containerize the web server and build a javascript front-end to visualize simulations
* More (any) logging.
* Static analysis stack (mypy, pycodestyle, pylint, etc.)
* More testing, CICD pipeline definitions
    
To Run
* ./gol.py -h for more information
* ./gol.py --infile example.json for a quick & stable spin
* ./gol.py for randomly generated board of default size