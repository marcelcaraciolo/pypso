'''
Particle Swarm Optimization - PyPSO 

Copyright (c) 2009 Marcel Pinheiro Caraciolo
caraciol@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

0.10 2009-05-29 Initial version.
0.11 2009-06-08 Added support for heat map fitness swarm distribution

    This code is part of Pypso.
    Require matplotlib v.0.98.5.0+
    Used to create the graph analysis.
     
'''

from optparse import OptionParser
from optparse import OptionGroup

TOP = {
   "identify"   : 0, "iteration"  : 1, "bestFitness" : 2,
   "bestPosDim"    : 3
}


SWARM = {
   "identify"   : 0, "iteration" : 1, "bestFitVar"     : 2,
   "fitMin"     : 3, "bestFitMin"     : 4, "bestFitMax"     : 5,
   "fitMax"     : 6, "bestFitAvg"     : 7, "fitAvg"     : 8,
   "bestFitDev"     : 9
}

PARTICLES = {"identify" : 0, "iteration": 1, "particle": 2,
             "fitness" : 3, "bestFitness" : 4}



#Parse the data from row at the database
#@param line_record: The row
#@param field: The desired field
def parse(line_record, field):
   return line_record[TOP[field]]

def parseSwarm(line_record, field):
   return line_record[SWARM[field]]

def parseParticles(line_record, field):
   return line_record[PARTICLES[field]]



def graph_pop_heatmap_bestFitness(all, maximize, colormap="jet_r", filesave=None):
   pylab.imshow(all, aspect="equal", interpolation="gaussian", cmap=pylab.cm.jet_r)
   pylab.title("Plot of swarm best Fitness scores along the iteration")
   pylab.xlabel('Swarm')
   pylab.ylabel('Iterations')
   pylab.grid(True)
   pylab.colorbar()

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_pop_heatmap_fitness(all, maximize, colormap="jet", filesave=None):
   pylab.imshow(all, aspect="equal", interpolation="gaussian", cmap=pylab.cm.jet_r)
   pylab.title("Plot of swarm fitness scores along the iterations")
   pylab.xlabel('Swarm')
   pylab.ylabel('Generations')
   pylab.grid(True)
   pylab.colorbar()

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


def graph_diff_fitness(all, maximize, filesave=None):
   x = []

   diff_raw_y = []
   diff_fit_y = []

   for it in all:
      x.append(parseSwarm(it, "iteration"))
      diff_raw_y.append(parseSwarm(it, "fitMax") - parseSwarm(it, "fitMin"))
      diff_fit_y.append(parseSwarm(it, "bestFitMax") - parseSwarm(it, "bestFitMin"))

   pylab.figure()
   pylab.subplot(211)

   pylab.plot(x, diff_raw_y, "g", label="Fitness difference", linewidth=1.2)
   pylab.fill_between(x, diff_raw_y, color="g", alpha=0.1)

   diff_raw_max= max(diff_raw_y)
   gen_max_raw = x[diff_raw_y.index(diff_raw_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_raw_max,), xy=(gen_max_raw, diff_raw_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Iteration (#)")
   pylab.ylabel("Fitness difference")
   pylab.title("Plot of evolution identified by '%s'" % (options.identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   pylab.subplot(212) 

   pylab.plot(x, diff_fit_y, "b", label="Best Fitness difference", linewidth=1.2)
   pylab.fill_between(x, diff_fit_y, color="b", alpha=0.1)


   diff_fit_max= max(diff_fit_y)
   gen_max_fit = x[diff_fit_y.index(diff_fit_max)]

   pylab.annotate("Maximum (%.2f)" % (diff_fit_max,), xy=(gen_max_fit, diff_fit_max),  xycoords='data',
                xytext=(-150, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Iteration (#)")
   pylab.ylabel(" Best Fitness difference")

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()


def graph_maxmin_fitness(all, maximize, filesave=None):
   x = []
   max_y = []
   min_y = []
   avg_y = []

   for it in all:
      x.append(parseSwarm(it, "iteration"))
      max_y.append(parseSwarm(it, "fitMax"))
      min_y.append(parseSwarm(it, "fitMin"))
      avg_y.append(parseSwarm(it, "fitAvg"))

   pylab.figure()
   pylab.plot(x, max_y, "g", label="Max fitness")
   pylab.plot(x, min_y, "r", label="Min fitness")
   pylab.plot(x, avg_y, "b", label="Avg fitness")

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if not maximize: fit_max = min(min_y)
   else: fit_max = max(max_y)

   if not maximize: gen_max = x[min_y.index(fit_max)]
   else: gen_max = x[max_y.index(fit_max)]

   if not maximize: annot_label = "Minimum (%.2f)" % (fit_max,)
   else: annot_label = "Maximum (%.2f)" % (fit_max,)

   pylab.annotate(annot_label, xy=(gen_max, fit_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Iteration (#)")
   pylab.ylabel("Fitness score")
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (options.identify))
   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()



def graph_maxmin_bestFitness(all, maximize, filesave=None):
   x = []
   max_y = []
   min_y = []
   std_dev_y = []
   avg_y = []

   for it in all:
      x.append(parseSwarm(it, "iteration"))
      max_y.append(parseSwarm(it, "bestFitMax"))
      min_y.append(parseSwarm(it, "bestFitMin"))
      std_dev_y.append(parseSwarm(it, "bestFitDev"))
      avg_y.append(parseSwarm(it, "bestFitAvg"))

   pylab.figure()

   pylab.plot(x, max_y, "g", label="Max bestFit", linewidth=1.2)
   pylab.plot(x, min_y, "r", label="Min bestFit", linewidth=1.2)
   pylab.plot(x, avg_y, "b", label="Avg bestFit", linewidth=1.2)
   pylab.plot(x, std_dev_y, "k", label="Std Dev bestFit", linewidth=1.2)

   pylab.fill_between(x, min_y, max_y, color="g", alpha=0.1, label="Diff max/min")

   if not maximize: raw_max = min(min_y)
   else: raw_max= max(max_y)

   if not maximize: gen_max = x[min_y.index(raw_max)]
   else: gen_max = x[max_y.index(raw_max)]

   min_std = min(std_dev_y)
   gen_min_std = x[std_dev_y.index(min_std)]

   max_std = max(std_dev_y)
   gen_max_std = x[std_dev_y.index(max_std)]

   if not maximize: annot_label = "Minimum (%.2f)" % (raw_max,)
   else: annot_label = "Maximum (%.2f)" % (raw_max,)


   pylab.annotate(annot_label, xy=(gen_max, raw_max),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Min StdDev (%.2f)" % (min_std,), xy=(gen_min_std, min_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.annotate("Max StdDev (%.2f)" % (max_std,), xy=(gen_max_std, max_std),  xycoords='data',
                xytext=(8, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc"),
                )

   pylab.xlabel("Iteration (#)")
   pylab.ylabel("Best Fitness score")
   pylab.title("Plot of evolution identified by '%s' (best Fitness particles scores)" % (options.identify))

   pylab.grid(True)
   pylab.legend(prop=FontProperties(size="smaller"))

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()



def graph_errorbars_fitness(all, minimize, filesave=None):
   x = []
   y = []
   yerr_max = []
   yerr_min = []

   for it in all:
      x.append(parseSwarm(it, "iteration"))
      y.append(parseSwarm(it, "fitAvg"))
      ymax = parseSwarm(it, "fitMax") - parseSwarm(it, "fitMin")
      ymin = parseSwarm(it, "fitAvg") - parseSwarm(it, "fitMin")

      yerr_max.append(ymax)
      yerr_min.append(ymin)

   pylab.figure()
   pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
   pylab.xlabel('Iteration (#)')
   pylab.ylabel('Fitness Min/Avg/Max')
   pylab.title("Plot of evolution identified by '%s' (fitness scores)" % (options.identify))
   pylab.grid(True)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_errorbars_bestFitness(all, minimize, filesave=None):
   x = []
   y = []
   yerr_max = []
   yerr_min = []

   for it in all:
      x.append(parseSwarm(it, "iteration"))
      y.append(parseSwarm(it, "bestFitAvg"))
      ymax = parseSwarm(it, "bestFitMax") - parseSwarm(it, "bestFitAvg")
      ymin = parseSwarm(it, "bestFitAvg") - parseSwarm(it, "bestFitMin")

      yerr_max.append(ymax)
      yerr_min.append(ymin)

   pylab.figure()
   pylab.errorbar(x, y, [yerr_min, yerr_max], ecolor="g")
   pylab.xlabel('Iteration (#)')
   pylab.ylabel('best Fitness score Min/Avg/Max')
   pylab.title("Plot of evolution identified by '%s' (best Fitness scores)" % (options.identify))

   pylab.grid(True)

   if filesave:
      pylab.savefig(filesave)
      print "Graph saved to %s file !" % (filesave,)
   else:
      pylab.show()

def graph_compare_bestFitness_boxplot(all,id_list,iteration=None,logScale=False,filesave=None):
	data = []
	k = 0
	for db in all:
	    data.append([])
	    for identify in db:
			if iteration:  #Iteraton defined
			    data[k].append(parse(identify[iteration],"bestFitness"))
	   		else:
				lastIndex = len(identify)-1
				data[k].append(parse(identify[lastIndex],"bestFitness"))
	    k+=1
	pylab.figure()
	pylab.boxplot(data, vert=1)	
	if not iteration:
		iteration = "Last Iteration"
	if logScale:
		pylab.yscale('log')
	pylab.title("Boxplot of simulations identified by '%s' (%s) (best Fitness scores)" %(id_list,iteration))
	pylab.grid(True)
	pylab.xlabel("Simulations")
	pylab.ylabel("BestFitness")
	if filesave:
		pylab.savefig(filesave)
		print "Graph saved to %s file !" % (filesave,)
	else:
		pylab.show()
		print "Graph created!"

def graph_bestFitness_boxplot(all,id_list, filesave=None,offSet=500,logScale=True):
    data = []
    k  = 0
    for i in xrange(len(all[0])):
	    data.append([])
	    for j in xrange(len(all)):
			if (i % offSet) == 0:
		 		data[k].append(parse(all[j][i],"bestFitness"))
	    k+=1
    data = filter(lambda x: x !=[], data) 
    pylab.figure()
    pylab.boxplot(data)
    if logScale:
    	pylab.yscale('log')
    pylab.title("Boxplot of evolutions identified by '%s' (best Fitness scores)" %(options.identify))
    pylab.xlabel("Time steps(iterations)")
    pylab.ylabel("BestFitness")
    pylab.grid(True)
    if filesave:
        pylab.savefig(filesave)
        print "Graph saved to %s file !" % (filesave,)
    else:
        pylab.show()
        print "Graph created!"

def graph_compare_bestFitness(all, id_list, filesave=None):
    data = []
    k = 0
    if type(all[0][0]) == list:    
        try:
            print "Loading module numpy for some calculation...",
            import numpy
            print " done!\n"
        except:
            print "\ERROR: cannot import Numpy ! Group Report is not available !"
            exit()
            
        for db in all:
            data.append([])
            for i in xrange(len(db[0])):
                bestFitList = []
                for it_out in db:
                    bestFitList.append(parse(it_out[i],"bestFitness"))
                avgFit = numpy.mean(bestFitList)
                data[k].append([i+1,avgFit])
            k+=1

    else:
        for it_out in all:
            data.append([])
            for it in it_out:
                data[k].append([parse(it,"iteration"),parse(it,"bestFitness")])
            k+=1
    
    print "Loading data..." 
    
    colors_list = ["g","b","r","k","m","y"]
    index = 0
    
    pylab.figure()
    
    for it_out in data:
        x = []
        y = []
        for it in it_out:
            x.append(it[0])
            y.append(it[1])
            
        pylab.plot(x, y, colors_list[index], label = "%s" %(id_list[index],), linewidth=3.0)
        
        index += 1
     
    pylab.xlabel("Number of time steps(iterations)")
    pylab.ylabel("Fitness")
    pylab.legend(prop=FontProperties(size="smaller"))
    
    if filesave:
        pylab.savefig(filesave)
        print "Graph saved to %s file !" % (filesave,)
    else:
        pylab.show()
        print "Graph created!"




if __name__ == "__main__":
    #from pypso import __version__ as pypso_version
    #from pypso import __author__ as pypso_author

    popGraph = False
	
    #print "PyPso %s - Graph Plot Tool" % (pypso_version,)
    #print "By %s\n" % (pypso_author,)
   
    parser = OptionParser()
   
    parser.add_option("-f", "--file", dest="dbfile",
                     help="Database file to read (default is 'pypso.db'.",
                     metavar="FILENAME", default="pypso.db")
   
   
    parser.add_option("-i", "--identify", dest="identify",
                     help="The identify of simulation.", metavar="IDENTIFY")
   
    parser.add_option("-o","--outfile",dest="outfile",
                     help="""Write the report to a pdf file (use just the filename)""",
                     metavar="OUTFILE")
   
    parser.add_option("-e", "--extension", dest="extension",
                  help="""Graph image file format. Supported options (formats) are: emf, eps, pdf, png, ps, raw, rgba, svg, svgz. Default is 'png'.""",
                  metavar="EXTENSION", default="png")
   
    parser.add_option("-t", "--tsrange", dest="tsrange",
                  help="""This is the time steps range of the graph, ex: 1:30 (interval between 1 and 30).""",
                  metavar="TSRANGE")

    parser.add_option("-c", "--colormap", dest="colormap",
 				 help="""Sets the Color Map for the graph types 8 and 9. Some options are: summer, bone, gray, hot, jet, cooper, spectral. The default is 'jet'.""",
			     metavar="COLORMAP", default="jet")
    
    parser.add_option("-m", "--maximize", action="store_true", 
				 help="Sets the 'Maximize''mode, default is the Minimize mode. This option makes sense if you are maximizing your evaluation function." ,
				 dest="maximize")   

    group = OptionGroup(parser, "Graph types", "These are the supported graph types")
   
    group.add_option("-1", action="store_true", help="""Compare best fitness of two or more evolutions/simulations (For evolution: you must specify the identify comma-separed list with --identify (-i) parameter, like 'one, two, three'), the maximum is 6 items. 
                                                       (For simulation: you must specify the file (dbfile) comma-separed with --file (-f) parameter, like 'one, two , three'), the maximum is 6 items.""" , dest="compare_bestFitness")
    group.add_option("-2", action="store_true", help="""Compare best fitness distribution (last iteration) of two or more simulations (Boxplot) 
														(For simulation: you must specify the file (dbfile) comma-separed with --file (-f) parameter, like 'one, two , three'), the maximum is 6 items.""", dest="compare_bestFitness_boxplot")
    group.add_option("-3", action="store_true", help="""Best Fitness distribution of two or more evolutions (Boxplot) (For evolution: you must specify the identify comma-separed list with --identify (-i) parameter, like 'one, two, three'), the maximum is 6 items. """, dest="bestFitness_boxplot")
    group.add_option("-4", action="store_true", help="Error bars graph (best fitness).", dest="errorbars_bestFitness")
    group.add_option("-5", action="store_true", help="Error bars graph (fitness).", dest="errorbars_fitness")
    group.add_option("-6", action="store_true", help="Max/Min/avg/std. dev graph(best fitness)", dest="maxminBestFitness")
    group.add_option("-7", action="store_true", help= "Max/Min/avg graph (fitness score)", dest="maxminFitness")
    group.add_option("-8", action="store_true", help= "Fitness and bestFitness min/max difference graph.", dest="diff_fitness")
    group.add_option("-9", action="store_true", help="Show a heat map of swarm fitness score distribution between iterations.", dest="pop_heatmap_fitness")
    group.add_option("--10", action="store_true", help="Show a heat map of swarm best fitness score distribution between iterations.", dest="pop_heatmap_bestFitness")



    parser.add_option_group(group)
   
    (options,args) = parser.parse_args()
   
    if (not options.dbfile):
        parser.print_help()
        exit()
   
    db_list = options.dbfile.split(",")
    db_list = map(str.strip, db_list)
    
   
    if (options.identify and len(db_list) > 1):
        parser.error("You must choose simulation or evolution graphs!")
    
    if (not options.identify and len(db_list)==1):
        parser.print_help()
        exit()
    
    if not options.compare_bestFitness and not options.errorbars_fitness and not options.errorbars_bestFitness and \
    not options.maxminBestFitness and not options.maxminFitness and not options.diff_fitness and not options.pop_heatmap_fitness and \
	not options.pop_heatmap_bestFitness and not options.compare_bestFitness_boxplot and not options.bestFitness_boxplot:
        parser.error("You must choose one graph type !")
    
    print "Loading modules...."
    
    import os.path
    for dbfile in db_list:
        if not os.path.exists(dbfile):
            print "Database file '%s' not found !" % (dbfile, )
            exit()
    
    import pylab
    from matplotlib.font_manager import FontProperties
    import matplotlib.cm
    import sqlite3
    import math
    import os
    
    print "Loading database and creating graph..."

    identify_list = None
    
    if options.identify:
        identify_list = options.identify.split(',')
        identify_list = map(str.strip,identify_list)
    
    all = None

    if options.pop_heatmap_fitness or options.pop_heatmap_bestFitness:
        conn = sqlite3.connect(options.dbfile) 
        c = conn.cursor()
	
        if options.tsrange:
		    tsrange = options.tsrange.split(":")
		    ret = c.execute("select distinct iteration from particles where identify = ? and iteration between ? and ?", (options.identify,tsrange[0],tsrange[1]))
        else:
            ret = c.execute("select distinct iteration from particles where identify = ?", (options.identify,))
    
        iterations = ret.fetchall()
        if len(iterations) <= 0:
	        print "No iteration data found for the identify '%s' !" %(options.identify,)
	        exit()
 
        all = []
        for it in iterations:
            swarm_tmp = []
            print it
            ret = c.execute("select * from particles where identify = ? and iteration = ?", (options.identify, it[0])) 
            ret_fecth = ret.fetchall()
            for pt in ret_fecth:
                if options.pop_heatmap_fitness:
			        swarm_tmp.append(parseParticles(pt,"fitness"))
                else:
		            swarm_tmp.append(parseParticles(pt,"bestFitness"))
            all.append(swarm_tmp)
        ret.close()
        conn.close()

        if len(all) <= 0:
		    print "No statistic data found for the identify  '%s' ! " %(options.identify,)
		    exit()
   
        print "%d iterations found ! " % (len(all),)
   
        popGraph = True

    #Case One: Simulation Graphs
    if len(db_list) > 1 and not popGraph:
        all = []
        i = 0
        if (not options.compare_bestFitness and not options.compare_bestFitness_boxplot):
            parser.error("You can only use the compare bestFitness graph type for simulations analysis!")
        
        for db_file in db_list:
            all.append([])
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            temp = c.execute("select distinct identify from topology")
            fetchtemp = temp.fetchall()
            if len(fetchtemp) > 0:
                for item in fetchtemp:
                    if options.tsrange:
                        tsrange = options.tsrange.split(":")
                        ret = c.execute("select * from topology where identify = ? and iteration between ? and ?", (item[0],tsrange[0],tsrange[1]))
                    else:
                        ret = c.execute("select * from topology where identify = ?", (item[0],))  
                    fetchall = ret.fetchall()   
                    if len(fetchall) > 0:
                        all[i].append(fetchall)   
            i+=1
            
        temp.close()
        conn.close()
        
        if len(all)< len(db_list):
            print "No statistic data found for the database list '%s' !" % (options.dbfile,)
            exit()
        
        total = []
        for all_out in all:
            total.append(len(all_out))
            if len(all_out) <= 0:
                print "No statistic data found for the database list '%s' !" % (options.dbfile,)
                exit()
        
        j = 0
        for sum in total:
            print "%d identify found for %s database." % (sum,db_list[j])
            j+=1


    #Case Two: Evolution Graphs (One identify)
    elif len(identify_list) == 1 and not popGraph:
		if options.compare_bestFitness or options.compare_bestFitness_boxplot or options.bestFitness_boxplot:
			parser.error("You can't use this graph type with only one identify !")
		
		conn = sqlite3.connect(options.dbfile)
		c = conn.cursor()
		
		if options.tsrange:
			tsrange = options.tsrange.split(":")
			ret = c.execute("select * from swarm where identify = ? and iteration between ? and ?", (options.identify, tsrange[0], tsrange[1]))
		else:
			ret = c.execute("select * from swarm where identify = ?", (options.identify,))
		
		all = ret.fetchall()
		
		ret.close()
		conn.close()
		
		if len(all) <= 0:
			print "No statistic data found for the identify '%s' !" % (options.identify,)
		
		print '%d iterations found !' % (len(all),)

	#Case Two: Evolution Graphs (More than one identify)
    elif len(identify_list) > 1 and not popGraph:
		all = []
		if (not options.compare_bestFitness and not options.bestFitness_boxplot):
			parser.error("You can't use many ids with this graph type! ")
		
		conn = sqlite3.connect(options.dbfile)
		c = conn.cursor()
		for item in identify_list:
			if options.tsrange:
				tsrange = options.tsrange.split(":")
				ret = c.execute("select * from topology where identify = ? and iteration between ? and ?", (options.identify, tsrange[0], tsrange[1]))
			else:
				ret = c.execute("select * from topology where identify = ?", (item,))
			fecthall = ret.fetchall()
			if len(fecthall) > 0:
				all.append(fecthall)
         
		ret.close()
		conn.close()

		if len(all) <= 0:
			print "No statistic data found for the identify list '%s' !" % (options.identify,)
			exit()
		
		print "%d identify found !" %(len(all),)
		
    if not identify_list:
        identify_list = db_list
    
    
    if options.compare_bestFitness:
        if options.outfile: graph_compare_bestFitness(all, identify_list, options.outfile + "." + options.extension)
        else: graph_compare_bestFitness(all, identify_list)
   
    if options.bestFitness_boxplot:
	    if options.outfile: graph_bestFitness_boxplot(all, identify_list, options.outfile + "." + options.extension)
	    else: graph_bestFitness_boxplot(all, identify_list)
	
    if options.compare_bestFitness_boxplot:
	    if options.outfile: graph_compare_bestFitness_boxplot(all, identify_list, options.outfile + "." + options.extension)
	    else: graph_compare_bestFitness_boxplot(all, identify_list)
	
    if options.errorbars_fitness:
		if options.outfile: graph_errorbars_fitness(all, options.maximize, options.outfile + "." + options.extension)
		else: graph_errorbars_fitness(all, options.maximize)
		
    if options.errorbars_bestFitness:
		if options.outfile: graph_errorbars_bestFitness(all, options.maximize, options.outfile + "." + options.extension)
		else: graph_errorbars_bestFitness(all, options.maximize)
		
    if options.maxminBestFitness:
        if options.outfile: graph_maxmin_bestFitness(all, options.maximize, options.outfile + "." + options.extension)
        else: graph_maxmin_bestFitness(all, options.maximize)

    if options.maxminFitness:
        if options.outfile: graph_maxmin_fitness(all, options.maximize, options.outfile + "." + options.extension)
        else: graph_maxmin_fitness(all, options.maximize)	

    if  options.diff_fitness:
        if options.outfile: graph_diff_fitness(all, options.maximize, options.outfile + "." + options.extension)
        else: graph_diff_fitness(all, options.maximize)


    if options.pop_heatmap_fitness:
	    if options.outfile: graph_pop_heatmap_fitness(all, options.maximize, options.colormap, options.outfile + "." + options.extension)
	    else: graph_pop_heatmap_fitness(all, options.maximize, options.colormap)

    if options.pop_heatmap_bestFitness:
	    if options.outfile: graph_pop_heatmap_bestFitness(all, options.maximize, options.colormap, options.outfile + "." + options.extension)
	    else: graph_pop_heatmap_bestFitness(all, options.maximize, options.colormap)


