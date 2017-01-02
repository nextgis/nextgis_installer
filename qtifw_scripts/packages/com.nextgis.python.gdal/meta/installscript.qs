/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2016 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

function Component()
{

}

function CreateSymLink(name)
{
    component.addElevatedOperation("Execute", "{0}", "ln", "-s",
        "@TargetDir@/Applications/gdal.app/Contents/MacOS/" + name,
        "/usr/local/bin/" + name);
    component.registerPathForUninstallation("/usr/local/bin/" + name);
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        var utilities = [
            "epsg_tr.py",
            "esri2wkt.py",
            "gcps2vec.py",
            "gcps2wld.py",
            "gdal2tiles.py",
            "gdal2xyz.py",
            "gdal_fillnodata.py",
            "gdal_merge.py",
            "gdal_polygonize.py",
            "gdal_proximity.py",
            "gdal_retile.py",
            "gdal_sieve.py",
            "gdalchksum.py",
            "gdalident.py",
            "gdalimport.py",
            "mkgraticule.py",
            "pct2rgb.py",
            "rgb2pct.py"
        ];

        for ( i = 0; i < utilities.length; i++ ) {
            CreateSymLink(utilities[i]);
        }
    }
}
