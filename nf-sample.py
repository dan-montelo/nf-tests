import rhinoscriptsyntax as rs

nf = rs.GetPlugInObject('NorhternFlicker')

objs =rs.GetObjects("Pick a brep.", 16, True, False, False)

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




