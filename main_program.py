'''
Control: 
    robot.move_forward()
    robot.rotate_right()
    robot.rotate_left()

Sensors:    
    robot.ultrasonicFront() -> int
    robot.ultrasonicRight() -> int
    robot.ultrasonicLeft() -> int
    robot.detectFireFront() -> bool
    robot.scanEnvironment() -> string ("fire", "people", "collapse", "clear", "safe")

Actions: 
    robot.putOutFireFront()
    robot.sendMessageExplorationBase(Coord)
    robot.sendMessageRescueBase(Coord, path)
    robot.finishExploration()
'''

def main():
    ############################################
    #Test 3: Robot apaga fuego, envía correctamente
    # mensaje de derrumbe, salva personas y regresa
    # a la base.
    ############################################



    class Tile:
        def __init__(self):
            self.paredes = [False,False,False,False]
            self.estado = "clear"
            self.visitado = False
    


    mapa = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    x = 1
    y = 1
    direccion = 'e'
    safe = []
    stack = []

    for n in range (10):
            for m in range (10):
                mapa[n][m] = Tile()
                if(n == 0 or n == 9 or m == 0 or m == 9):
                    mapa[n][m].paredes = [True,True,True,True]
                    mapa[n][m].visitado = True
    
    while(True):
        #checarpared(direccion,x,y,mapa)
        #movimiento(direccion,x,y,mapa)
        

        ## Checar paredes ##
        if direccion == 'n':
            if(robot.ultrasonicFront() == 0):
                mapa[y][x].paredes[0] = True
                if(y != 0):
                    mapa[y-1][x].paredes[1] = True
            if(robot.ultrasonicRight() == 0):
                mapa[y][x].paredes[2] = True
                if(x != 7):
                    mapa[y][x+1].paredes[3] = True
            if(robot.ultrasonicLeft() == 0):
                mapa[y][x].paredes[3] = True
                if(x != 0):
                    mapa[y][x-1].paredes[2] = True
        elif direccion == 's':
            if(robot.ultrasonicFront() == 0):
                mapa[y][x].paredes[1] = True
                if(y != 7):
                    mapa[y+1][x].paredes[0] = True
            if(robot.ultrasonicRight() == 0):
                mapa[y][x].paredes[3] = True
                if(x != 0):
                    mapa[y][x-1].paredes[2] = True
            if(robot.ultrasonicLeft() == 0):
                mapa[y][x].paredes[2] = True
                if(x != 7):
                    mapa[y][x+1].paredes[3] = True
        elif direccion == 'e':
            if(robot.ultrasonicFront() == 0):
                mapa[y][x].paredes[2] = True
                if(x != 7):
                    mapa[y][x+1].paredes[3] = True
            if(robot.ultrasonicRight() == 0):
                mapa[y][x].paredes[1] = True
                if(y != 7):
                    mapa[y+1][x].paredes[0] = True
            if(robot.ultrasonicLeft() == 0):
                mapa[y][x].paredes[0] = True
                if(y != 0):
                    mapa[y-1][x].paredes[1] = True
        elif direccion == 'o':
            if(robot.ultrasonicFront() == 0):
                mapa[y][x].paredes[3] = True
                if(x != 0):
                    mapa[y][x-1].paredes[2] = True
            if(robot.ultrasonicRight() == 0):
                mapa[y][x].paredes[0] = True
                if(y != 0):
                    mapa[y-1][x].paredes[1] = True
            if(robot.ultrasonicLeft() == 0):
                mapa[y][x].paredes[1] = True
                if(y != 7):
                    mapa[y+1][x].paredes[0] = True
        
        ## Guardar posicion ##
        mapa[y][x].visitado = True
        #print(str(y) + str(x) + str(mapa[y][x].visitado))
        
        ####### Checar environment ####
        environment = robot.scanEnvironment()
        if(environment == "collapse"):
            robot.sendMessageExplorationBase(Coord(x-1,y-1))
            robot.rotate_right()
            robot.rotate_right()
            robot.move_forward()
            robot.rotate_right()
            robot.rotate_right()
            stack.pop()
            if(direccion == 'e'):
                x = x-1
            elif(direccion == 'o'):
                x = x+1
            elif(direccion == 'n'):
                y = y+1
            elif(direccion == 's'):
                y = y-1
        elif(environment == "people"):
            robot.sendMessageRescueBase(Coord(x-1,y-1))
        elif(environment == "safe"):
            safe.append([y-1,x-1])

        


        ## movimiento ##
        if direccion == 'e':
            
            if(mapa[y][x].paredes[1] == False and mapa[y+1][x].visitado == False):
                robot.rotate_right()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y+1
                direccion = 's'
                stack.append(direccion)
            elif(mapa[y][x].paredes[2] == False and mapa[y][x+1].visitado == False ):
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x+1
                stack.append(direccion)
            elif(mapa[y][x].paredes[0] == False and mapa[y-1][x].visitado == False):
                robot.rotate_left()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y-1
                direccion = 'n'
                stack.append(direccion)
            else:
                robot.rotate_right()
                robot.rotate_right()
                direccion = 'o'
                while (mapa[y+1][x].visitado != False or mapa[y][x].paredes[1] == True) and (mapa[y-1][x].visitado != False or mapa[y][x].paredes[0] == True) and (mapa[y][x+1].visitado != False or mapa[y][x].paredes[2] == True) and (mapa[y][x-1].visitado != False or mapa[y][x].paredes[3] == True) and len(stack) != 0:
                    print("m")
                    print(stack)
                    if(direccion == 'o'):
                        print("mo")
                        if(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            x = x+1
                            stack.pop()
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                    elif(direccion == 'e'):
                        print("me")
                        if(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                    elif(direccion == 's'):
                        print("ms")
                        if(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    elif(direccion == 'n'):
                        print("mn")
                        if(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'

        elif direccion == 'o':
            if(mapa[y][x].paredes[0] == False and mapa[y-1][x].visitado == False):
                robot.rotate_right()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y-1
                direccion = 'n'
                stack.append(direccion)
            elif(mapa[y][x].paredes[3] == False and mapa[y][x-1].visitado == False):
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x-1
                stack.append(direccion)
            elif(mapa[y][x].paredes[1] == False and mapa[y+1][x].visitado == False):
                robot.rotate_left()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y+1
                direccion = 's'
                stack.append(direccion)
            else:
                robot.rotate_right()
                robot.rotate_right()
                direccion = 'e'
                
                while (mapa[y+1][x].visitado != False or mapa[y][x].paredes[1] == True) and (mapa[y-1][x].visitado != False or mapa[y][x].paredes[0] == True) and (mapa[y][x+1].visitado != False or mapa[y][x].paredes[2] == True) and (mapa[y][x-1].visitado != False or mapa[y][x].paredes[3] == True) and len(stack) != 0:
                    print("h")
                    print(stack)
                    if(direccion == 'o'):
                        print("ho")
                        if(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            x = x+1
                            stack.pop()
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                    elif(direccion == 'e'):
                        print("he")
                        if(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                    elif(direccion == 's'):
                        print("hs")
                        if(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    elif(direccion == 'n'):
                        print("hn")
                        if(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    
                
        elif direccion == 'n':
            if(mapa[y][x].paredes[2] == False and mapa[y][x+1].visitado == False):
                robot.rotate_right()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x+1
                direccion = 'e'
                stack.append(direccion)
            elif(mapa[y][x].paredes[0] == False and mapa[y-1][x].visitado == False):
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y-1
                stack.append(direccion)
            elif(mapa[y][x].paredes[3] == False and mapa[y][x-1].visitado == False):
                robot.rotate_left()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x-1
                direccion = 'o'
                stack.append(direccion)
            else:
                robot.rotate_right()
                robot.rotate_right()
                direccion = 's'
                
                while (mapa[y+1][x].visitado != False or mapa[y][x].paredes[1] == True) and (mapa[y-1][x].visitado != False or mapa[y][x].paredes[0] == True) and (mapa[y][x+1].visitado != False or mapa[y][x].paredes[2] == True) and (mapa[y][x-1].visitado != False or mapa[y][x].paredes[3] == True) and len(stack) != 0:
                    print("f")
                    print(stack)
                    print("direccion: " + direccion)
                    if(direccion == 'o'):
                        print("fo")
                        if(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            x = x+1
                            stack.pop()
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                    elif(direccion == 'e'):
                        print("fe")
                        if(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                    elif(direccion == 's'):
                        print("fs")
                        if(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    elif(direccion == 'n'):
                        print("fn")
                        if(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    
        elif direccion == 's':
            if(mapa[y][x].paredes[3] == False and mapa[y][x-1].visitado == False):
                robot.rotate_right()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x-1
                direccion = 'o'
                stack.append(direccion)
            elif(mapa[y][x].paredes[1] == False and mapa[y+1][x].visitado == False):
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                y = y+1
                stack.append(direccion)
            elif(mapa[y][x].paredes[2] == False and mapa[y][x+1].visitado == False):
                robot.rotate_left()
                if(robot.detectFireFront()):
                    robot.putOutFireFront()
                robot.move_forward()
                x = x+1
                direccion = 'e'
                stack.append(direccion)
            else:
                robot.rotate_right()
                robot.rotate_right()
                direccion = 'n'
                
                while(mapa[y+1][x].visitado != False or mapa[y][x].paredes[1] == True) and (mapa[y-1][x].visitado != False or mapa[y][x].paredes[0] == True) and (mapa[y][x+1].visitado != False or mapa[y][x].paredes[2] == True) and (mapa[y][x-1].visitado != False or mapa[y][x].paredes[3] == True) and len(stack) != 0:
                    print("y")
                    print(stack)
                    print( "direccion:" + direccion)
                    if(direccion == 'o'):
                        print("yo")
                        if(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            x = x+1
                            stack.pop()
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                    elif(direccion == 'e'):
                        print("ye")
                        if(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                    elif(direccion == 's'):
                        print("ys")
                        if(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
                    elif(direccion == 'n'):
                        print("yn")
                        print(stack)
                        if(stack[len(stack)-1] == 'e' and mapa[y][x].paredes[3]==False):
                            robot.rotate_left()
                            robot.move_forward()
                            stack.pop()
                            x = x-1
                            direccion = 'o'
                        elif(stack[len(stack)-1] == 'o' and mapa[y][x].paredes[2]==False):
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            x = x+1
                            direccion = 'e'
                        elif(stack[len(stack)-1] == 's' and mapa[y][x].paredes[0]==False):
                            robot.move_forward()
                            stack.pop()
                            y = y-1
                            direccion = 'n'
                        elif(stack[len(stack)-1] == 'n' and mapa[y][x].paredes[1]==False):
                            robot.rotate_right()
                            robot.rotate_right()
                            robot.move_forward()
                            stack.pop()
                            y = y+1
                            direccion = 's'
        
        if(x == 1 and y == 1 and (mapa[y+1][x].visitado == True or mapa[y+1][x].paredes[2] == True) and (mapa[y][x+1].visitado == True or mapa[y+1][x].paredes[1] == True) ):
            print("La coordenada de los lugares seguros son: " + str(safe))
            robot.finishExploration()
            break
        
        #print(safe)
        """print(y)
        if(y == 7):
            break"""
        
        
    
    

if __name__ == "__main__":
    main()