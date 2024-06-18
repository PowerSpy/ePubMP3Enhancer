class test:
    global tesvar
    tesvar = 0
    def tesva(self):
        print(tesvar)
class hi:
    global tesvar
    tesvar = 1
    proto = test()
    proto.tesva()
