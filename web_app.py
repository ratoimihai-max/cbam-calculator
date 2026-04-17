from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from cbam_calculator import (
    COD_NC_IMPLICIT_PE_PRODUS,
    calculeaza_cbam,
    greutate_panou,
    tari_cbam,
    valori_implicite_pentru_tari,
    valori_CBAM,
)


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_json_body(handler: BaseHTTPRequestHandler) -> dict:
    content_length = int(handler.headers.get("Content-Length", "0"))
    if content_length <= 0:
        return {}

    raw = handler.rfile.read(content_length)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
    return json.loads(text)


class CBAMHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/api/options":
            self.handle_options()
            return

        self.serve_static()

    def do_POST(self) -> None:
        if self.path == "/api/calculate":
            self.handle_calculate()
            return

        json_response(self, 404, {"error": "Ruta nu exista."})

    def handle_options(self) -> None:
        coduri_nc = sorted({cod for _tara, cod in valori_CBAM})
        json_response(
            self,
            200,
            {
                "tipuri_produs": list(COD_NC_IMPLICIT_PE_PRODUS.keys()),
                "coduri_nc": coduri_nc,
                "tari": tari_cbam,
                "grosimi_panou": sorted(greutate_panou.keys()),
                "coduri_implicite": COD_NC_IMPLICIT_PE_PRODUS,
                "valori_directe_tari": valori_implicite_pentru_tari("implicit"),
                "valori_default_tari": valori_implicite_pentru_tari("2026"),
            },
        )

    def handle_calculate(self) -> None:
        try:
            data = read_json_body(self)
            rezultat = calculeaza_cbam(
                tip_produs=str(data.get("tip_produs", "")),
                suprafata_m2=float(data.get("suprafata_m2", 0)),
                tara=str(data.get("tara", "")),
                pret_ETS=float(data.get("pret_ETS", 0)),
                cod_NC=str(data.get("cod_NC") or ""),
                grosime_tabla_mm=to_optional_float(data.get("grosime_tabla_mm")),
                grosime_panou_mm=to_optional_int(data.get("grosime_panou_mm")),
                grosime_tabla_exterior_mm=to_optional_float(data.get("grosime_tabla_exterior_mm")),
                grosime_tabla_interior_mm=to_optional_float(data.get("grosime_tabla_interior_mm")),
                tip_panou=str(data.get("tip_panou") or "perete"),
                taxa_carbon_origine=float(data.get("taxa_carbon_origine") or 0),
                anul=str(data.get("anul") or "2026"),
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            json_response(self, 400, {"error": str(exc)})
            return

        json_response(
            self,
            200,
            {
                "greutate_kg_m2": rezultat.greutate_kg_m2,
                "greutate_tone": rezultat.greutate_tone,
                "emisii_tco2": rezultat.emisii_tco2,
                "cost_cbam_eur": rezultat.cost_cbam_eur,
                "cost_cbam_eur_m2": rezultat.cost_cbam_eur_m2,
                "valoare_implicita": rezultat.valoare_implicita,
                "sursa_valoare_implicita": rezultat.sursa_valoare_implicita,
            },
        )

    def serve_static(self) -> None:
        request_path = unquote(self.path.split("?", 1)[0])
        if request_path in {"", "/"}:
            file_path = STATIC_DIR / "index.html"
        else:
            safe_path = request_path.lstrip("/")
            file_path = (STATIC_DIR / safe_path).resolve()
            if STATIC_DIR.resolve() not in file_path.parents and file_path != STATIC_DIR.resolve():
                self.send_error(403)
                return

        if not file_path.exists() or not file_path.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def to_optional_float(value: object) -> float | None:
    if value in {None, ""}:
        return None
    return float(value)


def to_optional_int(value: object) -> int | None:
    if value in {None, ""}:
        return None
    return int(float(value))


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), CBAMHandler)
    print(f"CBAM web app pornita pe http://localhost:{PORT}")
    print("Pentru acces in retea: folositi IP-ul calculatorului sau URL-ul de deploy.")
    server.serve_forever()


if __name__ == "__main__":
    main()
