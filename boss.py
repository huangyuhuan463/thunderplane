import pygame
class Boss():
	"""表示单个Boss的类"""
	
	def __init__(self, ai_settings, screen):
		"""初始化Boss并设置他的起始位置"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#加载Boss图像,并设置其rect属性
		self.image = pygame.image.load('images/boss.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()#导入screen对象来放置boss
		
		#每个Boss最初都在屏幕左上角附近
		self.rect.centerx = self.screen_rect.centerx + 100
		self.rect.top = self.screen_rect.top
		
		#存储Boss的准确位置
		self.center = float(self.rect.centerx)
		
	def blitme(self):
		"""在指定位置绘制外Boss"""
		self.screen.blit(self.image, self.rect)
		
	def check_edges(self):
		"""如果Boss位于屏幕边缘,就返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		
	def update(self):
		"""向左或向右移动Boss"""
		self.center += (self.ai_settings.boss_speed_factor*
		                self.ai_settings.boss_fleet_direction)
		self.rect.centerx = self.center
		
	

