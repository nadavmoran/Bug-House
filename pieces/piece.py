class Piece:
    '''
    Father class for a piece for the gui
    '''
    def __init__(self, img, pos, color):
        self.pos = pos
        self.img = img.convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = self.pos
        self.color = color


    def set_piece(self, pos, game_display):
        '''
        changes the position of a piece
        :param pos:
        :param game_display:
        :return:
        '''
        self.pos = pos
        self.rect.center = pos
        game_display.blit(self.img, self.rect)