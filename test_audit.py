import gzip
import tempfile
import unittest
from datetime import date
from pathlib import Path

from drakes_log_audit import audit, date_from_name, render_markdown


class AuditTests(unittest.TestCase):
    def test_extracts_error_tps_and_player_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "latest.log"
            path.write_text(
                "[INFO] TPS from last 5s, 1m, 5m, 15m: 20.0, 12.5, 18.0, 19.0\n"
                "[ERROR] [Plugin] Something exploded 42\n"
                "[Not Secure] [Polis] Player » no funciona la maquina, mucho lag\n",
                encoding="utf-8",
            )
            report = audit([path])
            self.assertEqual(1, len(report["errors"]))
            self.assertEqual(12.5, report["tps"][0][2])
            self.assertEqual("Player: no funciona la maquina, mucho lag", report["complaints"][0]["text"])
            self.assertIn("Errores recurrentes", render_markdown(report))

    def test_reads_gzip_logs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "2026-07-22-1.log.gz"
            with gzip.open(path, "wt", encoding="utf-8") as handle:
                handle.write("[WARN] [Plugin] mensaje de prueba\n")
            report = audit([path])
            self.assertEqual(1, len(report["warnings"]))

    def test_reads_rotated_file_dates(self) -> None:
        self.assertEqual(date(2026, 7, 22), date_from_name(Path("2026-07-22-7.log.gz")))
        self.assertEqual(date(2026, 7, 24), date_from_name(Path("crash-2026-07-24_17.00.20-server.txt")))


if __name__ == "__main__":
    unittest.main()
