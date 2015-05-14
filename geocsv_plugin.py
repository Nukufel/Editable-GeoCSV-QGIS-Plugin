# -*- coding: utf-8 -*-
"""
/***************************************************************************
Editable GeoCSV
A QGIS plugin
                              -------------------
begin                : 2015-04-29        
copyright            : (C) 2015 by geometalab
email                : geometalab@gmail.com
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

import os.path
 
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QIcon, QAction
import resources_rc
from geocsv_controller import GeoCsvNewController, GeoCsvReconnectController

# import sys;
# sys.path.append(r'/Applications/liclipse/plugins/org.python.pydev_3.9.2.201502042042/pysrc')
# import pydevd

class EditableGeoCsv:
    
    def __init__(self, iface):          
#         pydevd.settrace()                    
        self.iface = iface        
        self.plugin_dir = os.path.dirname(__file__)        
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir,'i18n','geocsv_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
                        
        #container for all csv vector layers                        
        self.csvVectorLayers = []          
        #if the project file is successfully read, reconnect all CsvVectorLayers with datasource
        iface.projectRead.connect(lambda: GeoCsvReconnectController.getInstance().reconnectCsvVectorLayers(self.csvVectorLayers))
                                                      
    def initGui(self):
        self.toolbar = self.iface.addToolBar('geocsveditor')
        self.toolbar.setObjectName('geocsveditor')        
        addGeoCsvLayerIcon = QIcon(':/plugins/editablegeocsv/geocsv.png')
        addGeoCsvLayerText = QCoreApplication.translate('EditableGeoCsv', 'Add GeoCSV layer')        
        self.addGeoCsvLayerAction = QAction(addGeoCsvLayerIcon, addGeoCsvLayerText, self.iface.mainWindow())
        self.addGeoCsvLayerAction.triggered.connect(lambda: GeoCsvNewController.getInstance().createCsvVectorLayer(self.csvVectorLayers))
        self.toolbar.addAction(self.addGeoCsvLayerAction)
        self.iface.addPluginToMenu(QCoreApplication.translate('EditableGeoCsv', 'Editable GeoCSV'), self.addGeoCsvLayerAction)
                    
    def unload(self):        
        self.iface.removePluginMenu(
            QCoreApplication.translate('EditableGeoCsv', 'Editable GeoCSV'),
            self.addGeoCsvLayerAction)
        self.iface.removeToolBarIcon(self.addGeoCsvLayerAction)        
        del self.toolbar      