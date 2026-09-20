from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Person:
    """
    Uma pessoa que precisa atravessar a ponte.

    A identidade da pessoa é separada do seu tempo de travessia. Se as duas
    coisas fossem a mesma - identificar a pessoa pelo tempo que ela leva -, duas
    pessoas igualmente rápidas colapsariam em uma só dentro do conjunto de
    estados, e o problema mudaria silenciosamente.

    A ordenação é por tempo e, em caso de empate, por identificador, de modo que
    `min` e `max` sobre um conjunto de pessoas devolvem a mais rápida e a mais
    lenta. O rótulo não participa da comparação nem do hash: ele é apenas a
    forma de exibir a pessoa nos relatórios.
    """
    time: int
    id: int
    label: str = field(default="", compare=False)

    def __str__(self) -> str:
        return self.label or str(self.time)
