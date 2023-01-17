function Component()
{
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("Execute", "@TargetDir@/bin/cert_importer.exe", "--silent", "--target=@TargetDir@/share/ssl/certs/");
    }
}
