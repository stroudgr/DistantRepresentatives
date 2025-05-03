# Distant Representatives

Code for ORIE 6125 Final Project.

In the distant representatives problem, given input shapes in the plane, the goal is to place one point in each shape so that the points are as far apart from each other as possible. 


During my Master's program at the University of Waterloo, I helped discover an approximation algorithm when the shapes are rectangles, see the paper [here](https://drops.dagstuhl.de/opus/volltexte/2021/14598/). 

Beyond the scope of that paper,
I decided to implement this algorithm in Python.
The coding involved implementing an algorithm for maximal matching in a bipartite graph, and performing a special form of binary search.

Additionally, I've implemented a visualization tool for the problem using the FabricJs drawing library and a Flask backend server. 

To run locally:

```
pip install -r "requirements.txt"
flask --app DRflask run
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000)

<!--Try the demo page: [https://stroudgr.github.io./projects/distant-representatives/dr-demo.html](https://stroudgr.github.io./projects/distant-representatives/dr-demo.html)-->
