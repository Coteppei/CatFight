import pyxel
import time
import random

# 各画面処理
SCENE_TITLE = 0         # タイトル画面
SCENE_LOADING = 1       # ロード画面
SCENE_BATTLE = 2        # 戦闘画面
SCENE_GAMEOVER = 3      # ゲームオーバー画面
SCENE_CONFIMATION = 4   # リトライ画面
SCENE_CLEAR = 5         # クリア画面
SCENE_SECOND_BATTLE = 6 # 二回戦戦闘画面
SCENE_THIRD_BATTLE = 7  # 最終戦戦闘画面

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
        elif self.scene == SCENE_BATTLE:          # バトル画面
            self.update_battle_scene()
        elif self.scene == SCENE_GAMEOVER:      # ゲームオーバー画面
            self.update_gameover_scene()
        elif self.scene == SCENE_CONFIMATION:   # キャンセル確認画面
            self.update_confimation_scene()
        elif self.scene == SCENE_CLEAR:         # クリア画面
            self.update_clear_scene()
        elif self.scene == SCENE_SECOND_BATTLE:   # 二回戦バトル画面
            self.update_second_battle_scene()
        elif self.scene == SCENE_THIRD_BATTLE:  #三回戦バトル画面
            self.update_third_battle_scene()

    def update_title_scene(self):
        self.life = 2
        self.IfLihe = self.life
        self.enemyLife = 1                  # ブランケンの体力
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
        self.patternJudge = False           # 攻撃パターンが決まったかを判定する
        self.hipstrikeFlg = False           # 二回戦目の一トンのヒップアタックフラグ
        self.right_hand_flg = False         # リラマッチョの右手攻撃フラグ
        self.left_hand_flg = False          # リラマッチョの左手攻撃フラグ
        self.combo_flg = False              # リラマッチョのコングコンボフラグ
        self.retry = False                  # リトライを決定するためのフラグ
        self.end = False                    # ゲームをやめるためのフラグ
        self.nextFlg = False                # 次のステージへ遷移するためのフラグ

        pyxel.image(1).load(0, 0, "assets/firstLoading.png")    # 1回目のロード画面
        pyxel.image(1).load(0, 0, "assets/2ndLoading.png")      # 2回目のロード画面
        pyxel.image(1).load(0, 0, "assets/2ndLoading.png")      # 3回目のロード画面
        pyxel.image(1).load(0, 0, "assets/ring.png")            # 1回戦目の背景
        pyxel.image(1).load(0, 0, "assets/2ndRing.png")         # 2回戦目の背景
        pyxel.image(1).load(0, 0, "assets/3rdRing.png")         # 3回戦目の背景
        pyxel.image(1).load(0, 0, "assets/CatFight_OP.png")     # オープニング画面
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.battleStage = 2                                # ステージ設定
            self.loudingTimeCount = time.time()
            self.scene = SCENE_LOADING

    # 戦闘直前ロード画面
    def update_loading_scene(self):
        if self.battleStage == 1:
            pyxel.image(1).load(0, 0, "assets/firstLoading.png")
            # self.startTime = time.time() + 3
            if time.time() > self.loudingTimeCount + 5:
                self.enemyAttack = random.uniform(7, 8.5)
                self.scene = SCENE_BATTLE
                pyxel.playm(1, loop=True)
        elif self.battleStage == 2:
            pyxel.image(1).load(0, 0, "assets/2ndLoading.png")
            # self.startTime = time.time() + 3
            if time.time() > self.loudingTimeCount + 5:
                self.enemyLife = 1             # 一トンの体力
                self.enemyAttack = random.uniform(7, 8.5)
                self.scene_start_time = 0       # 前バトルでの敵の行動と自分の行動を比較するための開始時間をリセット
                self.pause_pressed_time = 0     # 前バトルでのポーズ時間の計測をリセット
                self.scene = SCENE_SECOND_BATTLE
                pyxel.playm(1, loop=True)
        elif self.battleStage == 3:
            pyxel.image(1).load(0, 0, "assets/3rdLoading.png")
            if time.time() > self.loudingTimeCount + 5:
                self.enemyLife = 1             # リラマッチョの体力
                self.enemyAttack = random.uniform(7, 8.5)
                self.scene_start_time = 0       # 前バトルでの敵の行動と自分の行動を比較するための開始時間をリセット
                self.pause_pressed_time = 0     # 前バトルでのポーズ時間の計測をリセット
                self.scene = SCENE_THIRD_BATTLE
                self.patternJudge = False       # ジャッジフラグのリセット
                pyxel.playm(1, loop=True)

    # バトル画面
    def update_battle_scene(self):
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
                    if self.timeCount - self.avoid_start_frame >= 0.25:  # 0.25秒間回避
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
                    self.enemyAttack = random.uniform(2.5, 4.5)   # 次の敵攻撃感覚のリセット
                # 攻撃後通常位置に戻る
                elif elapsed_time >= self.enemyAttack + 0.5:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)

            for enemy in enemies:
                pyxel.play(3, 1)
                self.scene = SCENE_GAMEOVER

            self.player.update()
        else:
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

    # 二回戦目バトル画面
    def update_second_battle_scene(self):
                # 背景画面
        pyxel.image(1).load(0, 0, "assets/2ndRing.png")
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
                    if self.timeCount - self.avoid_start_frame >= 0.25:  # 0.25秒間回避
                        self.avoidFlg = False
                        self.punchFlg = True
                        self.avoidanceRestrictions -=1
                        self.enemyLife += 10

            # 敵側動作
            # 30%でヒップストライクが70%で通常攻撃が飛んでくる
            num = random.random()
            if num < 0.3 and not self.patternJudge:
                self.hipstrikeFlg = True
                self.patternJudge = True
            elif not self.patternJudge:
                self.hipstrikeFlg = False
                self.patternJudge = True

            if self.scene_start_time == 0:
                self.scene_start_time = self.timeCount
            # 経過時間を計算
            elapsed_time = self.timeCount - self.scene_start_time
            # 攻撃動作
            # 通常攻撃
            if elapsed_time >= self.enemyAttack and not self.hipstrikeFlg:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if self.avoidFlg == True and elapsed_time >= self.enemyAttack + 0.5:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(1.5, 5)   # 次の敵攻撃感覚のリセット
                    self.patternJudge = False   # 攻撃判断をリセットする
                # 避けれていなかったらゲームオーバー
                elif elapsed_time >= self.enemyAttack + 0.5:

                    #デバッグ状態
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)
                    # self.scene_start_time = 0  # 次のシーンのためにリセット
                    # self.enemyAttack = random.uniform(1, 5)   # 次の敵攻撃感覚のリセット

            # 攻撃動作
            # ヒップストライク
            if elapsed_time >= self.enemyAttack and self.hipstrikeFlg:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if self.avoidFlg == True and elapsed_time >= self.enemyAttack + 0.6:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(1, 5)   # 次の敵攻撃感覚のリセット
                    self.patternJudge = False   # 攻撃判断をリセットする
                # 避けれていなかったらゲームオーバー
                elif elapsed_time >= self.enemyAttack + 0.6:

                    #デバッグ状態
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)
                    # self.scene_start_time = 0  # 次のシーンのためにリセット
                    # self.enemyAttack = random.uniform(1, 5)   # 次の敵攻撃感覚のリセット

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

    # 三回戦目バトル画面
    def update_third_battle_scene(self):

        # 背景画面
        pyxel.image(1).load(0, 0, "assets/3rdRing.png")
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
                    if self.timeCount - self.avoid_start_frame >= 0.25:  # 0.25秒間回避
                        self.avoidFlg = False
                        self.punchFlg = True
                        self.avoidanceRestrictions -=1
                        self.enemyLife += 10

            # 敵側動作
            # 35%右手攻撃、35%左手攻撃、30%コンボ攻撃
            num = random.random()
            if not self.patternJudge:
                if num < 0.4:
                    self.right_hand_flg = True
                    self.left_hand_flg = False
                    self.combo_flg = False
                    self.patternJudge = True
                elif num < 0.8:
                    self.right_hand_flg = False
                    self.left_hand_flg = True
                    self.combo_flg = False
                    self.patternJudge = True
                else:
                    self.right_hand_flg = False
                    self.left_hand_flg = False
                    self.combo_flg = True
                    self.patternJudge = True

            if self.scene_start_time == 0:
                self.scene_start_time = self.timeCount
            # 経過時間を計算
            elapsed_time = self.timeCount - self.scene_start_time
            # 右手攻撃動作
            if elapsed_time >= self.enemyAttack and self.right_hand_flg:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if self.avoidFlg == True and elapsed_time >= self.enemyAttack + 0.5:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(0.8, 5.0)   # 次の敵攻撃感覚のリセット
                    self.patternJudge = False   # 攻撃判断をリセットする
                # 攻撃後通常位置に戻る
                elif elapsed_time >= self.enemyAttack + 0.5:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)

            # 左手攻撃動作
            if elapsed_time >= self.enemyAttack and self.left_hand_flg:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if self.avoidFlg == True and elapsed_time >= self.enemyAttack + 0.75:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(2, 5.5)   # 次の敵攻撃感覚のリセット
                    self.patternJudge = False  # 攻撃判断をリセットする
                # 攻撃後通常位置に戻る
                elif elapsed_time >= self.enemyAttack + 0.75:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)

            # コングコンボ攻撃動作
            if elapsed_time >= self.enemyAttack and self.combo_flg:
                # このときプレイヤー側が避ける動作をしていた場合、攻撃を無効化する
                if elapsed_time >= self.enemyAttack + 0.5 and not self.avoidFlg:
                    self.scene = SCENE_GAMEOVER
                    self.patternJudge = False  # 攻撃判断をリセットする
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(5, 7.5)   # 次の敵攻撃感覚のリセット
                    pyxel.playm(0, loop=True)
                elif elapsed_time >= self.enemyAttack + 0.6 and not self.avoidFlg:
                    self.scene = SCENE_GAMEOVER
                    pyxel.playm(0, loop=True)
                elif self.avoidFlg and elapsed_time >= self.enemyAttack + 0.6:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                    self.enemyAttack = random.uniform(5, 7.5)   # 次の敵攻撃感覚のリセット
                    self.patternJudge = False  # 攻撃判断をリセットする


            for enemy in enemies:
                pyxel.play(3, 1)
                self.scene = SCENE_GAMEOVER

            self.player.update()
        else:
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

    # ゲームオーバー画面
    def update_gameover_scene(self):
        if self.life > 0 and pyxel.btnp(pyxel.KEY_UP) or self.life > 0 and pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            # 上ボタンを押すとリトライを立てる
            self.retry = True
            self.end = False
        elif pyxel.btnp(pyxel.KEY_S) and self.retry or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and self.retry:
            # リトライフラグが立っていると再挑戦する
            self.retry = False
            self.pouseCount = 3
            self.life -= 1
            # self.startTime = time.time()
            self.scene = SCENE_BATTLE
            pyxel.playm(1, loop=True)
            if self.battleStage == 1:
                random.uniform(1.5, 3.5)
                self.scene = SCENE_BATTLE
            elif self.battleStage == 2:
                random.uniform(1.5, 4.5)
                # self.scene_start_time = 0
                self.scene = SCENE_SECOND_BATTLE
            elif self.battleStage == 3:
                random.uniform(1.5, 4.5)
                self.scene = SCENE_THIRD_BATTLE
        elif self.life > 0 and pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            # 下ボタンを押すとエンドフラグを立てる
            self.retry = False
            self.end = True
        elif pyxel.btnp(pyxel.KEY_S) and self.end or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and self.end:
            #　エンドフラグが立っていると本当にやめる画面に遷移する。
            self.retry = True
            self.end = False
            self.scene = SCENE_CONFIMATION
        elif self.life == 0:
            # 残機を失ったら強制ゲームオーバー
            if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.scene = SCENE_TITLE
        elif self.life > 0 and pyxel.btnp(pyxel.KEY_S) and not self.retry and not self.retry or self.life > 0 and pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and not self.retry and not self.retry:
            self.retry = True
            self.end = False

    # endを選択したときの分岐画面
    def update_confimation_scene(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            # エンドフラグを立てる
            self.retry = False
            self.end = True
        elif pyxel.btnp(pyxel.KEY_S) and self.end or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and self.end:
            # エンドフラグが立っているとタイトル画面に戻る
            self.end = False
            self.scene = SCENE_TITLE
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            # リトライフラグを立てる
            self.retry = True
            self.end = False
        elif pyxel.btnp(pyxel.KEY_S) and self.retry or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and self.retry:
            # リトライフラグが立っているとゲームーオーバー画面に戻る
            self.retry = False
            self.end = True
            self.scene = SCENE_GAMEOVER

    def update_clear_scene(self):
        if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) and self.battleStage < 3:
            self.nextFlg = True
        elif pyxel.btnp(pyxel.KEY_S) and self.nextFlg and self.battleStage < 3 or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) and self.nextFlg and self.battleStage < 3:
            self.nextFlg = False
            self.battleStage += 1
            self.scene_start_time = 0
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
        elif self.scene == SCENE_BATTLE:
            self.draw_battle_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_CONFIMATION:
            self.draw_confimation_scene()
        elif self.scene == SCENE_CLEAR:
            self.draw_clear_scene()
        elif self.scene == SCENE_SECOND_BATTLE:
            self.draw_second_battle_scene()
        elif self.scene == SCENE_THIRD_BATTLE:
            self.draw_third_battle_scene()

    # 初期画面
    def draw_title_scene(self):
        # 編集中2
        pyxel.text(25, 45, "Cat Fight!!", pyxel.frame_count % 16)
        pyxel.text(18, 80, "- GAME START -", 7)

    def draw_loading_scene(self):
        pyxel.blt(-3, 11, 0, 200, 40, 100, 80, 15)        #プレーヤー側の顔

    # 戦闘画面
    def draw_battle_scene(self):
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
                    pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)   #胴体
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

    # 二回戦目戦闘画面
    def draw_second_battle_scene(self):
        if not self.pause:
            self.player.draw()

            # 敵の画像
            # シーンが始まった瞬間に時間を設定
            if self.scene_start_time == 0:
                self.scene_start_time = self.timeCount
            # 経過時間を計算
            elapsed_time = self.timeCount - self.scene_start_time

            # 敵側UI
            if not self.hipstrikeFlg:
                if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                    # 攻撃準備
                    # if self.hipstrikeFlg:
                    #     pyxel.blt(0, 43, 2, 88, 175, 64, 70, 10)      # 胴体
                    # else:
                    pyxel.blt(13, 33, 2, 88, 175, 64, 70, 10)      # 胴体
                    pyxel.blt(20, 20, 2, 16, 160, 55, 48, 10)        # 頭部
                    pyxel.blt(12, 73, 2, 160, 160, 21, 26, 10)        # 右足
                    pyxel.blt(62, 81, 2, 168, 192, 21, 23, 10)        # 左足
                if elapsed_time >= self.enemyAttack and elapsed_time <= self.enemyAttack + 0.3:

                    # if self.hipstrikeFlg:
                    #     pyxel.blt(-15, 43, 2, 88, 175, 64, 70, 10)         # 胴体
                    # else:
                    # 攻撃直前
                    pyxel.blt(13, 43, 2, 88, 175, 64, 70, 10)        # 胴体
                    pyxel.blt(20, 30, 2, 16, 160, 55, 48, 10)        # 頭部
                    pyxel.blt(12, 83, 2, 160, 160, 21, 26, 10)        # 右足
                    pyxel.blt(62, 91, 2, 168, 192, 21, 23, 10)        # 左足
                elif elapsed_time >= self.enemyAttack + 0.3:
                    # if self.hipstrikeFlg:
                    #     pyxel.blt(60, 83, 2, 88, 175, 64, 70, 10)         # 胴体
                    # else:
                    pyxel.blt(13, 43, 2, 88, 175, 64, 70, 10)        # 胴体
                    pyxel.blt(12, 83, 2, 160, 160, 21, 26, 10)        # 右足
                    pyxel.blt(62, 91, 2, 168, 192, 21, 23, 10)        # 左足
                    if elapsed_time >= self.enemyAttack + 0.5:

                        self.scene_start_time = 0  # 次のシーンのためにリセット
                if elapsed_time < self.enemyAttack - 0.5:
                    # 通常状態
                    pyxel.blt(13, 13, 2, 88, 175, 64, 70, 10)      # 胴体
                    pyxel.blt(20, 0, 2, 16, 160, 55, 48, 10)        # 頭部
                    pyxel.blt(12, 53, 2, 160, 160, 21, 26, 10)        # 右足
                    pyxel.blt(62, 61, 2, 168, 192, 21, 23, 10)        # 左足

            # 敵側UI※ヒップストライク時の動作
            if self.hipstrikeFlg:
                if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                    # 攻撃準備
                    pyxel.blt(13, 13, 2, 88, 175, 64, 70, 10)      # 胴体
                if elapsed_time >= self.enemyAttack and elapsed_time <= self.enemyAttack + 0.2:
                    # 攻撃直前
                    pyxel.blt(0, 13, 2, 88, 175, 64, 70, 10)         # 胴体
                elif elapsed_time >= self.enemyAttack and elapsed_time <= self.enemyAttack + 0.33:
                    # 攻撃直前
                    pyxel.blt(-15, 13, 2, 88, 175, 64, 70, 10)         # 胴体
                elif elapsed_time >= self.enemyAttack and elapsed_time <= self.enemyAttack + 0.5:
                    # 攻撃直前
                    pyxel.blt(45, 50, 2, 88, 175, 64, 70, 10)         # 胴体
                elif elapsed_time >= self.enemyAttack + 0.6:
                    self.scene_start_time = 0  # 次のシーンのためにリセット
                if elapsed_time < self.enemyAttack - 0.5:
                    # 通常状態
                    pyxel.blt(13, 13, 2, 88, 175, 64, 70, 10)      # 胴体
                    pyxel.blt(20, 0, 2, 16, 160, 55, 48, 10)        # 頭部
                    pyxel.blt(12, 53, 2, 160, 160, 21, 26, 10)        # 右足
                    pyxel.blt(62, 61, 2, 168, 192, 21, 23, 10)        # 左足

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

            # 猫の攻撃モーション
            if  (pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.punchFlg == True:
                pyxel.blt(39, 47, 0, 69, 94, 100, 80, 15)       #右腕

            # 猫の体の上に頭を表示したいため、頭のみ下にセット
            if elapsed_time >= self.enemyAttack:
                if elapsed_time >= self.enemyAttack + 0.3 and not self.hipstrikeFlg:
                    pyxel.blt(20, 70, 2, 16, 208, 55, 48, 10)        # 頭部
                if elapsed_time >= self.enemyAttack + 0.5 and self.hipstrikeFlg:
                    # 攻撃
                    pyxel.blt(13, 50, 2, 88, 175, 64, 70, 10)         # 胴体
        # 騎士の画像
        else:
            pyxel.cls(0)
            pyxel.text(38, 50, "PAUSE", 7)

        # 三回戦目戦闘画面
    def draw_third_battle_scene(self):
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
            # 右手攻撃
            if self.right_hand_flg:
                if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                    # 攻撃準備
                    pyxel.blt(-3, 7, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(6, 47, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(43, 47, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack and elapsed_time < self.enemyAttack + 0.3:
                    # 攻撃直前
                    pyxel.blt(-3, 14, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(6, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(43, 54, 1, 208, 153, 35, 46, 6)     #左腕
                    # pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)        #胴体
                    # pyxel.blt(5, 10, 2, 96, 0, 90, 130, 3)        #右腕
                elif elapsed_time >= self.enemyAttack + 0.3:
                    pyxel.blt(-3, 14, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(43, 54, 1, 208, 153, 35, 46, 6)     #左腕
                    if elapsed_time >= self.enemyAttack + 0.5:

                        # pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)   #胴体
                        self.scene_start_time = 0  # 次のシーンのためにリセット
                if elapsed_time < self.enemyAttack - 0.5:
                    # 通常状態
                    pyxel.blt(3, 0, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 40, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(49, 40, 1, 208, 153, 35, 46, 6)      #左腕
                    # pyxel.blt(0, 80, 1, 24, 104, 70, 144, 6)      #下半身
                    # pyxel.blt(5, -30, 2, 96, 0, 90, 120, 3)      #右腕
            elif self.left_hand_flg:
                # 左手攻撃
                if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                    # 攻撃準備
                    pyxel.blt(9, 7, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(18, 47, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(55, 47, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack and elapsed_time < self.enemyAttack + 0.3:
                    # 攻撃直前
                    pyxel.blt(9, 14, 1, 90, 25, 168, 144, 6)     #胴体
                    pyxel.blt(18, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(55, 54, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack + 0.3 and elapsed_time < self.enemyAttack + 0.6:
                    pyxel.blt(9, 14, 1, 90, 25, 168, 144, 6)     #胴体
                    pyxel.blt(18, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(55, 54, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack + 0.6:
                    pyxel.blt(9, 14, 1, 90, 25, 168, 144, 6)     #胴体
                    pyxel.blt(18, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    if elapsed_time >= self.enemyAttack + 0.75:
                        self.scene_start_time = 0  # 次のシーンのためにリセット
                if elapsed_time < self.enemyAttack - 0.5:
                    # 通常状態
                    pyxel.blt(3, 0, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 40, 1, 170, 153, 29, 46, 6)    #右腕
                    pyxel.blt(49, 40, 1, 208, 153, 35, 46, 6)    #左腕
            elif self.combo_flg:
                # コンボ攻撃
                if elapsed_time >= self.enemyAttack - 0.5 and elapsed_time <= self.enemyAttack:
                    # 攻撃準備
                    pyxel.blt(3, 7, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 47, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(49, 47, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack and elapsed_time < self.enemyAttack + 0.35:
                    # 攻撃直前
                    pyxel.blt(3, 14, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(49, 54, 1, 208, 153, 35, 46, 6)     #左腕
                    # pyxel.blt(5, 10, 2, 0, 0, 90, 130, 3)        #胴体
                    # pyxel.blt(5, 10, 2, 96, 0, 90, 130, 3)        #右腕
                elif elapsed_time >= self.enemyAttack + 0.35 and elapsed_time < self.enemyAttack + 0.42:
                    pyxel.blt(3, 14, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(49, 54, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack + 0.42 and elapsed_time < self.enemyAttack + 0.52:
                    pyxel.blt(3, 14, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(49, 54, 1, 208, 153, 35, 46, 6)     #左腕
                elif elapsed_time >= self.enemyAttack + 0.52:
                    pyxel.blt(3, 14, 1, 90, 25, 168, 144, 6)     #胴体
                    pyxel.blt(11, 54, 1, 170, 153, 29, 46, 6)      #右腕
                    if elapsed_time >= self.enemyAttack + 0.6:
                        self.scene_start_time = 0  # 次のシーンのためにリセット
                if elapsed_time < self.enemyAttack - 0.5:
                    # 通常状態
                    pyxel.blt(3, 0, 1, 90, 25, 168, 144, 6)      #胴体
                    pyxel.blt(11, 40, 1, 170, 153, 29, 46, 6)      #右腕
                    pyxel.blt(49, 40, 1, 208, 153, 35, 46, 6)      #左腕
            else:
                # 通常状態
                pyxel.blt(3, 0, 1, 90, 25, 168, 144, 6)        #胴体
                pyxel.blt(11, 40, 1, 170, 153, 29, 46, 6)      #右腕
                pyxel.blt(49, 40, 1, 208, 153, 35, 46, 6)      #左腕

            if elapsed_time < self.enemyAttack - 0.5:
                # 通常状態
                pyxel.blt(3, 0, 1, 90, 25, 168, 144, 6)        #胴体
                pyxel.blt(11, 40, 1, 170, 153, 29, 46, 6)      #右腕
                pyxel.blt(49, 40, 1, 208, 153, 35, 46, 6)      #左腕

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
            if elapsed_time >= self.enemyAttack and self.right_hand_flg:
                if elapsed_time >= self.enemyAttack + 0.3:
                    pyxel.blt(12, 54, 1, 184, 65, 55, 58, 6)      #右腕3
            elif elapsed_time >= self.enemyAttack and self.left_hand_flg:
                if elapsed_time > self.enemyAttack + 0.6:
                    pyxel.blt(29, 52, 1, 30, 167, 55, 62, 6)      #左腕49
            elif elapsed_time >= self.enemyAttack and self.combo_flg:
                if elapsed_time >= self.enemyAttack + 0.35 and elapsed_time < self.enemyAttack + 0.42:
                    pyxel.blt(18, 54, 1, 184, 65, 55, 58, 6)
                elif elapsed_time >= self.enemyAttack + 0.52:
                    pyxel.blt(23, 52, 1, 30, 167, 55, 62, 6)
                    1
        # 騎士の画像
        else:
            pyxel.cls(0)
            pyxel.text(38, 50, "PAUSE", 7)

    def draw_gameover_scene(self):
        if self.life > 0:
            if self.retry:
                pyxel.text(29, 25, "GAME OVER", 8)
                pyxel.text(30, 45, "CONTINUE", 7)
                pyxel.text(41, 80, "END", 13)
            elif self.end:
                pyxel.text(29, 25, "GAME OVER", 8)
                pyxel.text(30, 45, "CONTINUE", 13)
                pyxel.text(41, 80, "END", 7)
            else:
                pyxel.text(29, 50, "YOU LOSE", 8)
        else:
            pyxel.text(29, 60, "GAME OVER", 8)

    def draw_confimation_scene(self):
        if self.retry:
            pyxel.text(31, 25, "REALLY?", 8)
            pyxel.text(39, 45, "YES", 13)
            pyxel.text(41, 80, "NO", 7)
        elif self.end:
            pyxel.text(31, 25, "REALLY?", 8)
            pyxel.text(39, 45, "YES", 7)
            pyxel.text(41, 80, "NO", 13)

    def draw_clear_scene(self):
        if self.battleStage < 3 and not self.nextFlg:
            pyxel.text(33, 60, "YOU WIN", 7)
        elif self.battleStage < 3 and self.nextFlg:
            pyxel.text(26, 60, "NEXT STAGE!!", 7)
        else:
            pyxel.text(27, 55, "Congrats!", 7)
App()
