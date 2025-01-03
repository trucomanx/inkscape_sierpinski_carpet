#!/usr/bin/env python
# coding=utf-8
import inkex
import math
import sys
from lxml import etree

class RegularPolygonGenerator(inkex.EffectExtension):
    count=0;
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--fractal_deep", type=int, default=5, help="Fractal deep")
        pars.add_argument("--square_size",     type=float, default=100.0, help="Square size")
        pars.add_argument("--color_in_string", type=str, default="#000000", help="Color ex: black or #000000")


    def square_points(self,x,y,size):
        points = [f"{x},{y}", f"{x+size},{y}",f"{x+size},{y+size}",f"{x},{y+size}"]
        return points

    def integer_to_rgba(self, color_value):
        # Se a cor for uma string no formato hexadecimal, converta para inteiro
        if isinstance(color_value, str):
            color_value = int(color_value.lstrip('#'))
        
        # Extrair componentes RGBA (assumindo que o valor é no formato 0xAARRGGBB)
        red = (color_value >> 24) & 0xFF   # Extrair alfa (primeiros 8 bits)
        green = (color_value >> 16) & 0xFF      # Extrair vermelho (seguintes 8 bits)
        blue = (color_value >> 8) & 0xFF     # Extrair verde (seguindo os 8 bits)
        alfa = color_value & 0xFF            # Extrair azul (últimos 8 bits)

        # Converter para o formato hexadecimal #RRGGBB (sem o componente alpha)
        hex_color = f"#{red:02X}{green:02X}{blue:02X}"
        
        
        return hex_color, f"{alfa/255.0}"




    def draw_carpet(self,x, y, size, depth,color):
        if depth == 0:
            # Preenche o quadrado central
            
            color_hex, opacity=self.integer_to_rgba(color);
            #print('[[['+color_hex+']]]')
            
            points=self.square_points(x,y,size);
            
            polygon = etree.Element(
                inkex.addNS("polygon", "svg"),
                {
                    "points": " ".join(points),
                    "style": "fill:"+color_hex+";stroke:none",
                    #"style": "fill:(200,150,100,0.5);stroke:none",
                },
            )
            self.svg.get_current_layer().append(polygon)
            
            #self.count=self.count+1
            #print(f"Progresso: {self.count} concluído.", file=sys.stderr, flush=True)
            
            
        else:
            # Divide em 9 partes e desenha os subquadrados
            new_size = size / 3
            for dx in range(3):
                for dy in range(3):
                    if dx == 1 and dy == 1:
                        continue
                    else:
                        self.draw_carpet(
                            x + dx * new_size,
                            y + dy * new_size,
                            new_size,
                            depth - 1,
                            color
                        )


    def effect(self):
        fractal_deep = self.options.fractal_deep
        square_size = self.options.square_size
        color_in_string = self.options.color_in_string;
        #print("[[[",color_in_string,"]]]",type(color_in_string))
        self.draw_carpet(0, 0, square_size, fractal_deep,color_in_string)

if __name__ == "__main__":
    RegularPolygonGenerator().run()

