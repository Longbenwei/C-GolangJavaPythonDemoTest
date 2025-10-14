import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 60
GRID_ROWS = 5
GRID_COLS = 9

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("植物大战僵尸")

# 字体设置
font = pygame.font.SysFont("SimHei", 30)

# 游戏状态
class GameState:
    def __init__(self):
        self.money = 150  # 初始金钱
        self.score = 0
        self.game_over = False
        self.selected_plant = None
        self.zombies = []
        self.plants = []
        self.bullets = []
        self.sunlight = []
        self.wave = 1
        self.zombies_spawned = 0
        self.zombies_per_wave = 5 + self.wave * 2
        self.spawn_timer = 0
        self.spawn_delay = 3000  # 毫秒
        self.last_spawn_time = pygame.time.get_ticks()
        self.sunlight_timer = 0
        self.sunlight_delay = 5000  # 毫秒
        self.last_sunlight_time = pygame.time.get_ticks()

# 植物类
game_state = GameState()

class Plant:
    def __init__(self, x, y, plant_type):
        self.x = x
        self.y = y
        self.plant_type = plant_type
        self.health = 100
        self.attack_timer = 0
        self.attack_delay = 2000  # 毫秒
        self.last_attack_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE, GRID_SIZE)
        
        # 根据植物类型设置不同属性
        if plant_type == "向日葵":
            self.cost = 50
            self.sunlight_timer = 0
            self.sunlight_delay = 10000  # 毫秒
            self.last_sunlight_time = pygame.time.get_ticks()
        elif plant_type == "豌豆射手":
            self.cost = 100
            self.damage = 20
        
    def update(self):
        if self.plant_type == "向日葵":
            current_time = pygame.time.get_ticks()
            if current_time - self.last_sunlight_time > self.sunlight_delay:
                # 生成阳光
                game_state.sunlight.append(Sunlight(self.x * GRID_SIZE + 20, self.y * GRID_SIZE + 100 + 20))
                self.last_sunlight_time = current_time
        elif self.plant_type == "豌豆射手":
            # 攻击逻辑
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > self.attack_delay:
                self.shoot()
                self.last_attack_time = current_time
        
    def draw(self):
        # 绘制不同类型的植物
        if self.plant_type == "向日葵":
            pygame.draw.rect(screen, YELLOW, self.rect)
            # 在向日葵上画一个太阳图标
            sun_icon = pygame.Rect(self.x * GRID_SIZE + 20, self.y * GRID_SIZE + 100 + 15, 20, 20)
            pygame.draw.circle(screen, (255, 255, 0), sun_icon.center, 10)
        elif self.plant_type == "豌豆射手":
            pygame.draw.rect(screen, GREEN, self.rect)
            # 绘制豌豆射手的嘴
            mouth_rect = pygame.Rect(self.x * GRID_SIZE + 50, self.y * GRID_SIZE + 100 + 25, 10, 10)
            pygame.draw.rect(screen, (0, 150, 0), mouth_rect)
        
    def shoot(self):
        # 检查是否有僵尸在前方
        for zombie in game_state.zombies:
            if zombie.y == self.y and zombie.x > self.x:
                # 创建子弹
                bullet_x = self.x * GRID_SIZE + GRID_SIZE
                bullet_y = self.y * GRID_SIZE + 100 + GRID_SIZE // 2
                game_state.bullets.append(Bullet(bullet_x, bullet_y, self.damage))
                break

# 僵尸类
class Zombie:
    def __init__(self, row):
        self.x = GRID_COLS  # 从屏幕右侧进入
        self.y = row
        self.health = 100
        self.speed = 0.5
        self.damage = 10
        self.attack_timer = 0
        self.attack_delay = 1500  # 毫秒
        self.last_attack_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE + 100, GRID_SIZE, GRID_SIZE)
    
    def update(self):
        # 检查前方是否有植物
        has_plant_in_front = False
        for plant in game_state.plants:
            if plant.y == self.y and plant.x == int(self.x):
                has_plant_in_front = True
                # 攻击植物
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time > self.attack_delay:
                    plant.health -= self.damage
                    self.last_attack_time = current_time
                break
        
        # 如果前方没有植物，则移动
        if not has_plant_in_front:
            self.x -= self.speed / GRID_SIZE
        
        # 更新矩形位置
        self.rect.x = self.x * GRID_SIZE
        self.rect.y = self.y * GRID_SIZE + 100
        
        # 检查是否到达最左侧（游戏结束）
        if self.x < 0:
            game_state.game_over = True
        
        # 检查是否死亡
        if self.health <= 0:
            game_state.zombies.remove(self)
            game_state.score += 10
            game_state.money += 10  # 杀死僵尸获得金钱
    
    def draw(self):
        # 绘制僵尸
        pygame.draw.rect(screen, RED, self.rect)
        # 绘制僵尸的头
        head_rect = pygame.Rect(self.x * GRID_SIZE + 15, self.y * GRID_SIZE + 100 + 10, 30, 30)
        pygame.draw.ellipse(screen, (255, 200, 200), head_rect)
        # 绘制僵尸的眼睛
        pygame.draw.circle(screen, WHITE, (int(self.x * GRID_SIZE + 25), int(self.y * GRID_SIZE + 100 + 20)), 3)
        pygame.draw.circle(screen, WHITE, (int(self.x * GRID_SIZE + 35), int(self.y * GRID_SIZE + 100 + 20)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x * GRID_SIZE + 25), int(self.y * GRID_SIZE + 100 + 20)), 1)
        pygame.draw.circle(screen, BLACK, (int(self.x * GRID_SIZE + 35), int(self.y * GRID_SIZE + 100 + 20)), 1)
        # 绘制僵尸的嘴
        pygame.draw.line(screen, BLACK, (int(self.x * GRID_SIZE + 25), int(self.y * GRID_SIZE + 100 + 35)), 
                         (int(self.x * GRID_SIZE + 35), int(self.y * GRID_SIZE + 100 + 35)), 2)

# 子弹类
class Bullet:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.speed = 3
        self.damage = damage
        self.rect = pygame.Rect(x, y - 5, 10, 10)
    
    def update(self):
        self.x += self.speed
        self.rect.x = self.x
        
        # 检查是否击中僵尸
        for zombie in game_state.zombies:
            if self.rect.colliderect(zombie.rect):
                zombie.health -= self.damage
                if zombie in game_state.zombies:
                    game_state.bullets.remove(self)
                break
        
        # 检查是否超出屏幕
        if self.x > SCREEN_WIDTH:
            if self in game_state.bullets:
                game_state.bullets.remove(self)
    
    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 5)

# 阳光类
class Sunlight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fall_speed = 0.5
        self.value = 25
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)
        self.lifetime = 10000  # 10秒后消失
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self):
        # 缓慢下落
        self.y += self.fall_speed
        self.rect.y = self.y
        
        # 检查是否被玩家点击
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            game_state.money += self.value
            game_state.sunlight.remove(self)
        
        # 检查是否超出屏幕或超时
        current_time = pygame.time.get_ticks()
        if self.y > SCREEN_HEIGHT or current_time - self.spawn_time > self.lifetime:
            if self in game_state.sunlight:
                game_state.sunlight.remove(self)
    
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 15)

# 绘制游戏界面
def draw_game():
    screen.fill(GRAY)
    
    # 绘制网格
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE + 100, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
    
    # 绘制植物选择栏
    select_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
    pygame.draw.rect(screen, (150, 150, 150), select_bar)
    
    # 绘制向日葵选择按钮
    sunflower_btn = pygame.Rect(20, 20, 60, 60)
    pygame.draw.rect(screen, YELLOW, sunflower_btn)
    sunflower_text = font.render("50", True, BLACK)
    screen.blit(sunflower_text, (40, 85))
    # 绘制向日葵图标
    pygame.draw.circle(screen, (255, 255, 0), (50, 50), 20)
    
    # 绘制豌豆射手选择按钮
    peashooter_btn = pygame.Rect(100, 20, 60, 60)
    pygame.draw.rect(screen, GREEN, peashooter_btn)
    peashooter_text = font.render("100", True, BLACK)
    screen.blit(peashooter_text, (110, 85))
    # 绘制豌豆射手图标
    pygame.draw.rect(screen, (0, 150, 0), (110, 30, 40, 40))
    pygame.draw.rect(screen, (0, 100, 0), (140, 50, 10, 10))
    
    # 显示当前金钱
    money_text = font.render(f"金钱: {game_state.money}", True, YELLOW)
    screen.blit(money_text, (SCREEN_WIDTH - 200, 20))
    
    # 显示当前分数
    score_text = font.render(f"分数: {game_state.score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 200, 60))
    
    # 显示当前波数
    wave_text = font.render(f"第 {game_state.wave} 波", True, WHITE)
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - 50, 20))
    
    # 绘制选中的植物提示
    if game_state.selected_plant:
        plant_name = game_state.selected_plant
        hint_text = font.render(f"已选择: {plant_name}", True, WHITE)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 80, 60))
    
    # 绘制植物
    for plant in game_state.plants:
        plant.draw()
    
    # 绘制僵尸
    for zombie in game_state.zombies:
        zombie.draw()
    
    # 绘制子弹
    for bullet in game_state.bullets:
        bullet.draw()
    
    # 绘制阳光
    for sun in game_state.sunlight:
        sun.draw()
    
    # 绘制游戏结束界面
    if game_state.game_over:
        game_over_bg = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        pygame.draw.rect(screen, BLACK, game_over_bg)
        pygame.draw.rect(screen, RED, game_over_bg, 5)
        
        game_over_text = font.render("游戏结束!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 3 + 30))
        
        final_score_text = font.render(f"最终分数: {game_state.score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 3 + 80))
        
        restart_text = font.render("按R键重新开始", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 130))

# 检查网格位置是否可以种植植物
def can_plant(x, y):
    # 检查是否在有效网格内
    if x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS:
        return False
    
    # 检查该位置是否已有植物
    for plant in game_state.plants:
        if plant.x == x and plant.y == y:
            return False
    
    return True

# 生成僵尸
def spawn_zombies():
    current_time = pygame.time.get_ticks()
    if (game_state.zombies_spawned < game_state.zombies_per_wave and 
        current_time - game_state.last_spawn_time > game_state.spawn_delay):
        # 随机选择一行生成僵尸
        row = random.randint(0, GRID_ROWS - 1)
        game_state.zombies.append(Zombie(row))
        game_state.zombies_spawned += 1
        game_state.last_spawn_time = current_time
    
    # 检查是否完成当前波次
    if game_state.zombies_spawned >= game_state.zombies_per_wave and len(game_state.zombies) == 0:
        # 进入下一波
        game_state.wave += 1
        game_state.zombies_spawned = 0
        game_state.zombies_per_wave = 5 + game_state.wave * 2
        game_state.spawn_delay = max(1000, 3000 - game_state.wave * 100)  # 波次越高，生成越快
        game_state.money += 50  # 波次奖励

# 随机生成阳光
def spawn_sunlight():
    current_time = pygame.time.get_ticks()
    if current_time - game_state.last_sunlight_time > game_state.sunlight_delay:
        # 随机位置生成阳光
        x = random.randint(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE)
        game_state.sunlight.append(Sunlight(x, 100))
        game_state.last_sunlight_time = current_time

# 主游戏循环
def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN and not game_state.game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # 检查是否点击了植物选择按钮
                if 20 <= mouse_x <= 80 and 20 <= mouse_y <= 80:
                    # 向日葵按钮
                    if game_state.money >= 50:
                        game_state.selected_plant = "向日葵"
                elif 100 <= mouse_x <= 160 and 20 <= mouse_y <= 80:
                    # 豌豆射手按钮
                    if game_state.money >= 100:
                        game_state.selected_plant = "豌豆射手"
                elif mouse_y >= 100:
                    # 检查是否在网格上点击，并且已选择植物
                    grid_x = mouse_x // GRID_SIZE
                    grid_y = (mouse_y - 100) // GRID_SIZE
                    
                    if can_plant(grid_x, grid_y) and game_state.selected_plant:
                        # 创建植物
                        new_plant = Plant(grid_x, grid_y, game_state.selected_plant)
                        if game_state.money >= new_plant.cost:
                            game_state.plants.append(new_plant)
                            game_state.money -= new_plant.cost
                            game_state.selected_plant = None
            
            # 键盘事件
            if event.type == pygame.KEYDOWN:
                # R键重新开始游戏
                if event.key == pygame.K_r and game_state.game_over:
                    # 重置游戏状态
                    game_state.__init__()
        
        if not game_state.game_over:
            # 更新植物
            for plant in game_state.plants:
                plant.update()
                # 移除死亡的植物
                if plant.health <= 0:
                    game_state.plants.remove(plant)
            
            # 更新僵尸
            for zombie in game_state.zombies:
                zombie.update()
            
            # 更新子弹
            for bullet in game_state.bullets:
                bullet.update()
            
            # 更新阳光
            for sun in game_state.sunlight:
                sun.update()
            
            # 生成僵尸
            spawn_zombies()
            
            # 随机生成阳光
            spawn_sunlight()
        
        # 绘制游戏
        draw_game()
        
        # 刷新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)

if __name__ == "__main__":
    main()