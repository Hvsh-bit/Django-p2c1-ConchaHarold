import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .services import cargar_dispositivos


class CatalogoViewTests(TestCase):
    def test_catalogo_responde_y_utiliza_su_template(self):
        response = self.client.get(
            reverse("dispositivos:catalogo")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dispositivos/catalogo.html",
        )

    def test_catalogo_entrega_el_resumen_en_el_contexto(self):
        response = self.client.get(
            reverse("dispositivos:catalogo")
        )

        self.assertEqual(response.context.get("total"), 4)
        self.assertEqual(response.context.get("total_activos"), 3)

    def test_catalogo_entrega_cuatro_dispositivos(self):
        response = self.client.get(
            reverse("dispositivos:catalogo")
        )

        self.assertEqual(
            len(response.context["dispositivos"]),
            4,
        )

    def test_catalogo_muestra_resumen_y_dispositivos(self):
        response = self.client.get(
            reverse("dispositivos:catalogo")
        )

        self.assertContains(response, "Total de dispositivos")
        self.assertContains(response, "Dispositivos activos")
        self.assertContains(response, "Medidor inteligente")
        self.assertContains(response, "18.4 kWh")

    def test_catalogo_muestra_estado_vacio(self):
        with patch(
            "dispositivos.views.cargar_dispositivos",
            return_value=[],
        ):
            response = self.client.get(
                reverse("dispositivos:catalogo")
            )

        self.assertEqual(response.context["total"], 0)
        self.assertEqual(response.context["total_activos"], 0)
        self.assertContains(
            response,
            "No existen dispositivos disponibles.",
        )


class CargarDispositivosTests(SimpleTestCase):
    def test_carga_la_coleccion_json(self):
        dispositivos = cargar_dispositivos()

        self.assertEqual(len(dispositivos), 4)
        self.assertEqual(
            set(dispositivos[0]),
            {"id", "nombre", "estado", "consumo_kwh"},
        )

    def test_rechaza_un_elemento_raiz_que_no_sea_lista(self):
        with TemporaryDirectory() as directorio:
            base_dir = Path(directorio)
            data_dir = base_dir / "data"
            data_dir.mkdir()

            ruta = data_dir / "dispositivos.json"
            ruta.write_text(
                json.dumps({"nombre": "Registro incorrecto"}),
                encoding="utf-8",
            )

            with override_settings(BASE_DIR=base_dir):
                with self.assertRaisesRegex(
                    ValueError,
                    "Se esperaba una lista de dispositivos",
                ):
                    cargar_dispositivos()