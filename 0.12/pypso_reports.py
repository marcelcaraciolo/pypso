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

    This code is part of Pypso.
    Require matplotlib v.0.98.5.0+
    Used to create the pdf reports.

'''

from optparse import OptionParser
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors


TOP = {
   "identify"   : 0, "iteration"  : 1, "bestFitness" : 2,
   "bestPosDim"    : 3
}

#Parse the data from row at the database
#@param line_record: The row
#@param field: The desired field
def parse(line_record, field):
   return line_record[TOP[field]]



#Create the individual report
#@param all: All fetch data
#@param filesave: The output filename
def individual_report(all, filesave):
        
    PAGE_HEIGHT = defaultPageSize[1]
    styles = getSampleStyleSheet()
    
    elements = []
    
    doc = SimpleDocTemplate(filesave)
    
    title = Paragraph("PSO Evolution Report", styles["Title"])
    
    data = [["Iteration", "Best Position (1st Dimm.)" ,"  Best Fitness"]]
    
    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
     ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
     ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
     ('FONT', (0,0), (-1,0), 'Times-Bold'),
     ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black),
     ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black,
      1, None, None, 4,1),
     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.gray),
     ('FONT', (0,-1), (-1,-1), 'Times-Bold')]

    identify_status = False
    
    id = ""
    
    for it in all:
        if not identify_status:
            id = parse(it, "identify")
            identify_status = True
        data.append([parse(it,"iteration"),parse(it,"bestPosDim"),parse(it,"bestFitness")])
        
    identifier = Paragraph("Identifier: " + id,styles["Heading2"])   
    table = LongTable(data, style=ts)
    
    elements.append(title)
    elements.append(identifier)
    elements.append(table) 
    print "Please wait..."
    doc.build(elements)
    print '%s file has been created.' % (filesave,)

#Create the group report
#@param all: All fecth data
#@param filesave: The output filename
def group_report(all, filesave):
    
    try:
        print "Loading module numpy for some calculation...",
        import numpy
        print " done!\n"
    except:
        print "\ERROR: cannot import Numpy ! Group Report is not available !"
        exit()
    
    PAGE_HEIGHT = defaultPageSize[1]
    styles = getSampleStyleSheet()
    
    elements = []
    
    doc = SimpleDocTemplate(filesave)
    
    title = Paragraph("PSO Group Evolution Report", styles["Title"])
    
    data = [["Iteration", " Avg. Best Position (1st Dimm.)" , "Std. Deviation "," Avg. Best Fitness" ,"Std. Deviation"]]
    
    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
     ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
     ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
     ('FONT', (0,0), (-1,0), 'Times-Bold'),
     ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black),
     ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black,
      1, None, None, 4,1),
     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.gray),
     ('FONT', (0,-1), (-1,-1), 'Times-Bold')]
    
    id = parse(all[0][0],"identify") 
    
    for i in xrange(len(all[0])):
        bestPosList = []
        bestFitList = []
        for it_out in all:
            bestPosList.append(parse(it_out[i],"bestPosDim"))
            bestFitList.append(parse(it_out[i],"bestFitness"))
        avgPos = numpy.mean(bestPosList)
        avgFit = numpy.mean(bestFitList)
        stDevPos = numpy.std(bestPosList)
        stDevFit = numpy.std(bestFitList)
        data.append([i+1,avgPos,stDevPos,avgFit,stDevFit])
                 
        
    identifier = Paragraph("Identifier: " + id,styles["Heading2"]) 
    numberOfSimulations = Paragraph("Number of Simulations: " + str(len(all)),styles["Heading2"])  
    table = LongTable(data, style=ts)
    
    elements.append(title)
    elements.append(identifier)
    elements.append(numberOfSimulations)
    elements.append(table)
    print "Please wait..."
    doc.build(elements)
    
    print '%s file has been created.' % (filesave,)



if __name__ == "__main__":
    from pypso import __version__ as pypso_version
    from pypso import __author__ as pypso_author
    
    groupReport = False

    print "PyPso %s - Report Tool" % (pypso_version,)
    print "By %s\n" % (pypso_author,)
   
    parser = OptionParser()
   
    parser.add_option("-f", "--file", dest="dbfile",
                     help="Database file to read.",
                     metavar="FILENAME")
   
    parser.add_option("-i", "--identify", dest="identify",
                     help="The identify of simulation.", metavar="IDENTIFY")
   
    parser.add_option("-o","--outfile",dest="outfile",
                     help="""Write the report to a pdf file (use just the filename)""",
                     metavar="OUTFILE")
   
    (options,args) = parser.parse_args()
   
    if (not options.identify) or (not options.dbfile) or (not options.outfile):
        parser.print_help()
        exit()
    
    print "Loading modules..."
    
    import os.path
    if not os.path.exists(options.dbfile):
        print "Database file '%s' not found !" % (options.dbfile,)
        exit()
    
    import sqlite3
    import os
    
    print "Loading database and creating the report..."
    
    identify_list = options.identify.split(",")
    identify_list = map(str.strip,identify_list)
    
    all = None
    
    #Individual simulation report
    if len(identify_list) == 1:
        conn = sqlite3.connect(options.dbfile)
        c = conn.cursor()
        
        ret = c.execute("select * from topology where identify = ?",(options.identify,))
        
        all = ret.fetchall()
        
        ret.close()
        conn.close()
        
        if len(all) <= 0:
            print "No statistic data found for the identify '%s' !" % (options.identify,)
            exit()
        
        print "%d iterations found !" % (len(all),)
        
    #Group Simulation Report
    elif len(identify_list) > 1:
        all = []
        conn = sqlite3.connect(options.dbfile)
        c = conn.cursor()
        for item in identify_list:
            ret = c.execute("select * from topology where identify = ?", (item,))
            fetchall = ret.fetchall()
            if len(fetchall) > 0:
                all.append(fetchall)
        ret.close()
        conn.close()
    
        if len(all) <= 0:
            print "No statistic data found for identify list '%s' !" % (options.identify,)
            exit()
        #TODO : CHECK IF ALL ELEMENTS OF ALL ARE THE SAME !
    
        groupReport = True
    
        print "%d identify found !" % (len(all),)
    
    
    if not groupReport:
        individual_report(all,options.outfile + ".pdf")
    
    else:
        group_report(all,options.outfile + ".pdf")

       