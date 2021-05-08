
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("afterinstall","GDAL python"));
    component.setValue("Description",qsTranslate("afterinstall","GDAL python bindings"));
}

function create_bat(py_name)
{
    var contentString = "$echooff$python \"@TargetDir@\\bin\\"  + py_name + ".py\" %*";
    component.addOperation("AppendFile", "@TargetDir@\\bin\\" + py_name + ".bat", contentString);
    component.addOperation("Replace", "@TargetDir@\\bin\\" + py_name + ".bat", "$echooff$", "@");    
};

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        create_bat("epsg_tr");
        create_bat("esri2wkt");
        create_bat("gcps2vec");
        create_bat("gcps2wld");
        create_bat("gdal2tiles");
        create_bat("gdal2xyz");
        create_bat("gdal_fillnodata");
        create_bat("gdal_merge");
        create_bat("gdal_polygonize");
        create_bat("gdal_proximity");
        create_bat("gdal_retile");
        create_bat("gdal_sieve");
        create_bat("gdalchksum");
        create_bat("gdalident");
        create_bat("gdalimport");
        create_bat("mkgraticule");
        create_bat("pct2rgb");
        create_bat("rgb2pct");
        create_bat("gdal_calc");
        create_bat("ogrmerge");
        create_bat("gdal_pansharpen");
        create_bat("gdal_edit");
    }
}
