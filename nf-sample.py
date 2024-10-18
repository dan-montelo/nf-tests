import rhinoscriptsyntax as rs

#this is the key- currently this prints None.
nf = rs.GetPlugInObject('NorthernFlicker')
print (nf)
#print results
# #None

#with cadwork tools plugin loaded.
cw = rs.GetPlugInObject('CadworkTools')
print (cw)
#print results
#<CadworkTools.CadworkToolsScriptAccess object at 0x000000000000012A [CadworkTools.CadworkToolsScriptAccess]>

objs =rs.GetObjects("Pick a brep.", 16, True, False, False)

#if nf returned a NorthernFlicker.NorthernFlickerScriptAccess object at ....... then this would work:
for obj in objs:
    Width = nf.Width
    Depth = nf.Height
    Length = nf.Length
    vWidth = nf.vWidth
    vDepth = nf.vDepth
    vLength = nf.vLength
    ptStart = nf.ptStart
    ptEnd = nf.ptEnd
    refSrfPlane = nf.refSrfPlane
    bBox = nf.bBox
    BBoxVolume = nf.BBoxVolume




