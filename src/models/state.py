from dataclasses import dataclass
from typing import FrozenSet

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

    def __str__(self) -> str:
        lado_tocha = "Esquerda" if self.torch_is_left else "Direita"
        return f"Esq: {sorted(List(self.left_side))} | Dir: {sorted(list(self.right_side))} | Tocha: {lado_tocha}"