
#!/usr/bin/env python3
"""
Calculadora Científica em Python.

Operadores:
+, -, *, /, //, %, **

Funções:
sqrt, sin, cos, tan, log, log10, abs, round

Constantes:
pi, e

Utiliza AST para avaliar expressões sem usar eval().
"""

import ast
import math
import operator


OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCOES = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "abs": abs,
    "round": round,
}

CONSTANTES = {
    "pi": math.pi,
    "e": math.e,
}


class Calculadora(ast.NodeVisitor):

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            raise ValueError("Valor inválido.")

        if isinstance(node.value, (int, float)):
            if abs(node.value) > 10**100:
                raise ValueError("Número muito grande.")
            return node.value

        raise ValueError("Valor inválido.")

    def visit_Num(self, node):
        return node.n

    def visit_BinOp(self, node):
        tipo = type(node.op)

        if tipo not in OPERADORES:
            raise ValueError("Operador não permitido.")

        esquerda = self.visit(node.left)
        direita = self.visit(node.right)

        if tipo is ast.Pow:
            if abs(direita) > 1000:
                raise ValueError("Expoente muito grande.")

        resultado = OPERADORES[tipo](esquerda, direita)

        if isinstance(resultado, float) and not math.isfinite(resultado):
            raise ValueError("Resultado fora do limite numérico.")

        return resultado

    def visit_UnaryOp(self, node):
        tipo = type(node.op)

        if tipo not in UNARIOS:
            raise ValueError("Operador não permitido.")

        return UNARIOS[tipo](self.visit(node.operand))

    def visit_Name(self, node):
        if node.id in CONSTANTES:
            return CONSTANTES[node.id]

        raise ValueError(f"Nome desconhecido: {node.id}")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Função inválida.")

        if node.keywords:
            raise ValueError("Argumentos nomeados não permitidos.")

        nome = node.func.id

        if nome not in FUNCOES:
            raise ValueError(f"Função '{nome}' não permitida.")

        argumentos = [self.visit(arg) for arg in node.args]

        return FUNCOES[nome](*argumentos)

    def generic_visit(self, node):
        raise ValueError(
            f"Expressão não permitida: {type(node).__name__}"
        )


def calcular(expressao: str):
    if len(expressao) > 200:
        raise ValueError("Expressão muito longa.")

    arvore = ast.parse(expressao, mode="eval")
    return Calculadora().visit(arvore)


def main():
    print("=" * 50)
    print("CALCULADORA CIENTÍFICA")
    print("=" * 50)

    print("Digite 'sair' para encerrar.")
    print("Digite 'history' para consultar o histórico.")
    print()

    print("Exemplos:")
    print(" 2 + 3 * 4")
    print(" (2 + 5) ** 3")
    print(" sqrt(144)")
    print(" sin(pi / 2)")
    print()

    historico = []

    while True:
        try:
            entrada = input(">> ").strip()

            if not entrada:
                continue

            if entrada.lower() in {"sair", "exit", "quit", "q"}:
                print("Até logo!")
                break

            if entrada.lower() == "history":
                if not historico:
                    print("Histórico vazio.")
                else:
                    print("\nHistórico:")

                    for i, (expr, res) in enumerate(historico, 1):
                        print(f"{i}. {expr} = {res}")

                continue

            resultado = calcular(entrada)

            historico.append((entrada, resultado))

            print("Resultado:", resultado)

        except ZeroDivisionError:
            print("Erro: divisão por zero.")

        except (ValueError, TypeError, OverflowError, SyntaxError) as erro:
            print("Erro:", erro)

        except Exception as erro:
            print("Erro inesperado:", erro)


if __name__ == "__main__":
    main()
