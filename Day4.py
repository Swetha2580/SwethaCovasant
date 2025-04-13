
import os
if not os.path.exists('pkg'):
    os.makedirs('pkg')


with open('pkg/poly.py', 'w') as f:
    f.write("""
class Poly:
    def __init__(self, *coefficients):
        # Store coefficients in reverse order so that self.coefficients[i]
        # corresponds to the coefficient of x^i
        self.coefficients = list(coefficients[::-1])

    def __add__(self, other):
        len1 = len(self.coefficients)
        len2 = len(other.coefficients)
        result_coefficients = []
        for i in range(max(len1, len2)):
            coeff1 = self.coefficients[i] if i < len1 else 0
            coeff2 = other.coefficients[i] if i < len2 else 0
            result_coefficients.append(coeff1 + coeff2)
        return Poly(*result_coefficients[::-1])

    def __str__(self):
        terms = []
        for i, coeff in enumerate(self.coefficients):
            if coeff != 0:
                if i == 0:
                    terms.append(str(coeff))
                elif i == 1:
                    terms.append(f"{coeff}x")
                else:
                    terms.append(f"{coeff}x^{i}")
        if not terms:
            return "Poly(0)"
        return "Poly(" + ", ".join(terms[::-1]) + ")"

if __name__ == '__main__':
    a = Poly(1, 2, 3)  # Represents 1x^2 + 2x + 3
    b = Poly(1, 0, 1)  # Represents 1x^2 + 0x + 1
    print(f"Polynomial a: {a}")
    print(f"Polynomial b: {b}")
    c = a + b
    print(f"Polynomial a + b: {c}")

    a_long = Poly(1, 2, 3)      # 3 + 2x + 1x^2
    b_long = Poly(1, 0, 1, 1, 2, 3) # 3 + 2x + 1x^2 + 1x^3 + 0x^4 + 1x^5
    c_long = a_long + b_long
    print(f"Polynomial a_long: {a_long}")
    print(f"Polynomial b_long: {b_long}")
    print(f"Polynomial a_long + b_long: {c_long}")
""")

from pkg.poly import Poly

a = Poly(1, 2, 3)  
b = Poly(1, 0, 1, 1, 2, 3) 

c = a + b
print(c)