"""Offline regressions: Docker commands are mocked and never executed here."""

import argparse
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

from projects.flask.app import app as example_app
from scripts import batch_container_runner as batch
from scripts import container_resource_monitor as monitor
from scripts import container_runner as runner
from scripts import docker_compose_generator as compose
from scripts import docker_image_updater as updater
from scripts import image_cleaner as cleaner


ROOT = Path(__file__).resolve().parents[1]


class ComposeGeneratorTests(unittest.TestCase):
    def build(self, *args):
        return compose.build_compose(compose.make_parser().parse_args(args))

    def test_service_options_stay_with_their_service(self):
        data = self.build(
            "--networks", "frontend,backend", "--service-name", "web",
            "--service-image", "nginx:stable-alpine", "--service-ports", "127.0.0.1:8080:80",
            "--service-env", "URL:https://db:8443/path,EMPTY:",
            "--service-name", "db", "--service-image", "mysql:8.4",
            "--service-volumes", "dbdata:/var/lib/mysql",
        )
        self.assertEqual(data["services"]["web"]["environment"],
                         {"URL": "https://db:8443/path", "EMPTY": ""})
        self.assertEqual(data["services"]["web"]["ports"], ["127.0.0.1:8080:80"])
        self.assertNotIn("ports", data["services"]["db"])
        self.assertEqual(data["networks"], {"frontend": {}, "backend": {}})
        self.assertEqual(data["services"]["db"]["networks"], ["frontend", "backend"])
        self.assertEqual(data["volumes"], {"dbdata": {}})

    def test_optional_top_level_fields_are_omitted(self):
        data = self.build("--service-name", "web", "--service-image", "nginx")
        self.assertEqual(data, {"services": {"web": {"image": "nginx"}}})

    def test_bind_mounts_are_not_named_volume_declarations(self):
        data = self.build("--service-name", "web", "--service-image", "nginx",
                          "--service-volumes", r"./html:/html,/tmp:/temp,C:\data:/windows,cache:/cache")
        self.assertEqual(data["volumes"], {"cache": {}})

    def test_invalid_models_are_rejected(self):
        cases = (
            (),
            ("--service-name", "web"),
            ("--service-name", "bad name", "--service-image", "nginx"),
            ("--service-name", "web", "--service-image", "nginx",
             "--service-name", "web", "--service-image", "mysql"),
            ("--service-name", "web", "--service-image", "nginx", "--service-env", "BAD"),
            ("--service-name", "web", "--service-image", "nginx", "--service-env", "X:1,X:2"),
            ("--service-name", "web", "--service-image", "nginx", "--networks", "one,,two"),
        )
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.build(*args)

    def test_option_order_and_duplicates_have_cli_errors(self):
        for args in (("--service-image", "nginx"),
                     ("--service-name", "web", "--service-image", "nginx",
                      "--service-image", "mysql")):
            with self.subTest(args=args), redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as error:
                    compose.make_parser().parse_args(args)
                self.assertEqual(error.exception.code, 2)

    def test_file_round_trip_and_explicit_overwrite(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory, redirect_stdout(StringIO()):
            output = Path(directory) / "compose.yaml"
            args = ["--output", str(output), "--service-name", "web", "--service-image", "nginx"]
            compose.main(args)
            original = output.read_text()
            self.assertEqual(yaml.safe_load(original)["services"]["web"]["image"], "nginx")
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                compose.main(args)
            self.assertEqual(output.read_text(), original)
            compose.main(args + ["--force"])


class ContainerRunnerTests(unittest.TestCase):
    def setUp(self):
        self.client = runner.app.test_client()

    @patch.object(runner.subprocess, "run")
    def test_json_validation_prevents_docker_calls(self, run):
        for payload in (None, [], "text", {}, {"name": 12, "image": "nginx"},
                        {"name": "web; echo bad", "image": "nginx"},
                        {"name": "web", "image": "--privileged"},
                        {"name": "web", "image": "nginx; echo bad"}):
            with self.subTest(payload=payload):
                response = self.client.post("/launch_container", json=payload)
                self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.post("/launch_container", data="not json").status_code, 400)
        run.assert_not_called()

    @patch.object(runner.subprocess, "run")
    def test_valid_payload_and_legacy_keys_use_argument_list(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="container-id\n", stderr="")
        for payload in ({"name": "web", "image": "nginx:stable-alpine"},
                        {"d1": "web", "d2": "nginx:stable-alpine"}):
            response = self.client.post("/launch_container", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["container_id"], "container-id")
            self.assertEqual(run.call_args.args[0],
                             ["docker", "run", "-d", "--name", "web", "nginx:stable-alpine"])
            self.assertTrue(run.call_args.kwargs["check"])
            self.assertFalse(run.call_args.kwargs.get("shell", False))

    @patch.object(runner.subprocess, "run")
    def test_docker_errors_are_http_failures(self, run):
        for error, status in (
            (subprocess.CalledProcessError(1, ["docker"], stderr="daemon error"), 500),
            (FileNotFoundError("docker"), 503),
            (subprocess.TimeoutExpired(["docker"], 60), 504),
        ):
            with self.subTest(status=status):
                run.side_effect = error
                self.assertEqual(self.client.post("/launch_container",
                    json={"name": "web", "image": "nginx"}).status_code, status)


class BatchRunnerTests(unittest.TestCase):
    def test_url_environment_and_repeated_mounts(self):
        data = batch.parse_image("nginx,name=web,env=URL:https://api:8443/a,volume=one:/a,volume=two:/b")
        self.assertEqual(data["envs"], {"URL": "https://api:8443/a"})
        self.assertEqual(data["volumes"], ["one:/a", "two:/b"])

    @patch.object(batch, "run_container")
    def test_all_specs_validate_before_any_launch(self, run):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            batch.main(["nginx,name=valid", "nginx,port=70000"])
        run.assert_not_called()

    def test_invalid_image_port_and_unknown_options(self):
        for spec in ("--privileged", "nginx,port=0", "nginx,port=abc", "nginx,unknown=x",
                     "nginx,name=bad name", "nginx,env=MISSING", "nginx,port=80,port=81"):
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                batch.parse_image(spec)

    @patch.object(batch.subprocess, "run")
    def test_environment_is_one_argument_and_port_is_local(self, run):
        batch.run_container("nginx", port=80, envs={"VALUE": "a; echo b"})
        command = run.call_args.args[0]
        self.assertIn("VALUE=a; echo b", command)
        self.assertIn("127.0.0.1:80:80", command)
        self.assertTrue(run.call_args.kwargs["check"])

    @patch.object(batch, "run_container", side_effect=subprocess.CalledProcessError(1, ["docker"]))
    def test_docker_failure_returns_nonzero(self, run):
        with redirect_stderr(StringIO()):
            self.assertEqual(batch.main(["nginx"]), 1)


class ResourceMonitorTests(unittest.TestCase):
    @patch.object(monitor.subprocess, "run")
    def test_empty_stats_are_an_empty_list(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="\n  \n")
        self.assertEqual(monitor.get_container_stats(), [])

    @patch.object(monitor.subprocess, "run")
    def test_json_lines_and_mixed_units_use_docker_percentage(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout=(
            '{"Name":"web","CPUPerc":"125.50%","MemPerc":"81.25%",'
            '"MemUsage":"2.352MiB / 1.5GiB"}\n\n'))
        output = StringIO()
        with redirect_stdout(output):
            monitor.report_stats(monitor.get_container_stats(), 75.0, 80.0)
        self.assertIn("CPU: 125.5%, Memory: 81.25%", output.getvalue())
        self.assertEqual(output.getvalue().count("ALERT:"), 2)
        self.assertTrue(run.call_args.kwargs["check"])

    def test_zero_threshold_is_not_treated_as_disabled(self):
        output = StringIO()
        with redirect_stdout(output):
            monitor.report_stats([{"Name": "web", "CPUPerc": "0.1%", "MemPerc": "0.1%"}], 0, 0)
        self.assertEqual(output.getvalue().count("ALERT:"), 2)


class ImageUpdaterTests(unittest.TestCase):
    @patch.object(updater.subprocess, "run")
    def test_empty_container_output_does_not_inspect_empty_id(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="\n")
        with redirect_stdout(StringIO()):
            self.assertEqual(updater.main([]), 0)
        self.assertEqual(run.call_count, 1)

    @patch.object(updater, "pull_image")
    @patch.object(updater, "get_container_image", return_value="nginx:stable-alpine")
    @patch.object(updater, "get_running_containers", return_value=["one", "two"])
    def test_shared_image_is_pulled_once(self, containers, inspect, pull):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(updater.main([]), 0)
        pull.assert_called_once_with("nginx:stable-alpine")
        self.assertIn("Recreate", output.getvalue())

    @patch.object(updater, "get_running_containers")
    def test_restart_is_rejected_before_docker_calls(self, containers):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            updater.main(["--restart"])
        containers.assert_not_called()

    @patch.object(updater, "pull_image")
    @patch.object(updater, "get_container_image", return_value="sha256:local-image")
    @patch.object(updater, "get_running_containers", return_value=["one"])
    def test_local_image_ids_are_not_pulled(self, containers, inspect, pull):
        with redirect_stdout(StringIO()):
            self.assertEqual(updater.main([]), 0)
        pull.assert_not_called()


class ImageCleanerTests(unittest.TestCase):
    @patch.object(cleaner.subprocess, "run")
    def test_default_keeps_native_confirmation_and_reference_tracking(self, run):
        cleaner.prune_images()
        self.assertEqual(run.call_args.args[0], ["docker", "image", "prune"])
        self.assertTrue(run.call_args.kwargs["check"])

    @patch.object(cleaner.subprocess, "run")
    def test_age_uses_creation_filter_and_force_is_explicit(self, run):
        cleaner.prune_images(30, force=True)
        self.assertEqual(run.call_args.args[0],
                         ["docker", "image", "prune", "--all", "--filter", "until=720h", "--force"])

    def test_nonpositive_age_is_rejected(self):
        for days in ("0", "-1"):
            with self.subTest(days=days), self.assertRaises(argparse.ArgumentTypeError):
                cleaner.positive_days(days)

    @patch.object(cleaner.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["docker"]))
    def test_docker_failure_returns_nonzero(self, run):
        with redirect_stderr(StringIO()):
            self.assertEqual(cleaner.main([]), 1)


class FlaskExampleTests(unittest.TestCase):
    def test_application_response(self):
        response = example_app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello from Flask running in Docker!\n")
        self.assertEqual(response.mimetype, "text/plain")


if __name__ == "__main__":
    unittest.main()
