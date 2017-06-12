# A very simple Drag and Drop Example
# provided with no warranty whatsoever for any purpose, ever

# A very simple Drag and Drop Example
# provided with no warranty whatsoever for any purpose, ever

# This code creates a Text Control from which Text can be dragged,
# a Text Control to which Text can be dragged (from the first Text Control or from other applications),
# and a Text Control to which Files can be dragged from outside this application.
# While the later two windows can receive data from outside the application, the first window
# does not appear to be able to provide text to other applications.  Please feel free to fix
# this if you know how, as I think that would be more useful as an example.

# It is designed to demonstrate the fundamentals of very simple drag-and-drop operations.

""" This mini-app is designed to demonstrate simple Drag and Drop functioning in wx.Python """

__author__ = 'David Woods, Wisconsin Center for Education Research <dwoods@wcer.wisc.edu>'

# Import wx.Python
import wx

# Declare GUI Constants
MENU_FILE_EXIT = wx.NewId()
DRAG_SOURCE    = wx.NewId()

# Define Text Drop Target class
class TextDropTarget(wx.TextDropTarget):
   """ This object implements Drop Target functionality for Text """
   def __init__(self, obj):
      """ Initialize the Drop Target, passing in the Object Reference to
          indicate what should receive the dropped text """
      # Initialize the wx.TextDropTarget Object
      wx.TextDropTarget.__init__(self)
      # Store the Object Reference for dropped text
      self.obj = obj

   def OnDropText(self, x, y, data):
      """ Implement Text Drop """
      # When text is dropped, write it into the object specified
      self.obj.WriteText(data + '\n\n')

# Define File Drop Target class
class FileDropTarget(wx.FileDropTarget):
   """ This object implements Drop Target functionality for Files """
   def __init__(self, obj):
      """ Initialize the Drop Target, passing in the Object Reference to
          indicate what should receive the dropped files """
      # Initialize the wxFileDropTarget Object
      wx.FileDropTarget.__init__(self)
      # Store the Object Reference for dropped files
      self.obj = obj

   def OnDropFiles(self, x, y, filenames):
      """ Implement File Drop """
      # For Demo purposes, this function appends a list of the files dropped at the end of the widget's text
      # Move Insertion Point to the end of the widget's text
      self.obj.SetInsertionPointEnd()
      # append a list of the file names dropped
      self.obj.WriteText("%d file(s) dropped at %d, %d:\n" % (len(filenames), x, y))
      for file in filenames:
         self.obj.WriteText(file + '\n')
      self.obj.WriteText('\n')



class MainWindow(wx.Frame):
   """ This window displays the GUI Widgets. """
   def __init__(self,parent,id,title):
       wx.Frame.__init__(self,parent, wx.ID_ANY, title, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
       self.SetBackgroundColour(wx.WHITE)

       # Menu Bar
       # Create a MenuBar
       menuBar = wx.MenuBar()
       # Build a Menu Object to go into the Menu Bar
       menu1 = wx.Menu()
       menu1.Append(MENU_FILE_EXIT, "E&xit", "Quit Application")
       # Place the Menu Item in the Menu Bar
       menuBar.Append(menu1, "&File")
       # Place the Menu Bar on the ap
       self.SetMenuBar(menuBar)
       #Define Events for the Menu Items
       wx.EVT_MENU(self, MENU_FILE_EXIT, self.CloseWindow)

       # GUI Widgets
       # Define a Text Control from which Text can be dragged for dropping
       # Label the control
       wx.StaticText(self, -1, "Text Drag Source  (left-click to select, right-click to drag)", (10, 1))
       # Create a Text Control
       self.text = wx.TextCtrl(self, DRAG_SOURCE, "", pos=(10,15), size=(350,500), style = wx.TE_MULTILINE|wx.HSCROLL)
       # Make this control a Text Drop Target
       # Create a Text Drop Target object
       dt1 = TextDropTarget(self.text)
       # Link the Drop Target Object to the Text Control
       self.text.SetDropTarget(dt1)
       # Put some text in the control as a starting place to have something to copy
       for x in range(20):
          self.text.WriteText("This is line %d of some text to drag.\n" % x)
       # Define Right-Click as start of Drag
       wx.EVT_RIGHT_DOWN(self.text, self.OnDragInit)

       # Define a Text Control to recieve Dropped Text
       # Label the control
       wx.StaticText(self, -1, "Text Drop Target", (370, 1))
       # Create a read-only Text Control
       self.text2 = wx.TextCtrl(self, -1, "", pos=(370,15), size=(410,235), style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
       # Make this control a Text Drop Target
       # Create a Text Drop Target object
       dt2 = TextDropTarget(self.text2)
       # Link the Drop Target Object to the Text Control
       self.text2.SetDropTarget(dt2)

       # Define a Text Control to receive Dropped Files
       # Label the control
       wx.StaticText(self, -1, "File Drop Target (from off application only)", (370, 261))
       # Create a read-only Text Control
       self.text3 = wx.TextCtrl(self, -1, "", pos=(370,275), size=(410,235), style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
       # Make this control a File Drop Target
       # Create a File Drop Target object
       dt3 = FileDropTarget(self.text3)
       # Link the Drop Target Object to the Text Control
       self.text3.SetDropTarget(dt3)

       # Display the Window
       self.Show(True)


   def CloseWindow(self, event):
       """ Close the Window """
       self.Close()

   def OnDragInit(self, event):
       """ Begin a Drag Operation """
       # Create a Text Data Object, which holds the text that is to be dragged
       tdo = wx.PyTextDataObject(self.text.GetStringSelection())
       # Create a Drop Source Object, which enables the Drag operation
       tds = wx.DropSource(self.text)
       # Associate the Data to be dragged with the Drop Source Object
       tds.SetData(tdo)
       # Initiate the Drag Operation
       tds.DoDragDrop(True)



class MyApp(wx.App):
   """ Define the Drag and Drop Example Application """
   def OnInit(self):
      """ Initialize the Application """
      # Declare the Main Application Window
      frame = MainWindow(None, -1, "Drag and Drop Example")
      # Show the Application as the top window
      self.SetTopWindow(frame)
      return True


# Declare the Application and start the Main Loop
app = MyApp(0)
app.MainLoop()