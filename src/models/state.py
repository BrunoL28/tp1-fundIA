from dataclasses import dataclass
from typing import FrozenSet, Tuple

from .person import Person


@dataclass(frozen=True)
class State:
    """
    Representa um estado do problema da Ponte e da Tocha
    FrozenSet é usado para garantir que o conjunto de pessoas seja imutável e hashable.
    """
    left_side: FrozenSet[Person]
    right_side: FrozenSet[Person]
    torch_is_left: bool

    def is_goal(self) -> bool:
        """
        Verifica se o estado atual é o estado objetivo.
        O estado objetivo é quando todas as pessoas estão do lado direito da ponte, assim como a tocha.
        """
        return len(self.left_side) == 0 and not self.torch_is_left

    @property
    def torch_side_name(self) -> str:
        return "Esquerda" if self.torch_is_left else "Direita"

    def sort_key(self) -> Tuple:
        """
        Chave de ordenação determinística: primeiro pelo número de pessoas que já
        atravessaram, depois pelo lado da tocha e, por fim, pelas pessoas à
        esquerda. Garante que relatórios gerados em execuções diferentes saiam
        idênticos.
        """
        return (len(self.right_side), not self.torch_is_left, sorted(self.left_side))

    @staticmethod
    def _format_side(side: FrozenSet[Person]) -> str:
        return ", ".join(str(person) for person in sorted(side)) if side else "-"

    def diagram(self, multiline: bool = False) -> str:
        """
        Representação visual do estado, única em todo o projeto. O asterisco
        marca o lado da ponte em que a tocha se encontra.

        Ex.: `*[1, 2] ~~~ [5, 10]`, ou a mesma coisa em três linhas quando o
        rótulo precisa caber dentro de um nó do grafo.
        """
        left = self._format_side(self.left_side)
        right = self._format_side(self.right_side)
        torch_left = "*" if self.torch_is_left else ""
        torch_right = "" if self.torch_is_left else "*"

        if multiline:
            return f"{torch_left}[{left}]\n~~~\n[{right}]{torch_right}"
        return f"{torch_left}[{left}] ~~~ [{right}]{torch_right}"

    def __str__(self) -> str:
        return self.diagram()
