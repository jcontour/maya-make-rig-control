import maya.cmds as c
from functools import partial

# closes any open windows
if c.window('makeCtrl', exists=True):
	c.deleteUI('makeCtrl')

if c.window('rotCtrl', exists=True):
	c.deleteUI('rotCtrl')

# creating a new window
window = c.window('makeCtrl', title="Control Generator", iconName='Make Ctrl', widthHeight=(100, 275) )
c.columnLayout( adjustableColumn=True )
c.text(label="Select the joint that you want to make a control for", align='left', wordWrap=True)
c.button( label='Make control!', c='create_cc()')
c.showWindow( window )

# show alert dialogue with custom text
def showAlertWindow(text):
	cmds.confirmDialog( title='Error', message=text, button=['ok'], defaultButton='ok')


def create_cc():
	# gets most recently selected object
	selected = c.ls( selection=True, tail=1,)
	
	# if nothing is selected, show alert
	if not selected:
		alerttext = "Make sure your joint is selected"
		showAlertWindow(alerttext)

	joint = selected[0]
	cc_name = joint+'_ctrl'

	# if selected object is not a joint show alert
	if c.objectType( joint, isType='joint' ) == False:
		alerttext1 = "Make sure a joint is selected"
		showAlertWindow(alerttext1)
	# if everything checks out, make a control and place it into a positioning group
	else:
		cc = cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n=cc_name)
		c.group( cc_name, n='p_'+joint )

		# using a parent constraint, position the group at the joint
		# then delete the constraint
		c.parentConstraint( joint, 'p_'+joint, mo=False, n='const')
		c.delete('const')
		# close the window and open the rotation window
		c.deleteUI('makeCtrl')
		rotateCC(cc_name)

def rotateCC(ctrl):
	window = c.window('rotCtrl', title="Control Rotator", widthHeight=(200, 200) )
	c.columnLayout( adjustableColumn=True )
	c.text(label="Use these to rotate the control to the orientation you prefer", align='left', wordWrap=True)
	# three buttons that pass different arguments into a rotation function
	c.button( label='Rotate X', command=partial(rotate, ctrl, '90deg', 0, 0 ))
	c.button( label='Rotate Y', command=partial(rotate, ctrl, 0, '90deg', 0 ))
	c.button( label='Rotate Z', command=partial(rotate, ctrl, 0, 0, '90deg' ))
	c.showWindow( window )

def rotate(name,x,y,z, *args):
	c.select( name )
	# rotate the control, freeze the transformations, and delete the history
	c.rotate( x, y, z, r=True )
	c.makeIdentity( apply=True )
	c.delete(ch=True)
