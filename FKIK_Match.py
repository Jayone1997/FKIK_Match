import maya.cmds as cmds
from functools import partial

limb_data_dict = {}
global_limb_name = ""
upperLOC = ""
lowerLOC = ""
endLOC = ""
upperJnt = ""
lowerJnt = ""
endJnt = ""

def Import_data(*args):
    file_browse = cmds.fileDialog2(fileFilter="Maya Files (*.ma *.mb)", dialogStyle=2, fileMode=1, okCaption="Import", caption="Import Data")
    
    if file_browse:
        imported = cmds.file(file_browse[0], i=True, type="mayaBinary", returnNewNodes=True, ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True, importTimeRange="combine", preserveReferences=True)
        
        ik_fk_data = cmds.listRelatives(imported[0], children=True)
        
        cmds.select(imported[0], replace=True)
        sel = cmds.ls(selection=True)
        
        if sel[0] == "FK_IK_Limb_grp":
            print("Data successfully imported")
        else:
            cmds.parent(ik_fk_data, "FK_IK_Limb_grp")
            cmds.delete(imported[0])

    if cmds.objExists("FK_IK_Limb_grp"):
        child_objects = cmds.listRelatives("FK_IK_Limb_grp", children=True)

        if child_objects:
            existing_items = cmds.textScrollList(my_list, query=True, allItems=True)
            
            for child in child_objects:
                
                if existing_items and child in existing_items:
                    cmds.textScrollList(my_list, edit=True, removeItem=child)

                cmds.textScrollList(my_list, edit=True, append=child)

def Export_data(*args):
    cmds.select('FK_IK_Limb_grp', replace=True)
    cmds.ExportSelectionOptions()

    cmds.checkBoxGrp('exInHistoryBox', edit=True, enable=False, value1=False)
    cmds.checkBoxGrp('exInChannelsBox', edit=True, enable=False, value1=False)
    cmds.checkBoxGrp('exInExpressionsBox', edit=True, enable=False, value1=False)
    cmds.checkBoxGrp('exInConstraintsBox', edit=True, enable=False, value1=False)
    
    cmds.ExportSelection()

def Activate_RefreshButton(*args):
    text_fields = [textField1, textField2, textField3, textField4, textField5, textField6, textField7, textField8, textField9, textField9_Atr]
    for tf in text_fields:
        cmds.textField(tf, edit=True, text="")

    if cmds.objExists("FK_IK_Limb_grp"):
        child_objects = cmds.listRelatives("FK_IK_Limb_grp", children=True)

        if child_objects: 
            existing_items = cmds.textScrollList(my_list, query=True, allItems=True)
        
            for child in child_objects:
                
                if existing_items and child in existing_items:
                    cmds.textScrollList(my_list, edit=True, removeItem=child)
                
                cmds.textScrollList(my_list, edit=True, append=child)

    if not cmds.objExists("FK_IK_Limb_grp"):
        cmds.textScrollList(my_list, edit=True, removeAll=True)

        if cmds.textScrollList(ActivatedLimb, query=True, numberOfItems=True):
            cmds.textScrollList(ActivatedLimb, edit=True, removeAll=True)
    
def Activate_AddButton(textField, *args):
    selected_objects = cmds.ls(selection=True)

    if len(selected_objects) == 1:
        selected_object_name = selected_objects[0]
        cmds.textField(textField, edit=True, text=selected_object_name)
    else:
        pass

def Activate_SearchAndReplace(*args):
    search_text = cmds.textField(textField10, query=True, text=True)
    replace_text = cmds.textField(textField11, query=True, text=True)
    
    if search_text and replace_text:
        for tf in [textField1, textField2, textField3, textField4, textField5, textField6, textField7, textField8, textField9]:
            current_text = cmds.textField(tf, query=True, text=True)
            if search_text in current_text:
                new_text = current_text.replace(search_text, replace_text)
                cmds.textField(tf, edit=True, text=new_text)        

def Activate_ActiveButton(*args):
    # Check if all text fields have text
    all_text_fields = [textField1, textField2, textField3, textField4, textField5, textField6, textField7, textField8, textField9]
    
    if all(cmds.textField(tf, query=True, text=True) for tf in all_text_fields):
        createLimbNamePopup()

    else:
        cmds.confirmDialog(title='Warning', message='Add all limb data', button=['OK'], defaultButton='OK')

def Activate_AddLimbName(limbNameField, *args):
    limb_name = cmds.textField(limbNameField, query=True, text=True)

    AddLimbAvailable(limb_name)
    LimbPrepare(limb_name)

def createLimbNamePopup():
    if cmds.window("LimbNamePopup", exists=True):
        cmds.deleteUI("LimbNamePopup", window=True)

    cmds.window("LimbNamePopup", title="Add Limb Name", widthHeight=(230, 70))
    cmds.columnLayout(adjustableColumn=True, columnOffset=("both", 5))
    cmds.separator(height=10)
    limbNameField = cmds.textField(placeholderText="Enter Limb Name")
    cmds.separator(height=10)
    cmds.button(label="Add", width = 100, align='center', command=partial(Activate_AddLimbName, limbNameField))
    cmds.showWindow("LimbNamePopup")

def AddLimbAvailable(limb_name, *args):
    global global_limb_name

    if limb_name:
        global_limb_name = limb_name

        if not cmds.objExists(limb_name):
            cmds.group(em=True, name=limb_name)

        cmds.textScrollList(my_list, edit=True, append=limb_name)
        limb_data = [cmds.textField(tf, query=True, text=True) for tf in [textField1, textField2, textField3, textField4, textField5, textField6, textField7, textField8, textField9, textField9_Atr, textField9b, textField9c]]
        limb_data_dict[limb_name] = limb_data

        cmds.deleteUI("LimbNamePopup", window=True)
    else:
        cmds.warning("Please enter a valid limb name")

def LimbPrepare(limb_name,*args):
        global group_name0
        group_name0 = "FK_IK_Limb_grp"
        
        cmds.select(clear=True)
        
        if not cmds.objExists(group_name0):
            cmds.group(em=True, name=group_name0)

        text_in_textField1 = cmds.textField(textField1, query=True, text=True)
        text_in_textField2 = cmds.textField(textField2, query=True, text=True)
        text_in_textField3 = cmds.textField(textField3, query=True, text=True)
        text_in_textField4 = cmds.textField(textField4, query=True, text=True)
        text_in_textField5 = cmds.textField(textField5, query=True, text=True)
        text_in_textField6 = cmds.textField(textField6, query=True, text=True)
        text_in_textField7 = cmds.textField(textField7, query=True, text=True)
        text_in_textField8 = cmds.textField(textField8, query=True, text=True)
        text_in_textField9 = cmds.textField(textField9, query=True, text=True)
        text_in_textField9_Atr = cmds.textField(textField9_Atr, query=True, text=True)
        text_in_textField9b = cmds.textField(textField9b, query=True, text=True)
        text_in_textField9c = cmds.textField(textField9c, query=True, text=True)
        
        # Create a locator with the name "{text_in_textField1}Jnt"
        upperLOC = text_in_textField1 + "_LOC"
        lowerLOC = text_in_textField2 + "_LOC"
        endLOC = text_in_textField3 + "_LOC"
        FKupperLOC = text_in_textField4 + "_LOC"
        FKlowerLOC = text_in_textField5 + "_LOC"
        FKendLOC = text_in_textField6 + "_LOC"
        PolevectorLOC = text_in_textField7 + "_LOC"
        IKendLOC = text_in_textField8 + "_LOC"
        
        upperJnt = text_in_textField1 + "_grp"
        lowerJnt = text_in_textField2 + "_grp"
        endJnt = text_in_textField3 + "_grp"
        FKupperJnt = text_in_textField4 + "_grp"
        FKlowerJnt = text_in_textField5 + "_grp"
        FKendJnt = text_in_textField6 + "_grp"
        IKendJnt = text_in_textField8 + "_grp"

        cmds.spaceLocator(name=upperLOC)
        cmds.spaceLocator(name=lowerLOC)
        cmds.spaceLocator(name=endLOC)

        cmds.spaceLocator(name=FKupperLOC)
        cmds.spaceLocator(name=FKlowerLOC)
        cmds.spaceLocator(name=FKendLOC)
        cmds.spaceLocator(name=PolevectorLOC)
        cmds.spaceLocator(name=IKendLOC)
        
        #cmds.group(em=True, name=group_name0)
        cmds.group(em=True, name=upperJnt)
        cmds.group(em=True, name=lowerJnt)
        cmds.group(em=True, name=endJnt)
        cmds.group(em=True, name=FKupperJnt)
        cmds.group(em=True, name=FKlowerJnt)
        cmds.group(em=True, name=FKendJnt)
        cmds.group(em=True, name=IKendJnt)

        cmds.parent(upperLOC, upperJnt)
        cmds.parent(lowerLOC, lowerJnt)
        cmds.parent(endLOC, endJnt)
        cmds.parent(FKupperLOC, FKupperJnt)
        cmds.parent(FKlowerLOC, FKlowerJnt)
        cmds.parent(FKendLOC, FKendJnt)
        cmds.parent(IKendLOC, IKendJnt)
        cmds.parent(PolevectorLOC, lowerLOC)

        cmds.setAttr(endLOC+ ".translate", 0, 0, 0)
        cmds.setAttr(endLOC + ".rotate", 0, 0, 0)
        
        parent_constraint_grp1 = cmds.parentConstraint(text_in_textField1, upperJnt, weight=1)
        cmds.delete(parent_constraint_grp1)
        parent_constraint_grp2 = cmds.parentConstraint(text_in_textField2, lowerJnt, weight=1)
        cmds.delete(parent_constraint_grp2)
        parent_constraint_grp3 = cmds.parentConstraint(text_in_textField3, endJnt, weight=1)
        cmds.delete(parent_constraint_grp3)
        parent_constraint_grp4 = cmds.parentConstraint(text_in_textField4, FKupperJnt, weight=1)
        cmds.delete(parent_constraint_grp4)
        parent_constraint_grp5 = cmds.parentConstraint(text_in_textField5, FKlowerJnt, weight=1)
        cmds.delete(parent_constraint_grp5)
        parent_constraint_grp6 = cmds.parentConstraint(text_in_textField6, FKendJnt, weight=1)
        cmds.delete(parent_constraint_grp6)
        parent_constraint_grp8 = cmds.parentConstraint(text_in_textField6, IKendJnt, weight=1)
        cmds.delete(parent_constraint_grp8)

        parent_constraint_loc1 = cmds.parentConstraint(text_in_textField1, upperLOC, weight=1)
        cmds.delete(parent_constraint_loc1)
        parent_constraint_loc2 = cmds.parentConstraint(text_in_textField2, lowerLOC, weight=1)
        cmds.delete(parent_constraint_loc2)
        parent_constraint_loc3 = cmds.parentConstraint(text_in_textField3, endLOC, weight=1)
        cmds.delete(parent_constraint_loc3)
        parent_constraint_loc4 = cmds.parentConstraint(text_in_textField4, FKupperLOC, weight=1)
        cmds.delete(parent_constraint_loc4)
        parent_constraint_loc5 = cmds.parentConstraint(text_in_textField5, FKlowerLOC, weight=1)
        cmds.delete(parent_constraint_loc5)
        parent_constraint_loc6 = cmds.parentConstraint(text_in_textField6, FKendLOC, weight=1)
        cmds.delete(parent_constraint_loc6)
        parent_constraint_grp7 = cmds.parentConstraint(text_in_textField7, PolevectorLOC, weight=1)
        cmds.delete(parent_constraint_grp7)
        parent_constraint_loc8 = cmds.parentConstraint(text_in_textField8, IKendLOC, weight=1)
        cmds.delete(parent_constraint_loc8)

        cmds.parent(upperJnt, global_limb_name)
        cmds.parent(lowerJnt, global_limb_name)
        cmds.parent(endJnt, global_limb_name)
        cmds.parent(FKupperJnt, global_limb_name)
        cmds.parent(FKlowerJnt, global_limb_name)
        cmds.parent(FKendJnt, global_limb_name)
        cmds.parent(IKendJnt, global_limb_name)

        cmds.setAttr(global_limb_name + ".visibility", 0)
        cmds.parent(global_limb_name, group_name0)

        cmds.addAttr(limb_name, longName="Shoulder_Joint", dataType="string")
        cmds.setAttr(limb_name + ".Shoulder_Joint", text_in_textField1, type="string")

        cmds.addAttr(limb_name, longName="Elbow_Joint", dataType="string")
        cmds.setAttr(limb_name + ".Elbow_Joint", text_in_textField2, type="string")

        cmds.addAttr(limb_name, longName="Wrist_Joint", dataType="string")
        cmds.setAttr(limb_name + ".Wrist_Joint", text_in_textField3, type="string")

        cmds.addAttr(limb_name, longName="FK_Shoulder_Ctrl", dataType="string")
        cmds.setAttr(limb_name + ".FK_Shoulder_Ctrl", text_in_textField4, type="string")

        cmds.addAttr(limb_name, longName="FK_Elbow_Ctrl", dataType="string")
        cmds.setAttr(limb_name + ".FK_Elbow_Ctrl", text_in_textField5, type="string")

        cmds.addAttr(limb_name, longName="FK_Wrist_Ctrl", dataType="string")
        cmds.setAttr(limb_name + ".FK_Wrist_Ctrl", text_in_textField6, type="string")

        cmds.addAttr(limb_name, longName="PoleVector_Ctrl", dataType="string")
        cmds.setAttr(limb_name + ".PoleVector_Ctrl", text_in_textField7, type="string")

        cmds.addAttr(limb_name, longName="IK_Wrist_Ctrl", dataType="string")
        cmds.setAttr(limb_name + ".IK_Wrist_Ctrl", text_in_textField8, type="string")

        cmds.addAttr(limb_name, longName="FKIK_Switch", dataType="string")
        cmds.setAttr(limb_name + ".FKIK_Switch", text_in_textField9, type="string")

        cmds.addAttr(limb_name, longName="FKIK_SwitchAttr", dataType="string")
        cmds.setAttr(limb_name + ".FKIK_SwitchAttr", text_in_textField9_Atr, type="string")

        cmds.addAttr(limb_name, longName="FK_Value", dataType="string")
        cmds.setAttr(limb_name + ".FK_Value", text_in_textField9b, type="string")

        cmds.addAttr(limb_name, longName="IK_Value", dataType="string")
        cmds.setAttr(limb_name + ".IK_Value", text_in_textField9c, type="string")        

def List_DoubleClick(*args):
    selection_01 = cmds.textScrollList(my_list, query=True, selectItem=True)[0]
    
    cmds.textField(textField1, edit=True, text=cmds.getAttr(selection_01 + ".Shoulder_Joint"))
    cmds.textField(textField2, edit=True, text=cmds.getAttr(selection_01 + ".Elbow_Joint"))
    cmds.textField(textField3, edit=True, text=cmds.getAttr(selection_01 + ".Wrist_Joint"))
    cmds.textField(textField4, edit=True, text=cmds.getAttr(selection_01 + ".FK_Shoulder_Ctrl"))
    cmds.textField(textField5, edit=True, text=cmds.getAttr(selection_01 + ".FK_Elbow_Ctrl"))
    cmds.textField(textField6, edit=True, text=cmds.getAttr(selection_01 + ".FK_Wrist_Ctrl"))
    cmds.textField(textField7, edit=True, text=cmds.getAttr(selection_01 + ".PoleVector_Ctrl"))
    cmds.textField(textField8, edit=True, text=cmds.getAttr(selection_01 + ".IK_Wrist_Ctrl"))
    cmds.textField(textField9, edit=True, text=cmds.getAttr(selection_01 + ".FKIK_Switch"))
    cmds.textField(textField9_Atr, edit=True, text=cmds.getAttr(selection_01 + ".FKIK_SwitchAttr"))
    cmds.textField(textField9b, edit=True, text=cmds.getAttr(selection_01 + ".FK_Value"))
    cmds.textField(textField9c, edit=True, text=cmds.getAttr(selection_01 + ".IK_Value"))

    if selection_01:
        selected_limb = selection_01

        # Update text fields wcith data
        if selected_limb in limb_data_dict:
            for idx, tf in enumerate([textField1, textField2, textField3, textField4, textField5, textField6, textField7, textField8, textField9, textField9_Atr, textField9b, textField9c]):
                cmds.textField(tf, edit=True, text=limb_data_dict[selected_limb][idx])

        # Update ActivatedLimb with the selected limb name
        cmds.textScrollList(ActivatedLimb, edit=True, removeAll=True)  # Clear the current items
        cmds.textScrollList(ActivatedLimb, edit=True, append=selected_limb)

def Activate_RemoveLimbButton(*args):
    # Get selected items from my_list and ActivatedLimb
    selected_items_from_my_list = cmds.textScrollList(my_list, query=True, selectItem=True)
    selected_items_from_ActivatedLimb = cmds.textScrollList(ActivatedLimb, query=True, selectItem=True)
    
    items_to_remove = set()  # Using a set to avoid duplicate items
    if selected_items_from_my_list:
        items_to_remove.update(selected_items_from_my_list)
    if selected_items_from_ActivatedLimb:
        items_to_remove.update(selected_items_from_ActivatedLimb)

    for item in items_to_remove:
        # Remove the item from my_list and ActivatedLimb
        cmds.textScrollList(my_list, edit=True, removeItem=item)
        cmds.textScrollList(ActivatedLimb, edit=True, removeItem=item)
        
        # Check if an object with that name exists in Maya and delete it and its children
        if cmds.objExists(item):
            cmds.delete(item)  #

    remaining_items = cmds.textScrollList(my_list, query=True, allItems=True)
    if not remaining_items and cmds.objExists("FK_IK_Limb_grp"): 
        cmds.delete("FK_IK_Limb_grp")

def onToikButton(*args):
    if cmds.textScrollList(ActivatedLimb, query=True, allItems=True):
        selected_object = cmds.textField(textField9, query=True, text=True)
        target_attr = cmds.textField(textField9_Atr, query=True, text=True)
        
        FK_value = float(cmds.textField(textField9b, query=True, text=True))
        IK_value = float(cmds.textField(textField9c, query=True, text=True))

        BakeAnim = cmds.checkBox(BakeAnim_checkbox, query=True, value=True)
        cmds.select(clear=True)
        
        if not cmds.objExists(selected_object):
            cmds.warning("Object '{}' does not exist.".format(selected_object))
            return

        if not cmds.attributeQuery(target_attr, node=selected_object, exists=True):
            cmds.warning("Attribute '{}' does not exist on '{}'.".format(target_attr, selected_object))
            return

        cmds.setAttr("{}.{}".format(selected_object, target_attr), IK_value)

        text_in_textField1 = cmds.textField(textField1, query=True, text=True)
        text_in_textField2 = cmds.textField(textField2, query=True, text=True)
        text_in_textField3 = cmds.textField(textField3, query=True, text=True)
        text_in_textField4 = cmds.textField(textField4, query=True, text=True)
        text_in_textField5 = cmds.textField(textField5, query=True, text=True)
        text_in_textField6 = cmds.textField(textField6, query=True, text=True)

        upperLOC = text_in_textField1 + "_LOC"
        lowerLOC = text_in_textField2 + "_LOC"
        endLOC = text_in_textField3 + "_LOC"

        upperJnt = text_in_textField1 + "_grp"
        lowerJnt = text_in_textField2 + "_grp"
        endJnt = text_in_textField3 + "_grp"

        #shoulder
        constraint = cmds.orientConstraint(text_in_textField1, upperJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(upperJnt, upperLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(upperLOC, text_in_textField4, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField4)
        cmds.delete(constraint)

        #elbow
        constraint = cmds.parentConstraint(text_in_textField2, lowerJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.parentConstraint(lowerJnt, lowerLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(lowerLOC, text_in_textField5, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField5)
        cmds.delete(constraint)

        #wrist
        constraint = cmds.parentConstraint(text_in_textField3, endJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.parentConstraint(endJnt, endLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(endLOC, text_in_textField6, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField6)
        cmds.delete(constraint)

        cmds.setAttr("{}.{}".format(selected_object, target_attr), FK_value)


    else:
        cmds.warning("Add Activated Limb.")

def onTofkButton(*args):
    if cmds.textScrollList(ActivatedLimb, query=True, allItems=True):
        selected_object = cmds.textField(textField9, query=True, text=True)
        target_attr = cmds.textField(textField9_Atr, query=True, text=True)

        FK_value = float(cmds.textField(textField9b, query=True, text=True))
        IK_value = float(cmds.textField(textField9c, query=True, text=True))
        BakeAnim = cmds.checkBox(BakeAnim_checkbox, query=True, value=True)

        text_in_textField1 = cmds.textField(textField1, query=True, text=True)
        text_in_textField2 = cmds.textField(textField2, query=True, text=True)
        text_in_textField3 = cmds.textField(textField3, query=True, text=True)
        text_in_textField4 = cmds.textField(textField4, query=True, text=True)
        text_in_textField5 = cmds.textField(textField5, query=True, text=True)
        text_in_textField6 = cmds.textField(textField6, query=True, text=True)
        text_in_textField7 = cmds.textField(textField7, query=True, text=True)
        text_in_textField8 = cmds.textField(textField8, query=True, text=True)
        IK_Wrist_grp = text_in_textField8 + "_grp"
        
        if not cmds.objExists(selected_object):
            cmds.warning("Object '{}' does not exist.".format(selected_object))
            return

        if not cmds.attributeQuery(target_attr, node=selected_object, exists=True):
            cmds.warning("Attribute '{}' does not exist on '{}'.".format(target_attr, selected_object))
            return
        cmds.setAttr("{}.{}".format(selected_object, target_attr), FK_value)

        cmds.xform(text_in_textField7 + "_LOC", translation=[0, 0, 0], worldSpace=True)

        cmds.delete(cmds.parentConstraint(text_in_textField1, text_in_textField1 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField2, text_in_textField2 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField6, text_in_textField3 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField2, text_in_textField5 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField6, text_in_textField6 + "_grp", w=1))
        
        cmds.parent(text_in_textField7 + "_LOC", world=True) #Polevector LOC unparent

        # Get distance between Elbow and PoleVector:
        Shoulder_Ctrl = cmds.pointPosition(text_in_textField4 + "_LOC")
        PoleVector_Ctrl = cmds.pointPosition(text_in_textField7 + "_LOC")
        Dis_Elbow_PoleVector_result = ((Shoulder_Ctrl[0]-PoleVector_Ctrl[0])**2 + (Shoulder_Ctrl[1]-PoleVector_Ctrl[1])**2 + (Shoulder_Ctrl[2]-PoleVector_Ctrl[2])**2)**0.5
        
        # Get distance between Shoulder and Elbow:
        Shoulder_grp = cmds.pointPosition(text_in_textField1 + "_grp")
        Elbow_grp = cmds.pointPosition(text_in_textField2 + "_grp")
        Dis_Shoulder_Elbow_result = ((Shoulder_grp[0]-Elbow_grp[0])**2 + (Shoulder_grp[1]-Elbow_grp[1])**2 + (Shoulder_grp[2]-Elbow_grp[2])**2)**0.5
        
        # Get distance between Wrist and Elbow:
        Wrist_grp = cmds.pointPosition(text_in_textField3 + "_grp")
        Elbow_grp = cmds.pointPosition(text_in_textField2 + "_grp")
        Dis_Wrist_Elbow_result = ((Wrist_grp[0]-Elbow_grp[0])**2 + (Wrist_grp[1]-Elbow_grp[1])**2 + (Wrist_grp[2]-Elbow_grp[2])**2)**0.5
        
        Pole_Avarage = cmds.pointConstraint(text_in_textField1 + "_grp", text_in_textField7 + "_LOC", w=Dis_Wrist_Elbow_result)
        cmds.pointConstraint(text_in_textField3 + "_grp", text_in_textField7 + "_LOC", w=Dis_Shoulder_Elbow_result)
        cmds.delete(Pole_Avarage)
        cmds.delete(cmds.aimConstraint(text_in_textField1 + "_grp", text_in_textField2 + "_grp", text_in_textField7 + "_LOC", offset=[0,0,0], w=1, aimVector=[0,0,-1], upVector=[0,1,0], worldUpType="object", worldUpObject = text_in_textField1 + "_grp"))
        
        # Get distance between Elbow and PoleVector_Loc:
        Elbow_Ctrl_grp = cmds.pointPosition(text_in_textField5 + "_grp")
        PoleVector_Ctrl = cmds.pointPosition(text_in_textField7 + "_LOC")
        Dis_Elbow_PoleVectorLoc_result = ((Elbow_Ctrl_grp[0]-PoleVector_Ctrl[0])**2 + (Elbow_Ctrl_grp[1]-PoleVector_Ctrl[1])**2 + (Elbow_Ctrl_grp[2]-PoleVector_Ctrl[2])**2)**0.5

        Elbow_Distance = Dis_Elbow_PoleVectorLoc_result + Dis_Elbow_PoleVector_result
        cmds.move(0, 0, -Elbow_Distance, text_in_textField7 + "_LOC", r=True, os=True, wd=True)

        pointC = cmds.pointConstraint(text_in_textField7 + "_LOC", text_in_textField7, offset=(0,0,0), weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField7)
        cmds.delete(pointC)

        cmds.delete(cmds.parentConstraint(text_in_textField6, IK_Wrist_grp,  weight=1))
        parentC = cmds.parentConstraint(text_in_textField8 + "_LOC", text_in_textField8, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField8)
            
        cmds.delete(parentC)

        cmds.setAttr("{}.{}".format(selected_object, target_attr), IK_value)

        cmds.parent(text_in_textField7 + "_LOC", text_in_textField2 + "_LOC") ##Polevector LOC parent

        cmds.select(clear=True)


        
    else:
        cmds.warning("Add Activated Limb.")

def onToikButtonAll(*args):
    text_in_textField1 = cmds.textField(textField1, query=True, text=True)
    text_in_textField2 = cmds.textField(textField2, query=True, text=True)
    text_in_textField3 = cmds.textField(textField3, query=True, text=True)
    text_in_textField4 = cmds.textField(textField4, query=True, text=True)
    text_in_textField5 = cmds.textField(textField5, query=True, text=True)
    text_in_textField6 = cmds.textField(textField6, query=True, text=True)


    startFrame = int(cmds.playbackOptions(q=True, min=True))
    endFrame = int(cmds.playbackOptions(q=True, max=True))
    BakeAnim = cmds.checkBox(BakeAnim_checkbox, query=True, value=True)

    selected_object = cmds.textField(textField9, query=True, text=True)
    target_attr = cmds.textField(textField9_Atr, query=True, text=True)
    
    FK_value = float(cmds.textField(textField9b, query=True, text=True))
    IK_value = float(cmds.textField(textField9c, query=True, text=True))

    upperLOC = text_in_textField1 + "_LOC"
    lowerLOC = text_in_textField2 + "_LOC"
    endLOC = text_in_textField3 + "_LOC"

    upperJnt = text_in_textField1 + "_grp"
    lowerJnt = text_in_textField2 + "_grp"
    endJnt = text_in_textField3 + "_grp"
    cmds.select(clear=True)

    if cmds.textScrollList(ActivatedLimb, query=True, allItems=True):
        
        if not cmds.objExists(selected_object):
            cmds.warning("Object '{}' does not exist.".format(selected_object))
            return

        if not cmds.attributeQuery(target_attr, node=selected_object, exists=True):
            cmds.warning("Attribute '{}' does not exist on '{}'.".format(target_attr, selected_object))
            return

        cmds.setAttr("{}.{}".format(selected_object, target_attr), IK_value)

    else:
        cmds.warning("Add Activated Limb.")

    for i in range(startFrame, endFrame + 1):
        cmds.currentTime(i)

        #shoulder
        constraint = cmds.orientConstraint(text_in_textField1, upperJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(upperJnt, upperLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(upperLOC, text_in_textField4, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField4)
        cmds.delete(constraint)

        #elbow
        constraint = cmds.parentConstraint(text_in_textField2, lowerJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.parentConstraint(lowerJnt, lowerLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(lowerLOC, text_in_textField5, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField5)
        cmds.delete(constraint)

        #wrist
        constraint = cmds.parentConstraint(text_in_textField3, endJnt, weight=1)
        cmds.delete(constraint)
        constraint = cmds.parentConstraint(endJnt, endLOC, weight=1)
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(endLOC, text_in_textField6, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField6)
        cmds.delete(constraint)

    cmds.setAttr("{}.{}".format(selected_object, target_attr), FK_value)

def onTofkButtonAll(*args):
    selected_object = cmds.textField(textField9, query=True, text=True)
    target_attr = cmds.textField(textField9_Atr, query=True, text=True)

    FK_value = float(cmds.textField(textField9b, query=True, text=True))
    IK_value = float(cmds.textField(textField9c, query=True, text=True))

    startFrame = int(cmds.playbackOptions(q=True, min=True))
    endFrame = int(cmds.playbackOptions(q=True, max=True))
    BakeAnim = cmds.checkBox(BakeAnim_checkbox, query=True, value=True)

    text_in_textField1 = cmds.textField(textField1, query=True, text=True)
    text_in_textField2 = cmds.textField(textField2, query=True, text=True)
    text_in_textField3 = cmds.textField(textField3, query=True, text=True)
    text_in_textField4 = cmds.textField(textField4, query=True, text=True)
    text_in_textField5 = cmds.textField(textField5, query=True, text=True)
    text_in_textField6 = cmds.textField(textField6, query=True, text=True)
    text_in_textField7 = cmds.textField(textField7, query=True, text=True)
    text_in_textField8 = cmds.textField(textField8, query=True, text=True)
    IK_Wrist_grp = text_in_textField8 + "_grp"

    if cmds.textScrollList(ActivatedLimb, query=True, allItems=True):
        
        if not cmds.objExists(selected_object):
            cmds.warning("Object '{}' does not exist.".format(selected_object))
            return

        if not cmds.attributeQuery(target_attr, node=selected_object, exists=True):
            cmds.warning("Attribute '{}' does not exist on '{}'.".format(target_attr, selected_object))
            return

        cmds.setAttr("{}.{}".format(selected_object, target_attr), FK_value)

    else:
        cmds.warning("Add Activated Limb.")

    cmds.xform(text_in_textField7 + "_LOC", translation=[0, 0, 0], worldSpace=True)

    for i in range(startFrame, endFrame + 1):
        cmds.currentTime(i)

        cmds.delete(cmds.parentConstraint(text_in_textField1, text_in_textField1 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField2, text_in_textField2 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField6, text_in_textField3 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField2, text_in_textField5 + "_grp", w=1)) 
        cmds.delete(cmds.parentConstraint(text_in_textField6, text_in_textField6 + "_grp", w=1))
        
        cmds.parent(text_in_textField7 + "_LOC", world=True)

        # Get distance between Elbow and PoleVector:
        Shoulder_Ctrl = cmds.pointPosition(text_in_textField4 + "_LOC")
        PoleVector_Ctrl = cmds.pointPosition(text_in_textField7 + "_LOC")
        Dis_Elbow_PoleVector_result = ((Shoulder_Ctrl[0]-PoleVector_Ctrl[0])**2 + (Shoulder_Ctrl[1]-PoleVector_Ctrl[1])**2 + (Shoulder_Ctrl[2]-PoleVector_Ctrl[2])**2)**0.5
        
        # Get distance between Shoulder and Elbow:
        Shoulder_grp = cmds.pointPosition(text_in_textField1 + "_grp")
        Elbow_grp = cmds.pointPosition(text_in_textField2 + "_grp")
        Dis_Shoulder_Elbow_result = ((Shoulder_grp[0]-Elbow_grp[0])**2 + (Shoulder_grp[1]-Elbow_grp[1])**2 + (Shoulder_grp[2]-Elbow_grp[2])**2)**0.5
        
        # Get distance between Wrist and Elbow:
        Wrist_grp = cmds.pointPosition(text_in_textField3 + "_grp")
        Elbow_grp = cmds.pointPosition(text_in_textField2 + "_grp")
        Dis_Wrist_Elbow_result = ((Wrist_grp[0]-Elbow_grp[0])**2 + (Wrist_grp[1]-Elbow_grp[1])**2 + (Wrist_grp[2]-Elbow_grp[2])**2)**0.5
        
        Pole_Avarage = cmds.pointConstraint(text_in_textField1 + "_grp", text_in_textField7 + "_LOC", w=Dis_Wrist_Elbow_result)
        cmds.pointConstraint(text_in_textField3 + "_grp", text_in_textField7 + "_LOC", w=Dis_Shoulder_Elbow_result)
        cmds.delete(Pole_Avarage)
        cmds.delete(cmds.aimConstraint(text_in_textField1 + "_grp", text_in_textField2 + "_grp", text_in_textField7 + "_LOC", offset=[0,0,0], w=1, aimVector=[0,0,-1], upVector=[0,1,0], worldUpType="object", worldUpObject = text_in_textField1 + "_grp"))
        
        # Get distance between Elbow and PoleVector_Loc:
        Elbow_Ctrl_grp = cmds.pointPosition(text_in_textField5 + "_grp")
        PoleVector_Ctrl = cmds.pointPosition(text_in_textField7 + "_LOC")
        Dis_Elbow_PoleVectorLoc_result = ((Elbow_Ctrl_grp[0]-PoleVector_Ctrl[0])**2 + (Elbow_Ctrl_grp[1]-PoleVector_Ctrl[1])**2 + (Elbow_Ctrl_grp[2]-PoleVector_Ctrl[2])**2)**0.5

        Elbow_Distance = Dis_Elbow_PoleVectorLoc_result + Dis_Elbow_PoleVector_result
        cmds.move(0, 0, -Elbow_Distance, text_in_textField7 + "_LOC", r=True, os=True, wd=True)

        pointC = cmds.pointConstraint(text_in_textField7 + "_LOC", text_in_textField7, offset=(0,0,0), weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField7, breakdown=0, hierarchy='none', controlPoints=0, shape=0)
        cmds.delete(pointC)

        cmds.delete(cmds.parentConstraint(text_in_textField6, IK_Wrist_grp,  weight=1))
        parentC = cmds.parentConstraint(text_in_textField8 + "_LOC", text_in_textField8, weight=1)
        if BakeAnim:
            cmds.setKeyframe(text_in_textField8, breakdown=0, hierarchy='none', controlPoints=0, shape=0)
        cmds.delete(parentC)

        cmds.parent(text_in_textField7 + "_LOC", text_in_textField2 + "_LOC")
        
        cmds.select(clear=True)
        
    cmds.setAttr("{}.{}".format(selected_object, target_attr), IK_value)


if cmds.window("FKIKToolUI", exists=True):
    cmds.deleteUI("FKIKToolUI", window=True)

cmds.window("FKIKToolUI", title="FK IK Match v1.0", widthHeight=(500, 800))
cmds.columnLayout(adjustableColumn=True, columnOffset=("both", 5))

cmds.separator(height=10)
cmds.text(label='=================================================================', height=10)
cmds.separator(height=5, style='none')
cmds.text(label='FK IK Match', height=30)
cmds.text(label='=================================================================', height=10)
cmds.separator(height=10)

frame = cmds.frameLayout(label='Import & Export Data', collapsable=True) # Import & Export Data Category
cmds.separator(height=1)
rowLayout1 = cmds.rowLayout(numberOfColumns=2, columnWidth=[(1,250),(2,250)])
importButton = cmds.button(label="Import Data" , width=250 , command=Import_data)
exportButton = cmds.button(label="Export Data" , width=250, command=Export_data)
cmds.setParent('..') 
cmds.setParent('..') # Import & Export Data End Point
cmds.separator(height=7) 

frame = cmds.frameLayout(label='Limb Data', collapsable=True) # Limb Data Category
cmds.separator(height=3)

rowLayout1 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label1 = cmds.text(label=" Upper Joint")
textField1 = cmds.textField(width=280)
button1 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField1))
cmds.setParent('..') 

rowLayout2 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label2 = cmds.text(label=" Lower Joint")
textField2 = cmds.textField(width=280)
button2 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField2))
cmds.setParent('..') 

rowLayout3 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label3 = cmds.text(label=" Wrist / Foot Joint")
textField3 = cmds.textField(width=280)
button3 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField3))
cmds.setParent('..')

rowLayout4 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label4 = cmds.text(label=" FK Upper Ctrl")
textField4 = cmds.textField(width=280)
button4 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField4))
cmds.setParent('..')

rowLayout5 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label5 = cmds.text(label=" FK Lower Ctrl")
textField5 = cmds.textField(width=280)
button5 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField5))
cmds.setParent('..')

rowLayout6 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label6 = cmds.text(label=" FK Wrist / Foot Ctrl")
textField6 = cmds.textField(width=280)
button6 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField6))
cmds.setParent('..')

rowLayout7 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label7 = cmds.text(label=" Pole Vector Ctrl")
textField7 = cmds.textField(width=280)
button7 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField7))
cmds.setParent('..')

rowLayout8 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 100))
label8 = cmds.text(label=" IK Wrist / Foot Ctrl")
textField8 = cmds.textField(width=280)
button8 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField8))
cmds.setParent('..')

rowLayout9 = cmds.rowLayout(numberOfColumns=8) 
cmds.rowLayout(rowLayout9, edit=True, columnWidth=[(1,100),(2,10), (3,50), (4,30), (5,20), (6,33), (7,30), (8,10)])
label9 = cmds.text(label=" Switch Ctrl / Attr")
textField9 = cmds.textField(width=70)
textField9_Atr = cmds.textField(width=70)
label9b = cmds.text(label=" FK")
textField9b = cmds.textField(text='0', width=30)
label9c = cmds.text(label=" IK")
textField9c = cmds.textField(text='10', width=30)
button9 = cmds.button(label="Add", width=100, command=partial(Activate_AddButton, textField9))
cmds.setParent('..')

cmds.separator(height=7)

rowLayout10 = cmds.rowLayout(numberOfColumns=5,columnWidth5=(100,80,74,80,100))
label10 = cmds.text(label=" Search")
textField10 = cmds.textField(text="_R", width=100)
label11 = cmds.text(label="   Replace")
textField11 = cmds.textField(text="_L", width=100)
button10 = cmds.button(label="Search and Replace", width=100, command=Activate_SearchAndReplace)
cmds.setParent('..')

cmds.setParent('..') #Limb Data Category End point

cmds.separator(height=10)

Low_AvailableList = cmds.rowLayout(numberOfColumns=3, columnWidth3=(205,175,100))
cmds.text(label="", height=30)
cmds.text(label="Limbs avaiable", height=30)
RefreshButton = cmds.button(label="Refresh", width=100, command = Activate_RefreshButton)
cmds.setParent('..')

my_list = cmds.textScrollList('my_List', allowMultiSelection=True, height=120)

#==============
cmds.separator(height=7)
rowLayout12 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100,280,100))
label11z = cmds.text(label="Activated Limb")
ActivatedLimb = cmds.textScrollList(width=270, height=30)
RemoveLimbButton = cmds.button(label="Remove Limb", width=100,command=Activate_RemoveLimbButton)
cmds.setParent('..')

cmds.separator(height=7)
rowLayout13 = cmds.rowLayout(numberOfColumns=3, height=30)
toikButton = cmds.button(label="FK > IK", width=140, command=onToikButton)
ActiveButton = cmds.button(label="Activate", width=200, command=Activate_ActiveButton)
tofkButton = cmds.button(label="IK > FK", width=150, command =onTofkButton)
cmds.setParent('..')

cmds.setParent('..')

rowLayout14 = cmds.rowLayout(numberOfColumns=2, height=30)
toikButtonAll = cmds.button(label="FK > IK (All)", width=243, command =onToikButtonAll)
tofkButtonAll = cmds.button(label="IK > FK (All)", width=243, command =onTofkButtonAll)
cmds.setParent('..')

rowLayout15 = cmds.rowLayout(numberOfColumns=1)
BakeAnim_checkbox = cmds.checkBox(label='Bake Animation')
cmds.setParent('..')

# List Double Click Event
cmds.textScrollList(my_list, edit=True, doubleClickCommand=List_DoubleClick)

cmds.showWindow("FKIKToolUI")

