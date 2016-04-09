from graph import Graph;
from collections import Counter;
from itertools import dropwhile;
import config;

class Error :
    numNodes = 0;

    # 1s present in G but not in M    
    numUnmodelledErrors = 0;
    unmodelled = [];
    numUnmodelledErrorsOld = 0;
    unmodelledOld = [];
    

    # incorrect cell values in M wrt G
    numModellingErrors = 0;
    modelled = [];
    numModellingErrorsOld = 0;
    modelledOld = [];

    # number of unique cells in M
    numCellsCovered = 0;
    covered = [];
    numCellsCoveredOld = 0;
    coveredOld = [];

    # number of cells directly encoded by M, no error possible
    numCellsExcluded = 0;
    excluded = [];
    numCellsExcludedOld = 0;
    excludedOld = [];

    # number of overlapped edges (added by Yike)
    numEdgeOverlapped = 0;
    overlapped = [];
    numEdgeOverlappedOld = 0;
    overlappedOld = [];

    # final count of overlaps
    numOverlappedCells = 0;
    countOverlappedCells = [];
    
    
    # change set to list to allow duplicates
    def __init__(self, graph, err = None):

        if err is None :
            self.numNodes = graph.numNodes;

            self.unmodelled = [list(x) for x in graph.edges];
            self.numUnmodelledErrors = graph.numEdges;

            self.modelled = [list() for x in range(len(graph.edges))];
            self.numModellingErrors = 0;
        
            self.covered = [list() for i in range(self.numNodes)];
            self.numCellsCovered = 0;

            self.excluded = [list() for i in range(self.numNodes)];
            self.numCellsExcluded = 0;

            # add overlapped edges
            self.overlapped = [list() for x in range(len(graph.edges))];
            self.numEdgeOverlapped = 0;
	    #self.numOverlappedCells = 0;
	    self.countOverlappedCells = [list() for x in range(len(graph.edges))];
        else :
            self.numNodes = err.numNodes;

            self.unmodelled = [list(x) for x in err.unmodelled];
            self.numUnmodelledErrors = err.numUnmodelledErrors;

            self.modelled = [list(x) for x in err.modelled];
            self.numModellingErrors = err.numModellingErrors;

            self.covered = [list(x) for x in err.covered];
            self.numCellsCovered = err.numCellsCovered;

            self.excluded = [list(x) for x in err.excluded];
            self.numCellsExcluded = err.numCellsExcluded;

            # add overlapped edges
            self.overlapped = [list(x) for x in err.overlapped];
            self.numEdgeOverlapped = err.numEdgeOverlapped;
	    #self.numOverlappedCells = err.numOverlappedCells;
	    self.countOverlappedCells = [list(x) for x in err.countOverlappedCells];
    
    def recoverOld(self):
        self.numNodes = self.numNodesOld;
        
        self.unmodelled = self.unmodelledOld; 
        self.numUnmodelledErrors = self.numUnmodelledErrorsOld;

        self.modelled = self.modelledOld;
        self.numModellingErrors = self.numModellingErrorsOld;
        
        self.covered = self.coveredOld;
        self.numCellsCovered = self.numCellsCoveredOld;

        self.excluded = self.excludedOld;
        self.numCellsExcluded = self.numCellsExcludedOld;
        
        # add overlapped edges
        self.overlapped = self.overlappedOld;
        self.numEdgeOverlapped = self.numEdgeOverlappedOld;
       

    # checks whether edge (i,j) is covered
    def isModelled(self, i, j) :
        return (max(i,j)-1 in self.covered[min(i,j)-1]);
    def isCovered(self, i, j) :
        return self.isModelled(i,j);
    
    # checks whether edge (i,j) is overlapped
    #def isOverlapped(self, i , j) :
        #edgeCount = Counter(self.covered);
        #for key, count in dropwhile(lambda key_count: key_count[1] <= 1, edgeCount.most_common()):
            #del edgeCount[key];
        #return self.overlapped(i, j);
    
    # annotates edge (i,j) as covered
    # ! (i,j) does not have to be in E of G(V,E)
    def cover(self, i, j) :
        self.covered[min(i,j)-1].append(max(i,j)-1);
        self.numCellsCovered += 1;
        return;

    # annotates edge (i,j) as both covered, and error-free
    # ! (i,j) does not have to be in E of G(V,E)
    def coverAndExclude(self, i, j) :
        self.cover(i,j)
        self.exclude(i,j);
        return;
        
    def exclude(self, i, j) :
        self.excluded[min(i,j)-1].append(max(i,j)-1);
        self.numCellsExcluded += 1;
        return;
        
    def isError(self, i, j):
        return max(i,j)-1 in self.unmodelled[min(i,j)-1] or max(i,j)-1 in self.modelled[min(i,j)-1];
        
    def isExcluded(self, i, j):
        return max(i,j)-1 in self.excluded[min(i,j)-1];
        
    def isUnmodelledError(self, i, j):
        return max(i,j)-1 in self.unmodelled[min(i,j)-1];
    def isUnmodelledEdge(self, i, j):
        return self.isUnmodelledError(i,j);

    def isModellingError(self, i, j):
        return max(i,j)-1 in self.modelled[min(i,j)-1];

    # annotates edge (i,j) as correct
    def delError(self, i, j) :
        if self.isUnmodelledError(i,j) :
            self.delUnmodelledError(i,j);
        else :
            self.delModellingError(i,j);      

    # annotates edge (i,j) as not-modelled
    def addUnmodelledError(self, i, j) :
        self.unmodelled[min(i,j)-1].append(max(i,j)-1);
        self.numUnmodelledErrors += 1;
        
    # annotates edge (i,j) as correctly modelled
    def delUnmodelledError(self, i, j) :
        self.unmodelled[min(i,j)-1].remove(max(i,j)-1);
        self.numUnmodelledErrors -= 1;

    # annotates edge (i,j) as erronously modelled
    def addModellingError(self, i, j) :
        self.modelled[min(i,j)-1].append(max(i,j)-1);
        self.numModellingErrors += 1;
	if config.optDebug :
        	print "modelling error: " + str(self.numModellingErrors);
        
    # annotates edge (i,j) as incorrectly modelled
    def delModellingError(self, i, j) :
        self.modelled[min(i,j)-1].append(max(i,j)-1);
        self.numModellingErrors -= 1;
	if config.optDebug : 
        	print "modelling error (in delModError): " + str(self.numModellingErrors);
        

    # annotates edge (i, j) as overlapped
    def addOverlappedError(self, i, j) :
        self.overlapped[min(i,j)-1].append(max(i,j)-1);
        self.numEdgeOverlapped += 1;
	if config.optDebug and config.optOverlap :
		print "overlap: " + str(self.numEdgeOverlapped);
    		print "overlap edges: " + str(self.overlapped);
		
   # convert list of overlap to set, saving the size of set, number of occurrence for each cell
    def listToSet(self) :
	#print str(len(self.overlapped));
        noDupes = [[] for i in range(len(self.overlapped))];
	#print str(noDupes);
        #temp = set(self.overlapped);
        #[[noDupes[j].append(self.overlapped[j][i]) for i in range(len(self.overlapped[j])) if not noDupes.count(self.overlapped[j][i])] for j in range(len(self.overlapped))];
	for j in range(len(self.overlapped)) :
		for x in self.overlapped[j] :
			#if not noDupes[j] == [None]:
				if not noDupes[j].count(x) :
					noDupes[j].append(x);
	#for j in range(len(self.overlapped)) :
		#if config.optDebug :
			#print str(j) + "th: " + str(self.overlapped[j]);
		#noDupes.append(set(self.overlapped[j]));
        #numOverlappedCells = len(set(self.overlapped));
	noDupes = filter(None, noDupes);
	if config.optDebug :
	 print str(noDupes);
        countOverlappedCells = [[self.overlapped[j].count(x) for x  in noDupes[j]] for j in range(len(noDupes))];
        #countOverlappedCells = dict((self.overlapped.count(x)) for x in set(self.overlapped));
        #if config.Debug:
		#print "# of overlapped cells: " + str(self.numOverlappedCells);
        return countOverlappedCells;
	
    def plotCover(self):
        for idx in range(len(self.covered)) :
            mystr = "".join(["." for x in range(0,idx+1)]);
            for idy in range(idx+1,len(self.covered)) :
                if idy in self.covered[idx] :
                    mystr += "1";
                else :
                    mystr += "-";
            print mystr;

    def plotError(self):
        for idx in range(len(self.unmodelled)) : # uses 'unmodelled' only as numNodes
            mystr = "".join(["." for x in range(0,idx+1)]);
            for idy in range(idx+1,len(self.unmodelled)) :
                if idy in self.covered[idx] :
                    if idy in self.excluded[idx] :
                        mystr += "*";
                    elif idy in self.modelled[idx] :
                        mystr += "+";
                    else :
                        mystr += "-";
                else :
                    if idy in self.unmodelled[idx] :
                        mystr += "1";
                    else :
                        mystr += "0";
            print mystr;

    def plotExcluded(self):
        for idx in range(len(self.excluded)) :
            mystr = "".join(["." for x in range(0,idx+1)]);
            for idy in range(idx+1,len(self.excluded)) :
                if idy in self.excluded[idx] :
                    mystr += "1";
                else :
                    mystr += "0";
            print mystr;

    def listCover(self):
        print self.covered;
    
    def listError(self):
        for idx in range(len(self.unmodelled)) :
            if len(self.unmodelled[idx]) > 0 :
                print idx+1, "+: "+str([x+1 for x in self.unmodelled[idx]]), "-: "+str([x+1 for x in self.modelled[idx]]),;

    def listExcluded(self):
        print self.excluded;
