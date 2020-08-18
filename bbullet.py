import pygame
from pygame.sprite import Sprite

class BBullet(Sprite):
	"""boss子弹类"""
	def __init__(self, ai_settings, screen, boss):
		super().__init__()
		self.screen = screen
		
		#在(0,0)处创建一个表示子弹的矩形,再设置正确的位置
		self.rect = pygame.Rect(0,0,ai_settings.bbullet_width, ai_settings.bbullet_height)
		self.rect.centerx = boss.rect.centerx
		self.rect.bottom = boss.rect.bottom
		
		#存储用小数表示的子弹位置
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bbullet_color
		self.speed_factor = ai_settings.bbullet_speed_factor
		
	def update(self):
		"""向下移动子弹"""
		self.y += self.speed_factor
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""屏幕上绘制子弹"""
		pygame.draw.rect(self.screen, self.color, self.rect)
