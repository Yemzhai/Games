import sys
import pika
import uuid
import json
import threading
import math
import pygame


# ====DAR-TANKS server's fignia====
USERNAME = VIRTUAL_HOST = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'
IP = '34.254.177.17'
PORT = 5672


#====Pygame fignia====
pygame.init()
win = pygame.display.set_mode((800, 600))
#------------ ground ---------------
grassImg = "images/bkgnd_green_3_brt.jpg"
background = pygame.image.load(grassImg)
#------------ tanks ----------------
me = "images/tank_red.png"
myTank = pygame.image.load(me)
angle = 0
someone = "images/tank_blue.png"
enemyTank = pygame.image.load(someone)
#------------- bullet --------------
bullet1 = ("images/bullet.png")
myBullet =  pygame.image.load(bullet1)
bullet2 = ("images/enemy-bullet.jpg")
enemyBullet =  pygame.image.load(bullet2)



class TnakClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                 host=IP,
                 port=PORT,
                 virtual_host=VIRTUAL_HOST,
                 credentials=pika.PlainCredentials(
                     username=USERNAME,
                     password=PASSWORD
                 )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True)
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None
        self.roomId = None
        self.tankId = None
        self.token = None
    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message))

        while self.response is None:
            self.connection.process_data_events()


    def healthcheck(self):
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def register(self, id):
        message = {
            'roomId': 'room-'+str(id)
            # 'roomId': id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tankId = self.response['tankId']
            self.roomId = self.response['roomId']
            return True
        return False


    def turnTank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire(self, token):
        message = {
            'token': token,
        }
        self.call('tank.request.fire', message)




class TankConsumerClient(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                 host=IP,
                 port=PORT,
                 virtual_host=VIRTUAL_HOST,
                 credentials=pika.PlainCredentials(
                     username=USERNAME,
                     password=PASSWORD
                 )
             )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(
            queue='',
            auto_delete=True,
            exclusive=True
        )

        event_listener = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=event_listener,
            routing_key='event.state.'+'room-'+str(id)
            # routing_key='event.state.' + id

        )
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()
        # self.channel.stop_consuming()







# ============= TANK WAS DRAWN ======================
class Draw:
    def drawBullet(self, x, y, width, height, direction, colour, owner):
        myTankId = client.tankId

        if owner == myTankId:
           win.blit(myBullet, (x, y))
        else:
           win.blit(enemyBullet, (x, y))

    def drawTank(self, x, y, width, height, direction, colour, id, angle):

        #========== get TankId =====================
        font = pygame.font.SysFont(None, 25)
        txtId = font.render(id, True, (255, 0, 0))
        txtDirection = txtId.get_rect()
        txtDirection.center = (x+10+width/2, y+height+30)
        win.blit(txtId, txtDirection)

        #=============== management =================
        myTankId = client.tankId
        if id == myTankId:
            justTank = myTank
        else:
            justTank = enemyTank

        if direction == 'RIGHT':
            angle -= 90
            if angle < 0:
                angle += 360
            tank = pygame.transform.rotate(justTank, angle)

        if direction == 'LEFT':
            angle += 90
            if angle >= 360:
                angle -= 360
            tank = pygame.transform.rotate(justTank, angle)


        if direction == 'UP':
            tank = justTank


        if direction == 'DOWN':
            tank = pygame.transform.rotate(justTank, 180)

        win.blit(tank, (x, y))

draw = Draw()
#================================================================================================





def game():
    won = False
    lost = False
    timeOut = False
    first = True
    angle = 0
    font = pygame.font.SysFont(None, 55)
    run = True
    while run:
        i = 130
        background = pygame.image.load(grassImg)
        win.blit(background, (0, 0))
        # win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
        myTankId = client.tankId


        try:
            #=============== Remaining Time ==============
            remainingTime=event_client.response['remainingTime']
            txt = font.render('Remaining Time {}'.format(remainingTime), True, (204, 255, 255))
            txtDirection = txt.get_rect()
            txtDirection.center = (400, 70)
            win.blit(txt, txtDirection)

            #=============== Tank ====================
            # MY TANK ITEMS
            MytankX = None
            MytankY = None
            MytankWidth = None
            MytankHeight = None
            MytankDirection = None
            MytankHealth = None
            MytankScore = None

            # ENEMY TANK ITEMS
            EnemytankId = None
            EnemytankX = None
            EnemytankY = None
            EnemytankWidth = None
            EnemytankHeight = None
            EnemytankDirection = None

            tanks=event_client.response['gameField']['tanks']
            for tank in tanks:
                tankId = tank['id']
                if tankId == myTankId:
                    MytankX = tank['x']
                    MytankY = tank['y']
                    MytankWidth = tank['width']
                    MytankHeight = tank['height']
                    MytankDirection = tank['direction']
                    MytankHealth = tank['health']
                    MytankScore = tank['score']
                    tankColour = (0,255,255)
                    # win.blit(myTank, (tankX, tankY))
                    draw.drawTank(MytankX, MytankY, MytankWidth, MytankHeight, MytankDirection, tankColour, tankId, angle)
                else:
                    EnemytankX = tank['x']
                    EnemytankY = tank['y']
                    EnemytankWidth = tank['width']
                    EnemytankHeight = tank['height']
                    EnemytankDirection = tank['direction']
                    tankColour = (0, 255, 255)
                    # win.blit(myTank, (tankX, tankY))
                    draw.drawTank(EnemytankX, EnemytankY, EnemytankWidth, EnemytankHeight, EnemytankDirection, tankColour, tankId, angle)
                # ============== SCORE =========================
                if tankId == myTankId:
                    txtScore = font.render('Score {}'.format(MytankScore), True, (204, 255, 255))
                    txtDirection = txtScore.get_rect()
                    txtDirection.center = (70, 70)
                    win.blit(txtScore, txtDirection)
                    # ================= HEALTH ======================
                    txtHealth = font.render('HP {}'.format(MytankHealth), True, (255, 153, 204))
                    txtDirection.center = (740, 70)
                    win.blit(txtHealth, txtDirection)
                justTank = {}

                player = pygame.font.SysFont(None, 25)
                for tank in tanks:
                    justTank[tank['id']] = [tank['health'], tank['score']]
                justTankSorted = {u: v for u, v in sorted(justTank.items(), key=lambda item: item[1][1], reverse=True)}
                for tank_id, tank_item in justTankSorted.items():
                    if tank_id == myTankId:
                        txt = player.render(
                            'ME' + ' --- Score: {}'.format(tank_item[1]) + ' --- HP: {}'.format(tank_item[0]), True,
                            (0, 0, 128))
                    else:
                        txt = player.render(
                            'ID: {}'.format(tank_id) + ' --- Score: {}'.format(tank_item[1]) + ' --- HP: {}'.format(
                                tank_item[0]), True, (153, 204, 255))
                    win.blit(txt, (500, i))
                    i += 30
                #================================================

            #================ Bullet ======================
            bullets = event_client.response['gameField']['bullets']
            #ENEMY BULLET
            EnemybulletX = None
            EnemybulletY = None
            EnemybulletWidth = None
            EnemybulletHeight = None
            EnemybulletDirection = None

            for bullet in bullets:
                bulletOwner=  bullet['owner']
                if bulletOwner == myTankId:
                    MybulletX = bullet['x']
                    MybulletY = bullet['y']
                    MybulletWidth = bullet['width']
                    MybulletHeight = bullet['height']
                    MybulletDirection = bullet['direction']
                    bulletColour = (255, 0 ,0)
                    draw.drawBullet(MybulletX, MybulletY, MybulletWidth, MybulletHeight, MybulletDirection, bulletColour, bulletOwner)
                else:
                    EnemybulletX = bullet['x']
                    EnemybulletY = bullet['y']
                    EnemybulletWidth = bullet['width']
                    EnemybulletHeight = bullet['height']
                    EnemybulletDirection = bullet['direction']
                    bulletColour = (255, 0, 0)
                    draw.drawBullet(EnemybulletX, EnemybulletY, EnemybulletWidth, EnemybulletHeight, EnemybulletDirection,bulletColour, bulletOwner)

            #=====================AI==============================
            if (0 <= EnemybulletX + EnemybulletWidth <= MytankX or MytankX <= EnemybulletX + EnemybulletWidth <= 800) and MytankY <= EnemybulletY <= MytankY + MytankHeight:
                client.turnTank(client.token, 'DOWN')
            elif (0 <= EnemybulletY + EnemybulletHeight <= MytankY or MytankY <= EnemybulletY + EnemybulletHeight <= 600) and MytankX <= EnemybulletX <= MytankX + MytankWidth:
                client.turnTank(client.token, 'RIGHT')

            myTankId = client.tankId
            keys = pygame.key.get_pressed()
            winners = event_client.response['winners']
            for winner in winners:
                if winner['tankId'] == myTankId:
                    won=True
            if won:
                txt = font.render('GAME OVER \n You WIN my congratulations \n Your total score {}'.format(winners['score']), True, (255, 153, 204))
                txtDirection = txt.get_rect()
                txtDirection.center = (400, 300)
                win.blit(txt, txtDirection)
                won = False
                client.connection.close()
                if keys[pygame.K_r]:
                    game()
            losers = event_client.response['losers']
            for loser in losers:
                if loser['tankId'] == myTankId:
                    lost = True
            if lost:
                txt = font.render('GAME OVER \n You LOST \n Your total score {}'.format(losers['score']), True, (255, 153, 204))
                txtDirection = txt.get_rect()
                txtDirection.center = (400, 300)
                win.blit(txt, txtDirection)
                client.connection.close()
                if keys[pygame.K_r]:
                    game()

            if remainingTime == 0:
                txt = font.render('GAME OVER ', True, (255, 153, 204))
                txtDirection = txt.get_rect()
                txtDirection.center = (400, 300)
                win.blit(txt, txtDirection)
                client.connection.close()
                # run = False
                if keys[pygame.K_r]:
                    game()

            kicked = event_client.response['kicked']
            for kick in kicked:
                if kick['tankId'] == myTankId:
                    timeOut = True
            if timeOut:
                txt = font.render('GAME OVER\nYou kicked\nYour total score {}'.format(kicked['score']), True, (255, 153, 204))
                txtDirection = txt.get_rect()
                txtDirection.center = (400, 300)
                win.blit(txt, txtDirection)
                client.connection.close()
                pygame.quit()
                if keys[pygame.K_r]:
                    game()

        except:
            pass
        pygame.display.flip()
        # pygame.display.update()
    client.connection.close()
    pygame.quit()



client = TnakClient()
client.healthcheck()



def startAiMode(will = False):
    if will:
        event_client.start()
        game()

for i in range(1, 31):
    if client.register(i):
        event_client = TankConsumerClient(i)
        threadLock = threading.Lock()
        break

# client.register('room-7')
# # client.turnTank( client.token, 'UP')
# event_client = TankConsumerClient('room-7')
# event_client.start()
# game()


