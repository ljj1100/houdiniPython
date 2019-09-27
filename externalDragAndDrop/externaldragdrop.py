import os
import re

def dropAccept(filelist):

    file_list_split = filelist[0]
    path_txt = os.path.splitext(file_list_split)[1]

    if file_list_split and path_txt == ".hip":
        return True

    if file_list_split and path_txt == ".fbx":
        openUI(file_list_split)
        return True

    if file_list_split and path_txt == ".abc":
        geo = hou.node("/obj").createNode("geo")
        alembic_node = geo.createNode('alembic',node_name='Alembic')
        alembic_node.parm('fileName').set(file_list_split)
        return True


def openUI(filename):
    cam_check  = hou.ui.readMultiInput("What is the type?", (), buttons = ("cam", "object"))
    if cam_check[0] == 0:
    ##### import fbxCam
        fbx_import = hou.hipFile.importFBX(filename)
    ##### resolution setting
        houdini_ui = hou.ui.readMultiInput("Camera Setting", ("cam resolution x", "cam resolution y",), buttons = ("set", "defalt"), initial_contents=("1280", "720"))
        ui_button  = houdini_ui[0]
        ui_text    = houdini_ui[1]
    ##### import camera setting
        find_cam = [cam for cam in fbx_import[0].children() if cam.type().name()=="cam"]
        find_cam[0].setInput(0,(fbx_import[0].indirectInputs()[0]))
    ##### set Vector
        create_setVector = fbx_import[0].createNode("geo")
        create_setVector.setInput(0, find_cam[0])
        add_node = create_setVector.createNode("add")
        wrangle_node = create_setVector.createNode("attribwrangle")
    ##### parm setting
        add_node.parm("usept0").set(1)
        wrangle_node.parm("snippet").set("""v@up = {1,0,0};
v@N = {0,0,1};""")
    ##### input setting
        null_node = hou.node("/obj").createNode("null")
        fbx_import[0].setInput(0, null_node)
        wrangle_node.setInput(0, add_node)
    ##### create rivitSetting
        rivet_node = hou.node("/obj").createNode("rivet")
        rivet_node.parm("rivetsop").set(wrangle_node.path())
        rivet_node.parm("rivetgroup").set("0")
        rivet_node.parm("rivetuseattribs").set(1)
    ##### copy setting
        copy_node = hou.copyNodesTo(find_cam, hou.node("/obj"))
        copy_node[0].setInput(0, rivet_node)
        copy_node[0].parmTuple("t").set((0,0,0))
        copy_node[0].parmTuple("t").deleteAllKeyframes()
        copy_node[0].parmTuple("r").set((0, 0, 0))
        copy_node[0].parmTuple("r").deleteAllKeyframes()
        ##### copy parm
        if ui_button==0:
            copy_node[0].parmTuple("res").set((int(ui_text[0]), int(ui_text[1])))
        return ui_button, ui_text

    else:
        fbx_import = hou.hipFile.importFBX(filename)
        return fbx_import