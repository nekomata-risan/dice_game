import pyxel

SCREEN_WIDTH = 320      # 画面の幅
SCREEN_HEIGHT = 240     # 画面の高さ
DICE_OFFSET_X = 90
DICE_OFFSET_Y = 20
LIST_OFFSET_X = 50
LIST_OFFSET_Y = 60
DICE_WIGTH = 16
DICE_HEIGHT = 16
MAX_SHAKE = 3
MAX_ROUND = 12

class App:
    def __init__(self):
        self.diceArray = [0, 0, 0, 0, 0]
        self.keepDiceArray = [False, False, False, False, False]
        self.scoreArray = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.hiScore = 0
        self.sum = 0
        self.roundCount = 0
        self.shakeCount = 0
        self.isPlaySE = True

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="dice game", fps=60, display_scale=2)
        pyxel.mouse(True)
        pyxel.load("assets/main.pyxres")
        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        # サイコロ
        for i in range(len(self.diceArray)):
            index = self.diceArray[i]
            pyxel.blt(DICE_OFFSET_X + i * 2 * DICE_WIGTH, DICE_OFFSET_Y, 0, index * DICE_WIGTH, 0, DICE_WIGTH, DICE_HEIGHT, pyxel.COLOR_PURPLE)
            if self.keepDiceArray[i]:
                pyxel.text(DICE_OFFSET_X + i * 2 * DICE_WIGTH, DICE_OFFSET_Y - 10, "keep", pyxel.COLOR_WHITE)

        # 得点表
        pyxel.line(LIST_OFFSET_X, LIST_OFFSET_Y, LIST_OFFSET_X, LIST_OFFSET_Y + 150, pyxel.COLOR_WHITE)
        pyxel.line(LIST_OFFSET_X + 60, LIST_OFFSET_Y, LIST_OFFSET_X + 60, LIST_OFFSET_Y + 150, pyxel.COLOR_WHITE)
        pyxel.line(LIST_OFFSET_X + 84, LIST_OFFSET_Y, LIST_OFFSET_X + 84, LIST_OFFSET_Y + 150, pyxel.COLOR_WHITE)
        pyxel.line(LIST_OFFSET_X + 220, LIST_OFFSET_Y, LIST_OFFSET_X + 220, LIST_OFFSET_Y + 150, pyxel.COLOR_WHITE)
        pyxel.text(LIST_OFFSET_X, LIST_OFFSET_Y - 10, "Score Board", pyxel.COLOR_WHITE)
        for i in range(16):
            pyxel.line(LIST_OFFSET_X, LIST_OFFSET_Y + i * 10, LIST_OFFSET_X + 220, LIST_OFFSET_Y + i * 10, pyxel.COLOR_WHITE)

            tmpStr = ""
            if i == 0: tmpStr = "Role(Score)"
            if i == 1: tmpStr = "Ace"
            if i == 2: tmpStr = "Duce"
            if i == 3: tmpStr = "Three"
            if i == 4: tmpStr = "Four"
            if i == 5: tmpStr = "Five"
            if i == 6: tmpStr = "Six"
            if i == 7: tmpStr = "Chance"
            if i == 8: tmpStr = "Full House(25)"
            if i == 9: tmpStr = "Four Dice"
            if i == 10: tmpStr = "S.Straight(30)"
            if i == 11: tmpStr = "B.Straight(40)"
            if i == 12: tmpStr = "Yahtzee(50)"
            if i == 13: tmpStr = "Total Score"
            if i == 14: tmpStr = "Hi score"
            pyxel.text(LIST_OFFSET_X + 2, LIST_OFFSET_Y + i * 10 + 3, tmpStr, pyxel.COLOR_WHITE)
            tmpStr = ""
            if i == 0: tmpStr = "Score"
            if i > 0 and i < 13 and self.scoreArray[i - 1] >= 0: tmpStr = str(self.scoreArray[i - 1]).rjust(5)
            
            if i == 13: tmpStr = str(self.sum).rjust(5)
            if i == 14: tmpStr = str(self.hiScore).rjust(5)
            pyxel.text(LIST_OFFSET_X + 62, LIST_OFFSET_Y + i * 10 + 3, tmpStr, pyxel.COLOR_WHITE)
            tmpStr = ""
            if i == 0: tmpStr = "Role description"
            if i == 1: tmpStr = "Total of 1"
            if i == 2: tmpStr = "Total of 2"
            if i == 3: tmpStr = "Total of 3"
            if i == 4: tmpStr = "Total of 4"
            if i == 5: tmpStr = "Total of 5"
            if i == 6: tmpStr = "Total of 6"
            if i == 7: tmpStr = "Total number rolled"
            if i == 8: tmpStr = "3 cards and 2 pairs"
            if i == 9: tmpStr = "4 or more same dice"
            if i == 10: tmpStr = "4 or more consecutive numbers"
            if i == 11: tmpStr = "5 consecutive numbers"
            if i == 12: tmpStr = "All same dice"
            pyxel.text(LIST_OFFSET_X + 86, LIST_OFFSET_Y + i * 10 + 3, tmpStr, pyxel.COLOR_WHITE)

        tmpX = 16 if self.isPlaySE else 0
        pyxel.blt(LIST_OFFSET_X + 205, LIST_OFFSET_Y + 152, 0, tmpX, DICE_HEIGHT, DICE_WIGTH, DICE_HEIGHT, pyxel.COLOR_PURPLE)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x
            y = pyxel.mouse_y

            # 効果音設定
            if x >= LIST_OFFSET_X + 205 and x <= LIST_OFFSET_X + 221 and y >= LIST_OFFSET_Y + 152 and y <= LIST_OFFSET_Y + 168:
                self.isPlaySE = not self.isPlaySE

            if self.shakeCount == 0:
                return

            if self.shakeCount < MAX_SHAKE:
                # サイコロのキープON/OFF切り替え
                for i in range(5):
                    if DICE_OFFSET_X + i * 32 <= x and x <= DICE_OFFSET_X + i * 32 + DICE_WIGTH \
                        and DICE_OFFSET_Y <= y and y <= DICE_OFFSET_Y + DICE_HEIGHT:

                        self.keepDiceArray[i] = not self.keepDiceArray[i]
                        self.playSE(0)
                        return

            # 役の選択
            for i in range(12):
                if x < LIST_OFFSET_X + 60 or x > DICE_OFFSET_X + 100:
                    return
                if LIST_OFFSET_Y + (i + 1) * 10 <= y and y <= LIST_OFFSET_Y + (i + 2) * 10:
                    if self.scoreArray[i] >= 0:     # 既に選択した役の場合、何もしない
                        break
                    self.calc(i)
                    self.roundCount += 1
                    self.shakeCount = 0
                    self.resetKeep()
                    break
        
        elif pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.shakeDice()
        elif pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.reTry()

    def shakeDice(self):
        if self.isKeepAll():
            return

        if self.roundCount >= MAX_ROUND:
            self.reTry()

        if self.shakeCount == 0:
            self.resetKeep()

        if self.shakeCount >= MAX_SHAKE:
            self.playSE(1)
            return

        for i in range(len(self.diceArray)):
            if self.keepDiceArray[i]:
                continue

            self.diceArray[i] = pyxel.rndi(0, 5)

        self.shakeCount += 1

    def reTry(self):
        self.resetDice()
        for i in range(len(self.scoreArray)):
            self.scoreArray[i] = -1

        self.roundCount = 0
        self.shakeCount = 0
        self.sum = 0

    def calc(self, roleId):
        tmpVal = 0
        tmpSum = 0
        if roleId == 0:     # エース
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 0:
                    tmpVal += 1
        elif roleId == 1:   # デュース
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 1:
                    tmpVal += 1
            tmpVal *= 2
        elif roleId == 2:   # スリー
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 2:
                    tmpVal += 1
            tmpVal *= 3
        elif roleId == 3:   # フォー
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 3:
                    tmpVal += 1
            tmpVal *= 4
        elif roleId == 4:   # ファイブ
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 4:
                    tmpVal += 1
            tmpVal *= 5
        elif roleId == 5:   # シックス
            for i in range(len(self.diceArray)):
                if self.diceArray[i] == 5:
                    tmpVal += 1
            tmpVal *= 6
        elif roleId == 6:   # チャンス
            for i in range(len(self.diceArray)):
                tmpVal += self.diceArray[i] + 1
        elif roleId == 7:   # フルハウス
            isRole = True
            histDice = [0, 0, 0, 0, 0, 0]
            for i in range(len(self.diceArray)):
                histDice[self.diceArray[i]] += 1
            for i in range(len(histDice)):
                if (histDice[i] == 1 or histDice[i] == 4 or histDice[i] == 5):
                    isRole = False
            if isRole:
                tmpVal = 25
        elif roleId == 8:   # フォーダイス
            isRole = False
            histDice = [0, 0, 0, 0, 0, 0]
            for i in range(len(self.diceArray)):
                histDice[self.diceArray[i]] += 1
            for i in range(len(histDice)):
                if histDice[i] >= 4:
                    isRole = True
                    break
            if isRole:
                for i in range(len(self.diceArray)):
                    tmpVal += self.diceArray[i] + 1
        elif roleId == 9:   # S.ストレート
            isRole = True
            tmpDice = 0
            tmpArray = self.diceArray[:]
            tmpCount = 0
            tmpArray.sort()
            for i in range(len(tmpArray) - 1):
                tmpDice = tmpArray[i]
                if tmpDice + 1 != tmpArray[i + 1]:
                    tmpCount += 1
                if tmpCount > 1:
                    isRole = False
                    break
            if isRole:
                tmpVal = 30
        elif roleId == 10:  # B.ストレート
            isRole = True
            tmpDice = 0
            tmpArray = self.diceArray[:]
            tmpCount = 0
            tmpArray.sort()
            for i in range(len(tmpArray) - 1):
                tmpDice = tmpArray[i]
                if tmpDice + 1 != tmpArray[i + 1]:
                    isRole = False
                    break
            if isRole:
                tmpVal = 40
        elif roleId == 11:  # ヨット
            isRole = True
            tmpDice = 0
            for i in range(len(self.diceArray)):
                if i == 0:
                    tmpDice = self.diceArray[i]
                elif tmpDice != self.diceArray[i]:
                    isRole = False
                    break
            if isRole:
                tmpVal = 50

        self.scoreArray[roleId] = tmpVal
        for i in range(len(self.scoreArray)):
            if self.scoreArray[i] < 0:
                continue
            tmpSum += self.scoreArray[i]
        self.sum = tmpSum
        if self.sum > self.hiScore:
            self.hiScore = self.sum

        if roleId < 7:
            self.playSE(2)
        else:
            if tmpVal > 0:
                self.playSE(3)
            else:
                self.playSE(2)

    def resetDice(self):
        for i in range(len(self.diceArray)):
            self.diceArray[i] = 0
            self.keepDiceArray[i] = False

    def resetKeep(self):
        for i in range(len(self.keepDiceArray)):
            self.keepDiceArray[i] = False

    def isKeepAll(self):
        result = True
        for i in range(len(self.keepDiceArray)):
            if not self.keepDiceArray[i]:
                result = False
                break
        return result

    def playSE(self, index):
        if not self.isPlaySE:
            return
        pyxel.play(3, index)

App()
