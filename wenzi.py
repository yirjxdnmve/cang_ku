import random

def fen_ge_xian(biaoti):
    """分割线"""
    if biaoti == "":
        print("-" * 30)
    else:
        print("-" * 15 + biaoti + "-" * 15)

class Character:
    count = 0
    def __init__(self, name: str):
        """初始化角色的基本属性"""
        self.id = Character.count
        Character.count += 1
        self.name = name
        self.type = None
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 10
        self.agility = 3
        self.mp = 100
        self.max_mp = 100
        self.defense = random.randint(0, 5)
        self.xp = 0
        self.level = 1
        self.g = 0
        self.bei_bao = []

    def attack(self, target: "Character"):
        """攻击目标"""
        if target.hp <= 0:
            print(f"{target.name} 已经死亡，无法攻击")
            return
             
        damage = max(
            random.randint(0, 5), self.attack_power - target.defense
        )
        if random.randint(0, 100) < target.agility:
            print(f"{target.name} 闪避了 {self.name} 的攻击!")
        else:
            target.hp -= damage
            print(f"{self.name} 攻击了 {target.name}，造成了 {damage} 点伤害")
            if target.name == "洛洛":
               speak = random.choice(["咕...那里，不可以！", "呜！不可以打这种地方！", "那里...热起来了...好奇怪..."])
            else: 
               speak = random.choice(["嘶", "...", "呃啊——"])
            print(f"{target.name}:{speak}")

    def ju_shu_gong_ji(self, target: "Character"):
        """拘束攻击"""
        if random.random() < 0.5:
            print(f"{self.name}对{target.name}使用了拘束攻击！")
            if random.randint(1, 20) - target.agility > 14:
                print(f"{target.name}被拘束了！")
            else:
                print(f"{target.name}躲开了！")

    def __str__(self) -> str:
        """查询生命值"""        
        return f"{self.name} hp:{self.hp} mp:{self.mp} level:{self.level}"
    
    def judge_death(self):
        """判断是否死亡"""     
        if self.hp <= 0:
            if self.type == "player":
                print(f"{self.name}战败")
            print(f"{self.name}死亡！")
            return True
        else:
            return False
        
    def fa_shu(self):
        """法术"""
        if self.mp >= 25:
            self.mp -= 25
            hvfu = random.randint(20, self.max_mp/2)
            self.hp += hvfu
            print(f"{self.name}使用了法术，恢复了{hvfu}点生命！")
        else:
            print(f"{self.name}的法力不足！无法使用治疗术！")

    def get_xp_and_diao_lo(self):
        """获取经验值和掉落"""
        self.g += self.level*6
        if random.randint(0, 100) < 10:
            diao_lo =random.choice(["红药水", "蓝药水", "黄药水"])
            self.bei_bao.append(diao_lo)
            print(f"{self.name}获得了{diao_lo}！")
        self.xp += self.level*40
        if self.xp >= self.level*40:
            self.up_level()

    def up_level(self):
        """升级"""
        self.attack_power += 5
        self.defense += 5
        self.max_hp += 20
        self.hp = self.max_hp
        self.max_mp += 20
        self.mp = self.max_mp       
        self.level += 1
        self.xp = 0
        if self.type == "player":
            print(f"{self.name}升到了{self.level}级！")
            print(f"{self.name}感到充满了决心")
        
class Enemy(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "enemy"
        self.level = 1

class Player(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "player"
        self.attack_power = 20
        self.level = 1
        self.max_hp = 100
        self.max_mp = 100

class EnemyFactory:
    def __init__(self):
        """初始化敌人生存列表"""
        self.current_enemy = []

    def judge_enemy_is_null(self):
        """判断敌人是否为空"""
        return len(self.current_enemy) == 0

    def get_random_name(self):
        """随机生成敌人名字"""
        return random.choice(["史莱姆", "哥布林", "牛头人", "兽人", "翼人"])

    def sheng_cheng_gao_deng_ji_di_ren(self, level: int):
        """生成对应主角等级的敌人"""
        self.current_enemy.append(Enemy(f"{level}级{self.get_random_name()}"))
        if level > 1:
            for i in range(level-1):
                for enemy in self.current_enemy:
                    enemy.up_level()

    def remove_enemy(self, id: int):
        """移除敌人"""
        self.current_enemy = [enemy for enemy in self.current_enemy if enemy.id != id]

    def __str__(self) -> str:
        """查询敌人列表"""
        result = f"当前敌人：\n"
        for enemy in self.current_enemy:
            result += f"{enemy}\n"
        result +="\n"
        return f"当前敌人数量：{len(self.current_enemy)}\n" + result

class Game:
    """游戏类的初始化方法，创建玩家对象和敌人生存工厂"""
    def __init__(self):
        """初始化游戏，创建玩家和敌人生存广场"""
        self.player = Player("player")
        self.enemy_factory = EnemyFactory()
    
    def start(self):
        """开始游戏，进行战斗直到玩家死亡或退出游戏"""
        print("欢迎来到竞技场！")
        print("赛制是车轮战，只有当玩家死亡的时候才会结束！")
        player_name = input("请输入你的名字：")
        if player_name != "":
            self.player.name = player_name
        
        is_continue = True
        self.main_loop(is_continue)
        print(f"=====\n你一共杀死了{Character.count - 1}个敌人！\n=====")

    def shuang_fang_vhuang_tai(self):
        fen_ge_xian("玩家状态")
        print(self.player)
        fen_ge_xian("敌人状态")
        print(self.enemy_factory)
    
    def main_loop(self, is_continue):
        """游戏的主循环"""
        zairu = "1"
        while is_continue:
            if zairu == "1":
                fen_ge_xian("开始游戏")
                print("你睁开了眼睛，由石砖垒起的穹顶已经风化的坑坑洼洼，而你就躺在穹顶下的石板上，你坐起身环顾四周，地上堆满了各种锈迹斑斑的武器。\n"
                      "你晃了晃脑袋，大脑一片混沌。能够能想起来的只有四个字：“献上战斗”。你站起身，拿起了地上锈迹斑斑的短剑")
                print("1. 开始战斗")
                print("2. ? ? 苏醒 ? ?")
                shuru_1 = input("你决定好了吗?； ")
            if shuru_1 == "2":
                print(
                    "你意识到了这里的虚假，并且对这所谓的竞技场没兴趣，毫不犹疑的拒绝了。\n"
                    "你的意识逐渐模糊，石砖在你眼中崩塌，搅动，逐渐成为了不可辨别的色块，而当你再次睁开眼睛的时候，窗外阳光明媚，仿佛你刚才经历的只是一场梦。\n"
                    "现在，你醒了"
                    )
                is_continue = False

            if shuru_1 == "1" or shuru_1 == "":
                zairu = "0"
                if self.enemy_factory.judge_enemy_is_null():
                        self.enemy_factory.sheng_cheng_gao_deng_ji_di_ren(
                            self.player.level
                        )
                        print()
                        fen_ge_xian("敌人出现！")
                        print(self.enemy_factory)
                print("===================")
                print("1. 攻击")
                print("2. 治疗")
                print("3. 背包")
                print("4. 逃跑")
                choice = input("请选择： ")
                fen_ge_xian("开始战斗")
                if choice == "1" or choice == "":
                    for enemy in self.enemy_factory.current_enemy:
                        self.player.attack(enemy)
                        if enemy.judge_death():
                            self.enemy_factory.remove_enemy(enemy.id)
                            self.player.get_xp_and_diao_lo()
                                
                    for enemy in self.enemy_factory.current_enemy:
                        if random.random() < 0.5:
                            enemy.ju_shu_gong_ji(self.player)
                        else:
                            enemy.attack(self.player)
                            if self.player.judge_death():
                                is_continue = False
                    print() 
                    fen_ge_xian("玩家状态")
                    print(self.player)
                    print()
                    fen_ge_xian("敌人状态")
                    print(self.enemy_factory)
                if choice == "2":
                    self.player.fa_shu()
                    for enemy in self.enemy_factory.current_enemy:
                        enemy.attack(self.player)
                        if self.player.judge_death():
                            is_continue = False
                    print() 
                    fen_ge_xian("玩家状态")
                    print(self.player)
                    print()
                    fen_ge_xian("敌人状态")
                    print(self.enemy_factory)
                if choice == "3":
                    print(self.player.bei_bao)
                if choice == "4":
                    print("游戏结束！")
                    is_continue = False


if __name__ == "__main__":
    game = Game()
    game.start()
    input("按任意键退出")
    