class Renderer:
    def render_circle(self, radius):
        pass
    
    def render_square(self, side_length):
        pass
    
    def render_triangle(self, base, height):
        pass

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing Circle as pixels (radius: {radius})")
    
    def render_square(self, side_length):
        print(f"Drawing Square as pixels (side length: {side_length})")
    
    def render_triangle(self, base, height):
        print(f"Drawing Triangle as pixels (base: {base}, height: {height})")

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing Circle as vector (radius: {radius})")
    
    def render_square(self, side_length):
        print(f"Drawing Square as vector (side length: {side_length})")
    
    def render_triangle(self, base, height):
        print(f"Drawing Triangle as vector (base: {base}, height: {height})")

class Shape:
    def __init__(self, renderer):
        self.renderer = renderer
    
    def draw(self):
        pass
    
    def resize(self, factor):
        pass

class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        self.renderer.render_circle(self.radius)
    
    def resize(self, factor):
        self.radius *= factor
        print(f"Circle radius resized to {self.radius}")

class Square(Shape):
    def __init__(self, renderer, side_length):
        super().__init__(renderer)
        self.side_length = side_length
    
    def draw(self):
        self.renderer.render_square(self.side_length)
    
    def resize(self, factor):
        self.side_length *= factor
        print(f"Square side length resized to {self.side_length}")

class Triangle(Shape):
    def __init__(self, renderer, base, height):
        super().__init__(renderer)
        self.base = base
        self.height = height
    
    def draw(self):
        self.renderer.render_triangle(self.base, self.height)
    
    def resize(self, factor):
        self.base *= factor
        self.height *= factor
        print(f"Triangle resized to base: {self.base}, height: {self.height}")

def main():
    raster = RasterRenderer()
    vector = VectorRenderer()
    
    print("=== Растрові фігури ===")
    circle_raster = Circle(raster, 5)
    square_raster = Square(raster, 4)
    triangle_raster = Triangle(raster, 3, 6)
    
    circle_raster.draw()
    square_raster.draw()
    triangle_raster.draw()
    
    print("\n=== Векторні фігури ===")
    circle_vector = Circle(vector, 5)
    square_vector = Square(vector, 4)
    triangle_vector = Triangle(vector, 3, 6)
    
    circle_vector.draw()
    square_vector.draw()
    triangle_vector.draw()
    
    print("\n=== Зміна розміру фігур ===")
    circle_vector.resize(2)
    circle_vector.draw()
    
    square_raster.resize(0.5)
    square_raster.draw()
    
    print("\n=== Зміна рендерера ===")
    print("Перед зміною:")
    triangle_raster.draw()
    
    print("Після зміни:")
    triangle_raster.renderer = vector
    triangle_raster.draw()

if __name__ == "__main__":
    main()