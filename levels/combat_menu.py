"""
Menú de Combate por Turnos para Cursed Dungeon.

Este módulo implementa el menú de acciones del jugador en combate,
incluyendo submenús para habilidades e items.

Agentes: FrontendJunior + GameDevJunior
"""

import pygame
from typing import Literal, Optional, Tuple, List, Dict
from src.others import draw_text


class CombatMenu:
    """Menú de acciones de combate mejorado (FASE 5)."""
    
    # Opciones principales con iconos
    OPTIONS = ["⚔ Atacar", "✨ Habilidad", "🎒 Item", "🏃 Huir"]
    
    def __init__(self):
        """Inicializa el menú de combate."""
        self.current_selection = 0
        self.max_options = len(self.OPTIONS)
        self.submenu_active = False
        self.submenu_type = None  # "skill" o "item"
        self.submenu_selection = 0
        self.submenu_items = []
    
    def handle_input(self, event) -> Optional[str]:
        """
        Maneja la entrada del jugador en el menú.
        
        Args:
            event: Evento de pygame
        
        Returns:
            Acción seleccionada o None
        """
        if event.type != pygame.KEYDOWN:
            return None
        
        # Si estamos en un submenú
        if self.submenu_active:
            return self._handle_submenu_input(event)
        
        # Navegación en menú principal
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.current_selection = (self.current_selection - 1) % self.max_options
            return "navigate"
        
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.current_selection = (self.current_selection + 1) % self.max_options
            return "navigate"
        
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            selected_action = self.OPTIONS[self.current_selection]
            
            # Atacar y Huir son acciones directas (comparar con iconos)
            if "Atacar" in selected_action:
                return "attack"
            elif "Huir" in selected_action:
                return "flee"
            # Habilidad e Item abren submenús
            elif "Habilidad" in selected_action:
                return "skill_menu"
            elif "Item" in selected_action:
                return "item_menu"
        
        return None
    
    def _handle_submenu_input(self, event) -> Optional[str]:
        """
        Maneja la entrada en submenús.
        
        Args:
            event: Evento de pygame
        
        Returns:
            Acción seleccionada o None
        """
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
            # Cerrar submenú
            self.close_submenu()
            return "back"
        
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            if len(self.submenu_items) > 0:
                self.submenu_selection = (self.submenu_selection - 1) % len(self.submenu_items)
            return "navigate"
        
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if len(self.submenu_items) > 0:
                self.submenu_selection = (self.submenu_selection + 1) % len(self.submenu_items)
            return "navigate"
        
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if len(self.submenu_items) > 0:
                selected_item = self.submenu_items[self.submenu_selection]
                submenu_type = self.submenu_type
                self.close_submenu()
                
                if submenu_type == "skill":
                    return f"use_skill:{selected_item['id']}"
                elif submenu_type == "item":
                    return f"use_item:{selected_item['id']}"
        
        return None
    
    def open_submenu(self, submenu_type: Literal["skill", "item"], items: List[Dict]):
        """
        Abre un submenú con opciones.
        
        Args:
            submenu_type: Tipo de submenú ("skill" o "item")
            items: Lista de items/habilidades disponibles
        """
        self.submenu_active = True
        self.submenu_type = submenu_type
        self.submenu_items = items
        self.submenu_selection = 0
    
    def close_submenu(self):
        """Cierra el submenú activo."""
        self.submenu_active = False
        self.submenu_type = None
        self.submenu_items = []
        self.submenu_selection = 0
    
    def draw(self, screen, font, y_position: int = 530, inline_rect: Optional[Tuple[int, int, int, int]] = None, context: Optional[Dict] = None):
        """
        Dibuja el menú de combate.
        
        Args:
            screen: Superficie de pygame
            font: Fuente para renderizar texto
            y_position: Posición Y del menú
            inline_rect: Rectángulo interno (x, y, w, h) para dibujar dentro del cuadro inferior
            context: Datos extra (player, enemy, combat_mgr) para descripciones
        """
        if context is not None:
            self._context = context
        if self.submenu_active:
            if inline_rect:
                self._draw_inline_submenu(screen, font, inline_rect)
            else:
                self._draw_submenu(screen, font)
        else:
            if inline_rect:
                self._draw_inline_menu(screen, font, inline_rect)
            else:
                self._draw_main_menu(screen, font, y_position)

    def _draw_inline_menu(self, screen, font, inline_rect: Tuple[int, int, int, int]):
        """
        Dibuja el menú principal dentro del cuadro inferior (estilo Pokemon).
        
        Args:
            screen: Superficie de pygame
            font: Fuente para renderizar texto
            inline_rect: Rectángulo interno (x, y, w, h) del cuadro inferior
        """
        inner_x, inner_y, inner_w, inner_h = inline_rect
        padding = 6
        left_w = int(inner_w * 0.52)
        right_w = inner_w - left_w - padding
        left_x = inner_x
        right_x = inner_x + left_w + padding
        left_h = inner_h

        # Separador vertical entre opciones y descripcion
        sep_x = right_x - (padding // 2)
        pygame.draw.line(screen, (120, 120, 150), (sep_x, inner_y), (sep_x, inner_y + inner_h), 1)

        # Opciones en grilla 2x2 (estilo Pokemon)
        option_width = max(1, left_w // 2)
        option_height = max(1, left_h // 2)
        for i, option in enumerate(self.OPTIONS):
            row = i // 2
            col = i % 2
            cell_x = left_x + (col * option_width)
            cell_y = inner_y + (row * option_height)
            center_x = cell_x + option_width // 2
            center_y = cell_y + option_height // 2

            if i == self.current_selection:
                color = (255, 255, 120)
                highlight = pygame.Surface((option_width - 4, option_height - 4), pygame.SRCALPHA)
                highlight.fill((60, 60, 90, 140))
                screen.blit(highlight, (cell_x + 2, cell_y + 2))
                pygame.draw.rect(screen, (150, 200, 255), (cell_x + 2, cell_y + 2, option_width - 4, option_height - 4), 1)
            else:
                color = (200, 200, 200)

            option_text = self._truncate_text(font, option, option_width - 8)
            text = font.render(option_text, True, color)
            text_rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, text_rect)

        # Panel de descripcion a la derecha
        desc_lines = self._get_description_lines(font, right_w)
        line_h = int(font.get_height() * 0.85)
        desc_y = inner_y
        for line in desc_lines:
            text = self._render_scaled(font, line, (200, 200, 200), 0.85)
            screen.blit(text, (right_x, desc_y))
            desc_y += line_h

    def _draw_inline_submenu(self, screen, font, inline_rect: Tuple[int, int, int, int]):
        """
        Dibuja el submenu dentro del cuadro inferior (sin ventana flotante).
        """
        inner_x, inner_y, inner_w, inner_h = inline_rect
        padding = 6
        left_w = int(inner_w * 0.52)
        right_w = inner_w - left_w - padding
        left_x = inner_x
        right_x = inner_x + left_w + padding

        # Separador vertical
        sep_x = right_x - (padding // 2)
        pygame.draw.line(screen, (120, 120, 150), (sep_x, inner_y), (sep_x, inner_y + inner_h), 1)

        # Lista de habilidades/items en la columna izquierda
        line_h = font.get_height()
        max_rows = max(1, inner_h // line_h)
        items = self.submenu_items or []
        start = 0
        if len(items) > max_rows:
            start = max(0, self.submenu_selection - max_rows + 1)
        visible = items[start:start + max_rows]

        y = inner_y
        for idx, item in enumerate(visible):
            real_index = start + idx
            if real_index == self.submenu_selection:
                color = (255, 255, 120)
                highlight = pygame.Surface((left_w - 4, line_h), pygame.SRCALPHA)
                highlight.fill((60, 60, 90, 140))
                screen.blit(highlight, (left_x + 2, y))
            else:
                color = (200, 200, 200)

            name = item.get("name", "???")
            name_text = self._truncate_text(font, name, left_w - 12)
            text = font.render(name_text, True, color)
            screen.blit(text, (left_x + 4, y))
            y += line_h

        # Panel de descripcion a la derecha
        desc_lines = self._get_description_lines(font, right_w)
        desc_y = inner_y
        for line in desc_lines:
            text = self._render_scaled(font, line, (200, 200, 200), 0.85)
            screen.blit(text, (right_x, desc_y))
            desc_y += int(font.get_height() * 0.85)

    def _get_description_lines(self, font, max_width: int) -> List[str]:
        """Genera lineas de descripcion para la opcion seleccionada."""
        context = getattr(self, "_context", {}) or {}
        player = context.get("player")
        combat_mgr = context.get("combat_mgr")

        if self.submenu_active and self.submenu_items:
            selected = self.submenu_items[self.submenu_selection]
            description = selected.get("description", "")
            extra = ""
            if self.submenu_type == "skill":
                dmg_mult = selected.get("damage_multiplier", 0)
                if dmg_mult and dmg_mult > 0:
                    extra = f"Potencia: x{dmg_mult:.1f}"
                else:
                    extra = "Potencia: --"
            elif self.submenu_type == "item":
                quantity = selected.get("quantity", 0)
                extra = f"Cantidad: {quantity}"
        else:
            option = self.OPTIONS[self.current_selection]
            description = ""
            extra = ""
            if "Atacar" in option and player:
                description = "Ataque basico."
                weapon_damage = self._get_weapon_damage(player)
                extra = f"Potencia: {weapon_damage}"
            elif "Habilidad" in option:
                description = "Usa una habilidad especial."
                extra = "Potencia: --"
            elif "Item" in option:
                description = "Usa un item del inventario."
                extra = "Potencia: --"
            elif "Huir" in option:
                description = "Intentar escapar del combate."
                if combat_mgr:
                    flee_pct = int(combat_mgr.calculate_flee_chance() * 100)
                    extra = f"Prob: {flee_pct}%"
                else:
                    extra = "Prob: --"

        lines = []
        if description:
            lines.extend(self._wrap_text(font, description, max_width))
        if extra:
            lines.append(extra)
        if not lines:
            lines.append("...")
        return lines

    def _get_weapon_damage(self, player) -> int:
        """Obtiene el dano del arma si existe."""
        try:
            weapon = player.getWeapon()
            if isinstance(weapon, dict):
                return int(weapon.get("damage", 0))
        except Exception:
            pass
        return 0

    def _wrap_text(self, font, text: str, max_width: int) -> List[str]:
        """Wrap de texto basico para el panel de descripcion."""
        words = text.split()
        lines = []
        current = ""
        for word in words:
            trial = f"{current} {word}".strip() if current else word
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _truncate_text(self, font, text: str, max_width: int) -> str:
        """Trunca texto con puntos suspensivos para que no invada otra columna."""
        if font.size(text)[0] <= max_width:
            return text
        ellipsis = "..."
        available = max(0, max_width - font.size(ellipsis)[0])
        if available <= 0:
            return ellipsis
        truncated = ""
        for ch in text:
            trial = truncated + ch
            if font.size(trial)[0] <= available:
                truncated = trial
            else:
                break
        return truncated + ellipsis

    def _render_scaled(self, font, text: str, color, scale: float = 1.0) -> pygame.Surface:
        """Renderiza texto escalado para el cuadro inferior."""
        base = font.render(text, True, color)
        if scale == 1.0:
            return base
        new_w = max(1, int(base.get_width() * scale))
        new_h = max(1, int(base.get_height() * scale))
        return pygame.transform.smoothscale(base, (new_w, new_h))
    
    def _draw_main_menu(self, screen, font, y_position: int):
        """
        Dibuja el menú principal de acciones con diseño mejorado (FASE 5).
        
        Args:
            screen: Superficie de pygame
            font: Fuente para renderizar texto
            y_position: Posición Y del menú
        """
        screen_width = screen.get_width()
        menu_width = 550
        menu_height = 100
        menu_x = (screen_width - menu_width) // 2
        
        # Fondo del menú con mejor transparencia
        menu_bg = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_bg.fill((20, 20, 30, 220))
        screen.blit(menu_bg, (menu_x, y_position))
        
        # Borde brillante
        pygame.draw.rect(screen, (100, 100, 150), 
                        (menu_x, y_position, menu_width, menu_height), 3)
        
        # Dibujar opciones en horizontal con separadores
        option_width = menu_width // self.max_options
        
        for i, option in enumerate(self.OPTIONS):
            x = menu_x + (i * option_width)
            y = y_position + 35
            
            # Resaltar opción seleccionada
            if i == self.current_selection:
                # Fondo de selección animado
                highlight_surf = pygame.Surface((option_width - 10, 50))
                highlight_surf.set_alpha(180)
                highlight_surf.fill((80, 80, 120))
                screen.blit(highlight_surf, (x + 5, y_position + 20))
                
                # Borde de selección
                pygame.draw.rect(screen, (150, 200, 255), 
                               (x + 5, y_position + 20, option_width - 10, 50), 2)
                
                color = (255, 255, 100)  # Amarillo brillante
            else:
                color = (200, 200, 200)  # Gris claro
            
            # Dibujar texto centrado
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(x + option_width // 2, y))
            screen.blit(text, text_rect)
            
            # Separadores verticales (excepto el último)
            if i < self.max_options - 1:
                sep_x = menu_x + ((i + 1) * option_width)
                pygame.draw.line(screen, (60, 60, 80), 
                               (sep_x, y_position + 15), 
                               (sep_x, y_position + menu_height - 15), 2)
    
    def _draw_submenu(self, screen, font):
        """
        Dibuja el submenú de habilidades o items con diseño mejorado (FASE 5).
        
        Args:
            screen: Superficie de pygame
            font: Fuente para renderizar texto
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        submenu_width = 600
        submenu_height = min(450, 100 + len(self.submenu_items) * 55)
        submenu_x = (screen_width - submenu_width) // 2
        submenu_y = (screen_height - submenu_height) // 2
        
        # Fondo del submenú con mejor transparencia
        submenu_bg = pygame.Surface((submenu_width, submenu_height), pygame.SRCALPHA)
        submenu_bg.fill((25, 25, 40, 245))
        screen.blit(submenu_bg, (submenu_x, submenu_y))
        
        # Borde brillante doble
        pygame.draw.rect(screen, (120, 120, 180), 
                        (submenu_x, submenu_y, submenu_width, submenu_height), 4)
        pygame.draw.rect(screen, (80, 80, 140), 
                        (submenu_x + 3, submenu_y + 3, submenu_width - 6, submenu_height - 6), 2)
        
        # Título con fondo
        title = "✨ HABILIDADES" if self.submenu_type == "skill" else "🎒 ITEMS"
        title_bg = pygame.Surface((submenu_width - 20, 35), pygame.SRCALPHA)
        title_bg.fill((50, 50, 80, 200))
        screen.blit(title_bg, (submenu_x + 10, submenu_y + 10))
        
        title_text = font.render(title, True, (255, 255, 150))
        title_rect = title_text.get_rect(center=(submenu_x + submenu_width // 2, submenu_y + 27))
        screen.blit(title_text, title_rect)
        
        # Si no hay items
        if len(self.submenu_items) == 0:
            no_items_text = "No hay habilidades disponibles" if self.submenu_type == "skill" else "No hay items usables"
            text = font.render(no_items_text, True, (150, 150, 150))
            text_rect = text.get_rect(center=(submenu_x + submenu_width // 2, submenu_y + 80))
            screen.blit(text, text_rect)
            
            # Instrucción para cerrar
            esc_text = font.render("[ESC] Volver", True, (120, 120, 200))
            esc_rect = esc_text.get_rect(center=(submenu_x + submenu_width // 2, 
                                                 submenu_y + submenu_height - 30))
            screen.blit(esc_text, esc_rect)
            return
        
        # Listar items con mejor diseño
        item_y = submenu_y + 60
        for i, item in enumerate(self.submenu_items):
            # Fondo para item seleccionado
            if i == self.submenu_selection:
                highlight_bg = pygame.Surface((submenu_width - 30, 50), pygame.SRCALPHA)
                highlight_bg.fill((70, 70, 110, 180))
                screen.blit(highlight_bg, (submenu_x + 15, item_y - 5))
                
                color = (255, 255, 120)
                # Indicador de selección mejorado
                indicator = font.render("►", True, (255, 200, 100))
                screen.blit(indicator, (submenu_x + 20, item_y))
            else:
                color = (200, 200, 200)
            
            # Nombre del item
            item_name = item.get("name", "???")
            name_text = font.render(item_name, True, color)
            screen.blit(name_text, (submenu_x + 45, item_y))
            
            # Información adicional (maná, cantidad, etc.)
            info_text = ""
            info_color = color
            if self.submenu_type == "skill":
                mana_cost = item.get("mana_cost", 0)
                available = item.get("available", True)
                reason = item.get("reason", "")
                
                if available:
                    info_text = f"💙 {mana_cost} MP"
                    info_color = (100, 150, 255)
                else:
                    info_text = f"[{reason}]"
                    info_color = (150, 100, 100)
            
            elif self.submenu_type == "item":
                quantity = item.get("quantity", 1)
                info_text = f"x{quantity}"
                info_color = (150, 200, 150)
            
            if info_text:
                info_x = submenu_x + submenu_width - 130
                info_render = font.render(info_text, True, info_color)
                screen.blit(info_render, (info_x, item_y))
            
            item_y += 50
        
        # Descripción del item seleccionado con mejor formato
        if 0 <= self.submenu_selection < len(self.submenu_items):
            selected_item = self.submenu_items[self.submenu_selection]
            description = selected_item.get("description", "")
            
            if description:
                desc_y = submenu_y + submenu_height - 50
                # Recortar descripción si es muy larga
                max_desc_length = 60
                if len(description) > max_desc_length:
                    description = description[:max_desc_length] + "..."
                
                draw_text(screen, font, description, submenu_x + 20, desc_y, (180, 180, 220))
        
        # Instrucciones
        instructions_y = submenu_y + submenu_height - 25
        draw_text(screen, font, "[W/S] Navegar  [ENTER] Usar  [ESC] Volver", 
                 submenu_x + 20, instructions_y, (100, 100, 150))


def create_combat_menu() -> CombatMenu:
    """
    Factory function para crear un CombatMenu.
    
    Returns:
        CombatMenu inicializado
    """
    return CombatMenu()
