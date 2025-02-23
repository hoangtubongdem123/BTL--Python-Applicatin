from views.home_view import HomeView

class HomeController :
    def __init__(self,username):

        self.view = HomeView(username)

        self.view.mainloop()
