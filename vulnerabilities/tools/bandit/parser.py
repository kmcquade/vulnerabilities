import json

from datetime import datetime


class BanditParser(object):
    def get_scan_types(self):
        return ["Bandit Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Bandit Scan"

    def get_description_for_scan_types(self, scan_type):
        return "JSON report format"

    def get_findings(self, filename, test):
        data = json.load(filename)

        dupes = dict()
        if "generated_at" in data:
            find_date = datetime.strptime(data["generated_at"], "%Y-%m-%dT%H:%M:%SZ")

        for item in data["results"]:
            mitigation = ""
            impact = ""
            references = ""
            findingdetail = ""
            title = ""

            title = (
                "Test Name: "
                + item["test_name"]
                + " Test ID: "
                + item["test_id"]
                + "dfdfdfdfdffdfdfdffdfdfdfdfdfdffdf"
            )

            #  ##### Finding details information ######
            findingdetail += "Filename: " + item["filename"] + "\n"
            findingdetail += "Line number: " + str(item["line_number"]) + "\n"
            findingdetail += "Issue Confidence: " + item["issue_confidence"] + "\n\n"
            findingdetail += "Code:\n"
            findingdetail += item["code"] + "\n"

            sev = item["issue_severity"]
            mitigation = item["issue_text"]
            references = item["test_id"]

            dupe_key = title + item["filename"] + str(item["line_number"])

            if dupe_key in dupes:
                find = dupes[dupe_key]
            else:
                dupes[dupe_key] = True

                find = {
                    "title": title,
                    "description": findingdetail,
                    "severity": sev.title(),
                    "mitigation": mitigation,
                    "impact": impact,
                    "references": references,
                    "file_path": item["filename"],
                    "line": item["line_number"],
                    "date": find_date,
                    "static_finding": True,
                    "dynamic_finding": False,
                }
                dupes[dupe_key] = find
                findingdetail = ""

        return list(dupes.values())