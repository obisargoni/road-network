
from matplotlib import pyplot as plt
from QuadTree import QuadTree
import Util
import globals
import numpy as np
import random
import os
import sys

def main(size=10, max_nodes=800, seed = 1, outdir = "../"):
	"""
	if squares are not fully forming increase plane size
	:param size:
	:param max_nodes:
	:return:
	"""
	print( "size: "+str(size))
	print( "max_nodes: "+str(max_nodes))
	print( "seed: "+str(seed))

	random.seed(seed)

	globals.init()
	X=Util.getPlane(size)

	mins = (0.0, 0.0)
	maxs = (size-1.0, size-1.0)

	QT = QuadTree(X, mins, maxs, 0,0)

	QT.add_square()

	print( "Generating road network...")
	# for high density choose ones counter depth with highest number of squares randomly
	while(True):
		node=random.randrange(max(globals.node_index))
		if len(globals.node_index)>max_nodes: # limit network generation by number of nodes
			break

		Util.add_square_at(QT,node)

	#Util.printStats(globals.node_index)
	#Util.bfs_print(QT)

	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111)
	ax.set_xlim(0, size-1.0)
	ax.set_ylim(0, size-1.0)

	# for each depth generate squares
	print( "generating squares...")
	for d in range(0,len(globals.node_index)):
		QT.draw_rectangle(ax, depth=d)

	print( "writing data to files...")
	fn = open( os.path.join(outdir,'node-list'),'w')
	fe = open( os.path.join(outdir,'edge-list'),'w')

	edgeCount=0 #directed edge count
	for point in globals.edges:
		if point in globals.coord_id:
			fn.write(str(globals.coord_id[point])+","+str(point.x)+","+str(point.y)+"\n")

		for edge in globals.edges[point]:
			fe.write(str(globals.coord_id[point])+","+str(globals.coord_id[edge])+"\n")
			edgeCount=edgeCount+1

	fn.close()
	fe.close()

	print( "# of edges: "+str(edgeCount))

	plt.savefig(os.path.join(outdir, 'rand-quad-road-network.png'))

	dir_path = os.path.dirname(os.path.realpath(outdir))

	print( "generate road network image at: "+ dir_path + "/rand-quad-road-network.png")
	print( "node list at: "+ dir_path + "/node-list")
	print( "edge list at: "+ dir_path + "/edge-list")

	print( "Done")


if __name__ == "__main__":
	main(int(sys.argv[1]), int(sys.argv[2]))