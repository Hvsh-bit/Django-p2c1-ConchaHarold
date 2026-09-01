import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .services import cargar_json


class ZonasViewTests(TestCase):
    def test_listado_zonas_responde_y_utiliza_su_template(self):
        response = self.client.get(
            reverse("dispositivos:lista_zonas")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dispositivos/lista_zonas.html",
        )

    def test_listado_zonas_calcula_cantidad_dispositivos(self):
        response = self.client.get(
            reverse("dispositivos:lista_zonas")
        )

        cantidades = {
            zona["id"]: zona["cantidad_dispositivos"]
            for zona in response.context["zonas"]
        }

        self.assertEqual(cantidades, {1: 3, 2: 3, 3: 2})

    def test_detalle_zona_prepara_metricas_y_categorias(self):
        response = self.client.get(
            reverse(
                "dispositivos:detalle_zona",
                args=[1],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dispositivos/detalle_zona.html",
        )
        self.assertEqual(response.context["cantidad"], 3)
        self.assertAlmostEqual(
            response.context["total_consumo"],
            58.6,
        )
        self.assertEqual(response.context["estado"], "ALERTA")
        self.assertEqual(
            response.context["dispositivos"][0]["categoria_nombre"],
            "Medición y monitoreo",
        )

    def test_detalle_zona_informa_estado_normal(self):
        response = self.client.get(
            reverse(
                "dispositivos:detalle_zona",
                args=[2],
            )
        )

        self.assertAlmostEqual(
            response.context["total_consumo"],
            32.3,
        )
        self.assertEqual(response.context["estado"], "NORMAL")

    def test_detalle_zona_inexistente_responde_404(self):
        response = self.client.get(
            reverse(
                "dispositivos:detalle_zona",
                args=[999],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_detalle_zona_maneja_una_zona_sin_dispositivos(self):
        def cargar_coleccion(nombre_archivo):
            if nombre_archivo == "zonas.json":
                return [
                    {
                        "id": 99,
                        "nombre": "Sala de reuniones",
                        "limite_kwh": 10.0,
                    }
                ]

            if nombre_archivo == "dispositivos.json":
                return []

            return cargar_json(nombre_archivo)

        with patch(
            "dispositivos.views.cargar_json",
            side_effect=cargar_coleccion,
        ):
            response = self.client.get(
                reverse(
                    "dispositivos:detalle_zona",
                    args=[99],
                )
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cantidad"], 0)
        self.assertEqual(response.context["total_consumo"], 0)
        self.assertEqual(response.context["estado"], "NORMAL")
        self.assertContains(
            response,
            "Esta zona no tiene dispositivos.",
        )


class CargarJsonTests(SimpleTestCase):
    def test_carga_coleccion_dispositivos_requerida(self):
        dispositivos = cargar_json("dispositivos.json")

        self.assertGreaterEqual(len(dispositivos), 8)

        claves_esperadas = {
            "id",
            "nombre",
            "consumo_kwh",
            "zona_id",
            "categoria_id",
        }

        for dispositivo in dispositivos:
            self.assertEqual(
                set(dispositivo),
                claves_esperadas,
            )

    def test_dispositivos_referencian_datos_existentes(self):
        dispositivos = cargar_json("dispositivos.json")
        zonas = cargar_json("zonas.json")
        categorias = cargar_json("categorias.json")

        ids_zonas = {zona["id"] for zona in zonas}
        ids_categorias = {
            categoria["id"] for categoria in categorias
        }

        for dispositivo in dispositivos:
            self.assertIn(dispositivo["zona_id"], ids_zonas)
            self.assertIn(
                dispositivo["categoria_id"],
                ids_categorias,
            )

    def test_carga_minimo_tres_zonas(self):
        zonas = cargar_json("zonas.json")

        self.assertGreaterEqual(len(zonas), 3)

    def test_carga_minimo_tres_categorias(self):
        categorias = cargar_json("categorias.json")

        self.assertGreaterEqual(len(categorias), 3)

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
                    "dispositivos.json debe contener una lista",
                ):
                    cargar_json("dispositivos.json")
