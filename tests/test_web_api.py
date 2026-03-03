import json
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from risk_assessment_engine.engine.assessor import Assessor
from risk_assessment_engine.main import _get_ai_sample, _get_merchant_sample, _get_partner_sample, _get_vendor_sample
from risk_assessment_engine.models.research_data import ResearchData
from risk_assessment_engine.web.app import app


class WebApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "ok")

    def test_form_config_all_types(self):
        for assessment_type in ["merchant", "partner", "vendor", "ai"]:
            response = self.client.get(f"/api/form-config/{assessment_type}")
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assertEqual(body["assessment_type"], assessment_type)
            self.assertGreater(len(body["steps"]), 0)

    def test_form_config_unknown_type(self):
        response = self.client.get("/api/form-config/unknown")
        self.assertEqual(response.status_code, 404)

    def test_assess_merchant_happy_path(self):
        payload = _get_merchant_sample()
        response = self.client.post("/api/assess/merchant", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("result", data)
        self.assertIn("report_markdown", data)
        self.assertIn("download", data)

    def test_assess_partner_happy_path(self):
        payload = _get_partner_sample()
        response = self.client.post("/api/assess/partner", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())

    def test_assess_vendor_happy_path(self):
        payload = _get_vendor_sample()
        response = self.client.post("/api/assess/vendor", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())

    def test_assess_ai_happy_path(self):
        payload = _get_ai_sample()
        response = self.client.post("/api/assess/ai", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())

    def test_assess_unknown_type(self):
        response = self.client.post("/api/assess/unknown", json={})
        self.assertEqual(response.status_code, 404)

    def test_assess_validation_error_missing_required(self):
        payload = _get_merchant_sample()
        payload["merchant_info"] = {}
        response = self.client.post("/api/assess/merchant", json=payload)
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertEqual(body.get("error"), "validation_error")
        self.assertGreater(len(body.get("details", [])), 0)

    def test_assess_validation_error_wrong_type(self):
        payload = _get_merchant_sample()
        payload["parameter_i"]["app_store_rating"] = "bad-rating"
        response = self.client.post("/api/assess/merchant", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_state_leak_regression(self):
        base = Path("/Users/suryaf/projects/risk_assessment_engine/tests")
        first = ResearchData(**json.loads((base / "saku-rupiah-research.json").read_text(encoding="utf-8")))
        second = ResearchData(**json.loads((base / "koinworks-research.json").read_text(encoding="utf-8")))

        assessor = Assessor()
        result_1 = assessor.assess(first)
        result_2 = assessor.assess(second)

        trigger_codes_1 = [t.code for t in result_1.decision_result.auto_reject_triggers]
        trigger_codes_2 = [t.code for t in result_2.decision_result.auto_reject_triggers]

        self.assertIn("NO_BI_LICENSE", trigger_codes_1)
        self.assertEqual(trigger_codes_2, [])


if __name__ == "__main__":
    unittest.main()
