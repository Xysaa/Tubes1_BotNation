from typing import Optional, List, Tuple

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from time import sleep

class BotNation(BaseLogic):
    """
    Bot strategis yang fokus pada area sekitar base.
    Mengumpulkan diamond terdekat dan kembali ketika inventory mencapai batas.
    """
    
    def __init__(self):
        # Radius maksimum pencarian dari base
        self.search_radius = 7

    def next_move(self, board_bot: GameObject, board: Board):
        """Method utama untuk pengambilan keputusan pergerakan bot"""
        self.game_board = board
        self.player = board_bot

        # Cek waktu darurat - kurang dari 2 detik tersisa
        if (self.player.properties.milliseconds_left // 1000 < 2):
            print("OH NOOOOOOO")

        # Kembali ke base jika waktu hampir habis
        if (self.player.properties.milliseconds_left // 1000 <= self.calc_teleport_dist(self.player.position, self.player.properties.base) + 2):
            print("byee zzz")
            return self.head_to_base()

        # Ambil diamond dalam area pencarian
        nearby_gems = self.get_gems_in_radius(self.search_radius)
        if len(nearby_gems) == 0:
            nearby_gems = self.get_gems_in_radius(self.search_radius + 2)

        if len(nearby_gems) == 0:
            return self.move_to_center()
        
        # Kasus khusus hanya ada 2 diamond
        if len(nearby_gems) == 2:
            closest_gem = min(nearby_gems, key=lambda gem: self.calc_teleport_dist(self.player.position, gem.position))
            return self.nav_with_teleport(closest_gem.position)

        # Cari diamond dalam jangkauan 
        all_gems = self.game_board.diamonds
        gems_one_step = self.find_gems_within_steps(1, all_gems)
        gems_two_steps = self.find_gems_within_steps(2, all_gems)
        
        # Filter berdasarkan kapasitas inventory
        gems_one_step = list(filter(lambda gem: self.player.properties.diamonds + gem.properties.points < self.player.properties.inventory_size, gems_one_step))
        gems_two_steps = list(filter(lambda gem: self.player.properties.diamonds + gem.properties.points < self.player.properties.inventory_size, gems_two_steps))

        # Prioritaskan diamond dalam satu langkah
        if len(gems_one_step) > 0:
            # Pilih diamond bernilai tinggi (2 poin) terlebih dahulu
            for gem in gems_one_step:
                if (gem.properties.points == 2):
                    return self.nav_with_teleport(gem.position)
                
            optimal_gem = min(gems_one_step, key=lambda gem: self.calc_avg_gem_dist(gem.position, nearby_gems))
            return self.nav_with_teleport(optimal_gem.position)
        
        # Cek diamond dalam dua langkah
        elif len(gems_two_steps) > 0:
            # Pilih diamond bernilai tinggi (2 poin) terlebih dahulu
            for gem in gems_two_steps:
                if (gem.properties.points == 2):
                    return self.nav_with_teleport(gem.position)
                
            optimal_gem = min(gems_two_steps, key=lambda gem: self.calc_avg_gem_dist(gem.position, nearby_gems))
            return self.nav_with_teleport(optimal_gem.position)
        
        # Logika keputusan untuk kembali ke base
        if (self.player.properties.diamonds >= self.player.properties.inventory_size - 1):
            return self.head_to_base()
        elif (self.calc_teleport_dist(self.player.position, self.player.properties.base) <= 2 and self.player.properties.diamonds >= 3):
            return self.head_to_base()
        elif (self.calc_teleport_dist(self.player.position, self.player.properties.base) <= 1 and self.player.properties.diamonds >= 1):
            return self.head_to_base()
        
        # Cari posisi optimal dengan jarak rata-rata minimum ke diamond
        optimal_pos = self.find_best_adjacent_pos(self.player.position, nearby_gems)
        print(f"OTEWE KE {optimal_pos}")
        return self.nav_with_teleport(optimal_pos)
    
    def get_teleport_pair(self) -> Tuple[GameObject, GameObject]:
        """Mengambil kedua objek teleporter dari papan permainan"""
        teleports = [obj for obj in self.game_board.game_objects if obj.type == "TeleportGameObject"]
        if len(teleports) != 2:
            return None, None
        return teleports[0], teleports[1]
    
    def get_nearest_teleport(self):
        """Mencari teleporter yang paling dekat dengan posisi saat ini"""
        curr_pos = self.player.position
        tp1, tp2 = self.get_teleport_pair()
        nearest_tp = tp1 if (self.calc_manhattan_dist(curr_pos, tp1.position) < self.calc_manhattan_dist(curr_pos, tp2.position)) else tp2
        return nearest_tp
    
    def calc_manhattan_dist(self, pos_a: Position, pos_b: Position) -> int:
        """Menghitung jarak Manhattan antara dua posisi"""
        dx = abs(pos_a.x - pos_b.x)
        dy = abs(pos_a.y - pos_b.y)
        return dx + dy

    def calc_teleport_dist(self, pos_a: Position, pos_b: Position) -> int:
        """Menghitung jarak terpendek dengan mempertimbangkan penggunaan teleporter"""
        tp1, tp2 = self.get_teleport_pair()
        
        nearest_tp = tp1 if (self.calc_manhattan_dist(pos_a, tp1.position) < self.calc_manhattan_dist(pos_a, tp2.position)) else tp2
        other_tp = tp1 if (self.calc_manhattan_dist(pos_a, tp1.position) > self.calc_manhattan_dist(pos_a, tp2.position)) else tp2

        dist_to_tp = self.calc_manhattan_dist(pos_a, nearest_tp.position)
        tp_to_dest = self.calc_manhattan_dist(other_tp.position, pos_b)

        direct_dist = self.calc_manhattan_dist(pos_a, pos_b)

        return min(direct_dist, dist_to_tp + tp_to_dest)
    
    def nav_to_target(self, target: Position) -> Tuple[int, int]:
        """Navigasi menuju target tanpa mempertimbangkan teleporter"""
        dx = target.x - self.player.position.x
        dy = target.y - self.player.position.y
        
        move_dir = (0, 0)

        if abs(dx) > abs(dy):
            move_dir = (1 if dx > 0 else -1, 0)
        else:
            move_dir = (0, 1 if dy > 0 else -1)   

        curr_pos = self.player.position  

        # Cek batas area
        within_bounds = (curr_pos.x + move_dir[0] >= 0 and 
                        curr_pos.y + move_dir[1] >= 0 and 
                        curr_pos.x + move_dir[0] < self.game_board.width + 1 and 
                        curr_pos.y + move_dir[1] < self.game_board.height + 1)

        if within_bounds:
            return move_dir
        else:
            return (move_dir[0] * (-1), move_dir[1] * (-1))
    
    def nav_with_teleport(self, target: Position) -> Tuple[int, int]:
        """Navigasi menuju target dengan mempertimbangkan optimasi teleporter"""
        curr_pos = self.player.position

        if (self.calc_teleport_dist(curr_pos, target) == self.calc_manhattan_dist(curr_pos, target)):
            return self.nav_to_target(target)
        elif (self.calc_teleport_dist(curr_pos, target) < self.calc_manhattan_dist(curr_pos, target)):
            nearest_tp = self.get_nearest_teleport()
            return self.nav_to_target(nearest_tp.position)
        
    def head_to_base(self) -> Tuple[int, int]:
        """Navigasi kembali ke base rumah"""
        return self.nav_with_teleport(self.player.properties.base)
    
    def move_to_center(self) -> Tuple[int, int]:
        """Bergerak menuju pusat papan"""
        center_pos = Position(self.game_board.height // 2, self.game_board.width // 2)
        return self.nav_with_teleport(center_pos)
    
    def get_opponents(self) -> list[GameObject]:
        """Mendapatkan daftar semua bot musuh"""
        opponents = self.game_board.bots
        opponents.remove(self.player)
        return opponents
    
    def find_nearest_opponent(self) -> GameObject:
        """Mencari bot musuh yang paling dekat"""
        nearest = None
        min_dist = 30

        enemies = self.get_opponents()
        for enemy in enemies:
            enemy_dist = self.calc_teleport_dist(self.player.position, enemy.position)
            if enemy_dist < min_dist:
                min_dist = enemy_dist
                nearest = enemy
        return nearest
    
    def get_bot_idx(self, target_bot: GameObject) -> int:
        """Mendapatkan indeks bot tertentu dalam daftar bot"""
        bots = self.game_board.bots
        for i in range(len(bots)):
            if bots[i] == target_bot:
                return i
            
    def get_gems_in_radius(self, radius):
        """Mendapatkan semua diamond dalam radius tertentu dari base"""
        gems = self.game_board.diamonds
        return list(filter(lambda gem: self.calc_teleport_dist(gem.position, self.player.properties.base) <= radius, gems))
    
    def calc_avg_gem_dist(self, pos: Position, gems: list[GameObject]):
        """Menghitung jarak rata-rata berbobot dari posisi ke semua diamond"""
        total_dist = 0

        for gem in gems:
            # Bobot berdasarkan poin kuadrat dan ambil akar untuk optimasi
            weighted_dist = (self.calc_teleport_dist(gem.position, pos) * gem.properties.points * gem.properties.points) ** (0.25)
            total_dist += weighted_dist

        return total_dist / len(gems)
    
    def find_best_adjacent_pos(self, pos: Position, gems: list[GameObject]):
        """Mencari posisi bersebelahan dengan jarak rata-rata minimum ke diamond"""
        adjacent_positions = []
        adjacent_positions.append(Position(pos.y + 1, pos.x))
        adjacent_positions.append(Position(pos.y - 1, pos.x))
        adjacent_positions.append(Position(pos.y, pos.x + 1))
        adjacent_positions.append(Position(pos.y, pos.x - 1))

        return min(adjacent_positions, key=lambda p: self.calc_avg_gem_dist(p, gems))
    
    def find_gems_within_steps(self, steps: int, gems: list[GameObject]):
        """Mencari diamond dalam n langkah dari posisi saat ini"""
        return list(filter(lambda gem: self.calc_teleport_dist(self.player.position, gem.position) <= steps, gems))