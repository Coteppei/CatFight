import pyxel
import time


# 各画面処理
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_CONFIMATION = 3
SCENE_CLEAR = 4

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
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(3, 0)

    def draw(self):
        pyxel.blt(0, 0, 0, 0, 0, 0, 0, 0)

class App:
    def __init__(self):

        # 編集中1
        pyxel.init(90, 125, title="Cat Fight!!")
        # ポーズ画面
        self.pause = False # ポーズ状態を管理する変数

        # 画像のロード
        pyxel.load("assets/sample.pyxres")
        self.scene_start_time = 0  # シーンが始まった時間を保持する変数
        self.scene_duration = 5  # シーンが切り替わるまでの時間（秒）
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
        elif self.scene == SCENE_PLAY:          # バトル画面
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:      # ゲームオーバー画面
            self.update_gameover_scene()
        elif self.scene == SCENE_CONFIMATION:   # キャンセル確認画面
            self.update_confimation_scene()
        elif self.scene == SCENE_CLEAR:         # クリア画面
            self.update_clear_scene()

    def update_title_scene(self):
        self.life = 2
        self.enemyLife = 50
        self.avoidFlg = False
        self.actionFlg = False
        self.avoid_start_frame = 0 # 避ける時間を計測

        pyxel.image(1).load(0, 0, "assets/CatFight_OP.png")
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.scene = SCENE_PLAY
            pyxel.playm(1, loop=True)

    def update_play_scene(self):

        # 背景画面
        pyxel.image(1).load(0, 0, "assets/ring.png")

        # プレイヤー側操作
        # 画面上部の押下があったとき、ダメージを相手に与える
        # if not self.pause:        # ポーズ判定を一旦廃止

        # 攻撃動作
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.enemyLife -= 1
            self.attackFlg = True
            # 攻撃により相手のライフを0にしたとき、クリアを表示する
            if self.enemyLife == 0:
                self.scene = SCENE_CLEAR
                pyxel.playm(0, loop=True)
        # 回避動作
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.avoidFlg = True
            self.actionFlg = True
        if self.actionFlg:
            self.avoid_start_frame = time.time()
            self.actionFlg = False
        if self.avoidFlg:
            if time.time() - self.avoid_start_frame >= 1:  # 60フレームで1秒経過
                self.avoidFlg = False

        # 敵側動作
        if self.scene_start_time == 0:
            self.scene_start_time = time.time()
        # 経過時間を計算
        elapsed_time = time.time() - self.scene_start_time
        # 時間経過で攻撃準備
        if elapsed_time >= self.scene_duration and elapsed_time <= 5.5:
            pyxel.blt(0, 15, 2, 105, 80, 100, 80, 7)
        # 攻撃動作
        elif elapsed_time >= 5.5:
            pyxel.blt(0, 30, 2, 105, 80, 100, 80, 7)
            # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
            if self.avoidFlg == True and elapsed_time >= 6:
                self.scene_start_time = 0  # 次のシーンのためにリセット
            # 攻撃後通常位置に戻る
            elif elapsed_time >= 6:
                self.scene = SCENE_GAMEOVER
                pyxel.playm(0, loop=True)
        # 通常位置  デッドロジックのため廃止
        # if elapsed_time < self.scene_duration:
        #     pyxel.blt(0, 5, 2, 105, 80, 100, 80, 7)

        for enemy in enemies:
            pyxel.play(3, 1)
            self.scene = SCENE_GAMEOVER

        self.player.update()
        # else:         #ポーズ判定を一旦廃止
        #     pass

        # ポーズ画面の操作処理  一旦廃止
        # if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)):
        #     # ポーズ状態を反転させる
        #     self.pause = not self.pause

    # ゲームオーバー画面
    def update_gameover_scene(self):
        if self.life > 0 and pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.life -= 1
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
            self.scene = SCENE_TITLE

# フロント側
    def draw(self):
        pyxel.cls(0)

        self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
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

    # 戦闘画面
    def draw_play_scene(self):
        if not self.pause:
            self.player.draw()
            if  pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                pyxel.blt(10, 10, 2, 0, 0, 100, 80, 7)
            elif self.avoidFlg:
                pyxel.blt(10, 77, 2, 0, 0, 100, 80, 7)
            else:
                pyxel.blt(10, 54, 2, 0, 0, 100, 80, 7)

            # 敵の画像
            # シーンが始まった瞬間に時間を設定
            if self.scene_start_time == 0:
                self.scene_start_time = time.time()
            # 経過時間を計算
            elapsed_time = time.time() - self.scene_start_time

            if elapsed_time >= self.scene_duration and elapsed_time <= 5.5:
                pyxel.blt(10, 15, 2, 105, 80, 100, 80, 7)
            if elapsed_time >= 5.5:
                pyxel.blt(10, 30, 2, 105, 80, 100, 80, 7)
                if elapsed_time >= 6:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
            if elapsed_time < self.scene_duration:
                pyxel.blt(10, 5, 2, 105, 80, 100, 80, 7)
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
        pyxel.text(38, 55, "CLEAR!", 7)

App()
