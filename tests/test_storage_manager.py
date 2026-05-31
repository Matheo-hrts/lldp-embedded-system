import pytest
import os
import csv
import tempfile
from unittest.mock import patch
from storage_manager import save_csv, load_history, group_by_system

SAMPLE_FRAME = {
    "chassis_id": "00:8e:73:d4:31:d0",
    "port_id": "gi1/1/48",
    "vlan": "1",
    "ttl": "120",
    "system_name": "CiscoLLDP"
}

class TestSaveCsv:
    def test_creates_saves_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        assert os.path.exists("saves")

    def test_creates_csv_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        assert os.path.exists("saves/history.csv")

    def test_writes_headers(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        with open("saves/history.csv") as f:
            reader = csv.DictReader(f)
            assert "chassis_id" in reader.fieldnames
            assert "system_name" in reader.fieldnames
            assert "timestamp" in reader.fieldnames

    def test_writes_data(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        with open("saves/history.csv") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert rows[0]["chassis_id"] == "00:8e:73:d4:31:d0"
        assert rows[0]["system_name"] == "CiscoLLDP"

    def test_appends_multiple_rows(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        save_csv(SAMPLE_FRAME.copy())
        with open("saves/history.csv") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2

    def test_does_not_mutate_original(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        frame = SAMPLE_FRAME.copy()
        save_csv(frame)
        assert "timestamp" not in frame

class TestLoadHistory:
    def test_returns_empty_list_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = load_history()
        assert result == []

    def test_returns_list_of_dicts(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        result = load_history()
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    def test_loads_correct_data(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        result = load_history()
        assert result[0]["chassis_id"] == "00:8e:73:d4:31:d0"

    def test_loads_multiple_rows(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_csv(SAMPLE_FRAME.copy())
        save_csv(SAMPLE_FRAME.copy())
        result = load_history()
        assert len(result) == 2

class TestGroupBySystem:
    def test_groups_by_system_name(self):
        history = [
            {**SAMPLE_FRAME, "timestamp": "2026-01-01"},
            {**SAMPLE_FRAME, "timestamp": "2026-01-02"},
            {"chassis_id": "aa:bb:cc", "port_id": "gi1/1/1", "vlan": "1", "ttl": "120", "system_name": "OtherSwitch", "timestamp": "2026-01-01"}
        ]
        result = group_by_system(history)
        assert "CiscoLLDP" in result
        assert "OtherSwitch" in result
        assert len(result["CiscoLLDP"]) == 2
        assert len(result["OtherSwitch"]) == 1

    def test_returns_empty_dict_for_empty_list(self):
        result = group_by_system([])
        assert result == {}

    def test_preserves_frame_data(self):
        history = [{**SAMPLE_FRAME, "timestamp": "2026-01-01"}]
        result = group_by_system(history)
        assert result["CiscoLLDP"][0]["chassis_id"] == "00:8e:73:d4:31:d0"
