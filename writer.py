#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter

from math import floor
import parser


class writer:
    def __init__(self, user: parser.usuario):
        self.user = user
        self.w, self.h = A4
        self.c = canvas.Canvas("overlay.pdf", pagesize=A4)

    def write_dados_gerais(self):
        self.write_spaced(self.user.data, (452, 652))
        self.write_spaced(self.user.uf, (59, 623))
        self.write(self.user.municipio, (92, 624))
        self.write_spaced(self.user.ibge, (482, 623), 15)
        self.write(self.user.ubs, (62, 595))
        self.write_spaced(self.user.ubs_code, (343, 595))
        # skip data primeiros sintomas

    def write_notificacao_individual(self):
        self.write(self.user.nome, (62, 564))
        self.write_spaced(self.user.nascimento, (449, 564))
        # skip idade
        self.write_spaced(self.user.sexo[0], (232, 548))
        # skip gestante
        self.write_spaced(self.user.raca, (551, 547))
        self.write_spaced(self._find_esco(self.user.escolaridade), (553, 519))
        self.write_spaced(self.user.n_sus, (54, 474), 11.7)
        self.write(self.user.nome_mae, (236, 474))

    def write_dados_residencia(self):
        self.write_spaced(self.user.uf_residencia, (54, 443))
        self.write(self.user.municipio_residencia, (84, 444))
        self.write_spaced(self.user.ibge_residencia, (326, 444))
        self.write(self.user.distrito_residencia, (414, 444))
        self.write(self.user.bairro_residencia, (64, 419))
        self.write(self.user.logradouro_residencia, (198, 418))
        self.write_spaced(self.user.cod_logradouro_residencia, (479, 418))
        self.write(self.user.numero_residencia, (63, 395))
        self.write(self.user.complemento_residencia, (120, 395))
        self.write_spaced(self.user.complemento_residencia, (225, 369))
        # skip geo gampo 1
        # skip geo campo 2
        # skip ponto de referência
        self.write_spaced(self.user.cep_residencia, (458, 367), 14)
        self.write_spaced(self.user.telefone_residencia, (56, 343), 15)

        match self.user.zona_residencia:
            case "Urbana":
                zona = 1
            case "Rural":
                zona = 2
            case "Periurbana":
                zona = 3
            case _:
                zona = 9
        self.write_spaced(str(zona), (334, 354))

    def _find_esco(self, esco: str) -> str:
        esco = esco.lower()
        # remove acentos
        esco.replace("ã", "a").replace("é", "e").replace("ç", "c")

        if "analfabeto" in esco:
            return "0"
        if all(w in esco for w in ["1", "4", "serie", "incompleto"]):
            return "1"
        if all(w in esco for w in ["4", "serie", "completo"]):
            return "2"
        if all(w in esco for w in ["5", "8", "serie", "incompleto"]):
            return "3"
        if all(w in esco for w in ["fundamental", "completo"]):
            return "4"
        if all(w in esco for w in ["medio", "incompleto"]):
            return "5"
        if all(w in esco for w in ["medio", "completo"]):
            return "6"
        if all(w in esco for w in ["superior", "incompleto"]):
            return "7"
        if all(w in esco for w in ["superior", "completo"]):
            return "8"
        return "0"

    def write_spaced(
        self, to_write: str, coord: tuple[int, int], spacing: float = 14.5
    ):
        self.c.setFont("Times-Roman", 10)
        x, y = coord
        for char in to_write.replace("/", ""):
            self.c.drawString(x, y, char)
            x += spacing

    def write(self, to_write: str, coord: tuple[int, int]):
        self.c.setFont("Times-Roman", 10)
        x, y = coord
        self.c.drawString(x, y, to_write)

    def draw_grid(self):
        self.c.setStrokeColorRGB(0.1, 0.1, 0.1)
        self.c.setFont("Times-Roman", 3)
        for x in range(10, floor(self.w), 10):
            self.c.line(x, 0, x, self.h)

        for y in range(10, floor(self.h), 10):
            self.c.line(0, y, self.w, y)

        for x in range(10, floor(self.w), 10):
            for y in range(10, floor(self.h), 10):
                self.c.drawString(x + 1, y + 1, f"{x//10}|{y//10}")

    def save(self):
        self.write_dados_gerais()
        self.write_notificacao_individual()
        self.write_dados_residencia()
        self.c.save()

        # base = PdfReader(open("notificacao.pdf", "rb")).pages[0]
        # overlay = PdfReader(open("overlay.pdf", "rb")).pages[0]
        # base.merge_page(overlay)

        # output_pdf = PdfWriter()
        # output_pdf.add_page(base)
        # # output_pdf.add_page(overlay)

        # # Write the merged PDF to a new file
        # with open("merge.pdf", "wb") as output_file:
        #     output_pdf.write(output_file)


if __name__ == "__main__":
    u = parser.parse(parser.debug)
    w = writer(u)
    w.save()
