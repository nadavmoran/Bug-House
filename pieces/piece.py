class Piece:
    def __init__(self, img, pos, color):
        self.pos = pos
        self.img = img.convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = self.pos
        self.color = color

    def set_piece(self, pos, game_display):
        self.pos = pos
        self.rect.center = pos
        game_display.blit(self.img, self.rect)
