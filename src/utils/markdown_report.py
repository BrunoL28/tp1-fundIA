import os
import re

DOC_TITLE = "# Resultados da Execução - Ponte e Tocha"


def _markers(section_id: str):
    return f"<!-- BEGIN:{section_id} -->", f"<!-- END:{section_id} -->"


def upsert_section(filename: str, section_id: str, body: str, doc_title: str = DOC_TITLE) -> bool:
    """
    Escreve (ou reescreve) uma seção delimitada por marcadores dentro do relatório.

    Retorna True se uma seção existente foi substituída, False se foi criada.
    """
    begin, end = _markers(section_id)
    block = f"{begin}\n\n{body.strip()}\n\n{end}"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            current = f.read()
    else:
        current = f"{doc_title}\n"

    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)

    if pattern.search(current):
        updated = pattern.sub(lambda _match: block, current)
        replaced = True
    else:
        updated = f"{current.rstrip()}\n\n{block}\n"
        replaced = False

    with open(filename, "w", encoding="utf-8") as f:
        f.write(updated if updated.endswith("\n") else updated + "\n")

    return replaced
