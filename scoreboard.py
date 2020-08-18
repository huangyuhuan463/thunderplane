import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""显示得分信息的类"""
	
	def __init__(self, ai_settings, screen, stats):
		"""初始化显示得分涉及的属性"""
		self.screen  = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#显示得分信息时使用的字体设置
		self.text_color = (0, 0, 255)
		self.blood_color = (255, 0, 255)
		self.font = pygame.font.SysFont('arial', 36)
		
		#准备包含最高得分和当前得分
		#大招进度和boss血量的图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		self.prep_dazhaoprocess()		 	
		self.prep_bossblood()
		
	def prep_score(self):
		"""将得分转换为一张渲染的图像"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color)
		
		# 将得分放在屏幕左上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def show_score(self, stats, ai_settings):
		"""在屏幕上显示飞船和得分"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.screen.blit(self.process_image, self.process_rect)
		if stats.level >= ai_settings.boss_level:  #当关数大到达boss关数才绘制血量
			 self.screen.blit(self.blood_image, self.blood_rect)			
		#绘制飞船
		self.ships.draw(self.screen)
		
	def prep_high_score(self):
		"""将最高得分转换为渲染的图像"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "High Score: " + "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color)
		
		# 将最高得分放在屏幕顶部中央
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
		
	def prep_level(self):
		"""将等级转换为渲染的图像"""
		self.level_image = self.font.render("Level: " + str(self.stats.level), True, self.text_color)
		
		# 将等级放在得分下方
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
		
	def prep_ships(self):
		"""显示还有多少飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
			
	def prep_dazhaoprocess(self):
		"""显示大招进度"""
		process = str(self.stats.dazhao) + "%"
		self.process_image = self.font.render(process, True, self.text_color)
		
		# 将进度放在飞船下面
		self.process_rect = self.process_image.get_rect()
		self.process_rect.left = self.screen_rect.left + 15
		self.process_rect.top = 80
		
	def prep_bossblood(self):
		"""显示boss的血量"""
		blood = "blood: " + str(self.stats.boss_blood)
		self.blood_image = self.font.render(blood, True, self.blood_color)
		
		# 将血量放在等级下面
		self.blood_rect = self.blood_image.get_rect()
		self.blood_rect.right = self.level_rect.right
		self.blood_rect.top = self.level_rect.bottom + 10
