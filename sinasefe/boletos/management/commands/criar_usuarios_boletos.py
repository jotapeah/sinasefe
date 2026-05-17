from boletos.models import Boleto
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria usuários a partir dos boletos"

    def handle(self, *args, **options):
        User = get_user_model()

        boletos = (
            Boleto.objects
            .exclude(codigo_pagador__isnull=True)
            .exclude(codigo_pagador__exact="")
            .order_by("codigo_pagador")
        )

        codigos_processados = set()

        criados = 0
        existentes = 0

        for boleto in boletos:
            codigo_pagador = str(boleto.codigo_pagador).strip()

            if codigo_pagador in codigos_processados:
                continue

            codigos_processados.add(codigo_pagador)

            if User.objects.filter(username=codigo_pagador).exists():
                existentes += 1
                continue

            identificacao = str(boleto.identificacao or "")
            primeiros_digitos = identificacao[:3]

            senha = f"{codigo_pagador}{primeiros_digitos}"

            user = User.objects.create_user(
                username=codigo_pagador,
                first_name=boleto.nome_pagador or "",
                password=senha,
            )

            criados += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuário criado: {user.username}"
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Finalizado. Criados: {criados} | Existentes: {existentes}"
            )
        )
