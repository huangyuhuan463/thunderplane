import sys
import tkinter.messagebox
from time import sleep

import pygame
from bullet import Bullet
from bbullet import BBullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, aliens, sb, stats, bullets, flag):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_e:
		if(stats.dazhao > 100):
			put_dazhao(ai_settings, sb, stats, bullets)
			pygame.time.set_timer(pygame.USEREVENT, 5000)
	elif event.key == pygame.K_r:
		if(stats.dazhao > 200):
			put_dazhao1(ai_settings, sb, stats)
			pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
	elif event.key == pygame.K_t:
		if(stats.dazhao == 300):
			flag[2] = 0
			put_dazhao2(ai_settings, screen, sb, stats, bullets, aliens, ship)
			stats.boss_blood -= 5000 #大招3直接扣5000血量
			sb.prep_bossblood() # 更新boss血量
			ai_settings.bullet_width = 3
				
	
def put_dazhao(ai_settings, sb, stats, bullets):
	"""放100%大招"""
	stats.dazhao -= 100 #进度条减100
	sb.prep_dazhaoprocess()# 更新进度条
	ai_settings.bullets_allowed = 100# 允许无限发子弹
	
def put_dazhao1(ai_settings, sb, stats):
	"""放200%大招"""
	stats.dazhao -= 200 #进度条减200
	sb.prep_dazhaoprocess() #更新进度条
	ai_settings.bullets_allowed = 100# 允许无限发子弹
	ai_settings.bullet_width = 300# 子弹宽度变为300
	
def put_dazhao2(ai_settings, screen, sb, stats, bullets, aliens, ship):
	"""放300%大招"""
	ai_settings.bullet_width = 5000
	for i in range(1,4):
		fire_bullet(ai_settings, screen, ship, bullets)
	stats.dazhao = 0
	sb.prep_dazhaoprocess()# 更新进度条

def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果还没有到达限制,就发射一颗子弹"""
	#创建一颗子弹,并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		s = pygame.mixer.Sound('music/music1.ogg')
		s.play()
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
def check_keyup_events(event, ship):
	"""响应松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, flag, bbulets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			
			#检测事件KEYDOWN，按下键盘
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, ai_settings, screen, ship, aliens, sb, stats, bullets, flag)		
				
			
			#玩家响应KEYUP事件，松开右键转为false		
			elif event.type == pygame.KEYUP:
				check_keyup_events(event, ship)
				
			#玩家按下play, 启动游戏	
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets, mouse_x, mouse_y, bbulets)
			
			#当大招5秒后, 停止100%大招	
			elif event.type == pygame.USEREVENT:
				ai_settings.bullets_allowed = 3	
			
			#当大招5秒后, 停止200%大招	
			elif event.type == pygame.USEREVENT + 1:
				ai_settings.bullets_allowed = 3
				ai_settings.bullet_width = 3
			
			#boss 1秒发射一次子弹,1秒后开关置1	
			elif event.type == pygame.USEREVENT + 2:
				flag[4] = 1
												
				
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bbulets):
	"""在玩家单击Play按钮时开始新游戏"""
	button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_click and not stats.game_active:
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		bbulets.empty()
		
		# 创建一群新的外星人,并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# 弹出提示框
		tkinter.messagebox.showinfo('提示','按下键盘左右操纵飞船,空格射击')
		tkinter.messagebox.showinfo('提示','退出按q键')      	        
				
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, background, boss, bbulets):
	"""更新屏幕上的图像,并切换到新屏幕"""
	# 每次循环时都重绘图片
	screen.blit(background, (0,0))
	
	# 在飞船和外星人后面重绘子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	for bbullet in bbulets.sprites():
		bbullet.draw_bullet()
	ship.blitme()#让飞船处在底部中间
	if stats.level < ai_settings.boss_level:	
		aliens.draw(screen)
	else:
		boss.blitme()
	
	# 显示得分
	sb.show_score(stats, ai_settings)
	
	# 如果游戏处于非活动状态,就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()
		
	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, flag):
	"""更新子弹位置，并删除已经消失的子弹"""
	#更新子弹位置
	bullets.update()
		
	#删除以消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, flag)	
		
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, flag):
	"""响应子弹和外星人的碰撞"""
	#删除发生碰撞的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	# 如果使用大招杀的外星人不加点数
	if collisions and flag[2]:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			stats.dazhao += 5 * len(aliens) # 杀死一个外星人获得5%的大招进度
			if(stats.dazhao >= 300):
				stats.dazhao = 300			
			sb.prep_score()
			sb.prep_dazhaoprocess()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#删除现有的子弹,加快游戏节奏,并创建一群新的外星人
		bullets.empty()
		ai_settings.increase_speed()
		
		#提高等级
		stats.level += 1
		sb.prep_level()
		
		flag[2] = 1	
		
		create_fleet(ai_settings, screen, ship, aliens)
	
			
def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width +2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	#创建一个外星人群，并计算每行可容纳多少个外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
			 row_number)
			 
def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移,并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 0:
		#将ships_left减1
		stats.ships_left -= 1
		
		# 更新记分牌
		sb.prep_ships()
	
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
	
		#创建一群新的外星人,并将飞船放到屏幕中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#暂停
		sleep(0.5)
	
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		tkinter.messagebox.showinfo('提示','你输了,按Play重新开始')
	
def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""检查是否由外星人到达了屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样显示处理
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""检查是否有外星人位于屏幕边缘,并更新整群外星人位置"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
	# 检查是否有外星人到达屏幕底端
	check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
def check_high_score(stats, sb):
	"""检查是否诞生了新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def music_run():
	"""开启音乐"""
	pygame.mixer.init()
	pygame.time.delay(1000)
	pygame.mixer.music.load('music/music.mp3')
	pygame.mixer.music.play(-1)
	
def check_message(stats, flag, ai_settings):
	"""检查提示框是否触发"""
	if stats.level == 2 and flag[0]:
		# 弹出提示框
		tkinter.messagebox.showinfo('提示','当左上角数值满100时按e键放大招')
		flag[0] = 0
			
	if stats.level == 3 and flag[1]:
		# 弹出提示框
		tkinter.messagebox.showinfo('提示','大招也有很多等级')
		tkinter.messagebox.showinfo('提示','当左上角数值满200时试试看按r键,满300按t键')
		flag[1] = 0	
		
	if stats == ai_settings.boss_level and flag[5]:
		tkinter.messagebox.showinfo('提示','开始boss战!')
		tkinter.messagebox.showinfo('提示','注意看好时机躲避boss的子弹')
		tkinter.messagebox.showinfo('提示','利用你的武器狠狠的削他吧!')
		flag[5] = 0	
		
