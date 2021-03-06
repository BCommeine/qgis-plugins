# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ObjectLocker
                                 A QGIS plugin
 This plugin locks the selected objects
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-12-16
        copyright            : (C) 2021 by Attic Development
        email                : xxx
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

__author__ = 'Attic Development'
__date__ = '2021-12-16'
__copyright__ = '(C) 2021 by Attic Development'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis._core import QgsMessageLog
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       edit)


class ObjectLockerAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)

        fields = input_layer.fields()
        fieldnames = [field.name() for field in input_layer.fields()]

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / input_layer.featureCount() if input_layer.featureCount() else 0

        if 'LOCKED' not in fieldnames:
            QgsMessageLog.logMessage("This layer doesn't contain a LOCKED attribute.", 'Custom Logging')
            return {self.OUTPUT: None}

        input_layer.startEditing()

        if len(list(input_layer.getSelectedFeatures())) > 0:
            features = input_layer.getSelectedFeatures()
        else:
            features = input_layer.getFeatures()

        update_counter = 0

        for current, f in enumerate(features):

            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            # Check the number of updated features
            if f.attribute('LOCKED') == 'F':
                update_counter += 1

            # Set LOCKED attribute to TRUE ('T')
            f.setAttribute('LOCKED', 'T')

            # Save updated feature to source_layer
            input_layer.updateFeature(f)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        input_layer.commitChanges()

        QgsMessageLog.logMessage(f"{update_counter} features updated", 'Custom Logging')

        return {self.OUTPUT: None}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Lock Objects'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ObjectLockerAlgorithm()
