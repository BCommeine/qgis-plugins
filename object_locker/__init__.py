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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Attic Development'
__date__ = '2021-12-16'
__copyright__ = '(C) 2021 by Attic Development'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ObjectLocker class from file ObjectLocker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .object_locker import ObjectLockerPlugin
    return ObjectLockerPlugin()
