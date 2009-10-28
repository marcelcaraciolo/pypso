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

0.10 2009-05-25 Initial version.
0.11 2009-05-28 Added support for database adapter (SQLite3 database)
0.23 2009-09-19 Redesigned the Module for support new API and Docs.
'''

"""
:mod:`ReportAdapters` -- database adapters for statistics
=====================================================================

.. warning:: the use the of a Report Adapter can reduce the performance of the
             PSO Algorithm.

This module contains the adapters which you can use to save the statistics 
of every iteration in a file or database with the statistics as parameters.
You can use the report to plot convergence statistics graphs later.

.. seealso::

   Method :meth:`Pso.SimplePso.setReportAdapter`
      Report Adapters are set in the SimplePso Class.

"""


import csv
import Consts
import types
import sqlite3
import FloatStatistics


#DBSQLite Class - Adapter to dump data in SQLite3 database format
class ReportDB:
    """ ReportDB Class - Adapter to dump data in SQLite3 database format
   
   Example:
      >>> dbadapter = ReportDB(identify="test")

   When you run some PSO for the first time, you need to create the database, for this, you
   must use the *resetDB* parameter:

      >>> dbadapter = ReportDB(identify="test", resetDB=True)

   This parameter will erase all the database tables and will create the new ones.
   The *resetDB* parameter is different from the *resetIdentify* parameter, the *resetIdentify*
   only erases the rows with the same "identify" name.   

   :param dbname: the database filename
   :param identify: the identify if the run
   :param resetDB: if True, the database structure will be recreated
   :param resetIdentify: if True, the identify with the same name will be overwrite with new data
   :param frequency: the generational dump frequency
   :param commit_freq: the commit frequency

   """

    def __init__(self,dbname=Consts.CDefDBName,identify=None,resetDB=True,
                 resetIdentify=True,frequency=Consts.CDefDBStatsGenFreq, 
                 commit_freq=Consts.CDefDBStatsCommitFreq):
        """ The creator of the ReportDB Class """
        if identify is None:
            self.identify = datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%y-%H:%M")
        else:
            self.identify = identify
        
        self.connection = None
        self.resetDB = resetDB
        self.resetIdentify = resetIdentify
        self.dbName = dbname
        self.typeDict = {types.FloatType: "real"}
        self.statsGenFreq = frequency
        self.cursorPool = None
        self.commitFreq = commit_freq
    
    
    def __repr__(self):
        """ The string representation of adapter """
        ret = "Report DB Adapter [File='%s', identify='%s']" % (self.dbName, self.identify)
        return ret
    
    def open(self):
        """ Open the database connection """
        print "Opening database, dbname=%s" % self.dbName
        self.connection = sqlite3.connect(self.dbName)
        
        if self.resetDB:
            self.resetStructure((FloatStatistics.SwarmStatistics(),FloatStatistics.TopologyStatistics()))
        
        if self.resetIdentify:
            self.resetTableIdentify()
    

    def saveAndClose(self):
        """ Commit changes on database and closes connection """
        self.commit()
        self.close()
    
    def close(self):
        """ Close the database connection """
        print "Closing the database."
        if self.cursorPool:
            self.cursorPool.close()
            self.cursorPool = None
        self.connection.close()
    

    def commit(self):
        """ Commit changes to database """
        self.connection.commit()
    
    def getCursor(self):
        """ Return a cursor from the pool

          :rtype: the cursor

        """
        if not self.cursorPool:
            self.cursorPool = self.connection.cursor()
            return self.cursorPool
        else:
            return self.cursorPool
        
    
    def createStructure(self,stats):
        """ Create table using the Statistics class structure

          :param stats: the statistics object

        """
        c = self.getCursor()
        
        pstmt = "create table if not exists %s(identify text, iteration integer, " % (Consts.CDefReportDBSwarmTable)
        #Swarm statistics
        for k,v in stats[0].items():
            pstmt += "%s %s, " % (k, self.typeDict[type(v)])
        pstmt = pstmt[:-2] + ")"
        c.execute(pstmt)
        
        pstmt = "create table if not exists %s(identify text, iteration integer, bestFitness real, bestPosDim real)" % (Consts.CDefReportDBTopTable)
        #Topology statistics
        c.execute(pstmt)
        
        #Swarm individuals statistics
        pstmt = """create table if not exists %s(identify text, iteration integer,
                particle integer, fitness real, bestFitness real)""" % (Consts.CDefSQLiteDBPartTable)
        c.execute(pstmt)
        self.commit()
    
    def resetTableIdentify(self):
        """ Delete all records on the table with the same Identify """
        c = self.getCursor()
        stmt = "delete from %s where identify  = ?" % (Consts.CDefReportDBSwarmTable)
        stmt2 = "delete from %s where identify = ?" % (Consts.CDefReportDBTopTable)
        stmt3 = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBPartTable)
        
        try:
            c.execute(stmt, (self.identify,))
            c.execute(stmt2, (self.identify,))
            c.execute(stmt3, (self.identify,))
        except sqlite3.OperationalError, expt:
            if expt.message.find("no such table") >= 0:
                print "\n ## The DB Adapter can't find the tables ! Consider enable the parameter resetDB ! ##\n"
        
        self.commit()

    def resetStructure(self,stats):
        """ Deletes de current structure and calls createStructure

          :param stats: the statistics object

        """
        c = self.getCursor()
        c.execute("drop table if exists %s" % (Consts.CDefReportDBSwarmTable,))
        c.execute("drop table if exists %s" % (Consts.CDefReportDBTopTable,))
        c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBPartTable,))
        self.commit()
        self.createStructure(stats)

    #Inserts the statistics into the database
    #@param stats: The statistics objects
    #@param topology: The swarm to insert stats (class: Topology.Topology)
    #@param iteration: The iteration of the insert
    def insert(self,stats,topology,iteration):
        """ Inserts the statistics data to database

          :param stats: statistics object subclass of (:class:`Statistics.Statistics`)
          :param topology: swarm to insert stats subclass of (:class:`TopologyBase.TopologyBase`)
          :param iteration: the iteration of the insert
        """
        c = self.getCursor()
        #Swarm statistics
        pstmt = "insert into %s values (?, ?, " % (Consts.CDefReportDBSwarmTable)
        for i in xrange(len(stats[1])):
            pstmt += "?, "
        pstmt = pstmt[:-2] + ")"
        c.execute(pstmt, (self.identify,iteration) + stats[1].asTuple())

        #Topology statistics
        pstmt = "insert into %s values(?, ?, ?, ?) " % (Consts.CDefReportDBTopTable)
        c.execute(pstmt, (self.identify,iteration,stats[0]["bestFitness"],stats[0]["bestPosDim"]))
        
        #Particles statistics
        pstmt = "insert into %s values(?, ?, ?, ?, ?)" % (Consts.CDefSQLiteDBPartTable,)
        tups = []
        for i in xrange(len(topology)):
            particle = topology[i]
            tups.append((self.identify,iteration,i, particle.fitness, particle.ownBestFitness))
        c.executemany(pstmt,tups)
        if (iteration % self.commitFreq == 0):
            self.commit()
            

class ReportFileCSV:
    
       
    """ ReportFileCSV Class - Adapter to dump statistics in CSV format

       Example:
          >>> adapter = ReportFileCSV(filename="file.csv", identify="run_01",
                              frequency = 1, reset = True)

      :param filename: the CSV filename
      :param identify: the identify of the run
      :param frequency: the generational dump frequency
      :param reset: if is True, the file old data will be overwrite with the new

   """
   
    def __init__(self, filename=Consts.CDefCSVFileName, identify=None,
                 frequency = Consts.CDefCSVFileStatsGenFreq, reset= True):
        """ The creator of ReportFileCSV Class """
        if identify is None:
            self.identify = datetime.datetime.strftime(date.datetime.now(),"%d/%m/%y-%H:%M")
        else:
            self.identify = identify
        
        self.filename = filename
        self.statsGenFreq = frequency
        self.csvWriter = None
        self.fHandler = None
        self.reset = reset
     
     
    def __repr__(self):
        """ The string representation of adapter """
        ret = "ReportFileCSV Report Aadapter [File='%s', identify='%s']" % (self.filename,self.identify)
        return ret

    def open(self):
        """ Open the CSV file or creates a new file """
        print "Opening the CSV file to dump statistics [%s]" % self.filename
        if self.reset: open_mode = "w"
        else: open_mode = "a"
        self.fHandler = open(self.filename,open_mode)
        self.csvWriter = csv.writer(self.fHandler,delimiter=";")

    def close(self):
        """ Closes the CSV file handle """
        if self.fHandler:
            self.fHandler.close()
    

    def saveAndClose(self):
        """ Commits and closes """
        self.commit()
        self.close()
    
    def commit(self):
        """ Stub """
        pass
    
    
    def insert(self,stats,topology,iteration):
        """ Inserts the stats into the CSV file

          :param stats: statistics object (:class:`Statistics.Statistics`)
          :param topology: swarm to insert stats  subclass of (:class:`TopologyBase.TopologyBase`)
          :param iteration: the iteration of the insert

        """
        line = [self.identify,iteration]
        line.extend(stats[0].asTuple())
        line.extend(stats[1].asTuple())
        self.csvWriter.writerow(line)

