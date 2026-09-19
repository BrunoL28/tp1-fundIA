from dataclasses import dataclass
from typing import FrozenSet, Tuple

@dataclass(frozen=True)
class State:
    """
    Representa um estado do problema da Ponte e da Tocha
    FrozenSet é usado para garantir que o conjunto de pessoas seja imutável e hashable.
    """
    left_side: FrozenSet[int]
    right_side: FrozenSet[int]
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
        atravessaram, depois pelo lado da tocha e, por fim, pelos tempos à esquerda.
        Garante que relatórios gerados em execuções diferentes saiam idênticos.
        """
        return (len(self.right_side), not self.torch_is_left, sorted(self.left_side))

    @staticmethod
    def _format_side(side: FrozenSet[int]) -> str:
        return ", ".join(map(str, sorted(side))) if side else "-"

    def diagram(self) -> str:
        """
        Representação visual compacta do estado. O asterisco marca o lado da ponte
        em que a tocha se encontra. Ex.: `*[1, 2] ~~~ [5, 10]`
        """
        left = self._format_side(self.left_side)
        right = self._format_side(self.right_side)
        if self.torch_is_left:
            return f"*[{left}] ~~~ [{right}]"
        return f"[{left}] ~~~ [{right}]*"

    def __str__(self) -> str:
        return (
            f"Esq: [{self._format_side(self.left_side)}] | "
            f"Dir: [{self._format_side(self.right_side)}] | "
            f"Tocha: {self.torch_side_name}"
        )
