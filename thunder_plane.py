import pygame
import tkinter.messagebox

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
from boss import Boss
from pygame.sprite import Group
from button import Button
import game_functions as gf
import game_boss as gb

def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init() #初始化背景设置
	gf.music_run() #开启音乐
	ai_settings = Settings() #创建设置类对象
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height)) #设置分辨率
	pygame.display.set_caption("thunder plane") #设置标题
	
	background = pygame.image.load('images/timg.jpg').convert()# 设置背景图片
	
	# 创建Play按钮
	play_button = Button(ai_settings, screen, "Play")
	
	#创建一个用于存储游戏统计信息的实例,并创建记分牌
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#创建一艘飞船，一个子弹编组和一个外星人编组
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	bbulets = Group()
	boss = Boss(ai_settings, screen)
	
	# 标志信息0,1,5为提示框提示开关
	# 标志信息2为大招2不加点数开关
	# 标志信息3是给boss血量初始化开关
	# 标志信息4是boss每隔几秒发射子弹开关
	flag = [1 ,1, 1, 1, 1, 1]
	
	
	#创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#开始游戏主循环
	while True:
		
		#监视键盘和鼠标事件
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, flag, bbulets)
		
		#检查提示框是否触发
		gf.check_message(stats, flag, ai_settings)		
		
		if stats.game_active and stats.level < ai_settings.boss_level: 
			#根据移动标志调整飞船的位置
			ship.update()
			#更新子弹位置，并删除已经消失的子弹
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, flag)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
		
		#如果到达相应的级别触发boss站	
		if stats.game_active and stats.level == ai_settings.boss_level:
			aliens.empty()
			#根据移动标志调整飞船的位置
			ship.update()
			#更新子弹位置，并删除已经消失的子弹
			if flag[3]:
				stats.boss_blood = 10000 #重新给boss赋值
				flag[3] = 0
			gb.update_bullets(ai_settings, screen, stats, sb, ship, boss, bullets, play_button, bbulets)
			gb.update_boss(ai_settings, stats, sb, screen, ship, boss, bullets, bbulets, flag)
		

		
		#更新屏幕上的图像,并切换到新屏幕
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, background, boss, bbulets)
	
run_game()
