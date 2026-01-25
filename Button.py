import pygame

class Button:
    def __init__(self, scr: pygame.Surface, rect: pygame.Rect | tuple[int, int, int, int], color: list[int],
                 on_click_func, image_path: str | None = None,
                 btn_text: str = "", btntext_color: list[int] = (255, 255, 255),
                 font_path: str | None = None,
                 text_size: int = 0, border_thickness: int = 5, border_color: list[int] = (255, 255, 255),
                 corner_radius: int = 0) -> None:

        """
        Required arguments (in this order):
            - Surface, Rect, Color, On Click Function
        Unrequired arguments (in this order, after the required arguments):
            - Button Text*, Button Text Color, Font Path, Text Size**, Border Thickness, Border Color, Corner Radius

        **If the Text Size is set to 0, then, it uses this formula to calculate the size:

        rh = Rect Height (4th Rect argument)
        Text Size = rh - (rh // 3)

        :param scr:
        :param rect:
        :param color:
        :param btn_text:
        :param btntext_color:
        :param on_click_func:
        :param border_thickness:
        :param border_color:
        :param corner_radius:
        """

        self.screen = scr
        self.rect = pygame.Rect(rect)
        self.color = color

        self.text = btn_text
        self.text_size = text_size
        self.text_color = btntext_color
        self.font_path = font_path

        self.on_click = on_click_func

        self.active = True
        self.show = True

        self.border_thickness = border_thickness
        self.border_color = border_color

        self.original_color = color
        self.original_border_color = border_color

        self.is_being_pressed = False

        self.image_path = image_path

        if corner_radius < 0:
            raise ValueError(f"Corner radius cannot be negative. ({corner_radius})")
        else:
            self.corner_radius = corner_radius

        return

    def handle(self) -> None:
        if self.show:
            if not self.image_path:
                if self.corner_radius == 0:
                    pygame.draw.rect(self.screen, self.border_color,
                                     (self.rect[0] - self.border_thickness, self.rect[1] - self.border_thickness,
                                      self.rect[2] + (self.border_thickness * 2), self.rect[3] + (self.border_thickness * 2)
                                      ))

                    pygame.draw.rect(self.screen, self.color, self.rect)

                else:
                    # CORNERS
                    pygame.draw.circle(self.screen, self.border_color,
                                       (self.rect[0], self.rect[1]),
                                       self.corner_radius, draw_top_left=True)  # TOP LEFT

                    pygame.draw.circle(self.screen, self.border_color,
                                       (
                                           self.rect[0] + self.rect[2],
                                           self.rect[1]),
                                       self.corner_radius, draw_top_right=True)  # TOP RIGHT

                    pygame.draw.circle(self.screen, self.border_color,
                                       (
                                           self.rect[0],
                                           self.rect[1] + self.rect[3]),
                                       self.corner_radius, draw_bottom_left=True)  # BOTTOM LEFT

                    pygame.draw.circle(self.screen, self.border_color,
                                       (self.rect[0] + self.rect[2],
                                        self.rect[1] + self.rect[3]),
                                       self.corner_radius, draw_bottom_right=True)  # BOTTOM RIGHT

                    # LINES
                    pygame.draw.line(self.screen, self.border_color,
                                     (self.rect[0], self.rect[1] - self.corner_radius / 2),
                                     (self.rect[0]+self.rect[2], self.rect[1]-self.corner_radius/2),
                                     width=self.corner_radius + 1)  # top line

                    pygame.draw.line(self.screen, self.border_color,
                                     (self.rect[0] - (self.corner_radius / 2),
                                      self.rect[1]),
                                     (self.rect[0] - (self.corner_radius / 2),
                                      self.rect[1] + self.rect[3]),
                                     width=self.corner_radius + 1)  # left line

                    pygame.draw.line(self.screen, self.border_color,
                                     (self.rect[0],
                                      self.rect[1] + self.rect[3] + self.corner_radius / 2),
                                     (self.rect[0] + self.rect[2],
                                      self.rect[1] + self.rect[3] + self.corner_radius / 2),
                                     width=self.corner_radius + 1)  # bottom line

                    pygame.draw.line(self.screen, self.border_color,
                                     (self.rect[0] + self.rect[2] + self.corner_radius / 2,
                                      self.rect[1]),
                                     (self.rect[0] + self.rect[2] + self.corner_radius / 2,
                                      self.rect[1] + self.rect[3]),
                                     width=self.corner_radius + 1)  # right line

                    # FILL

                    pygame.draw.rect(self.screen, self.border_color, self.rect)

                    # CORNERS
                    pygame.draw.circle(self.screen, self.color,
                                       (self.rect[0] + self.corner_radius, self.rect[1] + self.corner_radius),
                                       self.corner_radius, draw_top_left=True)  # TOP LEFT

                    pygame.draw.circle(self.screen, self.color,
                                       (
                                       self.rect[0] + self.rect[2] - self.corner_radius, self.rect[1] + self.corner_radius),
                                       self.corner_radius, draw_top_right=True)  # TOP RIGHT

                    pygame.draw.circle(self.screen, self.color,
                                       (
                                       self.rect[0] + self.corner_radius, self.rect[1] + self.rect[3] - self.corner_radius),
                                       self.corner_radius, draw_bottom_left=True)  # BOTTOM LEFT

                    pygame.draw.circle(self.screen, self.color,
                                       (self.rect[0] + self.rect[2] - self.corner_radius,
                                        self.rect[1] + self.rect[3] - self.corner_radius),
                                       self.corner_radius, draw_bottom_right=True)  # BOTTOM RIGHT

                    # LINES
                    pygame.draw.line(self.screen, self.color,
                                     (self.rect[0] + self.corner_radius, self.rect[1] + self.corner_radius / 2),
                                     (self.rect[0] + self.rect[2] - self.corner_radius,
                                      self.rect[1] + self.corner_radius / 2),
                                     width=self.corner_radius + 1)  # top line

                    pygame.draw.line(self.screen, self.color,
                                     (self.rect[0] + (self.corner_radius / 2), self.rect[1] + self.corner_radius),
                                     (self.rect[0] + (self.corner_radius / 2),
                                      self.rect[1] + self.rect[3] - self.corner_radius),
                                     width=self.corner_radius + 1)  # left line

                    pygame.draw.line(self.screen, self.color,
                                     (self.rect[0] + self.corner_radius,
                                      self.rect[1] + self.rect[3] - self.corner_radius / 2),
                                     (self.rect[0] + self.rect[2] - self.corner_radius,
                                      self.rect[1] + self.rect[3] - self.corner_radius / 2),
                                     width=self.corner_radius + 1)  # bottom line

                    pygame.draw.line(self.screen, self.color,
                                     (self.rect[0] + self.rect[2] - self.corner_radius / 2,
                                      self.rect[1] + self.corner_radius),
                                     (self.rect[0] + self.rect[2] - self.corner_radius / 2,
                                      self.rect[1] + self.rect[3] - self.corner_radius),
                                     width=self.corner_radius + 1)  # right line

                    # FILL

                    pygame.draw.rect(self.screen, self.color, (self.rect[0] + self.corner_radius,
                                                               self.rect[1] + self.corner_radius,
                                                               self.rect[2] - self.corner_radius * 2,
                                                               self.rect[3] - self.corner_radius * 2))

                    debug = False
                    if debug:
                        # DEBUG THINGIES
                        pygame.draw.circle(self.screen, (255, 0, 0),
                                           (self.rect[0], self.rect[1]), 7)  # top left

                        pygame.draw.circle(self.screen, (0, 255, 0),
                                           (self.rect[0] + self.rect[2], self.rect[1]), 7)  # top right

                        pygame.draw.circle(self.screen, (0, 0, 255),
                                           (self.rect[0], self.rect[1] + self.rect[3]), 7)  # bottom left

                        pygame.draw.circle(self.screen, (255, 0, 255),
                                           (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]), 7)  # bottom right

                if self.text_size > 0:
                    size = self.text_size
                else:
                    size = self.rect[3] - (self.rect[3] // 3)

                btn_font = pygame.font.Font(self.font_path, size)

                textobj = btn_font.render(self.text, True, self.text_color)
                textobj_rect = textobj.get_rect()

                textobj_rect.center = (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2)

                self.screen.blit(textobj, textobj_rect)

                mouse_pos = pygame.mouse.get_pos()
                if self.rect.colliderect((mouse_pos[0], mouse_pos[1], 1, 1)) and self.active:

                    self.color = [max(0, x - 20) for x in self.original_color]
                    self.border_color = [max(0, x - 20) for x in self.original_border_color]

                    if pygame.mouse.get_pressed()[0]:
                        if not self.is_being_pressed:
                            self.on_click()

                        self.color = [max(0, x - 30) for x in self.original_color]
                        self.border_color = [max(0, x - 30) for x in self.original_border_color]


                        self.is_being_pressed = True
                    elif not pygame.mouse.get_pressed()[0]:
                        if self.is_being_pressed:
                            self.color = self.original_color
                            self.border_color = self.original_border_color
                        self.is_being_pressed = False
                else:
                    self.color = self.original_color
                    self.border_color = self.original_border_color

                return
            else:
                image_texture = pygame.image.load(self.image_path)
                resized_image = pygame.transform.scale(image_texture, (self.rect.width, self.rect.height))

                self.screen.blit(resized_image, self.rect)

                pygame.draw.circle(self.screen, self.border_color,
                                   (self.rect[0], self.rect[1]),
                                   self.corner_radius, draw_top_left=True)  # TOP LEFT

                pygame.draw.circle(self.screen, self.border_color,
                                   (
                                       self.rect[0] + self.rect[2],
                                       self.rect[1]),
                                   self.corner_radius, draw_top_right=True)  # TOP RIGHT

                pygame.draw.circle(self.screen, self.border_color,
                                   (
                                       self.rect[0],
                                       self.rect[1] + self.rect[3]),
                                   self.corner_radius, draw_bottom_left=True)  # BOTTOM LEFT

                pygame.draw.circle(self.screen, self.border_color,
                                   (self.rect[0] + self.rect[2],
                                    self.rect[1] + self.rect[3]),
                                   self.corner_radius, draw_bottom_right=True)  # BOTTOM RIGHT

                # LINES
                pygame.draw.line(self.screen, self.border_color,
                                 (self.rect[0], self.rect[1] - self.corner_radius / 2),
                                 (self.rect[0] + self.rect[2], self.rect[1] - self.corner_radius / 2),
                                 width=self.corner_radius + 1)  # top line

                pygame.draw.line(self.screen, self.border_color,
                                 (self.rect[0] - (self.corner_radius / 2),
                                  self.rect[1]),
                                 (self.rect[0] - (self.corner_radius / 2),
                                  self.rect[1] + self.rect[3]),
                                 width=self.corner_radius + 1)  # left line

                pygame.draw.line(self.screen, self.border_color,
                                 (self.rect[0],
                                  self.rect[1] + self.rect[3] + self.corner_radius / 2),
                                 (self.rect[0] + self.rect[2],
                                  self.rect[1] + self.rect[3] + self.corner_radius / 2),
                                 width=self.corner_radius + 1)  # bottom line

                pygame.draw.line(self.screen, self.border_color,
                                 (self.rect[0] + self.rect[2] + self.corner_radius / 2,
                                  self.rect[1]),
                                 (self.rect[0] + self.rect[2] + self.corner_radius / 2,
                                  self.rect[1] + self.rect[3]),
                                 width=self.corner_radius + 1)  # right line

                if self.text_size > 0:
                    size = self.text_size
                else:
                    size = self.rect[3] - (self.rect[3] // 3)

                btn_font = pygame.font.Font(self.font_path, size)

                textobj = btn_font.render(self.text, True, self.text_color)
                textobj_rect = textobj.get_rect()

                textobj_rect.center = (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2)

                self.screen.blit(textobj, textobj_rect)

                mouse_pos = pygame.mouse.get_pos()
                if self.rect.colliderect((mouse_pos[0], mouse_pos[1], 1, 1)) and self.active:

                    self.color = [max(0, x - 20) for x in self.original_color]
                    self.border_color = [max(0, x - 20) for x in self.original_border_color]

                    if pygame.mouse.get_pressed()[0]:
                        if not self.is_being_pressed:
                            self.on_click()

                        self.color = [max(0, x - 30) for x in self.original_color]
                        self.border_color = [max(0, x - 30) for x in self.original_border_color]

                        self.is_being_pressed = True
                    elif not pygame.mouse.get_pressed()[0]:
                        if self.is_being_pressed:
                            self.color = self.original_color
                            self.border_color = self.original_border_color
                        self.is_being_pressed = False
                else:
                    self.color = self.original_color
                    self.border_color = self.original_border_color

    def __str__(self):
        return f"Button <{self.text}>"


if __name__ == "__main__":
    pygame.init()

    WIDTH = 1920
    HEIGHT = 1080

    FPS = 120

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Button Test")

    clock = pygame.time.Clock()
    run = True
    fullscreen = False


    def on_click():
        print(button)


    button = Button(
        screen, pygame.Rect(300, 300, 500, 100), [255, 0, 0], on_click, "../files/daniil_orlov.png",
        "idk 7 maybe 7.2", [255, 255, 255], "files/papyrus.ttf",
        0, 15, [67, 67, 67], 20
    )
    button.show = True

    def button_layout_on_click():
        print("Hello, world!")

    button_layout = Button(
        scr=screen, rect=pygame.Rect(950, 300, 300, 100), color=[145, 20, 15], on_click_func=button_layout_on_click,
        image_path=None, btn_text="Go to space!", btntext_color=[0, 0, 0],
        font_path="../files/DynaPuff-VariableFont_wdth,wght.ttf", text_size=30, border_thickness=15,
        border_color=[120, 5, 0], corner_radius=0
    )
    button_layout.show = True


    def handle_keyinputs():
        global fullscreen, screen, run
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            if event.key == pygame.K_q:
                run = False


    main_color = (32, 32, 32)

    while run:
        screen.fill(main_color)
        button.handle()
        button_layout.handle()
        for event in pygame.event.get():
            handle_keyinputs()
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
