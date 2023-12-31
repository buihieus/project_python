#các thư viện được sử dụng
import random
import pygame 
import sys
# Define colors: định dạng màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLUE = (0, 0, 255)

# Define cell size and game window size: Xác định kích thước ô và kích thước cửa sổ trò chơi:
CELL_SIZE = 40
WINDOW_WIDTH = 8 * CELL_SIZE
WINDOW_HEIGHT = 8 * CELL_SIZE


# khỏi tạo lớp Minesweeper
class Minesweeper:
    # là phương thức khởi tạo của lớp
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.mines = set() #lưu trữ mìn trên bảng
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]#Theo dõi ô được mở
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]#theo dõi ô được đánh dấu là mìn

    # Initialize Pygame: Khởi tạo Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        
    #Phương thức này trả về danh sách các ô kề cạnh một ô (row, col) trên bảng trò chơi
    def get_adjacent_cells(self, row, col):
        adjacent_cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row = row + i
                new_col = col + j
                if self.is_valid(new_row, new_col):
                    adjacent_cells.append((new_row, new_col))
        return adjacent_cells
    
    # đặt ngẫu nhiên các quả mìn 
    def place_mines(self, start_row, start_col):
        excluded_cells = self.get_adjacent_cells(start_row, start_col)
        excluded_cells.append((start_row, start_col))
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in excluded_cells:
                self.mines.add((row, col))
                
    
    #thuật toán loang    
    def flood_fill(self, board, row, col, revealed):
        rows = len(board)
        cols = len(board[0])

        if row < 0 or row >= rows or col < 0 or col >= cols or revealed[row][col]:
            return

        revealed[row][col] = True

        if board[row][col] != 0:
            return

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                ni = row + dx
                nj = col + dy
                if 0 <= ni < rows and 0 <= nj < cols:
                    self.flood_fill(board, ni, nj, revealed)
                    
    #Phương thức này được sử dụng để kiểm tra xem một tọa độ ô (row, col) 
    # có hợp lệ trên bảng trò chơi hay không
    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols                
    
    #Phương thức này được sử dụng để đếm số lượng mìn kề cạnh ô (row, col) trên bảng trò chơi
    def count_adjacent_mines(self, row, col):
        count = 0
        adjacent_cells = self.get_adjacent_cells(row, col)
        for cell in adjacent_cells:
            if cell in self.mines:
                count += 1
        return count
 
    # phương thức trong lớp Minesweeper và được sử dụng để tiết lộ một ô cụ thể 
    # trong trò chơi Minesweeper và thực hiện các hành động liên quan đến việc tiết lộ ô đó.
    def reveal_cell(self, row, col):
        if not self.is_valid(row, col) or self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        if (row, col) in self.mines:
            self.board[row][col] = '*'
        else:
            count = self.count_adjacent_mines(row, col)
            self.board[row][col] = str(count) if count > 0 else ' '
            if count == 0:
                adjacent_cells = self.get_adjacent_cells(row, col)
                for cell in adjacent_cells:
                    self.reveal_cell(cell[0], cell[1])
                    
                revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]# theo dõi trạng thái tiết lộ ô
                self.flood_fill(self.board, row, col, revealed)# tiết lộ các ô trống liền kề
                  
           
    def choose_greedy_move(self):
        rows = self.rows
        cols = self.cols
        min_mines = float('inf')
        chosen_row, chosen_col = -1, -1

        for i in range(rows):
            for j in range(cols):
                if not self.revealed[i][j] and self.board[i][j] != '*':
                    count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ni = i + dx
                            nj = j + dy
                            if 0 <= ni < rows and 0 <= nj < cols and self.board[ni][nj] == '*':
                                count += 1
                    if count < min_mines:
                        min_mines = count
                        chosen_row = i#thuat toan tham lam  
                        chosen_col = j

        return chosen_row, chosen_col
    
   #chuyển đổi trạng thái từ ô đã đánh dấu và ngược lại 
    def toggle_flag(self, row, col):
        if not self.is_valid(row, col) or self.revealed[row][col]:
            return
        self.flagged[row][col] = not self.flagged[row][col]
    #
    def show_message(self, title, message):
        pygame.display.set_caption(title)  # Đặt tiêu đề cửa sổ
        font = pygame.font.Font(None, 36)  # Định dạng font chữ
        text = font.render(message, True, (0, 0, 0))  # Tạo đối tượng văn bản
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # Vị trí văn bản
        self.screen.fill(WHITE)  # Xóa màn hình với màu trắng
        self.screen.blit(text, text_rect)  # Vẽ văn bản lên màn hình
        pygame.display.flip()  # Cập nhật màn hình
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        
    #khởi tạo phương thức play 
    def play(self):
        #tạo vị trí ngẫu nhiên để đặt mìn
        start_row = random.randint(0, self.rows - 1)
        start_col = random.randint(0, self.cols - 1)
        self.place_mines(start_row, start_col)
        # vòng lặp chính để chơi trò chơi
        game_over = False
        while not game_over:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // CELL_SIZE
                        row = pos[1] // CELL_SIZE
                        if not self.revealed[row][col]:
                            if (row, col) in self.mines:
                                print("Game over! You hit a mine.")
                                self.draw_board()  # Vẽ lại bảng trò chơi trước khi hiển thị thông báo
                                self.show_message("Game Over", "You lost!")  # Hiển thị thông báo thua
                                game_over = True
                                self.reveal_board()
                                game_over = True
                            else:
                                self.reveal_cell(row, col)
                                if self.check_win():
                                    if self.check_win():
                                        self.draw_board()  # Vẽ lại bảng trò chơi trước khi hiển thị thông báo
                                        self.show_message("Congratulations!", "You won!")  # Hiển thị thông báo chiến thắng
                                        game_over = True
                                        print("Congratulations! You won!")
                                        game_over = True
                    elif event.button == 3:  # Right mouse button
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // CELL_SIZE
                        row = pos[1]// CELL_SIZE
                        self.toggle_flag(row, col)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Người chơi nhấn phím "h" để yêu cầu gợi ý
                        chosen_row, chosen_col = self.choose_greedy_move()
                        if chosen_row != -1 and chosen_col != -1:
                            self.reveal_cell(chosen_row, chosen_col)
                        
    #thực hiện việc vẽ bảng trò chơi và các ô trạng thái tương ứng lên giao diện đồ họa.
    def draw_board(self):
        self.screen.fill(GRAY)  # Màu nền xám cho các ô chưa mở
        for row in range(self.rows):
            for col in range(self.cols):
                cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[row][col]:
                    pygame.draw.rect(self.screen, WHITE, cell_rect)  # Màu nền trắng cho các ô đã mở
                    pygame.draw.rect(self.screen, BLACK, cell_rect, 1)
                    if self.board[row][col] == '*':
                        pygame.draw.circle(self.screen, BLUE,
                                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                        CELL_SIZE // 4)
                    else:
                        font = pygame.font.SysFont(None, 24)
                        text = font.render(self.board[row][col], True, BLACK)
                        text_rect = text.get_rect(
                            center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                        self.screen.blit(text, text_rect)
                elif self.flagged[row][col]:
                    pygame.draw.rect(self.screen, BLUE, cell_rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, cell_rect)
                    pygame.draw.rect(self.screen, BLACK, cell_rect, 1)
        pygame.display.flip()
        
    # hiển thị toàn bộ bảng trò chơi( bằng cách tiết lộ tất cả các ô)       
    def reveal_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.revealed[row][col] = True
                
    #Phương thức này được sử dụng để kiểm tra xem người chơi đã chiến thắng trò chơi hay chưa
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and (row, col) not in self.mines:
                    return False
        return True

minesweeper = Minesweeper(8, 8, 5)
minesweeper.play()