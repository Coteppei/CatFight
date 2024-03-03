import pyxel
import time
import random

# 各画面処理
SCENE_TITLE = 0
SCENE_LOADING = 1
SCENE_PLAY = 2
SCENE_GAMEOVER = 3
SCENE_CONFIMATION = 4
SCENE_CLEAR = 5
SCENE_SECOND_PLAY = 6

# 敵キャラのインスタンス
enemies = []


def load_bgm(msc, filename, snd1, snd2, snd3):
    # Loads a json file for 8bit BGM generator by frenchbread.
    # Each track is stored in snd1, snd2 and snd3 of the sound
    # respectively and registered in msc of the music.
    import json

    with open(filename, "rt") as file:
        bgm = json.loads(file.read())
        pyxel.sounds[snd1].set(*bgm[0])
        pyxel.sounds[snd2].set(*bgm[1])
        pyxel.sounds[snd3].set(*bgm[2])
        pyxel.musics[msc].set([snd1], [snd2], [snd3])

class Background:
    def __init__(self):
        self.stars = []

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed

    def draw(self):
        pyxel.blt(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)

class Player:
    def __init__(self, x, y):
        self.is_alive = True

    def update(self):       # 攻撃したときのSE音
        pyxel.blt(0, 0, 0, 0, 0, 0, 0, 0)

    def draw(self):
        pyxel.blt(0, 0, 0, 0, 0, 0, 0, 0)

class App:
    def __init__(self):

        # 編集中1
        pyxel.init(90, 125, title="Cat Fight!!")
        # ポーズ画面
        self.pause = False # ポーズ状態を管理する変数

        # 画像のロード

        pyxel.load("assets/character.pyxres")

        self.mouse_center_y = pyxel.height // 2

        # 味方の画像表示

        # 敵の画像表示
        pyxel.sounds[0].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[1].set("a3a2c2c2", "n", "7742", "s", 10)
        load_bgm(0, "assets/bgm_title.json", 2, 3, 4)
        load_bgm(1, "assets/bgm_play.json", 5, 6, 7)
        self.scene = SCENE_TITLE
        self.score = 0

        self.background = Background()
        self.player = Player(pyxel.width / 2, pyxel.height - 20)
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.background.update()
        if self.scene == SCENE_TITLE:           # タイトル画面
            self.update_title_scene()
        elif self.scene == SCENE_LOADING:       # ロード画面
            self.update_loading_scene()
        elif self.scene == SCENE_PLAY:          # バトル画面
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:      # ゲームオーバー画面
            self.update_gameover_scene()
        elif self.scene == SCENE_CONFIMATION:   # キャンセル確認画面
            self.update_confimation_scene()
        elif self.scene == SCENE_CLEAR:         # クリア画面
            self.update_clear_scene()
        elif self.scene == SCENE_SECOND_PLAY:   # 二回戦バトル画面
            self.update_second_play_scene()

    def update_title_scene(self):
        self.life = 2
        self.IfLihe = self.life
        self.enemyLife = 50
        self.avoidFlg = False
        self.actionFlg = False
        self.avoid_start_frame = 0          # 避ける時間を計測
        self.timeCount = time.time()        # 経過時間情報を更新
        self.pauseStartTimeCount = 0        # ポーズボタン押下後からの時間を計測
        self.pauseTimeCount = 0             # ポーズ時間中の経過時間を計測する用
        self.pauseEnemyFlg = False          # ポーズによって止まる敵の動作用
        self.pause_pressed_time = 0         # ポーズボタンを押したときのタイムラグを設定
        self.enemyAttack = 0
        self.scene_start_time = 0  # シーンが始まった時間を保持する変数
        # self.scene_duration = self.enemyAttack - 0.5  # シーンが切り替わるまでの時間（秒）
        self.punchFlg = True #Trueでパンチ可能状態
        self.avoidanceRestrictions = 30 # 回避回数を制限
        self.loudingTimeCount = 0           # ローディング画面開始からの時間を計測
        self.pouseCount = 3                 # ポーズの回数を制限
        self.pouseFlg = False               # 現在がポーズ状態か判定

        pyxel.image(1).load(0, 0, "assets/CatFight_OP.png")
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.battleStage = 1
            self.loudingTimeCount = time.time()
            self.scene = SCENE_LOADING

    # 戦闘直前ロード画面
    def update_loading_scene(self):
        if self.battleStage == 1:
            pyxel.image(1).load(0, 0, "assets/firstLoading.png")
            self.startTime = time.time() + 3
            if time.time() > self.loudingTimeCount + 5:
                self.enemyAttack = random.uniform(7, 8.5)
                self.scene = SCENE_PLAY
                pyxel.playm(1, loop=True)
        elif self.battleStage == 2:
            pyxel.image(1).load(0, 0, "assets/firstLoading.png")
            self.startTime = time.time() + 3
            if time.time() > self.loudingTimeCount + 5:
                self.enemyAttack = random.uniform(7, 8.5)
                self.scene = SCENE_PLAY
                pyxel.playm(1, loop=True)

    # バトル画面
    def update_play_scene(self):

        # 背景画面
        pyxel.image(1).load(0, 0, "assets/ring.png")
        # プレイヤー側操作
        # 画面上部の押下があったとき、ダメージを相手に与える
        if not self.pause:        # ポーズ判定を一旦廃止
            # ポーズ判定
            if self.pauseTimeCount == 0:
                self.timeCount = time.time()
            else:
                # ポーズ中の時間を経過時間から引いてポーズ直前に戻る
                self.timeCount = time.time() - (self.pauseTimeCount - self.pauseStartTimeCount)

            # 攻撃動作
            if (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.punchFlg == True:
                pyxel.play(3, 0)
                self.enemyLife -= 1
                self.attackFlg = True
                # 攻撃により相手のライフを0にしたとき、クリアを表示する
                if self.enemyLife == 0:
                    self.scene = SCENE_CLEAR
                    pyxel.playm(0, loop=True)
            # 回避動作
            if self.avoidanceRestrictions > 0:
                if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.avoidFlg = True
                    self.actionFlg = True
                    self.punchFlg = False
                if self.actionFlg:
                    self.avoid_start_frame = self.timeCount
                    self.actionFlg = False
                if self.avoidFlg:
                    if self.timeCount - self.avoid_start_frame >= 0.5:  # 0.5秒間回避
                        self.avoidFlg = False
                        self.punchFlg = True
                        self.avoidanceRestrictions -=1
                        self.enemyLife += 10

            # 敵側動作
            if self.scene_start_time == 0:
                self.scene_start_time = self.timeCount
            # 経過時間を計算
            elapsed_time = self.timeCount - self.scene_start_time
            # 攻撃動作
            if elapsed_time >= self.enemyAttack:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if self.avoidFlg == True and elapsed_time >= self.enemyAttack + 0.5:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(2, 5.5)   # 次の敵攻撃感覚のリセット
                # 攻撃後通常位置に戻る
                elif elapsed_time >= self.enemyAttack + 0.5:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)

            for enemy in enemies:
                pyxel.play(3, 1)
                self.scene = SCENE_GAMEOVER

            self.player.update()
        else:         # ポーズ判定を一旦廃止
            if self.pauseEnemyFlg == False:
                self.pauseStartTimeCount = time.time()
            self.pauseEnemyFlg = True
            self.pauseTimeCount = time.time()
            self.pouseFlg = True
            pass
            pyxel.stop()

        # ポーズ画面の操作処理
        if pyxel.btnp(pyxel.KEY_A) and self.pouseCount > 0 or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) and self.pouseCount > 0:
            if self.pause_pressed_time == 0:
                self.pause_pressed_time = time.time()
        if time.time() - self.pause_pressed_time >= 0.5 and self.pause_pressed_time != 0:
            self.pause_pressed_time = 0
            if self.pouseFlg == True:
                self.pouseCount -= 1
            self.pouseFlg = False
            pyxel.playm(1, loop=True)
            # ポーズ状態を反転させる
            self.pause = not self.pause

    def update_second_play_scene(self):
        1

    # ゲームオーバー画面
    def update_gameover_scene(self):
        if self.life > 0 and pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.pouseCount = 3
            self.life -= 1
            self.startTime = time.time()
            self.scene = SCENE_PLAY
            pyxel.playm(1, loop=True)
        elif self.life > 0 and pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.scene = SCENE_CONFIMATION
        else:
            # 残機を失ったら強制ゲームオーバー
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.scene = SCENE_TITLE

    # endを選択したときの分岐画面
    def update_confimation_scene(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.scene = SCENE_TITLE
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.scene = SCENE_GAMEOVER

    def update_clear_scene(self):
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.battleStage += 1
            self.loudingTimeCount = time.time()
            self.scene = SCENE_LOADING

# フロント側
    def draw(self):
        pyxel.cls(0)

        self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_LOADING:
            self.draw_loading_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_CONFIMATION:
            self.draw_confimation_scene()
        elif self.scene == SCENE_CLEAR:
            self.draw_clear_scene()

    # 初期画面
    def draw_title_scene(self):
        # 編集中2
        pyxel.text(25, 45, "Cat Fight!!", pyxel.frame_count % 16)
        pyxel.text(18, 80, "- GAME START -", 7)

    def draw_loading_scene(self):
        pyxel.text(43, 22, "NAME:Cato", 7)
        pyxel.text(43, 29, "HEIGHT:60cm", 7)
        pyxel.text(43, 36, "WEIGHT:6kg", 7)
        pyxel.blt(-3, 11, 0, 200, 40, 100, 80, 15)         #プレーヤー側の顔
        # pyxel.blt(50, 81, 0, 88, 24, 100, 80, 15)       #右腕

        pyxel.text(6, 82, "NAME:BulanKen", 7)
        pyxel.text(6, 89, "HEIGHT:200cm", 7)
        pyxel.text(6, 96, "WEIGHT:900kg", 7)


    # 戦闘画面
    def draw_play_scene(self):
        if not self.pause:
            self.player.draw()
                # pyxel.blt(20, 10, 0, 0, 0, 100, 80, 15)

            # 敵の画像
            # シーンが始まった瞬間に時間を設定
            if self.scene_start_time == 0:
                self.scene_start_time = self.timeCount
            # 経過時間を計算
            elapsed_time = self.timeCount - self.scene_start_time

            # 敵側UI
            if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                # 攻撃準備
                pyxel.blt(5, -10, 2, 0, 0, 90, 130, 3)        #胴体
                pyxel.blt(5, -10, 2, 96, 0, 90, 130, 3)        #右腕
            if elapsed_time >= self.enemyAttack:
                # 攻撃直前
                pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)        #胴体
                pyxel.blt(5, 10, 2, 96, 0, 90, 130, 3)        #右腕
                if elapsed_time >= self.enemyAttack + 0.5:
                    pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)
                    self.scene_start_time = 0  # 次のシーンのためにリセット
            if elapsed_time < self.enemyAttack - 0.5:
                # 通常状態
                pyxel.blt(5, -30, 2, 0, 0, 90, 130, 3)      #胴体
                pyxel.blt(5, -30, 2, 96, 0, 90, 120, 3)      #右腕

            # プレイヤー側UI
            if  (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.punchFlg == True:
                pyxel.blt(20, 67, 0, 0, 0, 100, 80, 15)         #胴体
                pyxel.blt(22, 78, 0, 136, 24, 100, 80, 15)       #左腕
            elif self.avoidFlg:
                pyxel.blt(50, 101, 0, 88, 24, 100, 80, 15)       #右腕
                pyxel.blt(20, 87, 0, 0, 0, 100, 80, 15)         #胴体
                pyxel.blt(22, 98, 0, 136, 24, 100, 80, 15)       #左腕
            else:
                pyxel.blt(50, 81, 0, 88, 24, 100, 80, 15)       #右腕
                pyxel.blt(20, 67, 0, 0, 0, 100, 80, 15)         #胴体
                pyxel.blt(22, 78, 0, 136, 24, 100, 80, 15)       #左腕

            # 敵の体の上に腕を表示したいため、右腕のみ下にセット
            if  (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.punchFlg == True:
                pyxel.blt(39, 47, 0, 69, 94, 100, 80, 15)       #右腕

            # 敵の攻撃はプレイヤーの上に置く
            if elapsed_time >= self.enemyAttack:
                if elapsed_time >= self.enemyAttack + 0.3:
                    pyxel.blt(5, 10, 2, 176, 0, 90, 120, 3)         #右腕
        # 騎士の画像
        else:
            pyxel.cls(0)
            pyxel.text(38, 50, "PAUSE", 7)

    def draw_gameover_scene(self):
        if self.life > 0:
            pyxel.text(29, 25, "GAME OVER", 8)
            pyxel.text(30, 45, "CONTINUE", 7)
            pyxel.text(41, 80, "END", 13)
        else:
            pyxel.text(29, 60, "GAME OVER", 8)

    def draw_confimation_scene(self):
        pyxel.text(31, 25, "REALLY?", 8)
        pyxel.text(39, 45, "YES", 7)
        pyxel.text(41, 80, "NO", 13)

    def draw_clear_scene(self):
        pyxel.text(27, 55, "NEXT STAGE!! ", 7)

App()
