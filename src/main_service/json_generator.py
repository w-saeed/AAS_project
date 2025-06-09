import json

class JsonGenerator:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.data = self._load_template()
        self.segments = self._find_segments()

    def _load_template(self) -> dict:
        with open(self.template_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _find_segments(self) -> dict:
        for submodel in self.data.get("submodels", []):
            for sme in submodel.get("submodelElements", []):
                if sme.get("idShort") == "Segments":
                    return sme
        raise Exception("Segments collection not found in your template!")

    def append_segments(self, segment_list: list):
        if not isinstance(segment_list, list):
            raise ValueError("segment_list must be a list of segment JSON objects.")
        self.segments["value"].extend(segment_list)

    def save(self, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)