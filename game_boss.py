import sys
import tkinter.messagebox
from time import sleep

import pygame
from bullet import Bullet
from bbullet import BBullet
from boss import Boss

def update_bullets(ai_settings, screen, stats, sb, ship, boss, bullets, play_button, bbulets):
	"""更新子弹位置，并删除已经消失的子弹"""
	#更新子弹位置
	bullets.update()
	bbulets.update()
		
	#删除以消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	#删除boss消失的子弹
	for bbulet in bbulets.copy():
		if bbulet.rect.top >= ai_settings.screen_height:
			bbulets.remove(bbulet)
			
	check_bullet_boss_collisions(ai_settings, screen, stats, sb, ship, boss, bullets, play_button, bbulets)
	
def check_bullet_boss_collisions(ai_settings, screen, stats, sb, ship, boss, bullets, play_button, bbulets):
	"""响应子弹和外星人的碰撞"""
	#删除发生碰撞的子弹和boss
	collisions = pygame.sprite.spritecollide(boss, bullets, True)
	if collisions:
		if ai_settings.bullet_width < 10:
			#对应普通子弹和大招1 
			stats.boss_blood -= 100 #血量减50
			stats.score += ai_settings.boss_points #记分
		elif ai_settings.bullet_width > 10 and ai_settings.bullet_width < 1000:
			#对应大招2
			stats.boss_blood -= 500
			stats.score += ai_settings.boss_points * 3 #记分
		stats.dazhao += 10 #大招进度加10
		if(stats.dazhao >= 300):
			stats.dazhao = 300			
		sb.prep_score()
		sb.prep_dazhaoprocess()
		sb.prep_bossblood()
		check_high_score(stats, sb)
	if stats.boss_blood <= 0:
		bullets.empty()
		bbulets.empty()
		stats.game_active = False
		tkinter.messagebox.showinfo('提示','恭喜你! 游戏通关')
		tkinter.messagebox.showinfo('提示','按下play可以重新开始')
		play_button.draw_button()
		pygame.mouse.set_visible(True)				

def check_high_score(stats, sb):
	"""检查是否诞生了新的最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def update_boss(ai_settings, stats, sb, screen, ship, boss, bullets, bbulets, flag):
	"""检查是否有boss位于屏幕边缘,并更新boss位置"""
	check_fleet_edges(ai_settings, boss)
	boss.update()
	
	if flag[4]: # 1秒boss发射子弹一次
		new_bullet = BBullet(ai_settings, screen, boss)
		bbulets.add(new_bullet)
		s2 = pygame.mixer.Sound('music/music2.ogg') #播放音乐
		s2.play()
		pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
		flag[4] = 0
	#如果boss发射的子弹碰到飞船	
	if pygame.sprite.spritecollide(ship, bbulets, True):
		ship_hit(ai_settings, stats, sb, screen, ship, boss, bullets)	
	
def check_fleet_edges(ai_settings, boss):
	"""有boss到达边缘时采取相应的措施"""
	if boss.check_edges():
		ai_settings.boss_fleet_direction *= -1
		
def ship_hit(ai_settings, stats, sb, screen, ship, boss, bullets):
	"""响应被外星人子弹击中的飞船"""
	if stats.ships_left > 0:
		#将ships_left减1
		stats.ships_left -= 1
		
		# 更新记分牌
		sb.prep_ships()
		
		bullets.empty()
		ship.center_ship()
	
		#暂停
		sleep(0.5)
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		tkinter.messagebox.showinfo('提示','你输了,按Play重新开始')
