# -*- coding: utf-8 -*-
"""
/***************************************************************************
 seasonDistance
                                 A QGIS plugin
 Calculates Owls Season Distance
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by University of Muenster
        email                : b_teka02@uni-muenster.de
        Members              : Vanesa Perez Sancho
                             : Harini Ravi
                             : Fana Gebremeskel Gebreegziabiher
                             : Denny Assarias Palinggi
                             : Brhane Bahrishum Teka
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import os
import math
from qgis.core import *
import qgis.utils
from datetime import datetime
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt



# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .owls_season_distance_dialog import seasonDistanceDialog
import os.path


class seasonDistance:
    """QGIS Plugin Implementation."""
    uniqueOwls = [0,0,0,0];
    coordinatesX = [0,0,0,0];
    coordinatesY = [0,0,0,0];
    distanceCovered=[0,0,0,0];
    previousDistance=[0,0,0,0];
    owlsType = [0,0,0,0]
    tags00 = []
    tags01 = []
    tags02 = []
    tags03 = []
    Seasons = ['Winter','Spring','Summer','Autumn']
    seasonsText=[]
    sd=[0,0,0,0]
    normalizedDistance=[0,0,0,0]
    startTimeStamp=['','','','']
    endTimeStamp=['','','','']
    distanceByMonth=[0,0,0,0,0,0,0,0,0,0,0,0]
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    distance2011=[0,0,0,0]
    distance2012=[0,0,0,0]
    distance2013=[0,0,0,0]
    distance2014=[0,0,0,0]
    distance2015=[0,0,0,0]
    distance2016=[0,0,0,0]
    distance2017=[0,0,0,0]
    #For Months standard deviation
    distanceMonth2011=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2012=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2013=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2014=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2015=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2016=[0,0,0,0,0,0,0,0,0,0,0,0]
    distanceMonth2017=[0,0,0,0,0,0,0,0,0,0,0,0]
    meanMonthCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    sdMonthly = [0,0,0,0,0,0,0,0,0,0,0,0]
    normalizedMonthlyDistance=[0,0,0,0,0,0,0,0,0,0,0,0]
    matrixForBoxPlot=[]
    matrixForMonthlyBoxPlot=[]
    #We don't know for what
    uniqueOwls2011=[0,0,0,0]
    uniqueOwls2012=[0,0,0,0]
    uniqueOwls2013=[0,0,0,0]
    uniqueOwls2014=[0,0,0,0]
    uniqueOwls2015=[0,0,0,0]
    uniqueOwls2016=[0,0,0,0]
    uniqueOwls2017=[0,0,0,0]
    meanDistance = [0,0,0,0]
    meanCount = [0,0,0,0]
    tagsJan=[]
    tagsFeb=[]
    tagsMar=[]
    tagsApr=[]
    tagsMay=[]
    tagsJun=[]
    tagsJul=[]
    tagsAug=[]
    tagsSept=[]
    tagsOct=[]
    tagsNov=[]
    tagsDec=[]
    uniqueOwlsMonth=[0,0,0,0,0,0,0,0,0,0,0,0]
    tags2011=[]
    tags2012=[]
    tags2013=[]
    tags2014=[]
    tags2015=[]
    tags2016=[]
    tags2017=[]
    seasonsIndex = [0,1,2,3]
    monthsIndex = [0,1,2,3,4,5,6,7,8,9,10,11]
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'seasonDistance_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = seasonDistanceDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Owls Season Distance')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'seasonDistance')
        self.toolbar.setObjectName(u'seasonDistance')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('seasonDistance', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/owls_season_distance/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Browse'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Owls Season Distance'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    
    def run(self):
        # Retrieve selected layer index
        self.dlg.comboBox.clear()
        layers = self.iface.mapCanvas().layers()
        layers_list = []
        for layer in layers:
            layers_list.append(layer.name());
        self.dlg.comboBox.addItems(layers_list);
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        tagsOneEach = ['1751', '1750', '1292', '1753', '1754', '3896', '3895', '3894', '3897', '3898', '4045', '5159', '4044', '3899', '5158', '4046', '4043', '4846', '3893', '3892', '4848']
        # Once selected
        if result:
            layer = layers[self.dlg.comboBox.currentIndex()]
            features = layer.getFeatures();
            for i in range(len(tagsOneEach)):
                expression = QgsExpression("tag_ident = '"+tagsOneEach[i]+"'");
                request = QgsFeatureRequest(expression)
                selection = layer.getFeatures(request)
                # Perform operation for each tag_ident -- meaning for each owl
                self.performComputation(selection)
            # Divide the distance calculated by the number of owls contributed to make the comparisons 1 vs 1 in each season
            self.normalizedDistance = [x/y for x, y in zip(self.distanceCovered, self.uniqueOwls)]
            # Divide the distance calculated by the number of owls contributed to make the comparisons 1 vs 1 in each month
            self.normalizedMonthlyDistance = [x/y for x, y in zip(self.distanceByMonth, self.uniqueOwlsMonth)]
            # Calculate seasonal mean distance for standard deviation of seasons in different years
            self.calculateMean();
            # calculate standard deviation among seasons in different years
            self.calculateSD();
            # calculate monthly mean in different years for standard deviation among those in different years
            self.calculateMeanMonthly();
            self.calculateSDMonthly();
            # Make plots
            self.distancePlot(self.Seasons,self.normalizedDistance,self.sd, self.months, self.normalizedMonthlyDistance,self.sdMonthly)
            
            
    def distancePlot(self,seasons,distanceSeasons,seasonalSd, months,distancMonthly,sdMonthly):
        # Divide by 1000 to convert from meters to kms
        distanceSeasons= [x / 1000 for x in distanceSeasons]
        seasonalSd=[x / 1000 for x in seasonalSd]
        distancMonthly= [x / 1000 for x in distancMonthly]
        sdMonthly=[x / 1000 for x in sdMonthly]
        # Make seasonal distance and standard deviation scatter plots with shared x 
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        xn = range(len(seasons))
        a1 = ax1.scatter(xn, distanceSeasons, color='g', s=45, label='Average Distance')
        a2 = ax2.scatter(xn, seasonalSd, color='b',s=25, label='Standard Deviation')
        ax1.set_xlabel('Seasons')
        ax1.set_ylabel('Distance in seasons(in KM)', color='g')
        ax2.set_ylabel('Standard Deviation(in KM)', color='b')
        plt.xticks(xn, seasons)
        p = [a1, a2]
        ax1.legend(p, [p_.get_label() for p_ in p],loc= 'upper left', fontsize= 'small')
        plt.title('Seasonal average distance covered by Owl & Standard Deviation')
        plt.show()
        # Make monthly distance and standard deviation scatter plots with shared x
        fig, ax3 = plt.subplots()
        ax4 = ax3.twinx()
        xn = range(len(months))
        b1 = ax3.scatter(xn, distancMonthly,color='g',s=35, label='Average Distance')
        b2 = ax4.scatter(xn, sdMonthly,color='b',s=35, label='Standard Deviation')
        ax3.set_xlabel('Months')
        ax3.set_ylabel('Distance in months(in KM)', color='g')
        ax4.set_ylabel('Standard Deviation in months(in KM)', color='b')
        plt.xticks(xn, months)
        pl = [b1, b2]
        ax3.legend(pl, [p_.get_label() for p_ in pl],loc= 'upper left', fontsize= 'small')
        plt.title('Monthly average distance covered by owls & Standard Deviation')
        plt.show()
        # Make seasonal distance for boxplot in kms
        for i in range(len(self.matrixForBoxPlot)):
           for j in range(len(self.matrixForBoxPlot[i])):
                self.matrixForBoxPlot[i][j] = self.matrixForBoxPlot[i][j]/1000
        fig, ax = plt.subplots()
        ax.boxplot(self.matrixForBoxPlot)
        plt.xticks([1, 2, 3,4], ['Winter', 'Spring', 'Summer','Autumn'])
        plt.title('Seasonal distance traveled boxplot(in KM)')
        plt.show()
        
        # Make monthly distance box plot
        for i in range(len(self.matrixForMonthlyBoxPlot)):
           for j in range(len(self.matrixForMonthlyBoxPlot[i])):
                self.matrixForMonthlyBoxPlot[i][j] = self.matrixForMonthlyBoxPlot[i][j]/1000
        fig, ax = plt.subplots()
        ax.boxplot(self.matrixForMonthlyBoxPlot)
        plt.xticks([1, 2, 3,4,5,6,7,8,9,10,11,12], months)
        plt.title('Monthly distance traveled boxplot(in KM)')
        plt.show()
    # Calculate monthly mean
    def calculateMeanMonthly(self):
        for i in range(len(self.distanceMonth2011)):
            self.matrixForMonthlyBoxPlot.append([])
        counter = -1
        for one,two,three,four,five,six,seven in zip(self.distanceMonth2011,self.distanceMonth2012,self.distanceMonth2013,self.distanceMonth2014,self.distanceMonth2015,self.distanceMonth2016,self.distanceMonth2017):
            counter = counter+1
            if one!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(one)
            if two!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(two)
            if three!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(three)
            if four!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(four)
            if five!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(five)
            if six!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(six)
            if seven!=0:
               self.meanMonthCount[counter] = self.meanMonthCount[counter] + 1
               self.matrixForMonthlyBoxPlot[counter].append(seven)

    # Calculate seasonal mean for standard deviation
    def calculateMean(self):
        for i in range(len(self.distance2017)):
            self.matrixForBoxPlot.append([])
        counter = -1
        for one,two,three,four,five,six,seven in zip(self.distance2011,self.distance2012,self.distance2013,self.distance2014,self.distance2015,self.distance2016,self.distance2017):
            counter = counter+1
            if one!=0:
               self.matrixForBoxPlot[counter].append(one)
               self.meanCount[counter] = self.meanCount[counter] + 1
            if two!=0:
               self.matrixForBoxPlot[counter].append(two)
               self.meanCount[counter] = self.meanCount[counter] + 1
            if three!=0:
               self.matrixForBoxPlot[counter].append(three)
               self.meanCount[counter] = self.meanCount[counter] + 1
            if four!=0:
               self.matrixForBoxPlot[counter].append(four)
               self.meanCount[counter] = self.meanCount[counter] + 1
            if five!=0:
                self.matrixForBoxPlot[counter].append(five)
                self.meanCount[counter] = self.meanCount[counter] + 1
            if six!=0:
                self.matrixForBoxPlot[counter].append(six)
                self.meanCount[counter] = self.meanCount[counter] + 1
            if seven!=0:
                self.matrixForBoxPlot[counter].append(seven)
                self.meanCount[counter] = self.meanCount[counter] + 1
    # Calculate standard deviation among seasons in different years
    def calculateSD(self):
        meanDistance = [x/y for x, y in zip(self.distanceCovered, self.meanCount)]
        for i in range(4):
            self.sd[i] = math.sqrt(((self.distance2011[i] - meanDistance[i])**2 + (self.distance2012[i] - meanDistance[i])**2 + (self.distance2013[i] - meanDistance[i])**2 + (self.distance2014[i] - meanDistance[i])**2 + (self.distance2015[i] - meanDistance[i])**2 + (self.distance2016[i] - meanDistance[i])**2 + (self.distance2017[i] - meanDistance[i])**2)/self.meanCount[i])
    # Calculate standard monthly standard deviation among months of different year
    def calculateSDMonthly(self):
        meanMonthDistance = [x/y for x, y in zip(self.distanceByMonth, self.meanMonthCount)]
        for i in range(12):
            self.sdMonthly[i] = math.sqrt(((self.distanceMonth2011[i] - meanMonthDistance[i])**2 + (self.distanceMonth2012[i] - meanMonthDistance[i])**2 + (self.distanceMonth2013[i] - meanMonthDistance[i])**2 + (self.distanceMonth2014[i] - meanMonthDistance[i])**2 + (self.distanceMonth2015[i] - meanMonthDistance[i])**2 + (self.distanceMonth2016[i] - meanMonthDistance[i])**2 + (self.distanceMonth2017[i] - meanMonthDistance[i])**2)/self.meanMonthCount[i])
    # Calculate the distance between two points using the projected UTM east and UTM north fields in the dataset
    def calculateDistance(self,lat1,lon1,lat2,lon2):
        dlat=(lat2-lat1)**2
        dlon=(lon2-lon1)**2
        distance=math.sqrt(dlat + dlon);
        return distance; 
    # Calculate distance traveled in months across different years for use in standard deviation 
    def perYearMonth(self,date_year,month_id,distanceCalculated):
        if date_year == 2011:
            self.distanceMonth2011[month_id] = distanceCalculated + self.distanceMonth2011[month_id];
        elif date_year == 2012:
            self.distanceMonth2012[month_id] = distanceCalculated + self.distanceMonth2012[month_id];
        elif date_year == 2013:
            self.distanceMonth2013[month_id] = distanceCalculated + self.distanceMonth2013[month_id];
        elif date_year == 2014:
            self.distanceMonth2014[month_id] = distanceCalculated + self.distanceMonth2014[month_id];
        elif date_year == 2015:
            self.distanceMonth2015[month_id] = distanceCalculated + self.distanceMonth2015[month_id];
        elif date_year == 2016:
            self.distanceMonth2016[month_id] = distanceCalculated + self.distanceMonth2016[month_id];
        elif date_year == 2017:
            self.distanceMonth2017[month_id] = distanceCalculated + self.distanceMonth2017[month_id];
    # Calculate distance traveled in seasons across different years for use in standard deviation  
    def perYear(self,date_year,seasonIn,distanceCalculated):
        if date_year == 2011:
            self.distance2011[seasonIn] = distanceCalculated + self.distance2011[seasonIn];
        elif date_year == 2012:
            self.distance2012[seasonIn] = distanceCalculated + self.distance2012[seasonIn];
        elif date_year == 2013:
            self.distance2013[seasonIn] = distanceCalculated + self.distance2013[seasonIn];
        elif date_year == 2014:
            self.distance2014[seasonIn] = distanceCalculated + self.distance2014[seasonIn];
        elif date_year == 2015:
            self.distance2015[seasonIn] = distanceCalculated + self.distance2015[seasonIn];
        elif date_year == 2016:
            self.distance2016[seasonIn] = distanceCalculated + self.distance2016[seasonIn];
        elif date_year == 2017:
            self.distance2017[seasonIn] = distanceCalculated + self.distance2017[seasonIn];
   # Count unique tags(owls) in seasons across different years for use normalization and average
    def perYearUnique(self,date_year,seasonIn,tag_ident):
        if date_year == 2011:
            if tag_ident not in self.tags2011:
                    self.uniqueOwls2011[seasonIn] = self.uniqueOwls2011[seasonIn]+ 1
                    self.tags2011.append(tag_ident)
        elif date_year == 2012:
            if tag_ident not in self.tags2012:
                    self.uniqueOwls2012[seasonIn] = self.uniqueOwls2012[seasonIn]+ 1
                    self.tags2012.append(tag_ident)
        elif date_year == 2013:
            if tag_ident not in self.tags2013:
                    self.uniqueOwls2013[seasonIn] = self.uniqueOwls2013[seasonIn]+ 1
                    self.tags2013.append(tag_ident)
        elif date_year == 2014:
            if tag_ident not in self.tags2014:
                    self.uniqueOwls2014[seasonIn] = self.uniqueOwls2014[seasonIn]+ 1
                    self.tags2014.append(tag_ident)
        elif date_year == 2015:
            if tag_ident not in self.tags2015:
                    self.uniqueOwls2015[seasonIn] = self.uniqueOwls2015[seasonIn]+ 1
                    self.tags2015.append(tag_ident)
        elif date_year == 2016:
            if tag_ident not in self.tags2016:
                    self.uniqueOwls2016[seasonIn] = self.uniqueOwls2016[seasonIn]+ 1
                    self.tags2016.append(tag_ident)
        elif date_year == 2017:
            if tag_ident not in self.tags2017:
                    self.uniqueOwls2017[seasonIn] = self.uniqueOwls2017[seasonIn]+ 1
                    self.tags2017.append(tag_ident)
    # Count unique tags in months across different years for use normalization and average
    def checkUniqueMonthly(self,tag_ident,monthId):
        if monthId == 0:
            if tag_ident not in self.tagsJan:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsJan.append(tag_ident)
        elif monthId == 1:
            if tag_ident not in self.tagsFeb:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsFeb.append(tag_ident)
        elif monthId == 2:
            if tag_ident not in self.tagsMar:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsMar.append(tag_ident)
        elif monthId == 3:
            if tag_ident not in self.tagsApr:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsApr.append(tag_ident)
        elif monthId == 4:
            if tag_ident not in self.tagsMay:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsMay.append(tag_ident)
        elif monthId == 5:
            if tag_ident not in self.tagsJun:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsJun.append(tag_ident)
        elif monthId == 6:
            if tag_ident not in self.tagsJul:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsJul.append(tag_ident)
        elif monthId == 7:
            if tag_ident not in self.tagsAug:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsAug.append(tag_ident)
        elif monthId == 8:
            if tag_ident not in self.tagsSept:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsSept.append(tag_ident)
        elif monthId == 9:
            if tag_ident not in self.tagsOct:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsOct.append(tag_ident)
        elif monthId == 10:
            if tag_ident not in self.tagsNov:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsNov.append(tag_ident)
        elif monthId ==11:
            if tag_ident not in self.tagsDec:
                    self.uniqueOwlsMonth[monthId] = self.uniqueOwlsMonth[monthId]+ 1
                    self.tagsDec.append(tag_ident)
    # Main function to check the season based on timestamp and call distance functions based on seasons
    def performComputation(self,selected_features):
        counter = 0;
        pnt_prev_x=[0,0,0,0];
        pnt_prev_y=[0,0,0,0];
        pnt_intial_x=0;
        pnt_intial_y=0;
        # Get the first location for distance calculation
        for feat in selected_features:
            pnt_intial_x=feat['utm_east'];
            pnt_intial_y=feat['utm_north'];
            break;
        # Start from the second field to calculate distance and add to the corresponding variable storage
        for feature in selected_features:
            counter = counter + 1;
            tag_timestamp = feature['timestamp']
            tag_ident = feature['tag_ident']
            pnt_now= feature.geometry();
            dt = datetime.strptime(tag_timestamp, '%Y-%m-%d %H:%M:%S')
            pnt_now_x=feature['utm_east'];
            pnt_now_y=feature['utm_north'];
            date_year = dt.year;
            date_day = dt.month+dt.day/30
            
            if date_day >= 6.7 and date_day <=9.7: #Summer
                self.owlsType[2] = self.owlsType[2]+1
                self.coordinatesX[2] = pnt_now_x;
                self.coordinatesY[2] = pnt_now_y;
                if pnt_prev_x[2]==0:
                    pnt_prev_x[2]=pnt_intial_x;
                    pnt_prev_y[2]=pnt_intial_y;
                else:
                    #Calculate distance
                    distanceCalculated = self.calculateDistance(pnt_prev_x[2],pnt_prev_y[2],self.coordinatesX[2],self.coordinatesY[2]);
                    #add the distance to a season based on year
                    self.perYear(date_year,2,distanceCalculated)
                    #Count the number of unique owls contributing to the calculation
                    self.perYearUnique(date_year,2,tag_ident)
                    #add the distance by month 
                    self.distanceByMonth[dt.month-1] = self.distanceByMonth[dt.month-1] + distanceCalculated;
                    #Count the number of unique owls contributing to the calculation in a month
                    self.checkUniqueMonthly(tag_ident,dt.month-1)
                    #add the distance to a month based on year
                    self.perYearMonth(date_year,dt.month-1,distanceCalculated)
                    #Add the total distance calculated in season
                    self.distanceCovered[2]=self.distanceCovered[2]+distanceCalculated
                    #Make this location the previous for the next iteration
                    pnt_prev_x[2]=self.coordinatesX[2];
                    pnt_prev_y[2]=self.coordinatesY[2];
                if tag_ident not in self.tags02:
                    self.uniqueOwls[2] = self.uniqueOwls[2]+1;
                    self.tags02.append(tag_ident)
                    self.seasonsText.append('summer')
            elif date_day >12.6 or (date_day>=1 and date_day<3.6): #Winter
                if self.startTimeStamp[0] == '':
                    self.startTimeStamp[0]=tag_timestamp;
                else:
                    self.endTimeStamp[0]=tag_timestamp;
                self.owlsType[0] = self.owlsType[0]+1
                self.coordinatesX[0] = pnt_now_x;
                self.coordinatesY[0] = pnt_now_y;
                if pnt_prev_x[0]==0:
                    pnt_prev_x[0]=pnt_intial_x;
                    pnt_prev_y[0]=pnt_intial_y;
                else:
                    distanceCalculated = self.calculateDistance(pnt_prev_x[0],pnt_prev_y[0],self.coordinatesX[0],self.coordinatesY[0]);
                    self.perYearUnique(date_year,0,tag_ident)
                    self.perYear(date_year,0,distanceCalculated)
                    self.distanceByMonth[dt.month-1] = self.distanceByMonth[dt.month-1] + distanceCalculated;
                    self.checkUniqueMonthly(tag_ident,dt.month-1);
                    self.perYearMonth(date_year,dt.month-1,distanceCalculated)
                    self.distanceCovered[0]=self.distanceCovered[0]+distanceCalculated
                    pnt_prev_x[0]=self.coordinatesX[0];
                    pnt_prev_y[0]=self.coordinatesY[0];
                if tag_ident not in self.tags00:
                    self.uniqueOwls[0] = self.uniqueOwls[0]+ 1
                    self.tags00.append(tag_ident)
                    self.seasonsText.append('winter')
            elif (date_day >=3.6 and date_day <6.7): #Spring
                if self.startTimeStamp[1] == '':
                    self.startTimeStamp[1]=tag_timestamp;
                else:
                    self.endTimeStamp[1]=tag_timestamp;
                self.owlsType[1] = self.owlsType[1]+1
                self.coordinatesX[1] = pnt_now_x;
                self.coordinatesY[1] = pnt_now_y;
                if pnt_prev_x[1]==0:
                    pnt_prev_x[1]=pnt_intial_x;
                    pnt_prev_y[1]=pnt_intial_y;
                else:
                    distanceCalculated = self.calculateDistance(pnt_prev_x[1],pnt_prev_y[1],self.coordinatesX[1],self.coordinatesY[1]);
                    self.perYearUnique(date_year,1,tag_ident)
                    self.perYear(date_year,1,distanceCalculated)
                    self.distanceByMonth[dt.month-1] = self.distanceByMonth[dt.month-1] + distanceCalculated;
                    self.perYearMonth(date_year,dt.month-1,distanceCalculated)
                    self.checkUniqueMonthly(tag_ident,dt.month-1);
                    self.distanceCovered[1]=self.distanceCovered[1]+distanceCalculated
                    pnt_prev_x[1]=self.coordinatesX[1];
                    pnt_prev_y[1]=self.coordinatesY[1];
                if tag_ident not in self.tags01:
                    self.uniqueOwls[1] = self.uniqueOwls[1]+1;
                    self.tags01.append(tag_ident)
                    self.seasonsText.append('spring')
            else: #autumn
                if self.startTimeStamp[3] == '':
                    self.startTimeStamp[3]=tag_timestamp;
                else:
                    self.endTimeStamp[3]=tag_timestamp;
                self.owlsType[3] = self.owlsType[3]+1
                self.coordinatesX[3] = pnt_now_x;
                self.coordinatesY[3] = pnt_now_y;
                if pnt_prev_x[3]==0:
                    pnt_prev_x[3]=pnt_intial_x;
                    pnt_prev_y[3]=pnt_intial_y;
                else:
                    distanceCalculated = self.calculateDistance(pnt_prev_x[3],pnt_prev_y[3],self.coordinatesX[3],self.coordinatesY[3]);
                    self.perYearUnique(date_year,3,tag_ident)
                    self.perYear(date_year,3,distanceCalculated)
                    self.distanceByMonth[dt.month-1] = self.distanceByMonth[dt.month-1] + distanceCalculated;
                    self.checkUniqueMonthly(tag_ident,dt.month-1);
                    self.perYearMonth(date_year,dt.month-1,distanceCalculated)
                    self.distanceCovered[3]=self.distanceCovered[3]+self.calculateDistance(pnt_prev_x[3],pnt_prev_y[3],self.coordinatesX[3],self.coordinatesY[3])
                    pnt_prev_x[3]=self.coordinatesX[3];
                    pnt_prev_y[3]=self.coordinatesY[3];
                if tag_ident not in self.tags03:
                    self.uniqueOwls[3] = self.uniqueOwls[3]+1
                    self.tags03.append(tag_ident)
                    self.seasonsText.append('autumn')