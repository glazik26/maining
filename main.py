import sys
import pygame
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Инициализация библиотеки
pygame.init()

# Загрузка изображений
background_img = pygame.image.load('img/background.jpg')  # Загрузка фона
bitcoin_img = pygame.image.load('img/bitcoin.png')  # Загрузка печеньки
button_img = pygame.image.load('img/button.png')
achivement_img = pygame.image.load('img/ach.png')

clickSFX = pygame.mixer.Sound("sound/click.wav")
clickSFX.set_volume(0.2)
achivementSFX = pygame.mixer.Sound("sound/ach.wav")
achivementSFX.set_volume(0.2)
upgradeSFX = pygame.mixer.Sound("sound/upgrade.wav")
upgradeSFX.set_volume(0.2)
pygame.mixer.music.load("sound/main.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# Цвета
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)


class MainBitcoin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250

        self.animation_state = False

    def draw(self):
        if self.animation_state:
            bitcoin_img_scaled = pygame.transform.scale(bitcoin_img,
                                                        (int(0.98 * self.length), int(0.98 * self.height)))
            window.blit(bitcoin_img_scaled, (
                bitcoin_img_scaled.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
        else:
            window.blit(bitcoin_img, (
                bitcoin_img.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))

    def collide(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)


class UpgradeButtons:
    def __init__(self, name, x, y, image, cost, cost_increase, cps):
        self.name = name
        self.x = x
        self.y = y
        self.length = 400
        self.height = 100
        self.image = image
        self.cost = cost
        self.cost_increase = cost_increase
        self.cps = cps
        self.quantity = 0
        self.created = 0

    def collide(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)

    def getCost(self):
        return self.cost * self.cost_increase ** self.quantity

    def draw(self, solid=True):
        image = self.image
        name = self.name
        cost_font = pygame.font.Font(None, 17)
        quantity_font = pygame.font.Font(None, 36)
        name_font = pygame.font.Font(None, 22)

        name = name_font.render(name, True, WHITE)
        cost = cost_font.render('{:.5f}'.format(self.getCost()), True, WHITE)
        quantity = quantity_font.render('{}'.format(self.quantity), True, WHITE)

        if solid:
            image.set_alpha(100)
        else:
            image.set_alpha(255)

        window.blit(image, (self.x, self.y))
        window.blit(name, (self.x + 100, self.y + self.height - 70))
        window.blit(cost, (self.x + 15, self.y + 15))
        window.blit(quantity, (self.x + self.length - 40, self.y + self.height - 70))


class Score:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.height = 100

    def draw(self):
        font = pygame.font.Font(None, 24)

        score = font.render('{:.5f} биткойн'.format(float(user.score)), True, WHITE)
        cps = font.render('в секунду : {:.6f}'.format(float(user.cps)), True, WHITE)
        window.blit(score, (score.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))))
        window.blit(cps, (cps.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2) + 20))))


class Player:
    def __init__(self):
        self.score = 0
        self.click_multiply = 0
        self.cps = 0

    def updateCPS(self, list_of_upgrades):
        self.cps = 0
        for upgrades in list_of_upgrades:
            self.cps += upgrades.cps * upgrades.quantity


class SaveButton:
    def __init__(self, name, x, y, image):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250
        self.image = image
        self.name = name

    def collide(self, mouse_pos):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)

    def draw(self):
        image = self.image
        name = self.name
        img_scaled = pygame.transform.scale(image, (150, 60))
        name_font = pygame.font.Font(None, 22)
        name = name_font.render(name, True, WHITE)
        img_scaled.set_alpha(255)

        window.blit(img_scaled, (self.x, self.y))
        window.blit(name, (self.x + 55, self.y + 15))


class achivementAlarm:
    def __init__(self, name, x, y, image):
        self.x = x
        self.y = y
        self.length = 250
        self.height = 250
        self.image = image
        self.name = name
        self.earned = False

    def draw(self):
        image = self.image
        name = self.name
        name_font = pygame.font.Font(None, 22)
        name = name_font.render(name, True, BLACK)
        image.set_alpha(200)

        window.blit(image, (self.x, self.y))
        window.blit(name, (self.x + 70, self.y + 10))

def makeSmall(x):
    return x * 10 ** -5


def save():
    fp = open('save.txt', 'w')
    fp.write(str(user.score) + '\n')
    fp.write(str(user.cps) + '\n')
    fp.write(str(upgrade_1.quantity) + '\n')
    fp.write(str(upgrade_2.quantity) + '\n')
    fp.write(str(upgrade_3.quantity) + '\n')
    fp.write(str(upgrade_4.quantity) + '\n')
    fp.write(str(upgrade_5.quantity) + '\n')
    fp.write(str(upgrade_6.quantity) + '\n')
    fp.close()


def load():
    fp = open('save.txt', 'r')
    data = fp.readlines()
    print(data)
    user.score = float(data[0])
    user.cps = float(data[1])
    upgrade_1.quantity = int(data[2])
    upgrade_2.quantity = int(data[3])
    upgrade_3.quantity = int(data[4])
    upgrade_4.quantity = int(data[5])
    upgrade_5.quantity = int(data[6])
    upgrade_6.quantity = int(data[7])
    fp.close()


def achivements():
    if user.score >= 0.0001 and not ach2.earned or ach1.earned and not ach2.earned:
        ach1.earned = True
        ach1.draw()
    if user.score >= 0.0002 and not ach3.earned or ach2.earned and not ach3.earned:
        ach2.earned = True
        ach2.draw()
    if user.score >= 0.0003 and not ach4.earned or ach3.earned and not ach4.earned:
        ach3.earned = True
        ach3.draw()
    if user.score >= 0.0004 and not ach5.earned or ach4.earned and not ach5.earned:
        ach4.earned = True
        ach4.draw()
    if user.score >= 0.0005 and not ach6.earned or ach5.earned and not ach6.earned:
        ach5.earned = True
        ach5.draw()
    if user.score >= 0.0006 and not ach7.earned or ach6.earned and not ach7.earned:
        ach6.earned = True
        ach6.draw()
    if user.score >= 0.0007 and not ach8.earned or ach7.earned and not ach8.earned:
        ach7.earned = True
        ach7.draw()
    if user.score >= 0.0008 and not ach9.earned or ach8.earned and not ach9.earned:
        ach8.earned = True
        ach8.draw()
    if user.score >= 0.0009 and not ach10.earned or ach9.earned and not ach10.earned:
        ach9.earned = True
        ach9.draw()
    if user.score >= 0.001 or ach10.earned:
        ach10.earned = True
        ach10.draw()



# Настройка окна
window = pygame.display.set_mode((1200, 680))  # Размер окна
pygame.display.set_caption("Clicker")  # Название окна

bitcoin = MainBitcoin(300, 220)
score_display = Score(100, 0)
user = Player()

click_power = makeSmall(1)
click_power_multiply = 1.25
upgrade_y = 10
upgrade_1 = UpgradeButtons('Сила клика', 792, upgrade_y, button_img, makeSmall(20), 2.8, 0)
upgrade_2 = UpgradeButtons('Сила клика2', 792, upgrade_y + 110 * 1, button_img, makeSmall(15), 1.15, makeSmall(0.1))
upgrade_3 = UpgradeButtons('Сила клика3', 792, upgrade_y + 110 * 2, button_img, makeSmall(100), 1.15, makeSmall(0.5))
upgrade_4 = UpgradeButtons('Сила клика4', 792, upgrade_y + 110 * 3, button_img, makeSmall(500), 1.15, makeSmall(4))
upgrade_5 = UpgradeButtons('Сила клика5', 792, upgrade_y + 110 * 4, button_img, makeSmall(3000), 1.15, makeSmall(10))
upgrade_6 = UpgradeButtons('Сила клика6', 792, upgrade_y + 110 * 5, button_img, makeSmall(10000), 1.15, makeSmall(40))
saveButton = SaveButton('SAVE', 20, 600, button_img)
loadButton = SaveButton('LOAD', 200, 600, button_img)
ach1 = achivementAlarm('Ачива 1', 450, 600, achivement_img)
ach2 = achivementAlarm('Ачива 2', 450, 600, achivement_img)
ach3 = achivementAlarm('Ачива 3', 450, 600, achivement_img)
ach4 = achivementAlarm('Ачива 4', 450, 600, achivement_img)
ach5 = achivementAlarm('Ачива 5', 450, 600, achivement_img)
ach6 = achivementAlarm('Ачива 6', 450, 600, achivement_img)
ach7 = achivementAlarm('Ачива 7', 450, 600, achivement_img)
ach8 = achivementAlarm('Ачива 8', 450, 600, achivement_img)
ach9 = achivementAlarm('Ачива 9', 450, 600, achivement_img)
ach10 = achivementAlarm('Ачива 10', 450, 600, achivement_img)

upgrades_list = [upgrade_1, upgrade_2, upgrade_3, upgrade_4, upgrade_5, upgrade_6]


# Функция отрисовки
def draw():
    window.blit(background_img, (-400, 0))  # Отрисовка фона

    achivements()
    bitcoin.draw()
    score_display.draw()
    saveButton.draw()
    loadButton.draw()
    for upgrade in upgrades_list:
        if user.score >= upgrade.getCost():
            upgrade.draw(solid=False)
        else:
            upgrade.draw(solid=True)

        user.score += upgrade.quantity * upgrade.cps * .01
        upgrade.created += upgrade.quantity * upgrade.cps * .01

    pygame.display.update()  # Обновление окна


# Основной цикл
while True:

    pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if bitcoin.collide(mouse_pos):
                clickSFX.stop()
                clickSFX.play()
                user.score += click_power
                bitcoin.animation_state = True

            if saveButton.collide(mouse_pos):
                save()

            if loadButton.collide(mouse_pos):
                load()

            for upgrade in upgrades_list:
                if upgrade.collide(mouse_pos) and user.score >= upgrade.getCost():
                    upgradeSFX.play()
                    if upgrade == upgrade_1:
                        click_power = click_power * click_power_multiply
                        user.score -= upgrade.getCost()
                        upgrade.quantity += 1
                    else:
                        user.score -= upgrade.getCost()
                        upgrade.quantity += 1
                        user.updateCPS(upgrades_list)

        if event.type == pygame.MOUSEBUTTONUP:
            bitcoin.animation_state = False

        if event.type == pygame.QUIT:
            sys.exit()

    draw()