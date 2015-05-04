import logging
from gi.repository import Gtk

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

class LoginWindow(Gtk.Window):

    #Selected saved account
    __account_number=0
    #Saved account ID
    __account_qqnumber=[]
    #Saved account encrypted password
    __account_encrypted_password=[]
    #Inputed new account ID
    __new_account_qqnumber=""
    #Inputed new account password
    __new_account_password=""
    #Login account ID
    __login_qqnumber=""
    #Login password
    __login_password=""
    #Ifsave button
    __ifsave=0
    #Selection of saved account
    __selection_number=1

    def __init__(self):

        logging.info("Initializing login interface.")

        #Getting saved account info
        self.get_saved_account_info(self)

        Gtk.Window.__init__(self, title="Login")
        self.set_border_width(20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        #Login button
        loginbutton_saved=Gtk.Button(label="Login")
        loginbutton_saved.connect("clicked",self.on_login_saved_clicked,self)
        loginbutton_new=Gtk.Button(label="Login")

        #Stack for content
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        #Saved account login
        saved_account_box= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        #Display saved account
        button=[]
        counter=1
        for i in self.__account_qqnumber:
            if counter==1:
                buttontemp=Gtk.RadioButton.new_with_label_from_widget(None, i)
                button.append(buttontemp)
                button[counter-1].connect("toggled",self.saved_account_toggled,counter,self)
                saved_account_box.pack_start(button[counter-1],True,True,0)
            else:
                buttontemp=Gtk.RadioButton.new_with_label_from_widget(button[0], i)
                button.append(buttontemp)
                button[counter-1].connect("toggled",self.saved_account_toggled,counter,self)
                saved_account_box.pack_start(button[counter-1],True,True,0)
            counter+=1
        #For login button
        saved_account_grid=Gtk.Grid()
        saved_account_grid.attach(loginbutton_saved,1,0,1,1)
        saved_account_box.pack_start(saved_account_grid,True,True,0)
        stack.add_titled(saved_account_box, "Saved Account", "Saved Account")

        #New account login
        qqnumber=Gtk.Entry()
        qqnumber.set_text("QQ Number")

        password=Gtk.Entry()
        password.set_text("Password")

        ifsave=Gtk.CheckButton("Save")
        ifsave.connect("clicked", self.ifsave_clicked,self)
        new_account_box_sub=Gtk.Box(spacing=6)
        new_account_box_sub.pack_start(ifsave,True,True,0)
        new_account_box_sub.pack_start(loginbutton_new,True,True,0)
        new_account_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        new_account_box.pack_start(qqnumber,True,True,0)
        new_account_box.pack_start(password,True,True,0)
        new_account_box.pack_start(new_account_box_sub,True,True,0)
        stack.add_titled(new_account_box, "New Account" , "New Account")

        #Switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

        #New account login connect, for entry definition should be placed here
        loginbutton_new.connect("clicked",self.on_login_new_clicked,self,qqnumber,password)

        #For test
        #self.saved_account_test(self)
        #self.write_account_info(self,"1","2")

    #Login button click
    #Login button for saved account
    def on_login_saved_clicked(self,button,father):
        selection=father.__selection_number
        #For test
        #print(selection,father.__account_qqnumber[selection-1],father.__account_encrypted_password[selection-1])
        father.login(father.__account_qqnumber[selection-1],father.__account_encrypted_password[selection-1])

    #Login button for new account
    def on_login_new_clicked(self,button,father,qqnumber,password):
        qid=qqnumber.get_text()
        pw=password.get_text()
        if father.__ifsave==1:
            father.write_account_info(father,qid,pw)
        father.login(qid,pw)

    #Save or not button
    def ifsave_clicked(self,button,father):
        if button.get_active():
            father.__ifsave=1
        else:
            father.__ifsave=0

    #Dealing with ratiobutton conflict
    #need modification
    def saved_account_toggled(self,button,name,father):
        if button.get_active():
            father.__selection_number=name

    #Getting saved account information form file
    def get_saved_account_info(self,father):
        logging.info("Getting saved account info.")
        f=open('accountinfo','r')
        count=1
        for line in f:
            if count % 2:
                #rstrip is to remove \n from the file
                father.__account_qqnumber.append(line.rstrip('\n'))
                count+=1
            else:
                father.__account_encrypted_password.append(line.rstrip('\n'))
                count+=1
        father.__account_number=len(father.__account_qqnumber)
        f.close()

    #Testing the saved account reading module
    def saved_account_test(self,father):
        print("account saved qqnumber")
        for a in father.__account_qqnumber:
            print a
        print("account saved password")
        for a in father.__account_encrypted_password:
            print a

    #Write new account information to file
    def write_account_info(self,father,number,password):
        logging.info("Saving new account information.")
        f=open('accountinfo','w')
        temp_account_number=len(father.__account_qqnumber)
        for i in range(0,temp_account_number):
            f.write(father.__account_qqnumber[i]+"\n"+father.__account_encrypted_password[i]+"\n")
        f.write(number+"\n")
        f.write(password+"\n")
        f.close()

    def login(self,qqnumber,password):
        return 0

win = LoginWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
